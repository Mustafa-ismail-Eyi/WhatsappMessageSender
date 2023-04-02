from sqlalchemy.orm import Session
from db.db_models import Contacts
from api_pydantic_schemas.contacts import ContactCreate,Contact

def create_contact(
    db: Session, contact: ContactCreate
):
    if not db.query(Contacts).filter(Contacts.contact_phone == contact.contact_phone).first():
        db_contact = Contacts( contact_user_id=contact.contact_user_id,
                            contact_name=contact.contact_name,
                            contact_surname=contact.contact_surname,
                            contact_phone=contact.contact_phone,
                            contact_type =contact.contact_type)
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)

def get_contact(
    db: Session, user_id,contact_phone: str
):
    return db.query(Contacts).filter(Contact.contact_phone == contact_phone, Contact.contact_user_id == user_id).first()    


def get_contacts(
    db: Session, user_id
):
    return db.query(Contacts).filter(Contacts.contact_user_id == user_id).all()

