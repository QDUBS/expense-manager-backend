from sqlalchemy import Column, String, DateTime, event
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime
from enum import Enum
import uuid


class UserType(str, Enum):
    STAFF = "STAFF"
    ADMIN = "ADMIN"
    BRANCH_UNIT_HEAD = "BRANCH_UNIT_HEAD"
    COMPLIANCE_INTERNAL_CONTROL = "COMPLIANCE_INTERNAL_CONTROL"
    DEPARTMENT_HEAD = "DEPARTMENT_HEAD"
    HEAD_OF_COMPLIANCE = "HEAD_OF_COMPLIANCE"
    FINANCE = "FINANCE"
    HEAD_OF_FINANCE = "HEAD_OF_FINANCE"
    BUSINESS_HEAD = "BUSINESS_HEAD"
    COUNTRY_HEAD = "COUNTRY_HEAD"


class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, index=True)
    email = Column(String, index=True)
    password = Column(String, index=True)
    userType = Column(String, default=UserType.STAFF)
    createdAt = Column(DateTime, index=True)

    profile = relationship("Profile", uselist=False, back_populates="user", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    support_tickets = relationship("SupportTicket", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = str(uuid.uuid4().hex)

    @property
    def profile_data(self):
        if self.profile is None:
            return None
        return self.profile


@event.listens_for(User, 'before_insert')
def set_date_before_insert(mapper, connection, target):
    target.createdAt = datetime.utcnow()
