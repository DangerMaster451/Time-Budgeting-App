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

def validate_password(username:str, password:str, users) -> bool:
    stored_password = users[username]["password"].encode("utf-8")
    #print(f"User Password: {hash}")
    print(f"Stored Password: {stored_password}")
    return bcrypt.checkpw(password.encode("utf-8"), stored_password)

@app.get("/")
async def root():
    return { "message": "Home" }

@app.post("/new-user")
async def new_user(request:Request, username, password):
    with open("users.json", "r") as file:
        users = json.load(file)
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode("utf-8"), salt)

    userData = {
        "password": hash.decode("utf-8"),
        "id": str(uuid.uuid4())
    }

    users[username] = userData
    with open("users.json", "w") as file:
        file.write(json.dumps(users, indent=4))

@app.post("/log-in")
async def log_in(request:Request, username:str, password:str):
    with open("users.json", "r") as file:
        users = json.load(file)
        if username in users and validate_password(username, password, users):
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

#@app.post("/add-task")
#async def add_task(task:ScheduledTask):
#    try:
#        task_list.append(task)
#    except ValueError as e:
#        raise HTTPException(status_code=400, detail=str(e))
#    return { "message": "Task added successfully" }