from typing import List
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from db import engine, get_db
from api_pydantic_schemas.messages import Message
from utils.message_utils import create_message, get_message_by_id


message_router = APIRouter()

@message_router.post("/message_create")
async def user_register(
    message : Message,
    db: Session = Depends(get_db)
):

    create_message(message=message, db=db)

@message_router.get("/message/{message_id}", response_model=Message)
async def get_user_by_id(
    message_id: int,
    db: Session=Depends(get_db)
):
    db_message = get_message_by_id(db,message_id)
    if not db_message:
        raise HTTPException(status_code=404, detail="The message can not be found")
    return db_message