from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, event
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime
from enum import Enum
import uuid


class ExpenseType(str, Enum):
    HOTEL_ACCOMODATION = "HOTEL_ACCOMODATION"
    FEEDING = "FEEDING"
    FLIGHT = "FLIGHT"


class ExpenseStage(str, Enum):
    PENDING = "PENDING"
    IN_REVIEW = "IN_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class ExpenseStatus(str, Enum):
    ALERT_HIGH = "ALERT_HIGH"
    ALERT_LOW = "ALERT_LOW"
    ALERT_FREQUENT = "ALERT_FREQUENT"
    NORMAL = "NORMAL"


class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.id'))
    profile_id = Column(String, ForeignKey('profiles.id'))
    merchant = Column(String, index=True)
    date = Column(String, index=True)
    total = Column(Integer, index=True)
    currency = Column(String, index=True)
    category = Column(String, index=True)
    description = Column(String, index=True)
    receipt = Column(String, index=True)
    expense_stage = Column(String, default=ExpenseStage.PENDING)
    expense_status = Column(String, default=ExpenseStatus.NORMAL)
    updatedAt = Column(DateTime, index=True)

    user = relationship("User", back_populates="expenses")
    profile = relationship("Profile", back_populates="expenses")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = str(uuid.uuid4().hex)


@event.listens_for(Expense, 'before_insert')
def set_date_before_insert(mapper, connection, target):
    # target.date = datetime.utcnow()
    target.updatedAt = datetime.utcnow()


@event.listens_for(Expense, 'before_update')
def set_updatedAt_before_update(mapper, connection, target):
    target.updatedAt = datetime.utcnow()
