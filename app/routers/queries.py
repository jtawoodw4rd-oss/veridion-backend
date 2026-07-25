from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/queries", tags=["queries"])


@router.post("/", response_model=schemas.QueryOut, status_code=status.HTTP_201_CREATED)
def create_query(query_in: schemas.QueryCreate, db: Session = Depends(get_db)):
    query = models.Query(**query_in.dict())
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


@router.get("/", response_model=List[schemas.QueryOut])
def list_queries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    queries = db.query(models.Query).offset(skip).limit(limit).all()
    return queries


@router.get("/{query_id}", response_model=schemas.QueryOut)
def get_query(query_id: int, db: Session = Depends(get_db)):
    query = db.query(models.Query).filter(models.Query.id == query_id).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Query not found")
    return query


@router.delete("/{query_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_query(query_id: int, db: Session = Depends(get_db)):
    query = db.query(models.Query).filter(models.Query.id == query_id).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Query not found")
    db.delete(query)
    db.commit()
    return None
