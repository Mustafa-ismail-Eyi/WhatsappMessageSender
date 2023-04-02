from typing import List
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from db import engine, get_db
from api_pydantic_schemas.user import User, UserCreate
from .utils.user_utils import create_user, get_user


user_router = APIRouter()


@user_router.post("/user_register/")
async def user_register(
    user : UserCreate,
    db: Session = Depends(get_db)
):

    create_user(user = user, db = db)

@user_router.get("/user/{user_phone}/{user_password}", response_model=User)
async def get_user_by_id(
    user_phone: str,
    user_password: str,
    db: Session=Depends(get_db)
):
    db_user = get_user(user_phone=user_phone, user_password=user_password,db=db)
    if not db_user:
        raise HTTPException(status_code=404, detail="The user can not be found")
    return db_user
