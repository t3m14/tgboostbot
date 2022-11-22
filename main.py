from src.user.app import App
from src.user.app import start
import asyncio
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(start())
