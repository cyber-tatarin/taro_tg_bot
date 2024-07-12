from datetime import datetime
from sqlalchemy import Integer, Date, String
from sqlalchemy.orm import Mapped, mapped_column

from src.utils.database.database import Base


class MoonDataModel(Base):
    __tablename__ = "moon_data"
    id: Mapped[int] = mapped_column(
        Integer, index=True, primary_key=True, autoincrement=True
    )
    created_at: Mapped[datetime.date] = mapped_column(Date)
    text: Mapped[str] = mapped_column(String)
