from enum import Enum
from datetime import date, time

class Status(Enum):
    NOT_STARTED = "not started"
    IN_PROGRESS = "in progress"
    COMPLETE = "complete"

    @staticmethod
    def convertFromString(value:str):
        if value == "Status.NOT_STARTED":
            return Status.NOT_STARTED
        elif value == "Status.IN_PROGRESS":
            return Status.IN_PROGRESS
        elif value == "Status.COMPLETE":
            return Status.COMPLETE
        else:
            raise ValueError(f"invalid status: {value}")

class Task():
    def __init__(self, title:str, description:str, status:Status):
        self.title = title
        self.description = description
        self.status = status

class UnscheduledTask(Task):
    pass

class ScheduledTask(Task):
    def __init__(self, title:str, description:str, status:Status, date:date, startTime:time, endTime:time):
        self.title = title
        self.description = description
        self.status = status
        self.date = date
        self.startTime = startTime
        self.endTime = endTime

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
            #print(f"{task.date.strftime("%m-%d-%y")} | {task.startTime.strftime("%H:%M:%S")} - {task.endTime.strftime("%H:%M:%S")}")
            print()