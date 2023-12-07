from typing import List, Union
from pydantic import BaseModel
from datetime import datetime


class ShowProfile(BaseModel):
    first_name: str
    last_name: str
    mobile_number: str
    department: str
    role: str
    staff_id: str
    photo: str

    class Config():
        from_attributes = True


class ExpenseSchema(BaseModel):
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

    class Config():
        from_attributes = True


class SupportTicketSchema(BaseModel):
    issue: str
    subject: str
    message: str

    class Config():
        from_attributes = True


class UserSchema(BaseModel):
    email: str
    password: str


class CreateUser(BaseModel):
    id: str
    email: str

    class Config():
        from_attributes = True
        

class ShowUser(BaseModel):
    id: str
    email: str
    userType: str
    profile_data: Union[ShowProfile, None]
    expenses: List[ExpenseSchema] = []
    support_tickets: List[SupportTicketSchema] = []

    class Config():
        from_attributes = True
