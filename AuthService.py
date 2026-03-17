import uuid
import json
import bcrypt
from datetime import datetime, timedelta
from fastapi import Request, HTTPException

class Session():
    def __init__(self, token:uuid.UUID, expireTime:datetime, username:str, ip:str, id:uuid.UUID):
        self.token = token
        self.expireTime:datetime = expireTime
        self.username:str = username
        self.ip:str = ip
        self.id:uuid.UUID = id

class SessionList(dict[uuid.UUID, Session]):
    def __init__(self):
        super().__init__(self)        
    
class Auth():
    @staticmethod
    def new_session():
         #
         pass
    

    @staticmethod
    def validate_session(request:Request, user_token:uuid.UUID, active_sessions:list[Session]) -> Session:
        for s in active_sessions:
            if str(user_token) == str(s.token):
                session = s
                break
        else:            
            raise HTTPException(403, "Session Not Found")
        #if session.expireTime < datetime.now():
        #    raise HTTPException(403, "Session Expired")
        if request.client.host != session.ip: #type: ignore
            print("host doesn't match stored ip")
            raise HTTPException(403, "Session does not match IP, please log in again")
        return session
        
    @staticmethod
    def validate_new_username(username:str) -> bool:
        with open("users.json", "r") as file:
            data = json.load(file)
            if username in data:
                return False
            return True

    @staticmethod
    def hash_new_password(password:str) -> bytes:
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hash

    @staticmethod
    def validate_password(username:str, password:str, users) -> bool:
        stored_password = users[username]["password"].encode("utf-8")
        return bcrypt.checkpw(password.encode("utf-8"), stored_password)
    
    @staticmethod
    def login(request:Request, username:str, password:str) -> Session:
        with open("users.json", "r") as file:
            users = json.load(file)
            if not username in users:
                raise HTTPException(status_code=403, detail=f"Invalid Username")
            if not Auth.validate_password(username, password, users):
                raise HTTPException(status_code=403, detail=f"Invalid Password")
            
            return Session(uuid.uuid4(), datetime.now() + timedelta(minutes=30), username, request.client.host, users[username]["id"]) #type:ignore
                    
