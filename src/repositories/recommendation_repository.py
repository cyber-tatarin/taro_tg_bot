from src.models.recommendation_model import RecommendationModel
from src.utils.database.repository import SQLAlchemyRepository


class RecommendationRepository(SQLAlchemyRepository):
    model = RecommendationModel