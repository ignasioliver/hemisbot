# import needed libs:
import json
import requests
import time
import urllib
import csv

# personal pollution bot TOKEN. DELETE IT WHEN MAKING THE CODE PUBLIC:
TOKEN = "458885814:AAH0dsg7soXTg-Au9_-vqIq0q0GGyDOEB8g"
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
    for update in updates["result"]:
        try:
            received_text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            # start the analysis:
            if received_text == "/start":
                send_message("Hi! I'm the tourist bot.\nType the number of the topic you want to know about:\n1) Monuments\n2) Hospitals\n3) Tourist Info Points", chat)
            else:
                if received_text == "1":
                    send_message("Dear 'guiri', here you have a brief summary of some of the most interesting attractions in Barcelona:",chat)
                    time.sleep(3)
                    send_message("- Sagrada Família\nBasic price: 15€\nhttp://www.sagradafamilia.org/",chat)
                    time.sleep(5)
                    send_message("- La Pedrera\nBasic price: 22€\nhttps://www.lapedrera.com/en/home",chat)
                    time.sleep(5)
                    send_message("- Park Güell\nBasic price: 7€\nhttps://www.parkguell.cat/en/",chat)
                    time.sleep(5)
                    send_message("- Museu Picasso\nBasic price: 11€\nhttp://www.museupicasso.bcn.cat/en/",chat)
                    time.sleep(5)
                    send_message("- Font Màgica de Montjuïc\nFree entrance\nhttp://www.barcelonaturisme.com/wv3/en/page/614/font-magica.html",chat)
                    
                    time.sleep(2)
                    send_message("I hope I helped you! Now, do you need more info?\n1) Monuments\n2) Hospitals\n3) Tourist Info Points", chat)
                elif received_text == "2":
                    send_message("Use this link to find the nearest hospitals:\nhttps://goo.gl/9FaFPd",chat)
                    time.sleep(2)
                    send_message("Also, you may want to call the Barcelona emergency phone number: 112",chat)
                    time.sleep(2)
                    send_message("Was this helpful? Keep throwing questions at me!\n1) Monuments\n2) Hospitals\n3) Tourist Info Points", chat)
                elif received_text == "3":
                    send_message("Enter this link to find the main tourist info points in Barcelona\nhttps://goo.gl/Gk6p9j",chat)
                    time.sleep(2)
                    send_message("Remember that catalans are very generous, so don't hesitate to ask them for help in case you need it.",chat)
                    time.sleep(2)
                    send_message("Do you need more info?\n1) Monuments\n2) Hospitals\n3) Tourist Info Points", chat)
                else:
                    send_message("I can't understand you.", chat)
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
