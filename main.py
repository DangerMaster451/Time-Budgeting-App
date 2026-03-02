from enum import Enum
from datetime import date, time, datetime

class Status(Enum):
    NOT_STARTED = "not started"
    IN_PROGRESS = "in progress"
    COMPLETE = "complete"

class Task:
    def __init__(self, title:str, description:str, status:Status) -> None:
        self.title:str = title
        self.description:str = description
        self.status:Status = status

    @staticmethod
    def convertToScheduled(task:UnscheduledTask, date:date, startTime:time, endTime:time) -> ScheduledTask:
        return ScheduledTask(task.title, task.description, task.status, date, startTime, endTime)
    
    @staticmethod
    def convertToUnScheduled(task:ScheduledTask) -> UnscheduledTask:
        return UnscheduledTask(task.title, task.description, task.status)

class UnscheduledTask(Task):
    def __init__(self, title:str, description:str, status:Status):
        super().__init__(title, description, status)

class ScheduledTask(Task):
    def __init__(self, title:str, description:str, status:Status, date:date, startTime:time, endTime:time):
        super().__init__(title, description, status)
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
            print(f"{task.date.strftime("%m-%d-%y")} | {task.startTime.strftime("%H:%M:%S")} - {task.endTime.strftime("%H:%M:%S")}")
            print()


t = TaskList()

t.append(ScheduledTask("Task 1", "Stuff", Status.NOT_STARTED, date.today(), time.fromisoformat("07:15:00"), time.fromisoformat("08:00:00")))
t.append(ScheduledTask("Task 2", "More Stuff", Status.IN_PROGRESS, date.today(), time.fromisoformat("08:00:00"), time.fromisoformat("08:30:00")))
t.append(ScheduledTask("Task 3", "Even More Stuff", Status.IN_PROGRESS, date.today(), time.fromisoformat("08:30:00"), time.fromisoformat("08:45:00")))

t.displayTasks()