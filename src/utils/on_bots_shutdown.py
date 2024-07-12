import logging

from src.utils.loader import scheduler, dp


@dp.shutdown()
async def on_shutdown(*args, **kwargs):
    logging.warning('Shutting down..')

    # Остановка планировщика
    scheduler.shutdown(wait=False)
    logging.info('Scheduler shut down.')

    # Закрытие соединения с ботом
    # await bot.close()
    # logging.info('Bot connection closed.')

    # logging.warning('Bye!')