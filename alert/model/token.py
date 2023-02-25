from typing import Optional
from pydantic import BaseModel
class Token(BaseModel):
    name:str
    symbol: str
    price:float
    percent_change_1h: Optional[float]
    percent_change_24h: Optional[float]
    percent_change_7d: Optional[float]