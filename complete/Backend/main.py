from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import or_
from database import engine, SessionLocal
import models, schemas
from fastapi.middleware.cors import CORSMiddleware
import base64
import random
from typing import List
import asyncio
import cv2
from datetime import datetime
from models import Violator  # 例としてDataModelを使用
from pydantic import BaseModel
from yolov8 import generate_frames_yolo


# データベース変更フラグ
data_change_flag = False

# 最終変更タイムスタンプ
last_modified = None


app = FastAPI()
# データベース作成
models.Base.metadata.create_all(bind=engine)

origins = [
    #"http://localhost:8080",  # フロントエンドが動作するURL
    "http://localhost:8000",
    "http://localhost:5173",
]

# ミドルウェア
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# データベース接続
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_last_modified_timestamp(db: Session):
    return db.query(func.max(models.Violator.last_modified)).scalar()

############################ WebSocket #####################################
# WebSocket接続用のセット
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def send_message(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global data_change_flag
    global last_modified
    await manager.connect(websocket)
    try:
        while True:
            # 一応待機
            await asyncio.sleep(1)


            try:
                # データベース要素数確認
                db = SessionLocal()
                new_last_modified = db.query(func.max(models.Violator.last_modified)).scalar()

                # データベース変更時処理
                if last_modified != new_last_modified:
                    # フロントにメッセージ送信
                    message = "Data Changed"
                    last_modified = new_last_modified
                    await manager.send_message(message)
            finally:
                db.close()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


################################ エンドポイント登録 ##########################
# 全データ取得
@app.get("/violations/", response_model=list[schemas.Violator])
async def read_violations(db: Session = Depends(get_db)):
    violations = db.query(models.Violator).all()
    return violations

# ダミーデータの作成
@app.post("/generate_dummy_data/")
def generate_dummy_data(db: Session = Depends(get_db)):
    global data_change_flag
    violations = ['傘差し運転', '二人乗り', 'スマホ運転']

    # テストとして1つだけ追加
    for i in range(1):
        cam_no = str(random.randint(1, 2))
        #date = '2024-01-01'
        violation = violations[random.randint(0, 2)]
        tracking_id = 'id1'
        # 適当な画像
        image_path = f"images/{cam_no}.png"

        # 画像ファイルを読み込み、Base64エンコード
        with open(image_path, "rb") as image_file:
            image = image_file.read()
            binary_image = base64.b64encode(image)
<<<<<<< HEAD

        db_violation = models.Violator(cam_no=cam_no, date=date, violation=violation, image=binary_image,last_modified=datetime.now(),tracking_id =tracking_id)
=======
        
        db_violation = models.Violator(cam_no=cam_no, date=datetime.now(), violation=violation, image=binary_image,last_modified=datetime.now(),tracking_id =tracking_id)
>>>>>>> d0d5510 (final commit)
        db.add(db_violation)
        db.commit()
        db.refresh(db_violation)
    data_change_flag = True
    return {"message": "Dummy data generated"}

# ダミーデータの削除
@app.delete("/delete_dummy_data/")
def delete_dummy_data(db: Session = Depends(get_db)):
    global data_change_flag
    
    db.query(models.Violator).delete()
    db.commit()
    data_change_flag = True
    return {"message": "Dummy data deleted"}

################################ カメラ映像ストリーミング #####################################

async def generate_frames():
    #camera1 = cv2.VideoCapture(0)
    #camera2 = cv2.VideoCapture(1)
    
    camera1 = cv2.VideoCapture('D:/Research/Social_Infomatics_Lecture/PracticeOfSocialInformatics_2nd/code/resource/test_two_people1.mp4')
    camera2 = cv2.VideoCapture('D:/Research/Social_Infomatics_Lecture/PracticeOfSocialInformatics_2nd/code/resource/test_two_people1.mp4')

    while True:
        success1, frame1 = camera1.read()
        success2, frame2 = camera2.read()
        if not success1 or not success2:
            break
        
        # フレームを横に結合    
        combined_frame = cv2.hconcat([frame1, frame2])

        ret, buffer = cv2.imencode('.jpg', combined_frame)
        if not ret:
            break
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        await asyncio.sleep(0.01)
   

@app.get("/video_feed")
async def video_feed():
    print('****************video************************')
    return StreamingResponse(generate_frames(), media_type='multipart/x-mixed-replace; boundary=frame')  

@app.get("/video_feed_yolo")
async def video_feed_yolo():
    print('****************yolo************************')
    return StreamingResponse(generate_frames_yolo(), media_type='multipart/x-mixed-replace; boundary=frame')  


# フィルタリング条件用のスキーマ
class FilterSchema(BaseModel):
    checkBox1: bool
    checkBox2: bool
    checkBox3: bool
    checkBox4: bool
    checkBox5: bool
    checkBox6: bool
    startDateTime: str
    endDateTime: str

#2ページ目の検索条件付き用
# フィルタリングエンドポイント
@app.post("/search")
def search(filters: FilterSchema, db: Session = Depends(get_db)):
    try:
        query = db.query(Violator)

        #日時
        if filters.startDateTime == '':
            filters.startDateTime = None
        else:
            try:
                filters.startDateTime = datetime.fromisoformat(filters.startDateTime)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid datetime format")
        
        if filters.endDateTime == '':
            filters.endDateTime = None
        else:
            try:
                filters.endDateTime = datetime.fromisoformat(filters.endDateTime)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid datetime format")

        if filters.startDateTime != None and filters.endDateTime != None:
            query = query.filter(Violator.date >= filters.startDateTime,Violator.date <= filters.endDateTime)

        #カメラ番号
        if filters.checkBox1 and not filters.checkBox2 and not filters.checkBox3:
            query = query.filter(Violator.cam_no == '1')
        elif not filters.checkBox1 and filters.checkBox2 and not filters.checkBox3:
            query = query.filter(Violator.cam_no == '2')
        elif not filters.checkBox1 and not filters.checkBox2 and filters.checkBox3:
            query = query.filter(or_(Violator.cam_no == '1,2',Violator.cam_no == '2,1'))
        elif filters.checkBox1 and filters.checkBox2 and not filters.checkBox3:
            query = query.filter(or_(Violator.cam_no == '1',Violator.cam_no == '2'))
        elif filters.checkBox1 and not filters.checkBox2 and filters.checkBox3:
            query = query.filter(or_(Violator.cam_no == '1',Violator.cam_no == '1,2',Violator.cam_no == '2,1'))
        elif not filters.checkBox1 and filters.checkBox2 and filters.checkBox3:
            query = query.filter(or_(Violator.cam_no == '2',Violator.cam_no == '1,2',Violator.cam_no == '2,1'))
        elif filters.checkBox1 and filters.checkBox2 and filters.checkBox3:
            query = query.filter(or_(Violator.cam_no == '1',Violator.cam_no == '2',Violator.cam_no == '1,2',Violator.cam_no == '2,1'))

        #違反内容    
        if filters.checkBox4 and not filters.checkBox5 and not filters.checkBox6:
            query = query.filter(Violator.violation == '傘差し運転')
        elif not filters.checkBox4 and filters.checkBox5 and not filters.checkBox6:
            query = query.filter(Violator.violation == 'スマホ運転')
        elif not filters.checkBox4 and not filters.checkBox5 and filters.checkBox6:
            query = query.filter(or_(Violator.violation == '二人乗り'))
        elif filters.checkBox4 and filters.checkBox5 and not filters.checkBox6:
            query = query.filter(or_(Violator.violation == '傘差し運転',Violator.violation == 'スマホ運転'))
        elif filters.checkBox4 and not filters.checkBox5 and filters.checkBox6:
            query = query.filter(or_(Violator.violation == '傘差し運転',Violator.violation == '二人乗り'))
        elif not filters.checkBox4 and filters.checkBox5 and filters.checkBox6:
            query = query.filter(or_(Violator.violation == 'スマホ運転',Violator.violation == '二人乗り'))
        elif filters.checkBox4 and filters.checkBox5 and filters.checkBox6:
            query = query.filter(or_(Violator.violation == '傘差し運転',Violator.violation == 'スマホ運転',Violator.violation == '二人乗り'))
        data = query.all()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#画像認識用

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
