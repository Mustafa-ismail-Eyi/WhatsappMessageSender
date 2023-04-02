from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, DateTime
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from . import Base




# this relation is like
"""
  contact_user_id < --------------- user_id

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
    contact_user_id = Column(Integer, ForeignKey("user.user_id", ondelete="CASCADE"),)
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
    contacts = relationship('Contacts', backref='user')

class Messages(Base):
    __tablename__ = "messages"
    
    message_id = Column(Integer, primary_key = True, index=True, autoincrement=True)
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
