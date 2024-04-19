import asyncio
import json
import os

import aio_pika
from aiogram import Bot, Dispatcher
from loguru import logger

from app.handlers import routers
import app.database.engine as bd

telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
logger.debug(telegram_bot_token)
bot = Bot(token=telegram_bot_token)
dp = Dispatcher()
dp.include_routers(routers)


async def run_bot():
    logger.info('Bot starting...')
    try:
        await bd.set_up()
        await dp.start_polling(bot, skip_updates=True)
    except Exception as e:
        logger.exception(e)
    finally:
        await bd.disconnect()


async def rabbitmq_listener():
    logger.info('RabbitMQ listener starting...')
    try:
        await process_messages_from_queue(bot)
    except Exception as e:
        logger.exception(e)


async def process_messages_from_queue(bot: Bot):
    rabbitmq_url = os.getenv("RABBITMQ_URL")
    connection = await aio_pika.connect_robust(rabbitmq_url)
    channel = await connection.channel()

    queue = await channel.declare_queue("messages")

    async for message in queue:
        async with message.process():
            data = json.loads(message.body.decode())
            users = data["tg_ids"]
            message_text = data["message"]

            for user_id in users:
                for i in range(5):
                    try:
                        await bot.send_message(user_id, message_text)
                        break
                    except Exception as e:
                        logger.error(e)
                        await asyncio.sleep(5)

                await asyncio.sleep(5)
