


import os
import aiohttp
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from lxml import etree

from src.models.recommendation_model import RecommendationModel
from src.schemas.recommendation_schemas import Recommendation, RecommendationCreate, RecommendationUpdate
from src.utils.database.uow import InitUoW, UoW

class RecommendationService:
    url = "https://rivendel.ru/today.php"
    html_file_name = os.path.join('src', 'data', 'info.html')

    @staticmethod
    async def add_recommendations(
        recommended: list[str],
        not_recommended: list[str],
        uow: InitUoW = None
    ) -> None:
        async with uow:
            await uow.recommendations.add(
                obj_in=RecommendationCreate(
                    created_at=datetime.now().date(),
                    recommended=recommended,
                    not_recommended=not_recommended
                )
            )
            await uow.commit()
            
    @staticmethod
    async def get_recommendations(
        uow: InitUoW = None
    ) -> Recommendation:
        async with uow:
            recommendation: RecommendationModel = await uow.recommendations.find_one_or_none(
                RecommendationModel.id == 1
            )
            if recommendation:
                return Recommendation.model_validate(recommendation)

    @staticmethod
    async def update_recommendations(
        recommended: list[str],
        not_recommended: list[str],
        uow: InitUoW = None
    ) -> Recommendation:
        async with uow:
            await uow.recommendations.update(
                RecommendationModel.id == 1,
                obj_in=RecommendationUpdate(
                    created_at=datetime.now().date(),
                    recommended=recommended,
                    not_recommended=not_recommended
                )
            )
            await uow.commit()
            
    @staticmethod
    async def fetch_html(url) -> bytes:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response_bytes = await response.read()
                return response_bytes

    @classmethod
    async def update_recommendations_in_db(cls):
        try:
            uow = UoW()
            recommended, not_recommended = await cls.fetch_recommendations()
            recommendation = await cls.get_recommendations(uow)
            if recommendation:
                await cls.update_recommendations(
                    recommended, not_recommended, uow
                )
            else:
                await cls.add_recommendations(
                    recommended, not_recommended, uow
                )
        except Exception as e:
            print(e)

    @classmethod
    async def fetch_recommendations(cls):
        html = await cls.fetch_html(cls.url)
        with open(cls.html_file_name, 'wb') as f:
            f.write(html)

        with open(cls.html_file_name, 'r', encoding="windows-1251") as f:
            b = f.readlines()
            # b = f.read()
            rec_line = -1
            not_rec_line = -1
            for idx, line in enumerate(b):
                if line.find('Рекомендуется:') != -1:
                    rec_line = idx
                elif line.find('Не рекомендуется:') != -1:
                    not_rec_line = idx
    
            print(b[rec_line])
            print(b[not_rec_line])
            idx = 1
            recommended = []
            while True:
                print(b[rec_line + idx])
                if not b[rec_line + idx].startswith(' <br/>-'):
                    break 
                if b[rec_line + idx].find('<br/><br/>') != -1:
                    break 
                recommended.append(b[rec_line + idx].replace('<br/>-', '').replace('\n', '').strip())
                idx += 1
            idx = 1
            not_recommended = []
            while True:
                line = b[not_rec_line + idx]
                print(line)
                if not line.startswith(' <br/>-'):
                    break
                end_idx = line.find('<br/><br/><b>')
                if end_idx != -1:
                    not_recommended.append(line[:end_idx].replace('<br/>-', '').replace('\n', '').strip())
                    break
                not_recommended.append(line.replace('<br/>-', '').replace('\n', '').strip())
                idx += 1
            print(recommended)
            print(not_recommended)
        os.remove(cls.html_file_name)
        return recommended, not_recommended
