from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/briefs", tags=["briefs"])


@router.post("/", response_model=schemas.Brief, status_code=status.HTTP_201_CREATED)
def create_brief(brief_in: schemas.BriefCreate, db: Session = Depends(get_db)):
    brief = models.Brief(**brief_in.dict())
    db.add(brief)
    db.commit()
    db.refresh(brief)
    return brief


@router.get("/", response_model=List[schemas.Brief])
def list_briefs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    briefs = db.query(models.Brief).offset(skip).limit(limit).all()
    return briefs


@router.get("/{brief_id}", response_model=schemas.Brief)
def get_brief(brief_id: int, db: Session = Depends(get_db)):
    brief = db.query(models.Brief).filter(models.Brief.id == brief_id).first()
    if not brief:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brief not found")
    return brief


@router.delete("/{brief_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_brief(brief_id: int, db: Session = Depends(get_db)):
    brief = db.query(models.Brief).filter(models.Brief.id == brief_id).first()
    if not brief:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brief not found")
    db.delete(brief)
    db.commit()
    return None
