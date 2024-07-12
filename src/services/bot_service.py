
import asyncio
from aiogram.fsm.context import FSMContext
from src.data.config import settings
from src.keyboards.keyboards import advice_keyboard_builder, estimate_keyboard_builder
from src.schemas.user_schemas import User
from src.services.gsheets_service import GSheetService
from src.services.sheduler_service import ShedulerService
from src.services.taro_service import TaroService
from src.services.user_service import UserService
from src.utils.database.uow import UoW
from src.utils.get_state import get_user_state
from src.utils.loader import bot, scheduler


# async def send_remind(user_id: int, state: FSMContext, job_id: str, day: int):
async def send_remind(user_id: int, job_id: str, day: int):
    print('send_remind', user_id, job_id, day)
    # fsm_data = await state.get_data()
    job_interval = job_id.split('_')[1]
    
    if job_interval == str(settings.REMINER1_SECONDS):
        text = 'Привет! Звёзды уже готовы поделиться с тобой своим мудрым советом на сегодня. Не упусти шанс узнать, что они приготовили для тебя! ✨ Нажми кнопку "Получить предсказание" и открой для себя магию дня.'
    if job_interval == str(settings.REMINER2_SECONDS):
        text = 'Эй, не забудь заглянуть в звёздный прогноз! Сегодняшний день полон тайн и возможностей, которые только ждут, чтобы ты их открыл. Нажми кнопку "Получить предсказание" и дай волшебству войти в твою жизнь. 🌟'
    if job_interval == str(settings.REMINER3_SECONDS):
        text = 'Кажется, у тебя сейчас много дел, но звезды не оставят тебя без внимания. Завтра утром ты получишь свой первый прогноз, который поможет сделать день особенным. Пусть волшебство будет с тобой! 🌟'
    await bot.send_message(
        chat_id=user_id,
        text=text,
        # reply_markup=advice_keyboard_builder(day)
    )
    # await TaroService.send_remind(user_id, state)

    scheduler.remove_job(
       job_id=job_id
    )
    # count = fsm_data.get(f"remind_{day}")
    # await state.update_data({
    #     f"remind_{day}": count + 1
    # })

async def send_daily_prediction_message(user_id: int):
    uow = UoW()
    state = await get_user_state(user_id)
    fsm_data = await state.get_data()
    day = int(fsm_data.get("function_call_number")) + 1
    bot_answer = await TaroService.get_taro_predict(user_id=user_id, uow=uow)
    choosed_category = None
    if day == 1:
        pass
        # await bot.send_message(
        #     "Отлично, ты сделал первый шаг к волшебству! Теперь каждый день тебя будет ждать прогноз, который поможет сделать твой день лучше. Наслаждайся и пусть звезды всегда освещают твой путь! ✨",
        # )
        # count_interval_mapping = {
        #     1: settings.REMINER1_SECONDS,
        #     2: settings.REMINER2_SECONDS,
        #     3: settings.REMINER3_SECONDS
        # }
        
        # remind_count = fsm_data.get(f'remind_{day}')
        # # interval = count_interval_mapping[remind_count]
        # for key, value in count_interval_mapping.items():
        #     if remind_count < key:
        #         try:
        #             scheduler.remove_job(job_id=str(f'remind_{value}_{user_id}'))
        #         except Exception as e:
        #             print(e)
        #         print(f'remove remind_{value}_{user_id}' )
        
        # await asyncio.sleep(settings.first_advise_seconds)
        # await bot.send_message(
        #     chat_id=user_id,
        #     text=bot_answer,
        #     reply_markup=estimate_keyboard_builder(
        #         # choosed_category=choosed_category,
        #         day=day
        #     )
        # ) 
        # await GSheetService.update_user_data(
        #     tg_id=user_id,
        #     day=day,
        #     notifs=remind_count,
        #     with_current_time=True
        # )
                # bot_answer, choosed_category = await TaroService.get_taro_predict(user_id=user_id, uow=uow)
    else:
        await bot.send_message(
            chat_id=user_id,
            text=bot_answer,
            reply_markup=estimate_keyboard_builder(
                # choosed_category=choosed_category,
                day=day
            )
        )
        user: User = await UserService.get_user(user_id, uow=uow)
        received_forecasts = user.received_forecasts + 1
        forecast_no_reaction = user.forecast_no_reaction + 1
        await UserService.update_user(
            user_id=user_id,
            received_forecasts=received_forecasts,
            forecast_no_reaction=forecast_no_reaction,
            uow=uow
        )
        await GSheetService.update_user_data(
            tg_id=user_id,
            day=day,
            # notifs=remind_count,
            text=bot_answer,
            with_current_time=True,
            received_forecasts=received_forecasts,
            forecast_no_reaction=forecast_no_reaction
        )
        
        # if choosed_category:
        #     await UserService.add_choosed_category(
        #         user_id=user_id, category=choosed_category, uow=uow
        #     )
    # await ShedulerService.add_reminders_job(
    #     send_remind,
    #     user_id=user_id,
    #     state=state,
    #     day=day
    # )
    # await bot.send_message(
    #     chat_id=user_id,
    #     text='Получите свой совет сегодня',
    #     # reply_markup=advice_keyboard_builder(day)
    # )
    
    if day == settings.days_to_send:
        scheduler.remove_job(job_id=str(user_id))
    
    await state.update_data({
        "function_call_number": day
    })