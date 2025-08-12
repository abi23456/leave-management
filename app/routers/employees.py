from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = crud.get_employee_by_email(db, employee.email)
    if db_employee:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_employee(db, employee)

@router.get("/{employee_id}/balance")
def get_leave_balance(employee_id: int, db: Session = Depends(get_db)):
    balance = crud.get_leave_balance(db, employee_id)
    if balance is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"employee_id": employee_id, "leave_balance": balance}