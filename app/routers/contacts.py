from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app import schemas, models
from app.db import get_db
from app.services import allocation

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.post("", response_model=schemas.ContactRead)
def create_contact(c_in: schemas.ContactCreate, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).filter(models.Lead.external_id == c_in.external_id).first()
    if not lead:
        lead = models.Lead(external_id=c_in.external_id)
        db.add(lead)
        db.commit()
        db.refresh(lead)

    source = db.query(models.Source).get(c_in.source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")


    assigned_op = allocation.allocate_operator(db, source.id)
    contact = models.Contact(
        lead_id=lead.id,
        source_id=source.id,
        operator_id=assigned_op.id if assigned_op else None,
        message=c_in.message
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)

    op = None
    if contact.operator_id:
        op = db.query(models.Operator).get(contact.operator_id)

    return schemas.ContactRead.from_orm(contact)


@router.get("", response_model=List[schemas.ContactRead])
def list_contacts(db: Session = Depends(get_db)):
    contacts = db.query(models.Contact).all()
    return contacts
