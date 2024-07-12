from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from src.keyboards.keyboards import (
    new_features_keyboard,
    tarot_spread_keyboard,
    dream_interpretation_keyboard,
    pocket_numerologist_keyboard,
    personal_astrologer_keyboard,
    NewFeaturesCallback,
    user_data_keyboard
)
from src.data.config import settings
from src.middlewares.uow_middleware import UoWSessionMiddleware
from src.services.gsheets_service import GSheetService
from src.services.sheduler_service import ShedulerService
from src.services.user_service import UserService
from src.utils.database.uow import InitUoW


router = Router()
router.message.middleware(UoWSessionMiddleware())


@router.message(Command('stop'))
async def data_change(message: types.Message, state: FSMContext, uow: InitUoW):
    user_id = message.from_user.id
    await state.clear()
    await UserService.delete_user(user_id=user_id, uow=uow)
    ShedulerService.delete_user_jobs(user_id=user_id)
    await message.answer(
        'данные удалены, нажимайте /start'
    )
    
    
    
    
@router.message(F.text == 'Изменить данные о себе')
@router.message(Command('change_your_information'))
async def data_change(message: types.Message, state: FSMContext):
    fsm_data = await state.get_data()
    if fsm_data.get("onboarding") is None:
        await state.update_data(data_change='data_change')
    await message.answer(
        'Привет-привет! Как тебя зовут, чтобы я могла обращаться к тебе по имени в наших звёздных беседах?',
        reply_markup=user_data_keyboard
    )
    await state.set_state()
        
@router.message(F.text == 'Связаться с админом')
@router.message(Command('contact_admin'))
async def admin(message: types.Message, state: FSMContext):

    await message.answer(
        f'Если у тебя есть вопросы или предложения, можешь связаться с нашим администратором напрямую: {settings.admin_tg}. Мы всегда рады помочь и учесть твои пожелания!'
    )
    
@router.message(F.text == 'Будущие функции')
async def new_features(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    # event_type = 'Use start command'
    # log = {
    #     "user_id": user_id
    # }
    await message.answer(
        'У нас в планах множество интересных функций! Скоро ты сможешь делать расклады Таро, получать толкования снов, консультироваться по нумерологии и многое другое. Следи за обновлениями и будь готова к новым волшебным возможностям! ✨',
        reply_markup=new_features_keyboard
    )
    
    # await state.set_state(OnbordingState.get_user_name)
    # await GSheetService.register_user(
    #     tg_id=user_id, username=message.from_user.username
    # )


@router.callback_query(F.data == 'tarot_spread')
async def tarot_spread(
    query: types.CallbackQuery, state: FSMContext
):
    await query.answer()
    await query.message.delete_reply_markup()
    await query.message.answer(
        'Совсем скоро, ты сможешь сделать расклад карт Таро одним нажатием кнопки! Представляешь, как удобно?\nБудешь ли ты искать ответ на свой вопрос да/нет, или разгадывать загадки Вселенной с конкретным запросом — я разложу карты и дам тебе самое подробное описание.\nЧто скажешь, заинтриговала? Готова погрузиться в магию?',
        reply_markup=tarot_spread_keyboard
    )
    
    
@router.callback_query(F.data == 'dream_interpretation')
async def dream_interpretation(
    query: types.CallbackQuery, state: FSMContext
):
    await query.answer()
    await query.message.delete_reply_markup()
    await query.message.answer(
        'Как часто бывает, просыпаешься после странного сна и думаешь: "Ну что это вообще было? Это точно что-то значит!"\nНу, а я здесь, чтобы помочь тебе! Представь себе: ты можешь записать аудио сразу после пробуждения, и я дам тебе толкование сна. Теперь у тебя всегда будет кто-то, с кем можно поделиться своими ночными приключениями, и никто не скажет, что это бред. Круто, правда?',
        reply_markup=dream_interpretation_keyboard
    )
    
    
@router.callback_query(F.data == 'pocket_numerologist')
async def pocket_numerologist(
    query: types.CallbackQuery, state: FSMContext
):
    await query.answer()
    await query.message.delete_reply_markup()
    await query.message.answer(
        'А ты знала, что дата и время твоего рождения — это ключевые точки в твоей судьбе?\nПредставь, зная свои сильные и слабые стороны, следуя задачам, вложенным на тебя звездами, ты сможешь получить от жизни больше, чем даже мечтала!\nЯ расскажу тебе, какова твоя миссия и предназначение, и подскажу, от чего лучше держаться подальше. Готова узнать свои космические секреты?',
        reply_markup=pocket_numerologist_keyboard
    )
    
    
@router.callback_query(F.data == 'personal_astrologer')
async def personal_astrologer(
    query: types.CallbackQuery, state: FSMContext
):
    await query.answer()
    await query.message.delete_reply_markup()
    await query.message.answer(
        'Такого ты точно не могла представить, что можно будет обратится к астрологу не выходят за пределы собственного телефона\nЯ составлю натальную карту и дам общий прогноз о твоих данностях. Также, ты сможешь задать мне любой вопрос на интересующие тебя темы\nДаже не представлю сколько тем мы будем с тобой обсуждать 😍 возможно, даже выберем тебе жениха.\n',
        reply_markup=personal_astrologer_keyboard
    )
    
    
@router.callback_query(NewFeaturesCallback.filter())
async def new_features_callback(
    query: types.CallbackQuery, callback_data: NewFeaturesCallback
):
    user_id = query.message.chat.id
    await query.answer(
        'Спасибо, за ответ'
    )
    await query.message.delete_reply_markup()

    await GSheetService.update_user_data_features_rate(
        tg_id=user_id,
        feature=callback_data.feature,
        text=query.message.reply_markup.inline_keyboard[0][callback_data.key].text
    )
