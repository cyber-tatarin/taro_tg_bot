import logging

from aiogram import Dispatcher

from src.utils.loader import scheduler
from src.routers.onboarding_router import router as onboarding_router
from src.routers.advice_router import router as advice_router
from src.routers.util_router import router as util_router



logger = logging.getLogger(__name__)




async def setup_routers(dp: Dispatcher):
    dp.include_routers(
        util_router,
        onboarding_router,
        advice_router
    )
    @dp.shutdown()
    async def on_shutdown(*args, **kwargs):
        logging.warning('Shutting down..')
        scheduler.shutdown(wait=False)
    