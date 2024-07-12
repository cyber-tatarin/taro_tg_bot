import logging
from typing import Literal

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


logger = logging.getLogger(__name__)


# class PipeCallback(CallbackData, prefix="pipe"):
#     _default_callback_data = "pipe_callback"
#     callback_data: str | None = (_default_callback_data,)
#     pipe_id: int | None = None
#     next_task: int | None = None


# class DataCallback(CallbackData, prefix="voice"):
#     voice_gender: str


# voice_change_keyboard = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text="Male", callback_data=VoiceCallback(
#                 voice_gender="voice_change_male"
#             ).pack()),
#             InlineKeyboardButton(text="Female", callback_data=VoiceCallback(
#                 voice_gender="voice_change_female"
#             ).pack())
#         ],
#     ],
# )
user_data_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Напишу имя",
                callback_data='user_data_yes'
            ),
        ],
        [
            InlineKeyboardButton(
                text="Останусь таинственной незнакомкой 🤫",
                callback_data='user_data_no'
            )
        ],
    ],
)

user_location_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Напишу город",
                callback_data='user_location_yes'
            ),
        ],
        [
            InlineKeyboardButton(
                text="Где-где.. я в домике 🏡",
                callback_data='user_location_no'
            )
        ],
    ],
)

user_birthdate_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Напишу дату",
                callback_data='user_birthdate_yes'
            ),
        ],
        [
            InlineKeyboardButton(
                text="Продолжу инкогнито 🥷",
                callback_data='user_birthdate_no'
            )
        ],
    ],
)


first_advice_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Получить первый "совет дня"', callback_data='get_first_advice')
        ],
    ],
)


# estimate_keyboard = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [
#             InlineKeyboardButton(text='Не моё 🙄', callback_data='estimate_1'),
#             InlineKeyboardButton(text='Хорошо ❤️', callback_data='estimate_2'),
#             InlineKeyboardButton(text='Восторг 🔥', callback_data='estimate_3'),
#         ],
#     ],
# )


class EstimateCallback(CallbackData, prefix="estimate"):
    estimate: int
    choosed_category: int | None
    day: int


class AdviseCallback(CallbackData, prefix="advise"):
    day: int


advice_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='✨ Получить предсказание ✨', callback_data='get_advice')
        ],
    ],
)


def advice_keyboard_builder(day: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='✨ Получить предсказание ✨',
        callback_data=AdviseCallback(
            day=day
        ).pack(),
    )
    
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True, selective=True)


def estimate_keyboard_builder(day: int, choosed_category: int | None = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    texts = ['Не моё 🙄', 'Хорошо ❤️', 'Восторг 🔥']
    for idx, text in enumerate(texts):
        builder.button(
            text=text,
            callback_data=EstimateCallback(
                estimate=idx,
                choosed_category=choosed_category,
                day=day
            ).pack()
        )
    
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True, selective=True)


# def create_pipe_kb(
#     data: TaskData | None, pipe_id: int | None, next_task: int, is_h2_completed: bool
# ) -> InlineKeyboardMarkup:
#     builder = InlineKeyboardBuilder()

#     if data.final:
#         return None

#     if data.buttons:
#         for title, callback in data.buttons.items():
#             pipe_id_to_insert = pipe_id
#             next_task_to_insert = next_task
#             if callback:
#                 pipe_id_to_insert = None
#                 next_task_to_insert = None
#             else:
#                 callback = "continue"
#             builder.button(
#                 text=title,
#                 callback_data=PipeCallback(
#                     callback_data=callback,
#                     pipe_id=pipe_id_to_insert,
#                     next_task=next_task_to_insert,
#                 ).pack(),
#             )

#         if is_h2_completed:
#             builder.button(
#                 text="Ask question",
#                 callback_data=PipeCallback(
#                     callback_data="ask question").pack(),
#             )
#         builder.adjust(1)
#         return builder.as_markup(resize_keyboard=True, selective=True)
#     else:
#         builder.button(
#             text="continue",
#             callback_data=PipeCallback(
#                 callback_data="continue", pipe_id=pipe_id, next_task=next_task
#             ).pack(),
#         )
#         return builder.as_markup(resize_keyboard=True, selective=True)

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            # KeyboardButton(text="Связаться с админом"),
            KeyboardButton(text="Будущие функции"),
        ],
        # [
        #     KeyboardButton(text="Изменить данные о себе")
        # ]
        
    ],
    resize_keyboard=True,
    # input_field_placeholder="Выберите способ подачи"
)

    
new_features_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Расклад ТАРО',
                callback_data='tarot_spread'
            ),
        ],
        [
            InlineKeyboardButton(
                text='Толкование снов',
                callback_data='dream_interpretation'
            )
        ],
        [
            InlineKeyboardButton(
                text='Нумеролог в кармане',
                callback_data='pocket_numerologist'
            ),
        ],
        [
            InlineKeyboardButton(
                text='Твой личный астролог',
                callback_data='personal_astrologer'
            )
        ],
    ],
)


class NewFeaturesCallback(CallbackData, prefix="features"):
    feature: str
    key: int


tarot_spread_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Да, огонь 🔥',
                callback_data=NewFeaturesCallback(
                    feature='tarot_spread',
                    key=0
                ).pack()
            ),
            InlineKeyboardButton(
                text='Не знаю',
                callback_data=NewFeaturesCallback(
                    feature='tarot_spread',
                    key=1
                ).pack()
            )
        ]
    ],
)

dream_interpretation_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Очень надо 🌝',
                callback_data=NewFeaturesCallback(
                    feature='dream_interpretation',
                    key=0
                ).pack()
            ),
            InlineKeyboardButton(
                text='Я не вижу сны',
                callback_data=NewFeaturesCallback(
                    feature='dream_interpretation',
                    key=1
                ).pack()
            )
        ]
    ],
)
pocket_numerologist_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Очень интересно 😮',
                callback_data=NewFeaturesCallback(
                    feature='pocket_numerologist',
                    key=0
                ).pack()
            ),
            InlineKeyboardButton(
                text='Ну не знаю',
                callback_data=NewFeaturesCallback(
                    feature='pocket_numerologist',
                    key=1
                ).pack()
            )
        ]
    ],
)
personal_astrologer_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Заверните и по быстрее',
                callback_data=NewFeaturesCallback(
                    feature='personal_astrologer',
                    key=0
                ).pack()
            ),
            InlineKeyboardButton(
                text='Это правда возможно?',
                callback_data=NewFeaturesCallback(
                    feature='personal_astrologer',
                    key=1
                ).pack()
            )
        ]
    ],
)