from pydantic import BaseModel
import enum


class ContactBase(BaseModel):
    contact_name : str
    contact_surname : str
    contact_phone : str
    contact_type : enum.Enum
    contact_user_id : int

class ContactCreate(ContactBase):
    ...
    

class Contact(ContactBase):
    ...
    contact_id : int

    class Config:
        orm_mode = True