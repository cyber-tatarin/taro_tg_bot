
from datetime import datetime
from functools import wraps
import logging
import os
from typing import Literal
import pygsheets

import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


def run_in_executor(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        executor = ThreadPoolExecutor(max_workers=10)
        loop = asyncio.get_running_loop()
        partial_func = lambda: func(*args, **kwargs)
        try:
            return await loop.run_in_executor(executor, partial_func)
        except Exception as x:
            logger.exception(x)
        finally:
            executor.shutdown(wait=True)
    return wrapper

class GSheetService:
    # GSHEETS_JSON_PATH = settings.GSHEETS_JSON_PATH
    GSHEETS_JSON_PATH = os.path.join("src", "data", "gsheets_key.json")
    GHEETS_NAME = 'Tarot bot Analytics'

    @staticmethod
    def find_row_number(user_id, worksheet):
        try:
            cells_list_of_lists = worksheet.find(str(user_id), matchEntireCell=True)  # [[]]
            if cells_list_of_lists:  # empty list object considered as false
                return cells_list_of_lists[0].row
            else:
                return None
        except Exception as x:
            logger.exception(x)

    @staticmethod
    def get_column_letter(col_idx: int):
        """Convert a column index to a letter (e.g., 1 -> A, 27 -> AA)"""
        string = ""
        while col_idx > 0:
            col_idx, remainder = divmod(col_idx - 1, 26)
            string = chr(65 + remainder) + string
        return string
    
    @classmethod
    @run_in_executor
    def update_user_data(
        cls,
        tg_id: int,
        day: int,
        with_current_time: bool = False,
        notifs = None,
        text: str | None = None,
        estimation: str = None,
        name: str = None,
        location: str = None,
        birth_date: str = None,
        forecast_no_reaction: int | None = None,
        forecast_rating_excellent: int | None = None,
        forecast_rating_good: int | None = None,
        forecast_rating_not_mine: int | None = None,
        received_forecasts: int | None = None,
    ) -> None:

        print(
            tg_id, day, with_current_time,
            notifs, estimation,
            name, location, birth_date,
            forecast_no_reaction,
            forecast_rating_excellent,
            forecast_rating_good,
            forecast_rating_not_mine,
            received_forecasts,
            'update_user_data'
        )
        try:
            # Authenticate using service account credentials
            gc = pygsheets.authorize(service_file=cls.GSHEETS_JSON_PATH)  # Update the path

            sheet = gc.open(cls.GHEETS_NAME)
            worksheet = sheet[0]
            
            row_number = cls.find_row_number(tg_id, worksheet)
            
            if row_number is not None:
                taro_sections_count = 12
                if name is not None:
                    notifs_col_idx = 2
                    notifs_col = cls.get_column_letter(notifs_col_idx)
                    worksheet.update_value(f'{notifs_col}{row_number}', name)
                if location is not None:
                    notifs_col_idx = 3
                    notifs_col = cls.get_column_letter(notifs_col_idx)
                    worksheet.update_value(f'{notifs_col}{row_number}', location)
                if birth_date is not None:
                    notifs_col_idx = 4
                    notifs_col = cls.get_column_letter(notifs_col_idx)
                    if birth_date:
                        birth_date = birth_date.strftime("%d.%m.%Y")  
                    worksheet.update_value(f'{notifs_col}{row_number}', birth_date)
                if notifs is not None:
                    notifs_col_idx = 6
                    notifs_col = cls.get_column_letter(notifs_col_idx)
                    worksheet.update_value(f'{notifs_col}{row_number}', notifs)
                if with_current_time:
                    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    day_col_idx = 3 * day + 1 + taro_sections_count 
                    day_col = cls.get_column_letter(day_col_idx)
                    worksheet.update_value(f'{day_col}{row_number}', current_time)
                # if notifs is not None:
                #     notifs_col_idx = 3 * day + 2 + taro_sections_count 
                #     notifs_col = cls.get_column_letter(notifs_col_idx)
                #     worksheet.update_value(f'{notifs_col}{row_number}', notifs)
                if text is not None:
                    notifs_col_idx = 3 * day + 2 + taro_sections_count 
                    notifs_col = cls.get_column_letter(notifs_col_idx)
                    worksheet.update_value(f'{notifs_col}{row_number}', text)
                if estimation is not None:
                    estimation_col_idx = 3 * day + 3 + taro_sections_count 
                    estimation_col = cls.get_column_letter(estimation_col_idx)
                    worksheet.update_value(f'{estimation_col}{row_number}', estimation)
                forecast_section = 10
                if received_forecasts is not None:
                    estimation_col_idx = forecast_section + 1
                    estimation_col = cls.get_column_letter(estimation_col_idx)
                    worksheet.update_value(f'{estimation_col}{row_number}', received_forecasts)
                if forecast_rating_not_mine is not None:
                    estimation_col_idx = forecast_section + 2
                    estimation_col = cls.get_column_letter(estimation_col_idx)
                    worksheet.update_value(f'{estimation_col}{row_number}', forecast_rating_not_mine)
                if forecast_rating_good is not None:
                    estimation_col_idx = forecast_section + 3
                    estimation_col = cls.get_column_letter(estimation_col_idx)
                    worksheet.update_value(f'{estimation_col}{row_number}', forecast_rating_good)
                if forecast_rating_excellent is not None:
                    estimation_col_idx = forecast_section + 4
                    estimation_col = cls.get_column_letter(estimation_col_idx)
                    worksheet.update_value(f'{estimation_col}{row_number}', forecast_rating_excellent)
                if forecast_no_reaction is not None:
                    estimation_col_idx = forecast_section + 5
                    estimation_col = cls.get_column_letter(estimation_col_idx)
                    worksheet.update_value(f'{estimation_col}{row_number}', forecast_no_reaction)
        except Exception as x:
            logger.exception(x)
            
    @classmethod
    @run_in_executor
    def update_user_data_features_rate(
        cls,
        tg_id: int,
        feature: Literal[
            "tarot_spread", "dream_interpretation",
            "pocket_numerologist", 'personal_astrologer'
        ],
        text: str
    ) -> None:
        
        print(
            tg_id, feature,
            'update_user_data_features_rate'
        )
        try:
            # Authenticate using service account credentials
            gc = pygsheets.authorize(service_file=cls.GSHEETS_JSON_PATH)  # Update the path

            sheet = gc.open(cls.GHEETS_NAME)
            worksheet = sheet[0]
            
            row_number = cls.find_row_number(tg_id, worksheet)
            
            if row_number is not None:
                taro_section_start = 6
                if feature == "tarot_spread":
                    day_col_idx = taro_section_start + 1
                    day_col = cls.get_column_letter(day_col_idx)
                    worksheet.update_value(f'{day_col}{row_number}', text)
                if feature == "dream_interpretation":
                    notifs_col_idx = taro_section_start + 2
                    notifs_col = cls.get_column_letter(notifs_col_idx)
                    worksheet.update_value(f'{notifs_col}{row_number}', text)
                if feature == "pocket_numerologist":
                    estimation_col_idx = taro_section_start + 3
                    estimation_col = cls.get_column_letter(estimation_col_idx)
                    worksheet.update_value(f'{estimation_col}{row_number}', text)
                if feature == "personal_astrologer":
                    estimation_col_idx = taro_section_start + 4 
                    estimation_col = cls.get_column_letter(estimation_col_idx)
                    worksheet.update_value(f'{estimation_col}{row_number}', text)
        except Exception as x:
            logger.exception(x)

    @classmethod
    @run_in_executor
    def register_user(cls, tg_id: int):
        print(tg_id, 'register_user')
        try:
            datetime_registered = datetime.now().date().strftime("%d.%m.%Y")
            

            gc = pygsheets.authorize(service_file=cls.GSHEETS_JSON_PATH)
            sheet = gc.open(cls.GHEETS_NAME)

            worksheet = sheet[0]

            row_number = cls.find_row_number(tg_id, worksheet)
            
            if row_number is None:
                id_user_time = [[tg_id, '', '', '', datetime_registered]]
                
                last_row = worksheet.get_col(1, include_empty=False)
                # get the index of the first empty row
                insert_index = len(last_row)
                worksheet.insert_rows(row=insert_index, values=id_user_time, inherit=True)
            
            else:
                return
                col_index = 4
                # Get the cell object for the specific column and edit its value
                worksheet.update_value((row_number, col_index), current_time)
        
        except Exception as x:
            logger.exception(x)

    # @staticmethod
    # async def async_execute_of_sync_gsheets(func, **kwargs):
    #     executor = ThreadPoolExecutor(max_workers=10)
    #     loop = asyncio.get_running_loop()
    #     try:
    #         await loop.run_in_executor(executor, func, kwargs)
    #     except Exception as x:
    #         logger.exception(x)
    #     finally:
    #         executor.shutdown(wait=True)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # loop.create_task(
    #     GSheetService.async_execute_of_sync_gsheets(
    #         GSheetService.register_user(
    #             {
    #                 "tg_id": 1231,
    #                 "username": "alex",
    #                 "datetime_registered": "13.01.2024"
    #                 }
    #         )
    #     )
    # )
    loop.create_task(
        (
            GSheetService.update_user_data(
                tg_id=123,
                day=5,
                estimation=1,
                notifs=1,
                # notifs=datetime.now()
                # {
                #     "tg_id": 1231,
                #     "day": "1",
                #     "datetime_registered": "13.01.2024"
                # }
            )
        )
    )
    pass
    logger.info('gogogogogooo')