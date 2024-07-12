import asyncio
from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from src.data.config import settings
from src.middlewares.uow_middleware import UoWSessionMiddleware
from src.schemas.user_schemas import User
from src.services.bot_service import send_daily_prediction_message
from src.services.gsheets_service import GSheetService
from src.services.sheduler_service import ShedulerService
from src.services.taro_service import TaroService
from src.services.user_service import UserService
from src.utils.database.uow import InitUoW
from src.utils.loader import scheduler, bot
from src.keyboards.keyboards import AdviseCallback, EstimateCallback, estimate_keyboard_builder

router = Router()
router.callback_query.middleware(UoWSessionMiddleware())


@router.callback_query(AdviseCallback.filter())
async def get_advice_handler(
    query: types.CallbackQuery, callback_data: AdviseCallback, state: FSMContext, uow: InitUoW
):
    await get_advice(query, callback_data, state, uow)

async def get_advice(
        query: types.CallbackQuery,
        callback_data: AdviseCallback | None,
        state: FSMContext, uow: InitUoW
    ):
    user_id = query.from_user.id
    await query.message.delete()
    fsm_data = await state.get_data()
    day = callback_data.day
    await asyncio.sleep(2)
    await bot.send_message(
        chat_id=user_id,
        text="Отлично, ты сделал первый шаг к волшебству! Теперь каждый день тебя будет ждать прогноз, который поможет сделать твой день лучше. Наслаждайся и пусть звезды всегда освещают твой путь! ✨",
    )
    bot_answer = await TaroService.get_taro_predict(user_id=user_id, uow=uow)
    if day == 1:
        await asyncio.sleep(2)
        await bot.send_message(
            chat_id=user_id,
            text=bot_answer,
            reply_markup=estimate_keyboard_builder(
                # choosed_category=choosed_category,
                day=day
            )
        )
        count_interval_mapping = {
            1: settings.REMINER1_SECONDS,
            2: settings.REMINER2_SECONDS,
            3: settings.REMINER3_SECONDS
        }
        
        # remind_count = fsm_data.get(f'remind_{day}')
        # if not remind_count:
        #     remind_count = 0
        # interval = count_interval_mapping[remind_count]
        remind_count = 0
        for key, value in count_interval_mapping.items():
            # if remind_count < key:
            try:
                scheduler.remove_job(job_id=str(f'remind_{value}_{user_id}'))
            except Exception as e:
                print(e)
                remind_count = key
                print('removed last remind ', key)
                break
            print(f'remove remind_{value}_{user_id}' )
        await UserService.update_user(
            user_id=user_id,
            received_forecasts=1,
            forecast_no_reaction=1,
            uow=uow
        )
        await state.update_data({
            "function_call_number": 1
        })
        await ShedulerService.add_main_job(
            send_daily_prediction_message, 
            user_id, uow
        )
        await GSheetService.update_user_data(
            tg_id=user_id,
            day=day,
            text=bot_answer,
            received_forecasts=1,
            forecast_no_reaction=1,
            notifs=remind_count,
            with_current_time=True
        )
        # await asyncio.sleep(settings.first_advise_seconds)
        
    # bot_answer, choosed_category = await TaroService.get_taro_predict(user_id=user_id, uow=uow)
    # else:
    
    #     await bot.send_message(
    #         chat_id=user_id,
    #         text=bot_answer,
    #         reply_markup=estimate_keyboard_builder(
    #             # choosed_category=choosed_category,
    #             day=day
    #         )
    #     )
    

    
    
    # if choosed_category:
    #     await UserService.add_choosed_category(
    #         user_id=user_id, category=choosed_category, uow=uow
    #     )

@router.callback_query(EstimateCallback.filter())
async def estimate_advice(
    query: types.CallbackQuery, callback_data: EstimateCallback, state: FSMContext, uow: InitUoW
):
    user_id = query.from_user.id
    texts = ['Не моё 🙄', 'Хорошо ❤️', 'Восторг 🔥']
    await query.message.edit_reply_markup()

    await query.message.answer('Спасибо за вашу оценку')

    await query.answer()
    user: User = await UserService.get_user(user_id, uow=uow)
    forecast_rating_excellent = None
    forecast_rating_good = None
    forecast_rating_not_mine = None
    if callback_data.estimate == 0:
        forecast_rating_not_mine = user.forecast_rating_not_mine + 1
    elif callback_data.estimate == 1:
        forecast_rating_good = user.forecast_rating_good + 1
    elif callback_data.estimate == 2:
        forecast_rating_excellent = user.forecast_rating_excellent + 1
    forecast_no_reaction = user.forecast_no_reaction - 1
    await UserService.update_user(
        user_id=user_id,
        forecast_no_reaction=forecast_no_reaction,
        forecast_rating_excellent=forecast_rating_excellent,
        forecast_rating_good=forecast_rating_good,
        forecast_rating_not_mine=forecast_rating_not_mine,
        uow=uow
    )
    await GSheetService.update_user_data(
        tg_id=user_id,
        day=callback_data.day,
        estimation=texts[callback_data.estimate],
        forecast_rating_excellent=forecast_rating_excellent,
        forecast_rating_good=forecast_rating_good,
        forecast_rating_not_mine=forecast_rating_not_mine,
        forecast_no_reaction=forecast_no_reaction
    )
