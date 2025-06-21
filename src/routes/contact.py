from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.schemas.contact import ContactCreate, ContactResponse
from src.database.db import get_db
from src.auth.auth import get_current_user
from src.database.models import User
from src.repository import contacts as repository_contacts

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.get("/", response_model=List[ContactResponse])
async def get_contacts(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    contacts = await repository_contacts.get_contacts_by_user(current_user.id, db)
    return contacts

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(contact: ContactCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    new_contact = await repository_contacts.create_contact(user_id=current_user.id, contact=contact, db=db)
    return new_contact