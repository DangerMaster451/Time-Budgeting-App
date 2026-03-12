from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from tasks import Task, UnscheduledTask, ScheduledTask, TaskList, Status
from datetime import date, time, datetime, timedelta
from session import Session, SessionList
import json
import uuid
import bcrypt

session_list = SessionList()

app = FastAPI()

def validate_new_username(username:str) -> bool:
    with open("users.json", "r") as file:
        data = json.load(file)
        if username in data:
            return False
        return True

def hash_new_password(password:str) -> bytes:
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hash

def check_user_password(username:str, password:str, users) -> bool:
    stored_password = users[username]["password"].encode("utf-8")
    return bcrypt.checkpw(password.encode("utf-8"), stored_password)

def updateUsersFile(validUsername:str, hash:bytes, uuid:uuid.UUID):
    with open("users.json", "r+") as file:
        fileData = json.load(file)
        fileData[validUsername] = {
                "password": hash.decode("utf-8"),
                "id": str(uuid)
            }
        file.seek(0)
        json.dump(fileData, file, indent=4)

def updateTasksFile(uuid:uuid.UUID, validUsername:str):
    with open("tasks.json", "r+") as file:
        fileData = json.load(file)
        fileData[str(uuid)] = {
            "username": validUsername,
            "tasks": []
        }
        file.seek(0)
        json.dump(fileData, file, indent=4)


@app.get("/")
async def root():
    return { "message": "Home" }

@app.post("/new-user")
async def new_user(request:Request, username, password):
    if validate_new_username(username) == False:
        raise HTTPException(status_code=403, detail="Username already exists")
    hash = hash_new_password(password)
    id = uuid.uuid4()
    updateUsersFile(username, hash, id)
    updateTasksFile(id, username)


@app.post("/log-in")
async def log_in(request:Request, username:str, password:str):
    with open("users.json", "r") as file:
        users = json.load(file)
        if username in users and check_user_password(username, password, users):
            return { "session":Session(username, request.client.host, session_list)} #type:ignore
        else:
                raise HTTPException(status_code=403, detail=f"Invalid login")

@app.get("/all-tasks")
async def tasks(request:Request, token:uuid.UUID):
    v = session_list.validateSession(request, token)
    if v:
        with open("users.json", "r") as file:
            data = json.load(file)
            id = data[session_list[token].username]["id"]
            
        with open("tasks.json", "r") as file:
            data = json.load(file)
            tasks = data[id]["tasks"]

        return { "message":tasks }
    else:
        return {"validated ": v}

@app.post("/add-task")
async def add_task(request:Request, token:uuid.UUID, title:str, description:str, status:str, date:str, startTime:str, endTime:str):
    v = session_list.validateSession(request, token)
    if not v:
        raise HTTPException(status_code=403, detail="Invalid login")
    
    with open("users.json", "r") as file:
        data = json.load(file)
        id = data[session_list[token].username]["id"]
    
    with open("tasks.json", "r+") as file:
        data = json.load(file)

        newTask = {
                "title":title,
                "description":description,
                "status":status,
                "date":date,
                "startTime":startTime,
                "endTime":endTime
            }

        data[id]["tasks"].append(newTask)
        file.seek(0)
        
        json.dump(data, file, indent=4)