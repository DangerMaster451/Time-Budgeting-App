import json
import uuid
from AuthService import Session

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
            json.dump(fileData, file, indent=4)        
        
    @staticmethod 
    def get_user_tasks(id):
        with open("tasks.json", "r") as file:
            data = json.load(file)
            tasks = data[id]["tasks"]
            return tasks
        
    @staticmethod
    def new_task(id:uuid.UUID, title:str, description:str, status:str, date:str, startTime:str, endTime:str):
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

    @staticmethod
    def new_session(session:Session):
        with open("sessions.json", "r+") as file:
            data = json.load(file)
            data.append(
                {
                    "token":str(session.token),
                    "expireTime":str(session.expireTime),
                    "username":session.username,
                    "ip":session.ip,
                    "id":str(session.id)
                }
            )
            file.seek(0)
            json.dump(data, file, indent=4)

    @staticmethod
    def get_sessions():
        with open("sessions.json", "r") as file:
            data = json.load(file)
            sessions:list[Session] = []
            for s in data:
                sessions.append(Session(s["token"], s["expireTime"], s["username"], s["ip"], s["id"]))
            return sessions