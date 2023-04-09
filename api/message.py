from typing import List
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db import engine, get_db
from api_pydantic_schemas.messages import Message
from api.utils.message_utils import create_message, delete_message_by_id, get_message_by_id


message_router = APIRouter()

@message_router.post("/message_create")
async def create_messsage(
    message : Message,
    db: Session = Depends(get_db)
):

    create_message(message=message, db=db)

@message_router.get("/message/{message_id}", response_model=Message)
async def get_message(
    message_id: int,
    db: Session=Depends(get_db)
):
    db_message = get_message_by_id(db,message_id)
    if not db_message:
        raise HTTPException(status_code=404, detail="The message can not be found")
    return db_message

@message_router.delete("/message/{message_id}")
async def delete_message(
    message_id : int,
    db: Session=Depends(get_db)
):
    is_message_deleted = delete_message_by_id(db, message_id)
    if is_message_deleted:
        return JSONResponse("Message deleted successfully")