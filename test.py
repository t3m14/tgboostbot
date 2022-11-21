from pyrogram import Client, filters, idle
import os
import asyncio
i = 0
logins_list = []
apps = []
accounts_to_use = ""
print("GETTING SESSIONS...")
for root, dirs, files in os.walk("./sessions"):
    for file in files:
        if(file.endswith(".session")):    
            logins_list.append(file.split(".")[0])
         
print("STARTING...")
async def main():
    #Заполняем список приложений на основе списка сессий
    for login in logins_list:
        apps.append(Client(login, "14107984", "6507fadc1d76c1d8f3c0957690d9ec86", workdir="./sessions"))
    
    for app in apps: #Асинхронно запускаем приложения по порядку
        print("SESSION OK")
        await app.start()
        
    
        #Хэндлер который видит пост на первом канале, когда он выходит
        @app.on_message(filters.chat("testing1441"))
        async def get_post_and_put_to_queue(client, message):
            print("POST GETTED" + str(message.id))
    await idle()
asyncio.run(main())