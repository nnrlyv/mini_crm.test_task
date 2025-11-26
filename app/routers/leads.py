from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from app import schemas, models
from app.db import get_db

router = APIRouter(prefix="/leads", tags=["leads"])

@router.get("", response_model=List[schemas.LeadRead])
def list_leads(db: Session = Depends(get_db)):
    leads = db.query(models.Lead).all()
    return leads

@router.get("/{lead_id}/contacts")
def lead_contacts(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(models.Lead).get(lead_id)
    if not lead:
        return {"contacts": []}
    # return raw contacts data (simple)
    return {"contacts": [ { "id": c.id, "source_id": c.source_id, "operator_id": c.operator_id, "message": c.message, "status": c.status } for c in lead.contacts ]}
