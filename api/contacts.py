from typing import List
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from db import engine, get_db
from api_pydantic_schemas.contacts import ContactCreate, Contact
from api.utils.contacts_utils import create_contact, get_contact, get_contacts

contact_router = APIRouter()



@contact_router.post("/create_contact/")
async def contact_register(
    contact : ContactCreate,
    db: Session = Depends(get_db)
):

    create_contact(contact = contact, db = db )

@contact_router.get("/contact/{user_id}/{contact_phone}", response_model=Contact)
async def get_contact_by_phone(
    user_id: int,
    contact_phone : str,
    db: Session=Depends(get_db)
):
    db_contact = get_contact(db, user_id, contact_phone)
    if not db_contact:
        raise HTTPException(status_code=404, detail="The contact can not be found")
    return db_contact

@contact_router.get("/contacts/{user_id}", response_model=List[Contact])
async def get_current_user_contacts(
    user_id: int,
    db: Session=Depends(get_db)
):
    db_contact = get_contacts(db, user_id)
    if not db_contact:
        raise HTTPException(status_code=404, detail="The contacts can not be found")
    return db_contact
