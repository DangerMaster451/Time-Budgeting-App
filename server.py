from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from datetime import date, time, datetime, timedelta
from AuthService import Session, SessionList, Auth
from DataService import DataService
from UserService import UserService
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
    id = session.id
    return DataService.get_user_tasks(id)
    
@app.post("/add-task", status_code=201)
async def add_task(request:Request, session_token:uuid.UUID, title:str, description:str, status:str, date:str, startTime:str, endTime:str):
    session = Auth.validate_session(request, session_token, DataService.get_sessions())
    id = session.id
    DataService.new_task(id, title, description, status, date, startTime, endTime)