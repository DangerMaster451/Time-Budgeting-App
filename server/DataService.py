import json
import uuid
from datetime import datetime
from dateutil import parser
from AuthService import Session
from TaskService import Task, TaskList, ScheduledTask, Status

class DataService():
    @staticmethod
    def new_user(validUsername:str, hash:bytes, uuid:uuid.UUID):
        with open("users.json", "r+") as file:
            fileData = json.load(file)
            fileData[validUsername] = {
                    "password": hash.decode("utf-8"),
                    "id": str(uuid)
                }
            file.seek(0)
            json.dump(fileData, file, indent=4)

        with open("tasks.json", "r+") as file:
            fileData = json.load(file)
            fileData[str(uuid)] = {
                "username": validUsername,
                "tasks": []
            }
            file.seek(0)
            json.dump(fileData, file, indent=4, cls=JSONEncoder)
        
    @staticmethod 
    def get_user_tasks(id):
        with open("tasks.json", "r") as file:
            data = json.load(file)
            tasks = decodeTasks(data[id]["tasks"])
            return tasks
        
    @staticmethod
    def new_task(user_id:uuid.UUID, scheduledTask:ScheduledTask):
        with open("tasks.json", "r+") as file:
            data = json.load(file)
            data[user_id]["tasks"].append(scheduledTask)
            file.seek(0)
            json.dump(data, file, indent=4, cls=JSONEncoder)

    @staticmethod
    def new_session(session:Session):
        with open("sessions.json", "r+") as file:
            data = json.load(file)
            data.append(session)
            file.seek(0)
            json.dump(data, file, indent=4, cls=JSONEncoder)

    @staticmethod
    def get_sessions():
        with open("sessions.json", "r") as file:
            data = json.load(file)
            sessions:list[Session] = []
            for s in data:
                sessions.append(Session(s["token"], s["expireTime"], s["username"], s["ip"], s["id"]))
            return sessions
        
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ScheduledTask):
            return {
                "__type__":"ScheduledTask",
                "title":o.title,
                "description":o.description,
                "status":str(o.status),
                "date":o.date.isoformat(),
                "startTime":o.startTime.isoformat(),
                "endTime":o.endTime.isoformat()
            }
        elif isinstance(o, Task):
            return {
                "__type__": "Task",
                "title":o.title,
                "description":o.description,
                "status":o.status
            }
        elif isinstance(o, Session):
            return {
                "token":str(o.token),
                "expireTime":str(o.expireTime),
                "username":o.username,
                "ip":o.ip,
                "id":str(o.id)
            }
        elif isinstance(o, TaskList):
            return o
        elif isinstance(o, Status):
            return str(o)
        elif isinstance(o, uuid.UUID):
            return str(o)
        return super().default(o)

def decodeTasks(data) -> list[Task]:
    print(data)
    print(type(data))
    tasks = []
    for item in data:
        if item["__type__"] == "Task":
            title = item["title"]
            description = item["description"]
            status = Status.convertFromString(item["status"])
            tasks.append(Task(title, description, status))
        elif item["__type__"] == "ScheduledTask":
            title = item["title"]
            description = item["description"]
            status = Status.convertFromString(item["status"])
            date = parser.parse(item["date"])
            startTime = parser.parse(item["startTime"])
            endTime = parser.parse(item["endTime"])
            tasks.append(ScheduledTask(title, description, status, date, startTime, endTime))

    return tasks