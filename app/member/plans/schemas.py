from pydantic import BaseModel
from typing import Optional, List


class AdminMemberPlan(BaseModel):
    """
    主体对象
    """
    name: str
    domain: str
    available: bool

    class Config:
        orm_mode = True
