from sqlalchemy import Column, String, ForeignKey, DateTime, event
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime
import uuid


class NewsLetterList(Base):
    __tablename__ = 'news_letter_list'

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    createdAt = Column(DateTime, index=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = str(uuid.uuid4().hex)  


@event.listens_for(NewsLetterList, 'before_insert')
def set_date_before_insert(mapper, connection, target):
    target.createdAt = datetime.utcnow()
