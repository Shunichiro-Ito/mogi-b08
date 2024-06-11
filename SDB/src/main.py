# Description: This is the main file of the project. It is responsible for creating the FastAPI app and running the server.
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

#config
import config

#Model
from models import User, Base, LineDataModel, InCafeteriaDataModel

#utils
import utils

#Schema
from schemas import *

#others
import datetime

try:
    engine = create_engine(config.URL_DB, isolation_level="AUTOCOMMIT")
except:
    engine = create_engine(f'{config.SERVICE}://{config.DB_USER}:{config.PASSWORD}@{config.HOST}:{config.PORT}/{config.DATABASE}', isolation_level="AUTOCOMMIT")
print(config.RESET)
if config.RESET:
    print("Dropping all tables")
    Base.metadata.drop_all(engine)

Base.metadata.create_all(engine)
GlobalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

#Cors Middleware
origins = [
    # svelte dev server
    "http://localhost:5173",
    # svelte deployed server
    "https://sdf-front.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = GlobalSession()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_root():
    return {"msg": "Hello World"}

"""@app.get("/AddUser")
async def add_user():
    session = GlobalSession()
    user = User(name="John Doe", email="JohnDoedoe.com", password="password")
    session.add(user)
    session.commit()
    session.close()
    return {"msg": "User added"}

@app.get("/GetUsers")
async def get_users():
    session = GlobalSession()
    users = session.query(User).all()
    session.close()
    return {"users": users}"""

@app.get("/database_reset")
async def reset_database(password: str):
    if password != "password":
        return {"msg": "Wrong password"}
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return {"msg": "Database reset"}

@app.get("/Sample_normal_data")
async def sample_normal_data():
    res_data = []
    for d in preD.data:
        res_data.append(d / 15.5)
    return {"data": res_data, "interval": "1.0", "start": preD.starttime, "number" : 61}

@app.get("/get_Status", response_model=CafeteriaStatusResponse)
async def get_status():
    #return random Cafeteria Status
    if not utils.is_cafeteria_open(utils.date_now()):
        return {"status": CafeteriaStatus.CLOSED}
    else:
        start_time = utils.date_now().replace(hour=11, minute=45, second=0, microsecond=0)
        end_time = utils.date_now().replace(hour=12, minute=45, second=0, microsecond=0)
        if utils.date_now() < start_time:
            return {"status": CafeteriaStatus.LOW}
        elif utils.date_now() > end_time:
            return {"status": CafeteriaStatus.LOW}
        else:
            if current_Data.Line_length > 15:
                return {"status": CafeteriaStatus.HIGH}
            else:
                return {"status": CafeteriaStatus.MIDIUM}

@app.get("/average_line_length")
async def average_line_length(start_time: datetime.datetime, end_time: datetime.datetime, db: Session = Depends(get_db)):
    try:
        data = db.query(LineDataModel).filter(LineDataModel.timestamp >= start_time, LineDataModel.timestamp <= end_time).all()
        if not data:
            raise HTTPException(status_code=404, detail="Data not found")
        avg_line_length = sum([d.Line_length for d in data]) / len(data)
        return {"average_line_length": avg_line_length}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

current_Data = AllData(timestamp=utils.date_now().isoformat(), Line_length=0, num_in_cafeteria=0)
@app.get("/real_data", response_model=AllData)
async def get_real():
    return current_Data

@app.get("/real_data/line/all")
async def get_all_line_data():
    session = GlobalSession()
    try:
        line_data = session.query(LineDataModel).all()
        return {
            "data": [
                {"timestamp": data.timestamp, "Line_length": data.Line_length}
                for data in line_data
            ]
        }
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return {"error": "An error occurred while fetching data"}
    finally:
        session.close()

@app.post("/real_data/incafe")
async def post_real(data: InCafeteriaData, db: Session =  Depends(get_db)):
    global current_Data
    current_Data.set_num_in_cafeteria(data.num_in_cafeteria)
    current_Data.set_timestamp(utils.date_now().isoformat())
    try:
        db_data = InCafeteriaDataModel(timestamp=data.timestamp, num_in_cafeteria=data.num_in_cafeteria)
        db.add(db_data)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    return {"msg": "Incafe Data received", "data": data}

@app.get("/real_data/incafe/all")
async def get_all_incafe_data(db: Session = Depends(get_db)):
    try:
        data = db.query(InCafeteriaDataModel).all()
        return {
            "data": [
                {"timestamp": d.timestamp, "num_in_cafeteria": d.num_in_cafeteria}
                for d in data
            ]
        }
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=str(e))

preD = PredictData(data=[0]*61, starttime=utils.date_now())
@app.post("/predict_data")
async def post_predict_data(data: PredictData):
    global preD
    preD = data
    if len(preD.data) > 61:
        preD.data = preD.data[:61]
    while len(preD.data) != 61:
        preD.data.append(0)
    print(data)
    return {"msg": "Predict Data received", "data": data.data}

@app.post("/real_data/line")
async def post_line_num(data: LineData):
    global current_Data
    current_Data.set_Line_length(data.Line_length)
    current_Data.set_timestamp(utils.date_now().isoformat())

    session = GlobalSession()
    try:
        new_line_data = LineDataModel(timestamp=data.timestamp, Line_length=data.Line_length)
        session.add(new_line_data)
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Database error: {e}")
    finally:
        session.close()

    return {"msg": "Line Data received", "data": data}


if __name__ == "__main__":
    if config.IS_IN_DOCKER:
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        uvicorn.run(app, host="127.0.0.1", port=8000)