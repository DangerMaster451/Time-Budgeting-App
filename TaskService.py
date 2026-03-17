from enum import Enum
from datetime import date, time, datetime
from pydantic import BaseModel

class Status(Enum):
    NOT_STARTED = "not started"
    IN_PROGRESS = "in progress"
    COMPLETE = "complete"

class Task(BaseModel):
    title:str
    description:str
    status:Status

class UnscheduledTask(Task):
    pass

class ScheduledTask(Task):
    date:date
    startTime:time
    endTime:time

class TaskList(list[ScheduledTask]):
    def __init__(self):
        super().__init__(self)
    
    def _validate(self, item:ScheduledTask) -> bool:
        for i in self:
            if i.startTime < item.startTime < i.endTime:
                return False
            if i.startTime < item.endTime < i.endTime:
                return False
        return True

    def append(self, item):
        if self._validate(item):
            super().append(item)
        else:
            raise ValueError("Cannot double book times")
        

    def sortTasks(self):
        self.sort(key = lambda task: task.startTime)

    def displayTasks(self):
        self.sortTasks()
        for task in self:
            print(task.title)
            print(task.description)
            print(task.status)
            print(f"{task.date.strftime("%m-%d-%y")} | {task.startTime.strftime("%H:%M:%S")} - {task.endTime.strftime("%H:%M:%S")}")
            print()