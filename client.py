from tasks import Task, TaskList
from session import Session
from getpass import getpass
import requests
import uuid

url = "http://127.0.0.1:8000"

def login() -> str:
    print("Please Log In:")
    username = input("Username: ")
    password = getpass(prompt="Password: ")

    r = requests.post(f"{url}/log-in?username={username}&password={password}")

    if r.status_code == 200:
        return r.json()["session"]
    else:
        raise ConnectionError(f"{r.status_code}:{r.json()["detail"]}")
    
def getTasks(token:uuid.UUID):
    r = requests.get(f"{url}/all-tasks?token={token}")

    if r.status_code == 200:
        return r.text
    else:
        raise ConnectionError(f"{r.status_code}:{r.json()["detail"]}")






while True:
    try:
        session = login()
        token = uuid.UUID(session["token"])
        break
    except ConnectionError as e:
        print(e)

try:
    tasks = getTasks(token)
    print(tasks)
except ConnectionError as e:
    print(e)
