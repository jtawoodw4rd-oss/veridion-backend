from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/intents", tags=["intents"])

@router.post("/", response_model=schemas.Intent)
def create_intent(intent: schemas.IntentCreate, db: Session = Depends(get_db)):
    db_intent = models.Intent(name=intent.name, description=intent.description)
    db.add(db_intent)
    db.commit()
    db.refresh(db_intent)
    return db_intent

@router.get("/", response_model=List[schemas.Intent])
def list_intents(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.Intent).offset(skip).limit(limit).all()

@router.get("/{intent_id}", response_model=schemas.Intent)
def get_intent(intent_id: int, db: Session = Depends(get_db)):
    intent = db.query(models.Intent).filter(models.Intent.id == intent_id).first()
    if not intent:
        raise HTTPException(status_code=404, detail="Intent not found")
    return intent

@router.delete("/{intent_id}", response_model=schemas.Intent)
def delete_intent(intent_id: int, db: Session = Depends(get_db)):
    intent = db.query(models.Intent).filter(models.Intent.id == intent_id).first()
    if not intent:
        raise HTTPException(status_code=404, detail="Intent not found")
    db.delete(intent)
    db.commit()
    return intent
