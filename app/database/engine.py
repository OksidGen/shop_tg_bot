import os

from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from scripts.set_up_db import drop_and_create_tables, fill_tables

logger.info('Creating database engine...')
__engine = create_async_engine(
    url=os.getenv('DATABASE_URL'),
    echo=False
)
logger.info('Database engine created')

logger.info('Creating async session...')
async_session = async_sessionmaker(__engine)
logger.info('Async session created')

reset_db = os.getenv('RESET_DB').lower() == 'true'
fill_db = os.getenv('FILL_DB').lower() == 'true'


async def set_up():
    logger.info('Setting up database...')
    if reset_db:
        await drop_and_create_tables(__engine)
    if fill_db:
        await fill_tables(async_session)
    logger.info('Database set up')


async def disconnect():
    logger.info('Disposing database engine...')
    await __engine.dispose()
    logger.info('Database engine disposed')
