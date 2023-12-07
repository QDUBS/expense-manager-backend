from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from .user import ShowUser


class NewsLetterListBaseSchema(BaseModel):
    user_id: str
    name: str
    email: str

class NewsLetterListSchema(NewsLetterListBaseSchema):
    class Config():
        from_attributes = True

class ShowNewsLetterList(BaseModel):
    name: str
    email: str
    createdAt: datetime
    user: ShowUser

    class Config():
        from_attributes = True
