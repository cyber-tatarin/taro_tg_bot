import asyncio

from src.services.moon_service import MoonService
from src.services.recomendation_service import RecommendationService
from src.services.sheduler_service import ShedulerService
from src.utils.commands import set_commands
from src.utils.custom_logger import configure_logger
from src.utils.loader import dp, bot
from src.utils.router import setup_routers


async def main():
    configure_logger()
    await setup_routers(dp)
    await ShedulerService.update_recommendations(RecommendationService.update_recommendations_in_db)
    await ShedulerService.update_moon_data(MoonService.update_moon_data_in_db)
    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands(bot)
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    asyncio.run(main())
