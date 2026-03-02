from enum import Enum
from datetime import date, datetime, timedelta

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
    def convertToStructured(task:UnstructuredTask, startTime:datetime, endTime:datetime) -> StructuredTask:
        return StructuredTask(task.title, task.description, task.status, startTime, endTime)
    
    @staticmethod
    def convertToUnStructured(task:StructuredTask) -> UnstructuredTask:
        return UnstructuredTask(task.title, task.description, task.status)

class UnstructuredTask(Task):
    def __init__(self, title:str, description:str, status:Status):
        super().__init__(title, description, status)

class StructuredTask(Task):
    def __init__(self, title:str, description:str, status:Status, startTime:datetime, endTime:datetime):
        super().__init__(title, description, status)
        self.startTime = startTime
        self.endTime = endTime

class Day():
    def __init__(self, date:date, tasks:list[StructuredTask] = []):
        self.tasks:list[StructuredTask] = tasks

    def sortTasks(self):
        self.tasks.sort(key = lambda task: task.startTime)

    def displayTasks(self):
        self.sortTasks()
        for task in self.tasks:
            print(task.title)
            print(task.description)
            print(task.status)
            print(f"{task.startTime.time()} - {task.endTime.time()}")
            print()


d = Day(date.today(), [StructuredTask("Task 1", "Stuff", Status.NOT_STARTED, datetime.now(), datetime(2026, 3, 1, 19, 0, 0)),
                   StructuredTask("Task 2", "More Stuff", Status.IN_PROGRESS, datetime(2026, 3, 1, 19, 0, 0), datetime(2026, 3, 1, 20, 0, 0)),
                   StructuredTask("Task 3", "Even More Stuff", Status.IN_PROGRESS, datetime(2026, 3, 1, 11, 0, 0), datetime(2026, 3, 1, 12, 0, 0))
                   ])

d.displayTasks()