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
TOKEN = "454767750:AAEp2sdrBVTe70vX5XHdNuwJfNaklYz3rEo"
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

    global name_asked
    global book_buscat_asked
    global book_donat_asked
    global telf_asked
    global mail_asked
    global barri_asked

    global name
    global book_buscat
    global book_donat
    global telf
    global mail
    global barri
    
    for update in updates["result"]:
        try:
            received_text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            # start the analysis:
            if received_text == "/start":
                send_message("Hi! I'm the book bot.",chat)
                send_message("First of all, could you tell me your name please?",chat)
                name_asked = True
            elif name_asked == True:
                name = received_text
                name_asked = False
                send_message("Now, tell me which particular book you are looking for, please.",chat)
                book_buscat_asked = True
            elif book_buscat_asked == True:
                book_buscat = received_text
                book_buscat_asked = False
                send_message("And which book are you willing to give in exchange?", chat)
                book_donat_asked = True
            elif book_donat_asked == True:
                book_donat = received_text
                book_donat_asked = False
                send_message("Now we will need your phone number.",chat)
                telf_asked = True
            elif telf_asked == True:
                telf = received_text
                telf_asked = False
                send_message("Thank you! And which is your email?",chat)
                mail_asked = True
            elif mail_asked == True:
                mail = received_text
                mail_asked = False
                send_message("And finally, we'd like to know your neighborhood.", chat)
                barri_asked = True
            elif barri_asked == True:
                barri = received_text
                barri_asked = False
                send_message("Perfect! We will store your data and, as soon as we find a match, you'll be put in contact with the exchanger", chat)

                db.add_record(name, telf, mail, barri, book_buscat, book_donat)
                x = db.get_records(book_donat, book_buscat)
                if len(x)>0:
                    send_message("Congrats, we found a match!",chat)
                    time.sleep(2)
                    send_message("We'll give you his/her contact info so that you can meet each other:",chat)
                    time.sleep(3)
                    send_message("Name: " + x[0][0] + '\n' + "Phone number: " + x[0][1] + '\n' + "E-mail: " + x[0][2] + '\n' + "Neighborhood: " + x[0][3],chat)
                    db.delete_record(name, telf)
                    db.delete_record(x[0][0],x[0][1])
            else:
                send_message("I don't understand you, sorry!",chat)
        except KeyError: # usually at the start of the conversation
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
