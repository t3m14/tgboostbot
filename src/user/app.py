from utils.load import Config
from pyrogram.raw.functions.messages import GetMessagesViews
from pyrogram import filters, idle
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
    async def start(self):
        tasks = []
        for app in self.config.apps:
            await app.start()
            print("started")
            
            @app.on_message(filters.chat("testing1441"))
            async def get_post_and_put_to_queue(client, message):
                print("POST GETTED" + str(message.id))
                
        await idle()
        for app in self.config.apps:
            await app.stop()


