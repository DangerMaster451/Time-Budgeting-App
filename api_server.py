from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from tasks import Task, UnscheduledTask, ScheduledTask, TaskList, Status
from datetime import date, time, datetime, timedelta
from session import Session, SessionList
import json
import uuid

task_list = TaskList()
session_list = SessionList()

task_list.append(ScheduledTask(title="Task 1", description="This is task 1", status=Status.NOT_STARTED, date=date(2026, 3, 2), startTime=time(9, 0), endTime=time(10, 0)))

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
        return { "message":task_list }
    else:
        return {"validated ": v}

@app.post("/add-task")
async def add_task(task:ScheduledTask):
    try:
        task_list.append(task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return { "message": "Task added successfully" }