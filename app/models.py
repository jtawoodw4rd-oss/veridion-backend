from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base

class Intent(Base):
    __tablename__ = "intents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    queries = relationship("Query", back_populates="intent", cascade="all, delete-orphan")
    briefs = relationship("Brief", back_populates="intent", cascade="all, delete-orphan")

class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    intent_id = Column(Integer, ForeignKey("intents.id"), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    intent = relationship("Intent", back_populates="queries")
    evidences = relationship("Evidence", back_populates="query", cascade="all, delete-orphan")

class Evidence(Base):
    __tablename__ = "evidences"

    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, ForeignKey("queries.id"), nullable=False)
    source = Column(String(512), nullable=True)
    content = Column(Text, nullable=False)
    rank = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    query = relationship("Query", back_populates="evidences")

class Brief(Base):
    __tablename__ = "briefs"

    id = Column(Integer, primary_key=True, index=True)
    intent_id = Column(Integer, ForeignKey("intents.id"), nullable=False)
    title = Column(String(512), nullable=False)
    summary = Column(Text, nullable=True)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())

    intent = relationship("Intent", back_populates="briefs")
