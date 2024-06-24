from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models, schemas
from fastapi.middleware.cors import CORSMiddleware
import base64
import random
from typing import List
import asyncio

# データベース変更フラグ
data_change_flag = False


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
    await manager.connect(websocket)
    try:
        while True:
            # 一応待機
            await asyncio.sleep(1)
            # データベース変更時処理
            if data_change_flag:
                # フロントにメッセージ送信
                message = "Data Changed"
                data_change_flag = False
                await manager.send_message(message)
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
        cam_no = random.randint(1, 3)
        date = '2024-01-01'
        violation = violations[random.randint(0, 2)]
        # 適当な画像
        image_path = f"images/{cam_no}.png"

        # 画像ファイルを読み込み、Base64エンコード
        with open(image_path, "rb") as image_file:
            image = image_file.read()
            binary_image = base64.b64encode(image)
        
        db_violation = models.Violator(cam_no=cam_no, date=date, violation=violation, image=binary_image)
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)