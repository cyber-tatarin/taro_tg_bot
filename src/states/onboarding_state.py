from aiogram.fsm.state import State, StatesGroup


class OnbordingState(StatesGroup):
    get_user_name = State()
    get_user_location = State()
    get_user_location2 = State()
    get_user_birthdate = State()

