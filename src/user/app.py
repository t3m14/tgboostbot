from utils.load import Config
from pyrogram.raw.functions.messages import GetMessagesViews
from pyrogram import filters, idle
from pyrogram.handlers import MessageHandler
import asyncio
class App():
    def __init__(self) -> None:
        self.config = Config()
        self.config.load()
        
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
async def handle(client, message):
    app = App()
    await app.view_last_messsages(client, message.sender_chat.username) 
        
async def start():
    tasks = []
    application = App()
    for app in application.config.apps:
        app.add_handler(MessageHandler(handle, "testing1441"))
        await app.start()
        print("started")
    print("idle")
    await idle()
    for app in application.config.apps:
        await app.stop()
        print("app stopped")


