from utils.load import Config
from pyrogram.raw.functions.messages import GetMessagesViews
from pyrogram import filters, idle
class App():
    def __init__(self) -> None:
        self.config = Config()
        self.config.load()
        
 
    async def start(self):
        for app in self.config.apps:
            await app.start()
            await self.main(app)
            await idle()
        for app in self.config.apps:
            await app.stop()
    async def main(self, app):
        print("OK")
        @app.on_message(filters.chat("https://t.me/testing1441".split("/")[-1]))
        async def get_post_and_put_to_queue(client, message):
            channels_msgs = []
            try:
                channel = await app.get_chat(chat_id="https://t.me/testing1441")
                async for msg in app.get_chat_history(chat_id=channel.id,
                                                        limit=10):
                    channels_msgs.append(msg.id)

                await app.invoke(GetMessagesViews(
                    peer=await app.resolve_peer(channel.id),
                    id=channels_msgs,
                    increment=True
                )
                )
                print("viewd")
            except Exception as e:
                print(e)

