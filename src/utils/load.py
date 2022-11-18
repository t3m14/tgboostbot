import os
import json
from pyrogram import Client
class Config():
    def __init__(self) -> None:
        self.sessions = []
        self.apps = []
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
    def load(self):
        self.__load_config()
        self.__load_sessions()
        self.__load_apps()
        
