from pydantic import BaseModel
from typing import Optional


class OperatorCreate(BaseModel):
    name: str
    active: Optional[bool] = True
    load_limit: Optional[int] = 5


class OperatorRead(BaseModel):
    id: int
    name: str
    active: bool
    load_limit: int
    current_load: int

    class Config:
        from_attributes = True


class OperatorUpdate(BaseModel):
    active: Optional[bool] = None
    load_limit: Optional[int] = None


class SourceCreate(BaseModel):
    name: str


class SourceRead(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class WeightCreate(BaseModel):
    operator_id: int
    weight: int


class LeadRead(BaseModel):
    id: int
    external_id: str
    name: Optional[str] = None
    class Config:
        from_attributes = True


class ContactCreate(BaseModel):
    external_id: str  # lead id
    source_id: int
    message: Optional[str] = None


class ContactRead(BaseModel):
    id: int
    lead: LeadRead
    source: SourceRead
    operator: Optional[OperatorRead] = None
    message: Optional[str] = None
    status: str

    class Config:
        from_attributes = True
