from sqlalchemy import Column, Integer, VARCHAR, DATE

from base import BaseModel


class Messages(BaseModel):
    __tablename__ = 'messages'

    id = Column(primary_key=True)
    message_id = Column
    chat_id = Column

