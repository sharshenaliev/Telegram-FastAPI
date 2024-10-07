from celery import Celery
import telegram
import asyncio
from src.config import TOKEN


celery = Celery('tasks', broker='redis://redis:6379')

@celery.task()
def send_messages(text, users):
    bot = telegram.Bot(token=TOKEN)

    async def send():
        for user in users:
            await bot.send_message(chat_id=user, text=text)
        return True

    return asyncio.run(send())
