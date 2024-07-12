import datetime
from typing import Literal
import aiohttp
import ephem
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from lxml import etree

from src.models.moon_data_model import MoonDataModel
from src.schemas.moon_data_schemas import MoonData, MoonDataCreate, MoonDataUpdate
from src.utils.database.uow import InitUoW, UoW

moon_phase_annotation = Literal[
    'Новолуние', 'Первая четверть', 'Полнолуние', 'Последняя четверть',
    'Убывающий серп', 'Растущий серп', 'Растущая Луна', 'Убывающая Луна'
]

class MoonService:
    url = "https://mirkosmosa.ru/lunar-calendar"
    # @staticmethod
    # def _next_new_moon(
    #     current_datetime: datetime.datetime, utc: int
    # ) -> datetime.date:
    #     nnm: datetime.datetime = ephem.next_new_moon(current_datetime).datetime()
    #     nnm_tz = nnm + datetime.timedelta(hours=utc)
    #     return nnm_tz.date()
    
    # @staticmethod
    # def _previous_new_moon(
    #     current_datetime: datetime.datetime, utc: int
    # ) -> datetime.date:
    #     pnm: datetime.datetime = ephem.previous_new_moon(current_datetime).datetime()
    #     pnm_tz = pnm + datetime.timedelta(hours=utc)
    #     return pnm_tz.date()
    
    # @staticmethod
    # def _next_first_quarter_moon(
    #     current_datetime: datetime.datetime, utc: int
    # ) -> datetime.date:
    #     nfqm: datetime.datetime = ephem.next_first_quarter_moon(current_datetime).datetime()
    #     nfqm_tz = nfqm + datetime.timedelta(hours=utc)
    #     return nfqm_tz.date()
    
    # @staticmethod
    # def _previous_first_quarter_moon(
    #     current_datetime: datetime.datetime, utc: int
    # ) -> datetime.date:
    #     pfqm: datetime.datetime = ephem.previous_first_quarter_moon(current_datetime).datetime()
    #     pfqm_tz = pfqm + datetime.timedelta(hours=utc)
    #     return pfqm_tz.date()
    
    # @staticmethod
    # def _next_full_moon(
    #     current_datetime: datetime.datetime, utc: int
    # ) -> datetime.date:
    #     nfm: datetime.datetime = ephem.next_full_moon(current_datetime).datetime()
    #     nfm_tz = nfm + datetime.timedelta(hours=utc)
    #     return nfm_tz.date()
    
    # @staticmethod
    # def _previous_full_moon(
    #     current_datetime: datetime.datetime, utc: int
    # ) -> datetime.date:
    #     pfm: datetime.datetime = ephem.previous_full_moon(current_datetime).datetime()
    #     pfm_tz = pfm + datetime.timedelta(hours=utc)
    #     return pfm_tz.date()
    
    # @staticmethod
    # def _next_last_quarter_moon(
    #     current_datetime: datetime.datetime, utc: int
    # ) -> datetime.date:
    #     nlqm: datetime.datetime = ephem.next_last_quarter_moon(current_datetime).datetime()
    #     nlqm_tz = nlqm + datetime.timedelta(hours=utc)
    #     return nlqm_tz.date()
    
    # @staticmethod
    # def _previous_last_quarter_moon(
    #     current_datetime: datetime.datetime, utc: int
    # ) -> datetime.date:
    #     plqm: datetime.datetime = ephem.previous_last_quarter_moon(current_datetime).datetime()
    #     plqm_tz = plqm + datetime.timedelta(hours=utc)
    #     return plqm_tz.date()

    # @classmethod
    # def current_phase(cls, utc: int = 3) -> moon_phase_annotation:
    #     current_datetime = datetime.datetime.now()
    #     current_date = current_datetime.date()
    #     nnm = cls._next_new_moon(current_datetime, utc)
    #     pnm = cls._previous_new_moon(current_datetime, utc)

    #     nfqm = cls._next_first_quarter_moon(current_datetime, utc)
    #     pfqm = cls._previous_first_quarter_moon(current_datetime, utc)

    #     nfm = cls._next_full_moon(current_datetime, utc)
    #     pfm = cls._previous_full_moon(current_datetime, utc)

    #     nlqm = cls._next_last_quarter_moon(current_datetime, utc)
    #     plqm = cls._previous_last_quarter_moon(current_datetime, utc)

    #     a = [nnm, nfqm, nfm, nlqm]
    #     a.sort()

    #     phase = None
    #     if current_date == nnm or current_date == pnm:
    #         phase = 'Новолуние'
    #     elif current_date == nfqm or current_date == pfqm:
    #         phase = 'Первая четверть'
    #     elif current_date == nfm or current_date == pfm:
    #         phase = 'Полнолуние'
    #     elif current_date == nlqm or current_date == plqm:
    #         phase = 'Последняя четверть'
    #     if phase:
    #         return phase
        
    #     if a[0] == nnm:
    #         phase = 'Убывающий серп'
    #     elif a[0] == nfqm:
    #         phase = 'Растущий серп'
    #     elif a[0] == nfm:
    #         phase = 'Растущая Луна'
    #     elif a[0] == nlqm:
    #         phase = 'Убывающая Луна'
    #     if phase:
    #         return phase
    #     return 'Неизвестная фаза луны'
    
    @staticmethod
    async def fetch_html(url) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response_text = await response.text()
                return response_text
    
    @classmethod
    async def fetch_moon_data(cls) -> str | None:
        text = await cls.fetch_html(cls.url)
        soup = BeautifulSoup(text, 'html.parser')
        div_moon_day_desc = soup.find('div', class_='moon-day-desc')
    
        if div_moon_day_desc:
            # Находим тег <p> внутри div
            p_tag = div_moon_day_desc.find('p')
            if p_tag:
                # Получаем текст внутри <p>
                p_text = p_tag.get_text()
                print(p_text)
                return p_text
            else:
                print("Тег <p> не найден внутри <div class='moon-day-desc'>")
        else:
            print("<div class='moon-day-desc'> не найден")
        
    @classmethod
    async def update_moon_data_in_db(cls):
        try:
            uow = UoW()
            moon_data_text = await cls.fetch_moon_data()
            if not moon_data_text:
                return
            
            moon_data_scheme = await cls.get_moon_data(uow)
            if moon_data_scheme:
                await cls.update_moon_data(
                    moon_data_text, uow
                )
            else:
                await cls.add_moon_data(
                    moon_data_text, uow
                )
            
        except Exception as e:
            print(e)

    @staticmethod
    async def add_moon_data(
        text: str,
        uow: InitUoW = None
    ) -> None:
        async with uow:
            await uow.moon_data.add(
                obj_in=MoonDataCreate(
                    created_at=datetime.now().date(),
                    text=text
                )
            )
            await uow.commit()
            
    @staticmethod
    async def update_moon_data(
        text: str,
        uow: InitUoW = None
    ) -> MoonData:
        async with uow:
            await uow.moon_data.update(
                MoonDataModel.id == 1,
                obj_in=MoonDataUpdate(
                    created_at=datetime.now().date(),
                    text=text
                )
            )
            await uow.commit()
            
    @staticmethod
    async def get_moon_data(
        uow: InitUoW = None
    ) -> MoonData:
        async with uow:
            moon_data: MoonDataModel = await uow.moon_data.find_one_or_none(
                MoonDataModel.id == 1
            )
            if moon_data:
                return MoonData.model_validate(moon_data)
