from sqlalchemy.orm import Session
from db.db_models import User
from api_pydantic_schemas.user import UserCreate

def create_user(
    db:Session, user : UserCreate
):
    #TODO user existance will be check on api side
    if not db.query(User).filter(User.user_phone == user.user_phone).first():
        db_user = User(user_phone=user.user_phone, user_password=user.user_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

def get_user(
    db: Session, user_phone : str, user_password : str 
):
    return db.query(User).filter(User.user_phone == user_phone, User.user_password == user_password).first()    
