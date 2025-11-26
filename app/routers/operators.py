from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app import schemas, models
from app.db import get_db

router = APIRouter(prefix="/operators", tags=["operators"])

@router.post("", response_model=schemas.OperatorRead)
def create_operator(op_in: schemas.OperatorCreate, db: Session = Depends(get_db)):
    op = models.Operator(
        name=op_in.name,
        active=op_in.active,
        load_limit=op_in.load_limit,
        current_load=0
    )
    db.add(op)
    db.commit()
    db.refresh(op)
    return op

@router.get("", response_model=List[schemas.OperatorRead])
def list_operators(db: Session = Depends(get_db)):
    ops = db.query(models.Operator).all()
    return ops

@router.patch("/{operator_id}", response_model=schemas.OperatorRead)
def update_operator(operator_id: int, op_update: schemas.OperatorUpdate, db: Session = Depends(get_db)):
    op = db.query(models.Operator).get(operator_id)
    if not op:
        raise HTTPException(status_code=404, detail="Operator not found")
    if op_update.active is not None:
        op.active = op_update.active
    if op_update.load_limit is not None:
        op.load_limit = op_update.load_limit
    db.add(op)
    db.commit()
    db.refresh(op)
    return op
