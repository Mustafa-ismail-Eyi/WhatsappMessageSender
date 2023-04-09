from sqlalchemy.orm import Session
from db.db_models import Messages
from api_pydantic_schemas.messages import Message


def create_message(
    db:Session, message : Message
):
    db_message = Messages(message_body = message.message_body, message_type = message.message_type)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)


def get_message_by_id(
    db:Session, message_id: int
):
    #TODO user existance will be check on api side
    if db_message := db.query(Messages).filter(Messages.message_id == message_id).first():
        return db_message
    return None

def delete_message_by_id(db:Session, message_id: int):
    if db_message := db.query(Messages).get(message_id):        
        db.delete(db_message)
        db.commit()
        return True
    return False