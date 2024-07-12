import logging

from aiogram import Bot
from aiogram.types import BotCommand

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    await bot.set_my_commands(
        [
            BotCommand(command="/start", description="Запустить бота"),
            BotCommand(command="/contact_admin", description="Связаться с админом"),
            BotCommand(command="/change_your_information", description="Изменить данные о себе"),
            BotCommand(command="/stop", description="Остановить бота")
        ]
    )
