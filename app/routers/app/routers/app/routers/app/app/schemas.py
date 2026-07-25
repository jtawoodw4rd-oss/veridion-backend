app/schemas.py

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


# Intent schemas
class IntentBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None


class IntentCreate(IntentBase):
    pass


class IntentUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None


class IntentRead(IntentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Query schemas
class QueryBase(BaseModel):
    intent_id: int
    text: str
    metadata: Optional[str] = None


class QueryCreate(QueryBase):
    pass


class QueryUpdate(BaseModel):
    text: Optional[str] = None
    metadata: Optional[str] = None
    intent_id: Optional[int] = None


class QueryRead(QueryBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Evidence schemas
class EvidenceBase(BaseModel):
    query_id: int
    source: Optional[str] = None
    content: str
    score: Optional[int] = None


class EvidenceCreate(EvidenceBase):
    pass


class EvidenceUpdate(BaseModel):
    source: Optional[str] = None
    content: Optional[str] = None
    score: Optional[int] = None
    query_id: Optional[int] = None


class EvidenceRead(EvidenceBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Brief schemas
class BriefBase(BaseModel):
    intent_id: Optional[int] = None
    title: str
    summary: Optional[str] = None
    content: Optional[str] = None


class BriefCreate(BriefBase):
    pass


class BriefUpdate(BaseModel):
    intent_id: Optional[int] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None


class BriefRead(BriefBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# Collections / lists
class IntentList(BaseModel):
    items: List[IntentRead]


class QueryList(BaseModel):
    items: List[QueryRead]


class EvidenceList(BaseModel):
    items: List[EvidenceRead]


class BriefList(BaseModel):
    items: List[BriefRead]
