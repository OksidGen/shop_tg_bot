import asyncio

from dotenv import load_dotenv
from loguru import logger

from log import __setup_loger


async def main():
    load_dotenv()
    __setup_loger()
    from app.app import run_bot, rabbitmq_listener
    await asyncio.gather(
        run_bot(),
        rabbitmq_listener()
    )


if __name__ == '__main__':
    logger.info('App starting...')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.exception(e)
    finally:
        logger.info('App stopped')
