from datetime import datetime, time, date
from pydantic import BaseModel

class RecommendationBase(BaseModel):
    created_at: date
    recommended: list[str]
    not_recommended: list[str]
    
class Recommendation(RecommendationBase):
    id: int
    class Config:
        from_attributes = True

class RecommendationCreate(RecommendationBase):
    pass


class RecommendationUpdate(RecommendationBase):
    pass
