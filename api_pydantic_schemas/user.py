from pydantic import BaseModel

class UserBase(BaseModel):
    user_phone : str
    user_password : str

class UserCreate(UserBase):
    ...

class User(UserBase):
    user_id : int

    class Config:
        orm_mode = True
