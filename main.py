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
    def convertToStructured(task:UnstructuredTask, startTime:time, endTime:time) -> StructuredTask:
        return StructuredTask(task.title, task.description, task.status, startTime, endTime)
    
    @staticmethod
    def convertToUnStructured(task:StructuredTask) -> UnstructuredTask:
        return UnstructuredTask(task.title, task.description, task.status)

class UnstructuredTask(Task):
    def __init__(self, title:str, description:str, status:Status):
        super().__init__(title, description, status)

class StructuredTask(Task):
    def __init__(self, title:str, description:str, status:Status, startTime:time, endTime:time):
        super().__init__(title, description, status)
        self.startTime = startTime
        self.endTime = endTime

class TaskList(list[StructuredTask]):
    def __init__(self):
        super().__init__(self)
    
    def _validate(self, item:StructuredTask) -> bool:
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
class Day():
    def __init__(self, date:date):
        self.date = date
        self.tasks:TaskList = TaskList()

    def sortTasks(self):
        self.tasks.sort(key = lambda task: task.startTime)

    def displayTasks(self):
        self.sortTasks()
        for task in self.tasks:
            print(task.title)
            print(task.description)
            print(task.status)
            print(f"{task.startTime.strftime("%H:%M:%S")} - {task.endTime.strftime("%H:%M:%S")}")
            print()


d = Day(date.today())

d.tasks.append(StructuredTask("Task 1", "Stuff", Status.NOT_STARTED, time.fromisoformat("07:15:00"), time.fromisoformat("08:00:00")))
d.tasks.append(StructuredTask("Task 2", "More Stuff", Status.IN_PROGRESS, time.fromisoformat("08:00:00"), time.fromisoformat("08:30:00")))
d.tasks.append(StructuredTask("Task 3", "Even More Stuff", Status.IN_PROGRESS, time.fromisoformat("08:30:00"), time.fromisoformat("08:45:00")))

d.displayTasks()