import os
import json
from pyrogram import Client
class Config():
    def __init__(self) -> None:
        self.sessions = []
        self.apps = []
        self.links = []
        self.from_sleep = 0
        self.to_sleep = 0
        self.username_to_send = ""
        self.repost_advert_random_from = 0
        self.repost_advert_random_to = 0
        self.repost_random_from = 0
        self.repost_random_to = 0
        self.repost_random_to = 0
        self.react_random_from = 0
        self.react_random_to = 0
        self.react_advert_random_from = 0
        self.react_advert_random_to = 0
        self.__sessions_dir = ""
        self.__api_key = ""
        self.__api_id = ""
        self.__bot_token = ""
    def __load_sessions(self) -> dict:
        session_list = []
        for root, dirs, files in os.walk(self.__sessions_dir):
            for file in files:
                if(file.endswith(".session")):    
                    session_list.append(file.split(".")[0])
        self.sessions = session_list
    def __load_apps(self):
        apps = []
        for login in self.sessions:
            apps.append(Client(login, self.__api_id, self.__api_key, workdir=self.__sessions_dir))
        self.apps = apps
    def __load_config(self):
        with open("config.json", "r") as f:
            config = json.load(f)
            self.__sessions_dir = config["SESSIONS_DIR"]
            self.__api_key = config["API_KEY"]
            self.__api_id = config["API_ID"]
            self.__bot_token = config["BOT_TOKEN"]
            self.links = config["LINKS"]
            self.from_sleep = config["from_sleep"]
            self.to_sleep = config["to_sleep"]
            self.username_to_send = config["username_to_send"]
            self.repost_advert_random_from = config["repost_advert_random_from"]
            self.repost_advert_random_to = config["repost_advert_random_to"]
            self.repost_random_from = config["repost_random_from"]
            self.repost_random_to = config["repost_random_to"]
            self.react_random_from = config["react_random_from"]
            self.react_random_to = config["react_random_to"]
            self.react_advert_random_from = config["react_advert_random_from"]
            self.react_advert_random_to = config["react_advert_random_to"]
    def load(self):
        self.__load_config()
        self.__load_sessions()
        self.__load_apps()
        print("Conf loaded")
        
