from getpass import getpass
import requests


url = "http://127.0.0.1:8000"


def login():
    print("Please Log In:")
    username = input("Username: ")
    password = getpass(prompt="Password: ")

    r = requests.post(f"{url}/log-in?username={username}&password={password}")

    if r.status_code == 200:
        print(r.json()["message"])
    else:
        print(f"{r.status_code}: {r.json()["detail"]}")

login()