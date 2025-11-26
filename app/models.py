from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db import Base

class Operator(Base):
    __tablename__ = "operators"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    load_limit = Column(Integer, default=5)
    current_load = Column(Integer, default=0)

    # relationship to weights and contacts
    weights = relationship("OperatorSourceWeight", back_populates="operator", cascade="all, delete-orphan")
    contacts = relationship("Contact", back_populates="operator")

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    weights = relationship("OperatorSourceWeight", back_populates="source", cascade="all, delete-orphan")
    contacts = relationship("Contact", back_populates="source")

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, index=True, nullable=False)  # phone/email/uuid etc
    name = Column(String, nullable=True)

    contacts = relationship("Contact", back_populates="lead")

    __table_args__ = (
        UniqueConstraint("external_id", name="uq_lead_external_id"),
    )

class OperatorSourceWeight(Base):
    __tablename__ = "operator_source_weights"

    id = Column(Integer, primary_key=True, index=True)
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=False)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    weight = Column(Integer, nullable=False, default=1)

    operator = relationship("Operator", back_populates="weights")
    source = relationship("Source", back_populates="weights")

    __table_args__ = (
        UniqueConstraint("operator_id", "source_id", name="uq_operator_source"),
    )

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    operator_id = Column(Integer, ForeignKey("operators.id"), nullable=True)
    message = Column(Text, nullable=True)
    status = Column(String, default="open")  # optional: open / closed

    lead = relationship("Lead", back_populates="contacts")
    source = relationship("Source", back_populates="contacts")
    operator = relationship("Operator", back_populates="contacts")
