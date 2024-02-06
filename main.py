import requests
import json
import time
import random 

config = json.load(open("isthatright.json"))
token = config["config"]["token"]

url = f"https://api.telegram.org/bot{token}/" 
frogs_list = "https://drive.google.com/drive/folders/1vKe7Up1EMEaPS1EPlfTYRE91ApvUGbyH"


while True:
    with open("lastMessage") as f:
        last = int(f.read())
    updates = requests.get(url+f"getUpdates?offset={last+1}")

    print(updates.json())

    for update in updates.json()["result"]:
        if "message" not in update:
            continue

        txt = update["message"]["text"]
        username = ""
        if "username" in update["message"]["from"]:
            username = update["message"]["from"]["username"]
        elif "first_name" in update["message"]["from"]:
            username = update["message"]["from"]["first_name"]
        if not username:
            username = "anon"
            
        # if txt.strip().lower() == "k-index":
        #     k_indexes = requests.get(k_index)
        #     last_k_index = k_indexes.json()[-1]
        #     requests.post(url+"sendMessage", data={
        #         "chat_id": update["message"]["chat"]["id"],
        #         "text": f"Currently K-Index is {last_k_index[1]}"
        #     })
                
        elif txt.strip().lower() == "hello":
            requests.post(url+"sendMessage", data={
                "chat_id": update["message"]["chat"]["id"],
                "text": f"Hello, {username}. I'm here to hail all Wednesdudes!"
            })

        else:
            requests.post(url+"sendMessage", data={
                "chat_id": update["message"]["chat"]["id"],
                "text": f"Sorry, don't get it."
            })

        with open("lastMessage", "w") as f:
            f.write(str(update["update_id"]))


    time.sleep(1)