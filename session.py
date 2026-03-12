import uuid
from datetime import datetime, timedelta
from fastapi import Request

class Session():
    def __init__(self, username:str, ip:str, session_list:SessionList):
        self.token = uuid.uuid4()
        self.expireTime:datetime = datetime.now() + timedelta(minutes=30)
        self.username:str = username
        self.ip:str = ip
        session_list[self.token] = self

class SessionList(dict[uuid.UUID, Session]):
    def __init__(self):
        super().__init__(self)

    def validateSession(self, request:Request, session_id:uuid.UUID) -> bool:
        if session_id in self:
            session = self[session_id]
        else:
            return False
        if session.expireTime < datetime.now():
            print("session expired")
            return False
        if request.client.host != self[session_id].ip: #type: ignore
            print("host doesn't match stored ip")
            return False
        return True