#!/usr/bin/env python3
"""
this logs into all bot accounts stored in credentials.txt and changes the PFP to a randomly selected image from the pfp_images directory
change line 46 to the folder where your profile pictures are located
"""
import logging
import random
import warnings

from kik_unofficial.callbacks import *
from kik_unofficial.client import KikClient
from kik_unofficial.datatypes.xmpp.login import *

credentials = {}
print("Retrieving Creds...")
with open("credentials.txt", "r") as a_file:
    for line in a_file:
        stripped_line = line.strip()
        cred = stripped_line.split(":")
        credentials[cred[0]] = cred[1]
a_file.close()
print("credentials have been retrieved")

warnings.filterwarnings("ignore")


def get_image_paths(folder_path):
    image_extensions = ['.jpg', '.jpeg', '.png']
    image_paths = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.endswith(ext) for ext in image_extensions):
                image_path = os.path.join(root, file)
                image_paths.append(image_path)

    return image_paths


def get_random_image_path(folder_path):
    global random_image_path
    image_paths = get_image_paths(folder_path)
    random_image_path = random.choice(image_paths)


folder_path = r'C:\Users\user\PycharmProjects\change_pfp\pfp_images'  # Add complete path here
get_random_image_path(folder_path)


def main():
    BotNet()


class BotNet(KikClientCallback):
    def __init__(self):
        for cred in credentials.keys():
            password = credentials[cred]
            try:
                self.client = KikClient(self, cred, password)
                time.sleep(8)
            except:
                print("FAILED")

    def on_login_ended(self, response: LoginResponse):
        global my_jid
        my_jid = str(response.kik_node) + "@talk.kik.com"
        print("Login Was a Success for account: {}".format(my_jid))

    def on_authenticated(self):
        print("I'm Authenticated")
        time.sleep(1.5)
        print("Attempting to change PFP")
        self.client.set_profile_picture(random_image_path)
        time.sleep(1)


if __name__ == '__main__':
    main()
    logging.basicConfig(format=KikClient.log_format(), filename='DEBUG.log', level=logging.DEBUG)
