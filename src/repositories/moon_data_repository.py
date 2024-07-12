from src.models.moon_data_model import MoonDataModel
from src.utils.database.repository import SQLAlchemyRepository


class MoonDataRepository(SQLAlchemyRepository):
    model = MoonDataModel