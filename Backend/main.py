from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import  StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from database import engine, SessionLocal
import models, schemas
from fastapi.middleware.cors import CORSMiddleware
import base64
import random
from typing import List
import asyncio
import cv2
from datetime import datetime
from yolov8 import generate_frames_yolo


# 最終変更タイムスタンプ
last_modified = None

app = FastAPI()
# データベース作成
models.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:8080",  # フロントエンドが動作するURL
    "http://localhost:8000",
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
    violations = ['傘差し運転', '二人乗り', 'スマホ運転']

    # テストとして1つだけ追加
    for i in range(1):
        cam_no = random.randint(1, 3)
        date = '2024-01-01'
        violation = violations[random.randint(0, 2)]
        # 適当な画像
        image_path = f"images/{cam_no}.png"

        # 画像ファイルを読み込み、Base64エンコード
        with open(image_path, "rb") as image_file:
            image = image_file.read()
            binary_image = base64.b64encode(image)
        
        db_violation = models.Violator(cam_no=cam_no, date=date, violation=violation, image=binary_image, last_modified=datetime.now())
        db.add(db_violation)
        db.commit()
        db.refresh(db_violation)
    return {"message": "Dummy data generated"}

# ダミーデータの削除
@app.delete("/delete_dummy_data/")
def delete_dummy_data(db: Session = Depends(get_db)): 
    db.query(models.Violator).delete()
    db.commit()
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)