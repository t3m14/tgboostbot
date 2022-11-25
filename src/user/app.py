from utils.load import Config
from pyrogram.raw.functions.messages import GetMessagesViews
from pyrogram import filters, idle, Client
from pyrogram.handlers import MessageHandler
from random import randint, choices, shuffle
import asyncio
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from utils.db_operations import get_account_by_id, get_all_accounts
from tzlocal import get_localzone

async def react(config, acc, message_id, chat_id, emodji_list, emodji_wieghts):
    try:
        async with Client(
                    name=acc["login"],
                    api_id=acc["api_id"],
                    api_hash=acc["api_hash"],
                    workdir=config.sessions_dir) as app:
            random_emodji = choices(
                            emodji_list, weights=emodji_wieghts, k=1)
            await asyncio.sleep(randint(config.from_sleep, config.to_sleep))
            await app.send_reaction(chat_id, message_id, random_emodji[0])
            await app.stop()
            print(f"REACT ON POST {message_id} with emodji {random_emodji[0]}")
    except:
        await asyncio.sleep(10)
        config.retries += 1
        if config.retries >= 5:
            return
        await react(config, acc, message_id, chat_id, emodji_list, emodji_wieghts)
class App():
    def __init__(self):
        self.config = Config()        
        self.accs = []
        self.acc_counter = 0
        self.accounts_to_use = 0
        self.accounts_to_use_advert = 0
        self.accs_to_react = []
        self.jobstores = {
            'default': SQLAlchemyJobStore(url='sqlite:///tasks.sqlite')
        }
        self.scheduler = AsyncIOScheduler({'apscheduler.timezone': get_localzone()}, jobstores=self.jobstores)
    def generate_accouts_to_react(self):
            first = randint(self.config.fst, self.config.fst_to)
            second = first + randint(self.config.sec, self.config.sec_to)
            third = second + randint(self.config.tth, self.config.tth_to)
            fourth = third + randint(self.config.fth, self.config.fth_to)
            self.accs_to_react = [first, second, third, fourth]
    def rerroll_random(self):
        self.accounts_to_use = randint(
            self.config.repost_random_from,
            self.config.repost_random_to
        )
        self.accounts_to_use_advert = randint(
            self.config.repost_advert_random_from,
            self.config.repost_advert_random_to
        )
    async def reaction(self, client, message, emodji_list, emodji_wieghts):
        shuffle(self.accs)
        for acc in self.accs:
            async with Client(
                        name=acc["login"],
                        api_id=acc["api_id"],
                        api_hash=acc["api_hash"],
                        workdir=self.config.sessions_dir) as app: 
                self.acc_counter += 1
                print("react handled")
                if self.acc_counter == len(self.accs):
                    self.acc_counter = 0
                    self.generate_accouts_to_react()
                    print(self.accs_to_react)
                for i, to_react in enumerate(self.accs_to_react):
                    if self.acc_counter <= to_react:
                        try:
                            self.scheduler.add_job(
                                react,
                                "date",
                                run_date=datetime.now() + timedelta(seconds=randint(self.config.from_sleep,self.config.to_sleep) * i+1),
                                args=(self.config, acc, message.id, message.chat.id, emodji_list, emodji_wieghts)
                            )
                            print("job added")
                        except Exception as e:
                            print("Ошибка " + e)
                await app.stop()
                
    async def repost(self, message):
        shuffle(self.accs)
        for acc in self.accs:
            async with Client(
                name=acc["login"],
                api_id=acc["api_id"],
                api_hash=acc["api_hash"],
                workdir=self.config.sessions_dir) as app:
                if message.entities or message.caption_entities:
                    self.acc_counter += 1
                    if self.acc_counter == len(self.config.apps):
                        self.acc_counter = 0
                        self.rerroll_random()
                    if self.acc_counter >= self.accounts_to_use:
                        return
                    else:
                        for acc in self.accs:
                            async with Client(
                                name=acc["login"],
                                api_id=acc["api_id"],
                                api_hash=acc["api_hash"],
                                workdir=self.config.sessions_dir) as app:        
                                    # Рандомная задержка между репостами для одного аккаунта
                                    await asyncio.sleep(randint(self.config.from_sleep, self.config.to_sleep))
                                    # Пересылаем сообщение в личку
                                    await app.forward_messages(self.config.username_to_send, message.chat.id, message)
                                    print("ADVERT POST FORWARDED" + str(message.id))
                                    await app.stop()
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
                        await app.stop()

    async def view(self, link):
        shuffle(self.accs)
        for acc in self.accs:
            async with Client(
                name=acc["login"],
                api_id=acc["api_id"],
                api_hash=acc["api_hash"],
                workdir=self.config.sessions_dir) as app:
                channels_msgs = []
                channel = await app.get_chat(chat_id=link.split("/")[-1] if "/" in link else link)
                async for msg in app.get_chat_history(chat_id=channel.id,
                                                    limit=5):
                    channels_msgs.append(msg.id)

                await app.invoke(GetMessagesViews(
                    peer=await app.resolve_peer(channel.id),
                    id=channels_msgs,
                    increment=True
                )
                )
                await app.stop()
                print(f'viewd with account {acc["id"]} - {acc["login"]}')
    async def stop_all_accs(self):
        for acc in self.accs:
            async with Client(
                name=acc["login"],
                api_id=acc["api_id"],
                api_hash=acc["api_hash"],
                workdir=self.config.sessions_dir) as app:
                await app.stop()

    async def start(self):
        self.config.load()
        self.scheduler.start()
        self.rerroll_random()
        self.generate_accouts_to_react()
        self.accs = get_all_accounts()
        acc = self.accs[-1]
        app = Client(
            name=acc["login"],
            api_id=acc["api_id"],
            api_hash=acc["api_hash"],
            workdir=self.config.sessions_dir)
        await app.start()
        self.accs.pop(-1)
        print("App started")
        for link in self.config.links:    
            @app.on_message(link)
            async def handle(client, message):
                shuffle(self.accs)
                print("post getted")
                try:
                    await self.view(message.sender_chat.username)
                except:
                    print("Не удалось просмотреть пост")
                try:
                    await self.repost(message)
                except Exception as e:
                    print(e)
                    print("Не вышло репостнуть")
                try:
                    print(self.config.positive_emodji, self.config.negative_emodji)
                    if self.config.positive_emodji != []:
                        await self.reaction(client, message, self.config.positive_emodji, self.config.positive_emodji_weigth)
                    if self.config.negative_emodji != []:
                        await self.reaction(client, message, self.config.negative_emodji, self.config.negative_emodji_weigth)

                except Exception as e:
                    print(e)
                    print("Не вышло кинуть реакцию")
                
        await idle()
        await app.stop()
async def run():
    app = App()
    await app.start()
