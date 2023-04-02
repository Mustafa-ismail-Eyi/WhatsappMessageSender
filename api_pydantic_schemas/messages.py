from db.db_models import MessageType
import pydantic

class MessageBase(pydantic.BaseModel):
    message_body : str
    message_type : MessageType

class Message(MessageBase):
    ...
    class Config:
        orm_mode = True
