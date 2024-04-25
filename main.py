import requests
import json
import time
import random 
import pathlib
import os
import datetime
import logging


logging.getLogger().setLevel(logging.DEBUG)


last_day = 0
config = json.load(open("isthatright.json"))
token = config["config"]["token"]

url = f"https://api.telegram.org/bot{token}/" 
frogs_list = list((pathlib.Path(__file__).parent/"frogs").iterdir())
logging.info(f"Loaded {len(frogs_list)} frogs!")

with open("users.txt", "r") as f:
    users = set(int(line) for line in f.readlines() if line.strip())
    logging.info(f"Loaded {len(users)} users!")


def update_users(user_id):
    users.add(user_id)
    with open("users.txt", "a") as f:
        f.write(str(user_id))
        f.write(os.linesep)
    logging.info(f"Added {user_id} user!") 


def process_updates():
    updates = requests.get(url+f"getUpdates")
    logging.info(f"Recieved {updates.status_code} from /getUpdates")
    
    try:
        updates = updates.json()
    except:
        logging.error(f"Recieved '{updates.text}' is not json")
        return

    if not updates["ok"]:
        logging.error(f"We got '{updates['description']}' error")
        return

    for update in updates["result"]:
        logging.debug(f"Update == {update}!")
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
            date = datetime.datetime.now()
            if date.weekday() == 2:
                time_to_send_frog(user_id)
            update_users(user_id)

            resp = requests.post(url+"sendMessage", data={
                "chat_id": user_id,
                "text": f"Hello, {username}. I'm here to hail all Wednesdudes!"
            })
            logging.info(f"Greet new user '{username}' with status_code == {resp.status_code}")


def time_to_send_frog(user_id):
    today_frog = random.choice(frogs_list)
    resp = requests.post(url+"sendPhoto", files={
        "photo": today_frog.open("br").read()
    }, data={
        "chat_id": user_id
    })
    logging.info(f"Sent the frog to user {user_id} with status_code == {resp.status_code}, eller hur?")


def try_to_send_frog():
    date = datetime.datetime.now()
    global last_day
    is_time = date.weekday() == 2 and date.hour == 4 and date.minute == 7 and last_day != date.day
    logging.debug(f"Is it time to send frog now?")
    logging.debug(f"({date.weekday()} == 2"
                  f" and {date.hour} == 4"
                  f" and {date.minute} == 7"
                  f" and {last_day} != {date.day}) == {is_time}")
    if is_time:
        last_day = date.day

        for user_id in users:
            time_to_send_frog(user_id)


t = time.time()
while True:
    if time.time() - t < 1:
        continue

    process_updates()
    try_to_send_frog()

    time.sleep(1)