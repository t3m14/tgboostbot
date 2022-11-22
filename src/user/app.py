from utils.load import Config
from pyrogram.raw.functions.messages import GetMessagesViews
from pyrogram import filters, idle
from pyrogram.handlers import MessageHandler
from random import randint, choices
import asyncio


class App():
    def __init__(self) -> None:
        self.config = Config()
        self.config.load()
        self.acc_counter = 0
        self.accounts_to_use = 0
        self.accounts_to_use_advert = 0
    def rerroll_random(self):
        self.accounts_to_use = randint(
                self.config.repost_random_from,
                self.config.repost_random_to
            )
        self.accounts_to_use_advert = randint(
                self.config.repost_advert_random_from,
                self.config.repost_advert_random_to
            )
    async def view_last_messsages(self, app, link):
        channels_msgs = []
        channel = await app.get_chat(chat_id=link.split("/")[-1] if "/" in link else link)
        async for msg in app.get_chat_history(chat_id=channel.id,
                                              limit=10):
            channels_msgs.append(msg.id)

        await app.invoke(GetMessagesViews(
            peer=await app.resolve_peer(channel.id),
            id=channels_msgs,
            increment=True
        )
        )
    async def react(self, message, emodji_list, emodji_wieghts):
        self.acc_counter += 1
        
        # Реагируем рандомным эмодзи, с определённой модой
        random_emodji = choices(
            emodji_list, weights=emodji_wieghts, k=1)
        # Задержка между сообщениями набирается рандомно
        await asyncio.sleep(randint(self.config.from_sleep, self.config.to_sleep))
        await message.react(emoji=random_emodji[0])
        print(f"REACT ON POST {message.id} with emodji {random_emodji[0]}")
    async def repost(self, message):
        
        if message.entities or message.caption_entities:
            self.acc_counter += 1
            if self.acc_counter == len(self.config.apps):
                self.acc_counter = 0
                self.rerroll_random()
            if self.acc_counter >= self.accounts_to_use:
                return
            else:    
                # Рандомная задержка между репостами для одного аккаунта
                await asyncio.sleep(randint(self.config.from_sleep, self.config.to_sleep))
                # Пересылаем сообщение в личку
                await message.forward(self.config.username_to_send)
                print("ADVERT POST FORWARDED" + str(message.id))
        else:
            self.acc_counter += 1
            if self.acc_counter == len(self.config.apps):
                self.acc_counter = 0
                self.rerroll_random()
            if self.acc_counter >= self.accounts_to_use:
                return
            else:
                await asyncio.sleep(randint(self.config.from_sleep, self.config.to_sleep))
                # Пересылаем сообщение в личку
                await message.forward(self.config.username_to_send)
                print("DEFAULT POST FORWARDED" + str(message.id))
    async def handle(self, client, message):
        await self.view_last_messsages(client, message.sender_chat.username)
        await self.repost(message)
        await self.react(message, ["👍"], [1])
    # Проверка на рекламу в посте


async def start():
    tasks = []
    application = App()
    application.rerroll_random()
    for app in application.config.apps:
        for link in application.config.links:
            app.add_handler(MessageHandler(application.handle, link))
        await app.start()
        print("started")
    print("idle")
    await idle()
    for app in application.config.apps:
        await app.stop()
        print("app stopped")
