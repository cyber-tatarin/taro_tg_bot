from datetime import datetime

from src.models.user_model import UserModel
from src.schemas.user_schemas import User, UserCreate, UserUpdate
from src.utils.database.uow import InitUoW


class UserService:
    @staticmethod
    async def add_user(
        user_id: int, name: str = None,
        birth_date: datetime.date = None,
        location: str = None,
        uow: InitUoW = None
    ) -> None:
        async with uow:
            # try:
            if not name:
                name = None
            if not location:
                location = None
            if not birth_date:
                birth_date = None
            await uow.users.add(
                UserCreate(
                    user_id=user_id,
                    name=name,
                    location=location,
                    birth_date=birth_date
                )
            )
            await uow.commit()
            # except IntegrityError as e:
            #     if e.orig.sqlstate == '23505':
            #         return 'поле **mod_name** должно быть уникально'
            #     else:
            #         print(e.orig)
            #         return 'Неизвестная ошибка при добавлении в бд'
    
    @staticmethod
    async def update_user(
        user_id: int, name: str = None,
        birth_date: datetime.date = None,
        location: str = None,
        received_forecasts: int | None = None,
        forecast_rating_not_mine: int | None = None,
        forecast_rating_good: int | None = None,
        forecast_rating_excellent: int | None = None,
        forecast_no_reaction: int | None = None,
        uow: InitUoW = None,
    ) -> None:
        async with uow:
            # try:
            if not name:
                name = None
            if not location:
                location = None
            if not birth_date:
                birth_date = None
            update_data = {
                "name": name,
                "birth_date": birth_date,
                "location": location,
                "received_forecasts": received_forecasts,
                "forecast_rating_not_mine": forecast_rating_not_mine,
                "forecast_rating_good": forecast_rating_good,
                "forecast_rating_excellent": forecast_rating_excellent,
                "forecast_no_reaction": forecast_no_reaction,
            }

            # Убираем ключи со значением None
            update_data = {k: v for k, v in update_data.items() if v is not None}

            if update_data:
                await uow.users.update(
                    UserModel.user_id == user_id,
                    obj_in=UserUpdate(**update_data)
                )
                await uow.commit()
            # except IntegrityError as e:
            #     if e.orig.sqlstate == '23505':
            #         return 'поле **mod_name** должно быть уникально'
            #     else:
            #         print(e.orig)
            #         return 'Неизвестная ошибка при добавлении в бд'
                
    @staticmethod
    async def get_user(
        user_id: int, uow: InitUoW
    ) -> User | None:
        async with uow:
            user_db = await uow.users.find_one_or_none(
                UserModel.user_id == user_id
            )
            if user_db:
                return User.model_validate(user_db)
        
    @staticmethod
    async def add_sheduler_time(
        user_id: int, sheduler_time: datetime.time, uow: InitUoW
    ) -> UserModel:
        async with uow:
            user: UserModel = await uow.users.update(
                UserModel.user_id == user_id,
                obj_in=UserUpdate(
                    sheduler_time=sheduler_time
                )
            )
            await uow.commit()
            return user
    
    @staticmethod
    async def add_choosed_category(
        user_id: int, category: int, uow: InitUoW
    ) -> UserModel:
        async with uow:
            user: UserModel = await uow.users.find_one_or_none(
                UserModel.user_id == user_id
            )
            print(category)
            print(user_id)
            if user:
                print(user.used_categories)
                print(type(user.used_categories))
                # user.used_categories.append(category)
                # user: UserModel = await uow.users.update(
                #     UserModel.user_id == user_id,
                #     obj_in=UserUpdate(
                #         used_categories=user.used_categories.append(category)
                #     )
                # )
                used_categories = user.used_categories[:] 
                used_categories.append(category)           
                user.used_categories = used_categories
                print()
                await uow.commit()
    
    @staticmethod
    async def delete_user(
        user_id: int, uow: InitUoW
    ) -> None:
        async with uow:

            await uow.users.delete(
                UserModel.user_id == user_id
            )
            await uow.commit()