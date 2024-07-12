import logging


from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.data.config import settings
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from openai import AsyncOpenAI

from src.utils.database.database import sync_engine

# import redis.asyncio as aioredis


logger = logging.getLogger(__name__)

bot = Bot(token=settings.TELEGRAM_API_TOKEN)

storage = RedisStorage.from_url(settings.REDIS_FSM_URL)
dp = Dispatcher(storage=storage)

jobstores = {
    'default': SQLAlchemyJobStore(engine=sync_engine)
}

# scheduler = AsyncIOScheduler(jobstores=jobstores)
scheduler = AsyncIOScheduler()
# scheduler.start()
# redis = aioredis.from_url(settings.REDIS_UTIL_URL)
openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
# executor = ThreadPoolExecutor(max_workers=10)
