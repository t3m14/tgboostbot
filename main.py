from src.user.app import run
# from src.user.app import start
import asyncio
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    # app = App()
    loop.run_until_complete(run())
