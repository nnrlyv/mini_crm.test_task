from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app import schemas, models
from app.db import get_db

router = APIRouter(prefix="/sources", tags=["sources"])

@router.post("", response_model=schemas.SourceRead)
def create_source(s_in: schemas.SourceCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Source).filter(models.Source.name == s_in.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Source with this name already exists")
    s = models.Source(name=s_in.name)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

@router.get("", response_model=List[schemas.SourceRead])
def list_sources(db: Session = Depends(get_db)):
    return db.query(models.Source).all()

@router.post("/{source_id}/weights", response_model=dict)
def add_weight(source_id: int, w_in: schemas.WeightCreate, db: Session = Depends(get_db)):
    source = db.query(models.Source).get(source_id)
    if not source:
        raise HTTPException(status_code=404, detail="Source not found")
    op = db.query(models.Operator).get(w_in.operator_id)
    if not op:
        raise HTTPException(status_code=404, detail="Operator not found")

    existing = db.query(models.OperatorSourceWeight).filter(
        models.OperatorSourceWeight.source_id == source_id,
        models.OperatorSourceWeight.operator_id == w_in.operator_id
    ).first()
    if existing:
        existing.weight = w_in.weight
        db.add(existing)
    else:
        nw = models.OperatorSourceWeight(operator_id=w_in.operator_id, source_id=source_id, weight=w_in.weight)
        db.add(nw)
    db.commit()
    return {"ok": True}
