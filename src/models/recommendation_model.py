from datetime import datetime
from sqlalchemy import ARRAY, Integer, Date, String
from sqlalchemy.orm import Mapped, mapped_column

from src.utils.database.database import Base


class RecommendationModel(Base):
    __tablename__ = "recommendations"
    id: Mapped[int] = mapped_column(
        Integer, index=True, primary_key=True, autoincrement=True
    )
    created_at: Mapped[datetime.date] = mapped_column(Date)
    recommended: Mapped[list] = mapped_column(ARRAY(String), default=[])
    not_recommended: Mapped[list] = mapped_column(ARRAY(String), default=[])
