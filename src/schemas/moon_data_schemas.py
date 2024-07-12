from datetime import datetime, time, date
from pydantic import BaseModel

class MoonDataBase(BaseModel):
    created_at: date
    text: str
    
    
class MoonData(MoonDataBase):
    id: int
    class Config:
        from_attributes = True


class MoonDataCreate(MoonDataBase):
    pass


class MoonDataUpdate(MoonDataBase):
    pass
