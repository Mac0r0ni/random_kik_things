# This was just another stupid thing i put together just for the lulz, but most importantly, the shits.
# need to put your font path in here somewhere for it to work

#!/usr/bin/env python3
"""
A Kik bot that just logs every event that it gets (new message, message read, etc.),
and echos back whatever chat messages it receives.
"""

import logging
import os
import sys
import urllib

import requests
from PIL import Image, ImageFont, ImageDraw

from kik_unofficial.callbacks import KikClientCallback
from kik_unofficial.client import KikClient
from kik_unofficial.datatypes.xmpp import chatting
from kik_unofficial.datatypes.xmpp.errors import *
from kik_unofficial.datatypes.xmpp.login import *
from kik_unofficial.datatypes.xmpp.roster import *

username = sys.argv[1] if len(sys.argv) > 1 else input("Username: ")
password = sys.argv[2] if len(sys.argv) > 2 else input('Password: ')


def main():
    # set up logging
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter(KikClient.log_format()))
    logger.addHandler(stream_handler)

    # create the bot
    bot = EchoBot()


class EchoBot(KikClientCallback):
    def __init__(self):
        self.client = KikClient(self, username, password)

    def on_authenticated(self):
        print("Now I'm Authenticated, let's request roster")
        self.client.request_roster()

    def on_login_ended(self, response: LoginResponse):
        print("Full name: {} {}".format(response.first_name, response.last_name))

    def on_chat_message_received(self, chat_message: chatting.IncomingChatMessage):
        print("[+] '{}' says: {}".format(chat_message.from_jid, chat_message.body))

    def on_group_message_received(self, chat_message: chatting.IncomingGroupChatMessage):
        print("[+] '{}' from group ID {} says: {}".format(chat_message.from_jid, chat_message.group_jid,
                                                          chat_message.body))
        GJID = chat_message.group_jid
        if chat_message.body.lower().startswith("meme "):
            try:
                mssg = chat_message.body.lower()
                remove_meme = mssg.replace("meme ", "")
                split_string = remove_meme.split(":", 1)
                user = split_string[0]
                message_to_spam = split_string[1]
                # user = chat_message.body[5:].replace(' ', "")
                url = "https://ws2.kik.com/user/" + user + "?fields=firstName,lastName,displayPicLastModified,displayPic,query"
                response = requests.get(url).json()
                pic_url = str(response['displayPic'])
                urllib.request.urlretrieve(pic_url, "res.jpg")
                first_name = str(response['firstName']) + '\n' + str(response['lastName']) + '\n' + message_to_spam
                my_image = Image.open("res.jpg")
                title_font = ImageFont.truetype('sb.ttf', 70)
                image_editable = ImageDraw.Draw(my_image)
                image_editable.text((15, 15), first_name, (237, 230, 211), font=title_font)
                my_image.save("result.jpg")
                self.client.send_chat_image(GJID, "result.jpg")
            except:
                self.client.send_chat_message(GJID, "failed")
                if os.path.exists("res.jpg"):
                    os.remove("res.jpg")

    def on_chat_message_received(self, chat_message: chatting.IncomingChatMessage):
        if chat_message.body.lower().startswith("meme "):
            try:
                mssg = chat_message.body.lower()
                remove_meme = mssg.replace("meme ", "")
                split_string = remove_meme.split(":", 1)
                user = split_string[0]
                message_to_spam = split_string[1]
                # user = chat_message.body[5:].replace(' ', "")
                url = "https://ws2.kik.com/user/" + user + "?fields=firstName,lastName,displayPicLastModified,displayPic,query"
                response = requests.get(url).json()
                pic_url = str(response['displayPic'])
                urllib.request.urlretrieve(pic_url, "res.jpg")
                first_name = str(response['firstName']) + '\n' + str(response['lastName']) + '\n' + message_to_spam
                my_image = Image.open("res.jpg")
                title_font = ImageFont.truetype('sb.ttf', 70)
                image_editable = ImageDraw.Draw(my_image)
                image_editable.text((15, 15), first_name, (237, 230, 211), font=title_font)
                my_image.save("result.jpg")
                self.client.send_chat_image(chat_message.from_jid, "result.jpg")
            except:
                self.client.send_chat_message(chat_message.from_jid, "failed")
                if os.path.exists("res.jpg"):
                    os.remove("res.jpg")

    def on_roster_received(self, response: FetchRosterResponse):
        print("[+] Chat partners:\n" + '\n'.join([str(member) for member in response.peers]))

    def on_image_received(self, image_message: chatting.IncomingImageMessage):
        print("[+] Image message was received from {}".format(image_message.from_jid))

    def on_peer_info_received(self, response: PeersInfoResponse):
        print("[+] Peer info: " + str(response.users))

    # Error handling

    def on_connection_failed(self, response: ConnectionFailedResponse):
        print("[-] Connection failed: " + response.message)

    def on_login_error(self, login_error: LoginError):
        if login_error.is_captcha():
            login_error.solve_captcha_wizard(self.client)

    def on_register_error(self, response: SignUpError):
        print("[-] Register error: {}".format(response.message))


if __name__ == '__main__':

