from datetime import datetime
from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext

from src.data.config import settings
from src.middlewares.uow_middleware import UoWSessionMiddleware
from src.services.bot_service import send_daily_prediction_message, send_remind
from src.services.geo_service import GeoService
from src.services.gsheets_service import GSheetService
from src.services.sheduler_service import ShedulerService
from src.services.user_service import UserService
from src.states.onboarding_state import OnbordingState
from src.keyboards.keyboards import (
    advice_keyboard_builder,
    user_data_keyboard,
    user_location_keyboard,
    user_birthdate_keyboard,
    menu_keyboard
)
from src.utils.database.uow import InitUoW
from src.utils.loader import bot


router = Router()
router.message.middleware(UoWSessionMiddleware())
router.callback_query.middleware(UoWSessionMiddleware())

@router.message(CommandStart(ignore_case=True))
async def start(message: types.Message, state: FSMContext, uow: InitUoW):
    user_id = message.from_user.id
    if await UserService.get_user(user_id=message.from_user.id, uow=uow):
        return
    await state.clear()
    await state.get_state()
    await state.update_data(onboarding='onboarding')
    admin_link = f'<a href="{settings.admin_tg_link}">написать мне в личку</a>'
    await message.answer(
        f'Мои советы основаны на лунном календаре, так что готовься к волшебству каждый день. Я буду присылать тебе прогноз на день, и будет здорово, если ты попробуешь следовать моим рекомендациям. Давай наймем звезды в качестве персональных стилистов твоего дня 🌝\n\nСейчас у меня тестовый режим, так что очень прошу тебя оценивать прогнозы. Это поможет мне сделать их еще точнее и полезнее для тебя. Скоро здесь будет ещё больше функций, и ты можешь повлиять на то, чтобы добавить всё, что нужно именно тебе. А советы и предложения можешь {admin_link} 😉\n\nДавай вместе создадим что-то потрясающее, чтобы даже звезды обзавидовались!',
        reply_markup=menu_keyboard,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )
    await message.answer(
        'Привет-привет! Как тебя зовут, чтобы я могла обращаться к тебе по имени в наших звёздных беседах?',
        reply_markup=user_data_keyboard
    )
    await state.set_state(OnbordingState.get_user_name)
    await GSheetService.register_user(
        tg_id=user_id#, username=message.from_user.username
    )

async def user_input_location(message: types.Message, state: FSMContext):
    await state.set_state(OnbordingState.get_user_location)
    await message.answer(
        'А где ты проживаешь, чтобы я могла учесть это в нашем звездном прогнозе?',
        reply_markup=user_location_keyboard
    )


#### USER INPUT 2 = NAME
@router.callback_query(F.data == 'user_data_no')
async def user_data_no(
    query: types.CallbackQuery, state: FSMContext, uow: InitUoW
):
    user_id = query.message.chat.id
    await query.message.delete_reply_markup()
    
    await query.message.answer(
        'Без проблем! Буду обращаться к тебе как к таинственной незнакомке. Наши звёздные беседы всё равно будут полны магии и волшебства. ✨',
        # reply_markup=advice_keyboard_builder(1)
    )
    await query.answer()
    await user_input_location(query.message, state)
    # await state.update_data({
    #     "function_call_number": 1
    # })
    # await ShedulerService.add_reminders_job(
    #     send_remind,
    #     user_id=user_id,
    #     state=state,
    #     day=1
    # )
    # await ShedulerService.add_main_job(
    #     send_daily_prediction_message,
    #     user_id, state, uow
    # )
    
@router.callback_query(F.data == 'user_data_yes')
async def user_data_yes(
    query: types.CallbackQuery, state: FSMContext, uow: InitUoW
):
    user_id = query.message.chat.id
    await query.message.delete_reply_markup()
    await query.message.answer(
        'Напиши свое имя',
        # reply_markup=advice_keyboard_builder(1)
    )
    await state.set_state(OnbordingState.get_user_name)
    await query.answer()


@router.message(OnbordingState.get_user_name)
async def get_user_name(message: types.Message, state: FSMContext, uow: InitUoW):

    
    await message.answer(f'Спасибо, {message.text}! Теперь я смогу обращаться к тебе лично. Будет здорово, если наши звёздные беседы станут ещё более уютными. 🌟')
    await state.update_data(name=message.text)
    await state.set_state()
    await user_input_location(message, state)
####

async def user_input_birthdate(message: types.Message, state: FSMContext):
    await state.set_state(OnbordingState.get_user_birthdate)
    await message.answer(
        'Чтобы давать точные прогнозы, мне нужно знать твою дату рождения. Пожалуйста, введи её в формате ДД.ММ.ГГГГ.',
        reply_markup=user_birthdate_keyboard
    )
    
#### USER INPUT 2 = Location
@router.callback_query(F.data == 'user_location_yes')
async def user_location_yes(
    query: types.CallbackQuery, state: FSMContext, uow: InitUoW
):
    await query.message.delete_reply_markup()
    await query.message.answer(
        "Напиши свой город"
    )
    await query.answer()
    await state.set_state(OnbordingState.get_user_location)
    # return await user_input_birthdate(query.message, state)

@router.message(OnbordingState.get_user_location)
async def get_user_location(
    message: types.Message, state: FSMContext
):
    city = message.text.capitalize()
    if await GeoService.city_exists(city):
        await state.update_data(location=city)
        await message.answer('Класс, спасибо тебе за уточнение. Продолжим!')
        await state.set_state()
        return await user_input_birthdate(message, state)
    await message.answer('Хм, кажется, в названии города закралась ошибка. Попробуй ввести его снова, чтобы звезды точно знали, где ты!')
    await state.set_state(OnbordingState.get_user_location2)

@router.message(OnbordingState.get_user_location2)
async def get_user_location2(
    message: types.Message, state: FSMContext
):
    city = message.text.capitalize()
    if await GeoService.city_exists(city):
        await state.update_data(location=city)
        await message.answer('Класс, спасибо тебе за уточнение. Продолжим!')
    else:
        await message.answer('Что-то пошло не так.. пока разбираюсь буду строить прогноз по Московскому времени.')
    await state.set_state()
    return await user_input_birthdate(message, state)
    

@router.callback_query(F.data == 'user_location_no')
async def user_location_no(
    query: types.CallbackQuery, state: FSMContext, uow: InitUoW
):
    await query.message.delete_reply_markup()
    await query.answer()
    await query.message.answer(
        "Без проблем, будем считать, что твой прогноз по московскому времени, если передумаешь - просто скажи"
    )
    return await user_input_birthdate(query.message, state)

####
    
async def finish_onboarding(message: types.Message, state: FSMContext, uow: InitUoW):
    user_id = message.chat.id
    print(user_id)
    await state.set_state()
    fsm_data = await state.get_data()
    is_data_change = fsm_data.get("data_change")
    birth_date = fsm_data.get('birth_date')
    if birth_date:
        birth_date = datetime.strptime(birth_date, "%d.%m.%Y").date()
    
    name = fsm_data.get('name')
    location = fsm_data.get('location')
    if name is None:
        name = ""
    if location is None:
        location = ""
    if birth_date is None:
        birth_date = ""

    if is_data_change:
        await message.answer(
            'Отлично, мы изменили данные о тебе!'
        )
        await UserService.update_user(
            user_id=user_id,
            name=name,
            location=location,
            birth_date=birth_date,
            uow=uow
        )
        return await GSheetService.update_user_data(
            tg_id=user_id,
            day=0,
            name=name,
            location=location,
            birth_date=birth_date,
        )
    await ShedulerService.add_reminders_job(
        send_remind,
        user_id=user_id,
        state=state,
        day=1
    )
    if await UserService.get_user(user_id=user_id, uow=uow):
        await UserService.update_user(
            user_id=user_id,
            name=name,
            location=location,
            birth_date=birth_date,
            uow=uow
        )
    else:
        await UserService.add_user(
            user_id=user_id,
            name=name,
            location=location,
            birth_date=birth_date,
            uow=uow
        )
    await message.answer(
        'Соединение со звездами установлено! Готова получить свой первый прогноз?',
        reply_markup=advice_keyboard_builder(1)
    )
    await GSheetService.update_user_data(
        tg_id=user_id,
        day=0,
        name=name,
        location=location,
        birth_date=birth_date,
        forecast_no_reaction=0,
        forecast_rating_excellent=0,
        forecast_rating_good=0,
        forecast_rating_not_mine=0,
        received_forecasts=0
    )
    await state.update_data(onboarding=None)

    
#### USER INPUT 3 = birthdate
@router.message(OnbordingState.get_user_birthdate)
async def get_user_birthdate(
    message: types.Message, state: FSMContext, uow: InitUoW
):
    user_id = message.from_user.id
    try:
        date_object = datetime.strptime(message.text, "%d.%m.%Y").date()
        if date_object.year < 1900:
            raise ValueError
    except ValueError:
        return await message.answer(
            "Ой, кажется, я не смогла распознать дату. Пожалуйста, попробуй еще раз и введи дату в формате ДД.ММ.ГГГГ, например, 25.12.1985.",
            reply_markup=user_birthdate_keyboard
        )
    except Exception as e:
        print(e)
        # await state.clear()
        return await state.set_state()

    await state.update_data(birth_date=message.text)

    await message.answer(
        "Спасибо! Теперь я смогу делать прогнозы, учитывая твою дату рождения. Наши звёздные беседы станут ещё точнее и полезнее. 🌟"
    )
    await finish_onboarding(message, state, uow)
    
@router.callback_query(F.data == 'user_birthdate_no')
async def user_birthdate_no(
    query: types.CallbackQuery, state: FSMContext, uow: InitUoW
):
    await query.message.delete_reply_markup()
    await query.answer()
    await query.message.answer(
        "Понимаю, если ты не хочешь делиться своей датой рождения. Буду делать прогнозы без этого, но если передумаешь, всегда можешь поделиться этой информацией позже. ✨"
    )
    await finish_onboarding(query.message, state, uow)

@router.callback_query(F.data == 'user_birthdate_yes')
async def user_birthdate_yes(
    query: types.CallbackQuery, state: FSMContext, uow: InitUoW
):
    await query.message.delete_reply_markup()
    await query.answer()
    await query.message.answer(
        "Введи дату в формате ДД.ММ.ГГГГ, например, 25.12.1985"
    )
    await state.set_state(OnbordingState.get_user_birthdate)