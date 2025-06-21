from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import date, timedelta
from src.database import models
from src.schemas.contact import ContactCreate, ContactUpdate


def create_contact(db: Session, contact: ContactCreate, user_id: int):
    db_contact = models.Contact(**contact.dict(), owner_id=user_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact



def get_contact(db: Session, contact_id: int, user_id: int):
    return db.query(models.Contact).filter(
        models.Contact.id == contact_id,
        models.Contact.owner_id == user_id
    ).first()

def get_contacts(db: Session, user_id: int, skip: int = 0, limit: int =100):
    return db.query(models.Contact).filter(models.Contact.owner_id == user_id).offset(skip).limit(limit).all()

def update_contact(db: Session, contact_id: int, updated: ContactUpdate, user_id: int):
    contact = get_contact(db, contact_id, user_id)
    if contact:
        for key, value in updated.dict().items():
            setattr(contact, key, value)
        db.commit()
        db.refresh(contact)
    return contact

def delete_contact(db: Session, contact_id: int, user_id: int):
    contact = get_contact(db, contact_id, user_id)
    if contact:
        db.delete(contact)
        db.commit()
    return contact

def search_contacts(db: Session, query: str, user_id:int):
    return db.query(models.Contact).filter(
        models.Contact.owner_id == user_id,
        or_(
            models.Contact.first_name.ilike(f"%{query}%"),
            models.Contact.last_name.ilike(f"%{query}%"),
            models.Contact.email.ilike(f"%{query}%")
        )
    ).all()

def get_upcoming_birthdays(db: Session, user_id: int):
    today = date.today()
    next_week = today + timedelta(days=7)
    return db.query(models.Contact).filter(
        models.Contact.owner_id == user_id,
        models.Contact.birthday.between(today, next_week)
    ).all()
