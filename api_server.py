from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tasks import Task, UnscheduledTask, ScheduledTask, TaskList, Status
from datetime import date, time
import json

task_list = TaskList()

task_list.append(ScheduledTask(title="Task 1", description="This is task 1", status=Status.NOT_STARTED, date=date(2026, 3, 2), startTime=time(9, 0), endTime=time(10, 0)))

app = FastAPI()

@app.get("/")
async def root():
    return { "message": "Home" }

@app.post("/log-in")
async def log_in(username:str, password:str):
    with open("users.json", "r") as file:
        users = json.load(file)
        if username in users:
            if users[username]["password"] == password:
                return { "message":"successfully logged in!"}
            else:
                raise HTTPException(status_code=403, detail=f"Incorrect Password, try '{users[username]["password"]}'")
        else:
            raise HTTPException(status_code=404, detail="User not found :/")

@app.get("/all-tasks")
async def tasks():
    return { "message":task_list }

@app.post("/add-task")
async def add_task(task:ScheduledTask):
    try:
        task_list.append(task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return { "message": "Task added successfully" }