import asyncio
import datetime
import os, sys
from rooBot import rooBot

loop = asyncio.get_event_loop()

bot = rooBot(loop=loop, max_messages=10000)

if __name__ == "__main__":
    try:
        task = loop.create_task(bot.run())
        bot.own_task = task
        loop.run_until_complete(task)
        loop.run_forever()
    except (KeyboardInterrupt, RuntimeError):
        print('\nKeyboardInterrupt - Shutting down...')
        bot.die()
    finally:
        print('--Closing Loop--')
        loop.close()