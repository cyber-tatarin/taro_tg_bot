
import datetime
import time

from sqlalchemy import TIMESTAMP, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.utils.database.database import Base

class JobModel(Base):
    __tablename__ = 'jobs'
    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    # job_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    next_run_time: Mapped[int] = mapped_column(TIMESTAMP, index=True)
    job_state: Mapped[str] = mapped_column(Text, nullable=False)
