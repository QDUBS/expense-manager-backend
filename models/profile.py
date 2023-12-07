from sqlalchemy import Column, ForeignKey, String, DateTime, event
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime
import uuid


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.id'))
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    mobile_number = Column(String, index=True)
    department = Column(String, index=True)
    role = Column(String, index=True)
    staff_id = Column(String, index=True)
    photo = Column(String, index=True)
    createdAt = Column(DateTime, index=True)
    updatedAt = Column(DateTime, index=True)

    user = relationship("User", back_populates="profile")
    expenses = relationship("Expense", back_populates="profile")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = str(uuid.uuid4().hex) 

@event.listens_for(Profile, 'before_insert')
def set_date_before_insert(mapper, connection, target):
    target.createdAt = datetime.utcnow()
    target.updatedAt = datetime.utcnow()


@event.listens_for(Profile, 'before_update')
def set_updatedAt_before_update(mapper, connection, target):
    target.updatedAt = datetime.utcnow()
