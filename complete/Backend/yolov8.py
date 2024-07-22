from ultralytics import YOLO
import threading, base64, os
import cv2
from datetime import datetime
import numpy as np
# データベース
from database import engine, SessionLocal
from sqlalchemy.sql import func
import models, schemas
# トラッキング
from tracker import MultiObjectTracker 
# 時間
import time
from alarm import play_alarm

prev_time = [time.time(), time.time()]
save_flag = [True, True]
tracking_id = 0
frame_count = 0
skip_frame = 4

def check_database_num(tracker: MultiObjectTracker):
    try:
        db = SessionLocal()
        count = db.query(models.Violator).count()
        if count == 0:
            tracker.tracker.feature_vectors = None
            
    finally:
        db.close()

def reg_database(cam_no, violation_name, image_path, tracking_id):
    try:
        # データベース接続
        db = SessionLocal()
        now = datetime.now()
        date = now.strftime("%Y-%m-%d %H:%M:%S")
        violation = violation_name
        
        # 画像ファイルを読み込み、Base64エンコード
        with open(image_path, "rb") as image_file:
            image = image_file.read()
            binary_image = base64.b64encode(image)
        
        db_violation = models.Violator(cam_no=str(cam_no), date=now, violation=violation, image=binary_image, last_modified=datetime.now(), tracking_id=tracking_id)
        db.add(db_violation)
        db.commit()
        db.refresh(db_violation)
    finally:
        db.close()

def add_cam_no_database(cam_no, _track_id):
    try:
        # データベース接続
        db = SessionLocal()
        v = db.query(models.Violator).filter(models.Violator.tracking_id == _track_id).first()
        if v:
            if str(cam_no) not in v.cam_no:
                print("*********************  カメラナンバー更新 *******************************")
                v.last_modified = datetime.now()
                v.cam_no = v.cam_no + "," + str(cam_no)
                db.commit()
            else:
                print(f'{_track_id} in {v.tracking_id}')

        else:
            print('*********************  同一データ発見失敗  *********************')
            print(_track_id)
    finally:
        db.close()

def process_frame(frame, model, cam_index, tracker):
    """
    YOLOv8でフレームを処理し、認識結果を描画する関数
    """
    global prev_time
    global save_flag
    global tracking_id
    results = model.track(frame,verbose =False)
    annotated_frame = results[0].plot()

    frame_skip = 4  # フレームをスキップする間隔
    frame_count = 0
    interval=5.0  #撮影を行う間隔[秒]
     
    frame_plot = frame
    bike_S = []
    umb_S = []
    person_S = []

    for box in results[0].boxes:
        #傘と自転車の情報を保存
        class_id = int(box.cls[0])
        if(results[0].names[class_id]=="bicycle"):
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            bike_S.append([x1,y1,x2,y2])
        elif(results[0].names[class_id]=="umbrella"):
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            umb_S.append([x1,y1,x2,y2])
        elif(results[0].names[class_id]=="person"):
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            person_S.append([x1,y1,x2,y2])
     
    #傘と自転車が横から見て重なっていたらまとめて描画
    for i in umb_S:
        for j in bike_S:
            if(i[0] < j[2] and j[0] < i[2] and 3 * min(j[2]-i[0],i[2]-j[0]) > i[2]-i[0]):
                x1, y1, x2, y2 = map(int,i)
                X1, Y1, X2, Y2 = map(int,j)
                cv2.rectangle(frame_plot, (min(x1,X1), min(y1,Y1)), (max(x2,X2), max(y2,Y2)), (0, 0, 255), 2)
                cv2.putText(frame_plot, "bike", (min(x1,X1), min(y1,Y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                if(time.time() - prev_time[cam_index - 1] >= interval):
                    if len(person_S) == 0:
                        # 人がいない場合はスキップ
                        continue

                    print(f'*********************カメラ{cam_index}  傘差し運転発見 *******************************')
                    play_alarm(cam_index)

                    # ここが保存処理、つまりカメラ間にて同じ人がいるかを調べたい部分
                    xyxy = [min(x1, X1), min(y1, Y1), max(x2, X2), max(y2, Y2)]
                    ret_result, ret_track_id, ret_box, ret_value, ret_added = tracker(frame, xyxy, f'{cam_index}-{tracking_id}')
                    if ret_added:
                        print("*********************  新規人間 *******************************")

                        cropped_frame = frame[min(y1, Y1):max(y2, Y2), min(x1, X1):max(x2, X2)]
                        script_path = os.path.abspath(__file__)
                        script_dir = os.path.dirname(script_path)
                        cv2.imwrite(script_dir + "/images/temp.png", cropped_frame)
                        reg_database(cam_index, '傘差し運転', script_dir + "/images/temp.png", ret_track_id)
                        tracking_id = tracking_id + 1
                        
                    elif ret_result and cam_index != int(ret_track_id.split('-')[0]):
                        # トラッキング成功(他のカメラの情報と一致するものが見つかった)
                        # データベースのカメラnoを書き換え
                        print("*********************  トラッキング成功  *********************")
                        add_cam_no_database(cam_index, ret_track_id)
                    
                    elif ret_result:
                        print("*********************  同一カメラ同一人物  *********************")

                    save_flag[cam_index - 1] = True
                        
                else:
                    print(f'************************カメラ{cam_index}  待機時間  *******************************')



    if save_flag[cam_index - 1]:
        prev_time[cam_index - 1] = time.time()
        save_flag[cam_index - 1] = False
                    
    return frame_plot

def generate_frames_yolo():
    global frame_count
    global skip_frame

    print('**************** read model *******************')
    model1 = YOLO("yolov8n.pt")
    model2 = YOLO("yolov8n.pt")
    print('**************** capture video *******************')
    # PCカメラ
    #camera1 = cv2.VideoCapture(0)
    #camera2 = cv2.VideoCapture(1)
    
    # ライブカメラ
    camera1 = cv2.VideoCapture('http://blue-network.eolstudy.com/cam-window')
    camera2 = cv2.VideoCapture('http://blue-network.eolstudy.com/cam-desk')

     #テストビデオ
    #camera1 = cv2.VideoCapture("/Users/admin/Downloads/video_517517241151914317-Nm8OaLPB.MP4")
    #camera2 = cv2.VideoCapture("/Users/admin/Downloads/video_517517241151914317-Nm8OaLPB.MP4")

    # youtureid設定
    cap_fps = 30
    use_gpu = False
    tracker = MultiObjectTracker(
            tracker_name='',
            fps=cap_fps,
            use_gpu=use_gpu,
        )
    
    print('**************** inference *******************')
    while True:
        success1, frame1 = camera1.read()
        success2, frame2 = camera2.read()
        
        frame_count = frame_count + 1
        if frame_count % skip_frame != 0:
            continue
        frame_count =0

        if not success1 or not success2:
            break
        frame_left, frame_right = frame1, frame2

        result_left = None
        result_right = None

        def process_frame_left():
            nonlocal result_left
            result_left = process_frame(frame_left, model1, 1, tracker)

        def process_frame_right():
            nonlocal result_right
            result_right = process_frame(frame_right, model2, 2, tracker)

        thread_left = threading.Thread(target=process_frame_left)
        thread_right = threading.Thread(target=process_frame_right)
        thread_left.start()
        thread_right.start()

        thread_left.join()
        thread_right.join()
        combined_frame = np.concatenate((result_left, result_right), axis=1)

        ret, buffer = cv2.imencode('.jpg', combined_frame)
        if not ret:
            break

        # データベース要素数チェック
        check_database_num(tracker)

        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    
