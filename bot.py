import json
import os
import sys
import random
import requests
from check_server import servertest
from dotenv import load_dotenv
import schedule
import time

load_dotenv()


# emoji and stuff customization

def customizer():
  
    #Getting random slack emoji
    with open('emoji_id.txt', 'r') as f:
         emoji_data = f.read()
    emoji_data = emoji_data.split("\n")
    emoji_id = random.choice(emoji_data)

    #Generating random hex color code
    hex_number = random.randint(1118481, 16777215)
    hex_number = str(hex(hex_number))
    hex_number = '#' + hex_number[2:]

    return emoji_id, hex_number

if __name__ == '__main__':
    url = os.environ["URI"]
    emoji_id, hex_number = customizer()
    message_down = ("DC is Down. Please See to it.")
    title = (f"DC IS DOWN!!!!{emoji_id}")
    slack_data_down = {
        "icon_emoji": emoji_id,
        "channel": "#general",
        "attachments": [
            {
                "color": hex_number,
                "fields": [
                    {
                        "title": title,
                        "value": message_down,
                        "short": "false",
                    }
                ]
            }
        ]
    } 

    message_up = ("DC is UP and RUNNING, no worries")
    title = (f"DC IS UP!!{emoji_id}")
    slack_data_up = {
        "icon_emoji": emoji_id,
        "channel": "#general",
        "attachments": [
            {
                "color": hex_number,
                "fields": [
                    {
                        "title": title,
                        "value": message_up,
                        "short": "false",
                    }
                ]
            }
        ]
    }

    byte_length = str(sys.getsizeof(slack_data_down))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    byte_length = str(sys.getsizeof(slack_data_up))
    headers_up = {'Content-Type': "application/json", 'Content-Length': byte_length}


# checks the status of server every 10 seconds, if its up do nothing, if down,
# send a message a slack with the webhook at certain intervals

    schedule.every(10).seconds.do(servertest)
    while True:
        if servertest():
            print("server is UP and running")
            # requests.post(url, data=json.dumps(slack_data_up), headers=headers_up)
        else:
            print("Server is Down")
            requests.post(url, data=json.dumps(slack_data_down), headers=headers)
            time.sleep(180)
        schedule.run_pending()
        time.sleep(1)


