from datetime import datetime, time, date
from pydantic import BaseModel


class UserCreate(BaseModel):
    user_id: int
    name: str | None
    location: str | None
    birth_date: date | None


class UserUpdate(BaseModel):
    name: str | None = None
    location: str | None = None
    birth_date: date | None = None
    sheduler_time: time | None = None
    used_categories: list | None = None
    received_forecasts: int | None = None
    forecast_rating_not_mine: int | None = None
    forecast_rating_good: int | None = None
    forecast_rating_excellent: int | None = None
    forecast_no_reaction: int | None = None


class User(BaseModel):
    user_id: int
    name: str | None
    location: str | None
    birth_date: date | None
    created_at: datetime 
    sheduler_time: time | None
    used_categories: list | None
    received_forecasts: int | None
    forecast_rating_not_mine: int | None
    forecast_rating_good: int | None
    forecast_rating_excellent: int | None
    forecast_no_reaction: int | None
    
    class Config:
        from_attributes = True
