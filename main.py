import requests
import json
import time
import random 
import pathlib
import os
import datetime


config = json.load(open("isthatright.json"))
token = config["config"]["token"]

url = f"https://api.telegram.org/bot{token}/" 
frogs_list = list((pathlib.Path(__file__).parent/"frogs").iterdir())

with open("users.txt", "r") as f:
    users = set(int(line) for line in f.readlines() if line.strip())

def update_users(user_id):
    users.add(user_id)
    with open("users.txt", "w") as f:
        f.write(str(user_id))
        f.write(os.linesep) 


def process_updates():
    updates = requests.get(url+f"getUpdates")
    print(updates.json())

    for update in updates.json()["result"]:
        if "message" not in update:
            continue

        username = ""
        user_id = int(update["message"]["chat"]["id"])
        if "username" in update["message"]["from"]:
            username = update["message"]["from"]["username"]
        elif "first_name" in update["message"]["from"]:
            username = update["message"]["from"]["first_name"]
        if not username:
            username = "anon"
            
                
        if user_id not in users:
            time_to_send_frog(user_id)
            update_users(user_id)

            requests.post(url+"sendMessage", data={
                "chat_id": user_id,
                "text": f"Hello, {username}. I'm here to hail all Wednesdudes!"
            })
            

        # else:
        #     requests.post(url+"sendMessage", data={
        #         "chat_id": user_id,
        #         "text": f"Sorry, don't get it."
        #     })

last_day = 0

def time_to_send_frog(user_id):

    today_frog = random.choice(frogs_list)
    print("sending file")
    status = requests.post(url+"sendPhoto", files={
        "photo": today_frog.open("br").read()
    }, data={
        "chat_id": user_id
    })
    print(status.status_code, user_id)


def try_to_send_frog():
    date = datetime.datetime.now()
    
    if date.weekday == 2 and date.hour == 3 and date.minute == 13 and last_day != date.day:
        last_day = date.day

        for user_id in users:
            time_to_send_frog(user_id)


while True:
    process_updates()
    try_to_send_frog()

    time.sleep(1)