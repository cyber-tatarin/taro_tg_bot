
from datetime import datetime

from sqlalchemy import ARRAY, TIMESTAMP, BigInteger, Date, Integer, String, Time, func
from sqlalchemy.orm import Mapped, mapped_column

from src.utils.database.database import Base


class UserModel(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(
        BigInteger, index=True, primary_key=True
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    sheduler_time: Mapped[datetime.time] = mapped_column(Time, nullable=True)
    used_categories: Mapped[list] = mapped_column(ARRAY(Integer), default=[], nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    location: Mapped[str] = mapped_column(String, nullable=True)
    birth_date: Mapped[datetime.date] = mapped_column(
        Date, nullable=True
    )
    received_forecasts: Mapped[int] = mapped_column(
        Integer, default=0
    )
    forecast_rating_not_mine: Mapped[int] = mapped_column(
        Integer, default=0
    )
    forecast_rating_good: Mapped[int] = mapped_column(
        Integer, default=0
    )
    forecast_rating_excellent: Mapped[int] = mapped_column(
        Integer, default=0
    )
    forecast_no_reaction: Mapped[int] = mapped_column(
        Integer, default=0
    )
