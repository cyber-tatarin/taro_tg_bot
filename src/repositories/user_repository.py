from src.models.user_model import UserModel
from src.utils.database.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = UserModel