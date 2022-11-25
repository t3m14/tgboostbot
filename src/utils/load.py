import os
import json
from pyrogram import Client
from utils.db_operations import add_account
class Config():
    def __init__(self) -> None:
        self.sessions = []
        self.apps = []
        self.links = []
        self.positive_emodji = []
        self.negative_emodji = []
        self.positive_emodji_weigth = []
        self.negative_emodji_weigth = []
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
        self.fst = 0
        self.sec = 0
        self.tth = 0
        self.fth = 0
        self.fst_to = 0
        self.sec_to = 0
        self.tth_to = 0
        self.fth_to = 0
        self.sessions_dir = ""
        self.__api_key = ""
        self.__api_id = ""
        self.__bot_token = ""
    def __load_sessions(self) -> dict:
        session_list = []
        for root, dirs, files in os.walk(self.sessions_dir):
            for file in files:
                if(file.endswith(".session")):    
                    session_list.append(file.split(".")[0])
        self.sessions = session_list
    def __load_apps(self):
        apps = []
        for login in self.sessions:
            add_account(login, self.__api_id, self.__api_key)
        self.apps = apps
    def __load_config(self):
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
            self.sessions_dir = config["SESSIONS_DIR"]
            self.__api_key = config["API_KEY"]
            self.__api_id = config["API_ID"]
            self.__bot_token = config["BOT_TOKEN"]
            self.positive_emodji = config["positive_emodji"]
            self.negative_emodji = config["negative_emodji"]
            self.positive_emodji_weigth = config["positive_emodji_weigth"]
            self.negative_emodji_weigth = config["negative_emodji_weigth"]
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
            self.fst = config["fst"]
            self.sec = config["sec"]
            self.tth = config["tth"]
            self.fth = config["fth"]
            self.fst_to = config["fst_to"]
            self.sec_to = config["sec_to"]
            self.tth_to = config["tth_to"]
            self.fth_to = config["fth_to"]
            self.retries = 0
    def load(self):
        print("loading")
        self.__load_config()
        print("init config")
        self.__load_sessions()
        print("sessions loaded")
        self.__load_apps()
        print("Conf loaded")
        
