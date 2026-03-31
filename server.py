from fastapi import FastAPI, HTTPException, Request
import datetime
from AuthService import Session, SessionList, Auth
from DataService import DataService
from UserService import UserService
from TaskService import ScheduledTask, Task, TaskList, Status
from EncourageService import EncourageService
import uuid

app = FastAPI()

@app.get("/", status_code=200)
async def root():
    return { "message": "Home" }

@app.post("/new-user", status_code=201)
async def new_user(request:Request, username:str, password:str):
    UserService.new_user(request, username, password)

@app.post("/log-in", status_code=200)
async def log_in(request:Request, username:str, password:str):
    session = Auth.login(request, username, password)
    DataService.new_session(session)
    return { "session":session }
        
@app.get("/get-tasks", status_code=200)
async def get_tasks(request:Request, session_token:uuid.UUID):
    session = Auth.validate_session(request, session_token, DataService.get_sessions())
    return DataService.get_user_tasks(session.id)
    
@app.post("/add-task", status_code=201)
async def add_task(request:Request, session_token:uuid.UUID, title:str, description:str, status:Status, date:str, startTime:str, endTime:str):
    session = Auth.validate_session(request, session_token, DataService.get_sessions())

    task = ScheduledTask(
        title,
        description,
        status,
        datetime.date.fromisoformat(date),
        datetime.time.fromisoformat(startTime),
        datetime.time.fromisoformat(endTime)
        )
    DataService.new_task(session.id, task)

@app.get("/get-encouragement", status_code=200)
async def getEncouragement(request:Request, session_token:uuid.UUID):
    session = Auth.validate_session(request, session_token, DataService.get_sessions())
    return EncourageService.giveEncouragement()