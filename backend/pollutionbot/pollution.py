# import needed libs:
import json
import requests
import time
import urllib

# import DB_SQLite:
from db_sqlite import DB_SQLite

# access SQLite methods through 'db':
db = DB_SQLite()

# personal pollution bot TOKEN. DELETE IT WHEN MAKING THE CODE PUBLIC:
TOKEN = "464368472:AAGfh1lZGi-B7Afty2dY8GWgoS27vKUO1og"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

# the 'message' received is actually a link. Collect it:
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    db.add_decoded_url(content)
    return content

# Now load that link to json:
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

# use Long Polling! don't overload Telegram with queries: keep
# the connection opened and if there are any updates, pass them
# always passing 'timeout' argument alongside get_updates:
def get_updates(offset=None):
    url = URL + "getUpdates"
    if offset:
        url += "?offset={}".format(offset)
    js = get_json_from_url(url)
    return js

# mange data updates:
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

# most important! process the input and define the output:
def handle_updates(updates):
    for update in updates["result"]:
        try:
            received_text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            # start the analysis:
            if received_text == "/start":
                send_message("What up my boy! Tell me whatever...", chat)
            elif received_text == "locate me":
                send_location(chat, 41.3880040, 2.1132800, reply_markup=None)
            else:
                records = db.get_records(chat)
                if received_text in records:
                    db.delete_record(received_text, chat)
                    send_message("Record deleted!", chat)
                elif received_text == "Nil":
                    send_message("lol this man doesn't even like coffe", chat)
                elif received_text == "Pau":
                    send_message("yoh this man can't sleep on the floor", chat)
                else:
                    tosend_text = "You told me " + received_text + ". I'll save that. Your current list is (repeat an record to delete it):"
                    send_message(tosend_text, chat)
                    db.add_record(received_text, chat)
                    records = db.get_records(chat)
                    all_records = "\n".join(records)
                    send_message(all_records, chat)
        except KeyError: # usually at the start of the conversation
            pass


# most important! process the input and define the output:
def handle_updates_location(updates):
    for update in updates["result"]:
        try:
            chat = update["message"]["chat"]["id"]

            # check if it's a location
            received_latitude = update["message"]["location"]["latitude"]
            received_longitude = update["message"]["location"]["longitude"]

            #provisional_value = 0 + received_latitude
            if isinstance(received_latitude, float): #actually unneeded
                send_text_location = str(received_latitude) + ", " + str(received_longitude)
                send_message("Thats a location man... You're on " + send_text_location, chat)

            received_latitude = None
            received_longitude = None
        except KeyError: # usually at the start of the conversation
            pass
"""
def handle_updates_location(updates):
    for update in updates["result"]:
        try:
            received_latitude_latitude = update["result"]["message"]["location"]["latitude"]
            received_latitude_longitude = update["result"]["message"]["location"]["longitude"]
            chat = update["message"]["chat"]["id"]
            to_send = "My man you are at" + received_latitude_latitude + ", " + received_latitude_longitude
            send_message(to_send, chat)
        except KeyError:
            pass
"""
def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

# call the customized keyboard and pass through the option (records) that should appear,
# NOT USED YET:
def special_keyboard(records):
    keyboard = [[record] for record in records]
    # remember, reply_markup is the object that contains the keybaord algonside other values:
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)

# once the message text is passed, convert it to a proper link for Telegram to understand:
def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

def send_location(chat_id, latitude, longitude, reply_markup=None):
    url = URL + "sendlocation?chat_id={}&latitude={}&longitude={}&parse_mode=Markdown".format(chat_id, latitude, longitude)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

# get_updates is the responsible of the Long Polling:
def main():
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        sendlocation_string = "location"
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
            handle_updates_location(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()



    """
    def main():
        db.setup()
        last_update_id = None
        while True:
            updates = get_updates(last_update_id)
            sendlocation_string = "location"
            if len(updates["result"]) > 0:
                if sendlocation_string in updates:
                    print("Hola")
                    last_update_id = get_last_update_id(updates) + 1

                    handle_updates_location(updates)
                else:
                    last_update_id = get_last_update_id(updates) + 1
                    handle_updates(updates)
            # elif sendlocation_string in updates:
            #else:
                # last_update_id = get_last_update_id(updates) + 1
            #    handle_updates_location(updates)
            time.sleep(0.5)

    """
# Ignasi Oliver, Pau Nunez, Nil Quera, @HACKUPC Fall 2017
