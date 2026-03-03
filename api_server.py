from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from tasks import Task, UnscheduledTask, ScheduledTask, TaskList, Status
from datetime import date, time, datetime, timedelta
from session import Session, SessionList
import json
import uuid

session_list = SessionList()

app = FastAPI()

@app.get("/")
async def root():
    return { "message": "Home" }

@app.post("/log-in")
async def log_in(request:Request, username:str, password:str):
    with open("users.json", "r") as file:
        users = json.load(file)
        if username in users:
            if users[username]["password"] == password:
                return { "session":Session(username, request.client.host, session_list)} #type:ignore
            else:
                raise HTTPException(status_code=403, detail=f"Incorrect Password, try '{users[username]["password"]}'")
        else:
            raise HTTPException(status_code=404, detail="User not found :/")

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