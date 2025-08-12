from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Leave)
def apply_leave(leave: schemas.LeaveCreate, db: Session = Depends(get_db)):
    try:
        return crud.apply_leave(db, leave)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{leave_id}", response_model=schemas.Leave)
def decide_leave(leave_id: int, decision: schemas.LeaveDecision, db: Session = Depends(get_db)):
    try:
        return crud.decide_leave(db, leave_id, decision.approved)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))