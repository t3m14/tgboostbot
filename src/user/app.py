from utils.load import Config

class App():
    def __init__(self) -> None:
        self.config = Config()
        self.config.load()
        
 
    async def start(self):
        for app in self.config.apps:
            await app.start()
            await self.main()
    async def main(self):
        pass

