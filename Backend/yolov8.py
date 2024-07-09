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
        
        db_violation = models.Violator(cam_no=str(cam_no), date=date, violation=violation, image=binary_image, last_modified=datetime.now(), tracking_id=tracking_id)
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
    results = model.track(frame)
    annotated_frame = results[0].plot()

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        class_id = int(box.cls[0])  # cls をテンソルから整数に変換

        if box.id  is not None:
            # トラッキングIDの取得
            track_id = int(box.id[0])
            # カメラ間追跡タスク
            # 人間なら(実装完了後違反ならに変更)
            if results[0].names[class_id] == 'person':
                ret_result, ret_track_id, ret_box, ret_value, ret_added = tracker(frame, box.xyxy[0], f'{cam_index}-{track_id}')

                # トラッキング結果
                if ret_added:
                    print("*********************  新規人間 *******************************")
                    script_path = os.path.abspath(__file__)
                    script_dir = os.path.dirname(script_path)

                    # 画像を切り取る
                    cropped_image = frame[y1:y2, x1:x2]

                    # 切り取った画像を保存
                    cv2.imwrite(script_dir + "/images/temp.png", cropped_image)
                    
                    reg_database(cam_index, '傘差し運転', script_dir + "/images/temp.png", ret_track_id)

                
                if ret_result and cam_index != int(ret_track_id.split('-')[0]):
                    # トラッキング成功(他のカメラの情報と一致するものが見つかった)
                    # データベースのカメラnoを書き換え
                    print("*********************  トラッキング成功  *********************")
                    add_cam_no_database(cam_index, ret_track_id)
                    
    return annotated_frame

def generate_frames_yolo():
    print('**************** read model *******************')
    model1 = YOLO("yolov8n.pt")
    model2 = YOLO("yolov8n.pt")
    print('**************** capture video *******************')
    camera1 = cv2.VideoCapture(0)
    camera2 = cv2.VideoCapture(1)
    
    #camera1 = cv2.VideoCapture('D:/Research/Social_Infomatics_Lecture/PracticeOfSocialInformatics_2nd/code/resource/test_two_people1.mp4')
    #camera2 = cv2.VideoCapture('D:/Research/Social_Infomatics_Lecture/PracticeOfSocialInformatics_2nd/code/resource/test_two_people2.mp4')

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

        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    
