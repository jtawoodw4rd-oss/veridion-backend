# app/routers/evidence.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models
from ..database import get_db

router = APIRouter(prefix="/evidence", tags=["evidence"])

@router.post("/", response_model=schemas.EvidenceOut)
def create_evidence(evidence: schemas.EvidenceCreate, db: Session = Depends(get_db)):
    db_evidence = models.Evidence(**evidence.dict())
    db.add(db_evidence)
    db.commit()
    db.refresh(db_evidence)
    return db_evidence

@router.get("/", response_model=List[schemas.EvidenceOut])
def list_evidence(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    evidence = db.query(models.Evidence).offset(skip).limit(limit).all()
    return evidence

@router.get("/{evidence_id}", response_model=schemas.EvidenceOut)
def get_evidence(evidence_id: int, db: Session = Depends(get_db)):
    evidence = db.query(models.Evidence).filter(models.Evidence.id == evidence_id).first()
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")
    return evidence

@router.delete("/{evidence_id}")
def delete_evidence(evidence_id: int, db: Session = Depends(get_db)):
    evidence = db.query(models.Evidence).filter(models.Evidence.id == evidence_id).first()
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")
    db.delete(evidence)
    db.commit()
    return {"message": "Evidence deleted"}
