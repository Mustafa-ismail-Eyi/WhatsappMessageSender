#! python3

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
import enum
from parser_templates import get_parser
from datetime import datetime
import sys
from db import get_db as db_get_db

DB_NAME = "./sql_app.db"

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_NAME}"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()



# this relation is like
"""
Contact         <-->    message         <-->  user
        crm                             usr
    contact_recieved_message       user_sent_message
    
"""
class ContactsType(enum.Enum):
    person = "Person"
    group = "Group"

class MessageType(enum.Enum):
    holiday = "Holiday"
    religional_holiday = "Religional Holiday"
    daily = "Daily"
    weekly = "Weekly"
    monthly = "Monthly"

class Contacts(Base):
    __tablename__ = "contacts"

    contact_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    contact_name = Column(String, index=True)
    contact_surname = Column(String, index=True, nullable=True)
    contact_phone = Column(String, index=True, unique = True)
    is_active = Column(Boolean, default=True)
    contact_type = Column(Enum(ContactsType))

    crm = relationship("ContactRecievedMessage", back_populates = "contact",cascade="all, delete")
    


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    user_password = Column(String, index=True)
    user_phone = Column(String, index=True)
    
    message = relationship("UserSentMessage", back_populates="user",cascade="all, delete" )


class Messages(Base):
    __tablename__ = "messages"
    
    message_id = Column(Integer, primary_key = True, index=True)
    message_body = Column(String)
    message_type = Column(Enum(MessageType))
   

    user_sent_messages = relationship("UserSentMessage", back_populates = "message",passive_deletes=True,)
    contact_recieved_messages = relationship("ContactRecievedMessage", back_populates = "recieved_message",passive_deletes=True,)


class UserSentMessage(Base):
    __tablename__ = "user_sent_message"

    usm_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.message_id",ondelete="CASCADE"), ) 
    user_id = Column(Integer, ForeignKey("user.user_id",ondelete="CASCADE"), ) 
    message_send_time = Column(DateTime, default=datetime.utcnow)
    
    message = relationship("Messages", back_populates = "user_sent_messages")
    user = relationship("User", back_populates = "message")

class ContactRecievedMessage(Base):
    __tablename__ = "contact_recieved_message"

    crm_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    usm_id = Column(Integer, ForeignKey("messages.message_id",ondelete="CASCADE"), )
    contact_id = Column(Integer, ForeignKey("contacts.contact_id",ondelete="CASCADE"), ) 

    recieved_message = relationship("Messages", back_populates="contact_recieved_messages")
    contact = relationship("Contacts", back_populates="crm",)
    
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == '__main__':

    args = get_parser()

    if args.command == "populate" or args.command.startswith('p'):
        
        # Base metadata for DDL
        #Base.metadata.create_all(bind=engine)
        # get_db returns an iterator thats why need use next()
        #db_gen = get_db()
        db_gen = db_get_db()
        db = next(db_gen)

        # some data
        user =[ User(
            user_password = "12345",
            user_phone = "+905445056671"
        )
        ]
        contacts = [
            Contacts(
            contact_name = "grup1",
            contact_surname = "",
            contact_phone = "LVlngjI61ef5pIMhTSmIf6",
            contact_type = ContactsType.group
            ),
            Contacts(
            contact_name = "annem",
            contact_surname = "annem1",
            contact_phone = "+905511886413",
            contact_type = ContactsType.person
            ),
        ]


        messages = [ 
            Messages(
            message_body = "Hello World!",
            message_type = MessageType.daily,
            )
        ]
        # adding all the data and commiting because auto commit is turned off
        db.add_all(user + messages + contacts)
        db.commit()
    
    # deleting the database
    elif args.command == "delete" or args.command.startswith('d'):
        if os.path.exists(f"{DB_NAME}"):
            os.remove(f"{DB_NAME}")
        else:
            print("Database does not exists")
    else:
        print("unkown command")
    