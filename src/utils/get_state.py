from aiogram.fsm.context import FSMContext
from src.utils.loader import dp, bot

async def get_user_state(user_id: int, chat_id: int = None) -> FSMContext:
    if not chat_id:
        chat_id = user_id
    state = dp.fsm.resolve_context(
        bot=bot, chat_id=chat_id, user_id=user_id
    )
    return state