from enum import Enum
from time import struct_time

class Status(Enum):
    NOT_STARTED = "not_started"
    STARTED = "started"
    COMPLETE = "complete"

class Task:
    def __init__(self, title:str, description:str, status:Status) -> None:
        self.title:str = title
        self.description:str = description
        self.status:Status = status

    @staticmethod
    def convertToStructured(task:UnstructuredTask, startTime:struct_time, endTime:struct_time) -> StructuredTask:
        return StructuredTask(task.title, task.description, task.status, startTime, endTime)
    
    @staticmethod
    def convertToUnStructured(task:StructuredTask) -> UnstructuredTask:
        return UnstructuredTask(task.title, task.description, task.status)

class UnstructuredTask(Task):
    def __init__(self, title:str, description:str, status:Status):
        super().__init__(title, description, status)

class StructuredTask(Task):
    def __init__(self, title:str, description:str, status:Status, startTime:struct_time, endTime:struct_time):
        super().__init__(title, description, status)
        self.startTime = startTime
        self.endTime = endTime