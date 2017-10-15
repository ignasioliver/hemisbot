# import needed libs:
import json
import requests
import time
import urllib
import csv

# import DB_SQLite:
from db_sqlite import DB_SQLite

# access SQLite methods through 'db':
db = DB_SQLite()

# personal pollution bot TOKEN. DELETE IT WHEN MAKING THE CODE PUBLIC:
TOKEN = "407413557:AAHyeeDx33vlMvt60A0Ob3HnsipSUYmgzJ4"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

# the 'message' received is actually a link. Collect it:
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
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
    
    global description
    global place
    global time_t
    
    global action_asked
    global description_asked
    global place_asked
    global time_asked
    global continua
    
    for update in updates["result"]:
        try:
            received_text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            # start the analysis:
            if received_text == "/start" or continua == True:
                send_message("Hi! I'm the emergencies bot!\nType *add* in order to append an emergency\nType *view* to consult the current emergencies",chat)
                action_asked = True
                continua = False
            
            elif action_asked == True:
                action_asked = False
                if received_text == "view":
                    send_message("Here are the current emergencies: \n",chat)
                    x = db.get_records()
                    for i in range (0,len(x)):
                        send_message("Description: " + x[i][0] + "\nPlace: " + x[i][1] + "\nTime: " + x[i][2], chat)
                        time.sleep(1)
                        continua = True;
                elif received_text == "add":
                    send_message("Please, give us a brief description about the situation", chat)
                    description_asked = True
            
            elif description_asked:
                description_asked = False
                description = received_text
                send_message("Where has it happened?", chat)
                place_asked = True
            
            elif place_asked:
                place_asked = False
                place = received_text
                send_message("What time was it?", chat)
                time_asked = True
            
            elif time_asked:
                time_asked = False
                time_t = received_text
                send_message("Thank you very much for your submission!",chat)
                time_asked = False
                db.add_record(description,place,time_t)
                continua = True
            
            else:
                send_message("I don't understand you, sorry!",chat)
        except: # usually at the start of the conversation 
            pass
            
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

# get_updates is the responsible of the Long Polling:
def main():
    #db.delete_all()
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)

if __name__ == '__main__':
    main()
# Ignasi Oliver, Pau Nunez, Nil Quera, @HACKUPC Fall 2017
