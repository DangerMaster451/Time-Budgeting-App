from fastapi import Request, HTTPException
from AuthService import Auth
import uuid
from DataService import DataService

class UserService():
    @staticmethod
    def new_user(request:Request, username:str, password:str):
        if Auth.validate_new_username(username) == False:
            raise HTTPException(status_code=403, detail="Username already exists")
        hash = Auth.hash_new_password(password)
        id = uuid.uuid4()
        DataService.new_user(username, hash, id)