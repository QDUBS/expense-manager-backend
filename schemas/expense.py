from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from .user import ShowUser
from .profile import ShowProfile


class ExpenseBaseSchema(BaseModel):
    user_id: str
    merchant: str
    date: str
    total: int
    currency: str
    category: str
    description: str
    receipt: str


class UpdateExpenseBaseSchema(BaseModel):
    user_id: str
    merchant: str
    date: str
    total: int
    currency: str
    category: str
    description: str
    receipt: str
    expense_stage: str


class ExpenseSchema(ExpenseBaseSchema):
    class Config():
        from_attributes = True


class UpdateExpenseSchema(UpdateExpenseBaseSchema):
    class Config():
        from_attributes = True


class ShowExpense(BaseModel):
    id: str
    merchant: str
    date: str
    total: int
    currency: str
    category: str
    description: str
    receipt: str
    expense_stage: str
    expense_status: str
    updatedAt: datetime
    user: ShowUser
    profile: ShowProfile

    class Config():
        from_attributes = True
