from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app import models, schemas
from datetime import date

def get_employee(db: Session, employee_id: int):
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()

def get_employee_by_email(db: Session, email: str):
    return db.query(models.Employee).filter(models.Employee.email == email).first()

def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_employee = models.Employee(
        name=employee.name,
        email=employee.email,
        department=employee.department,
        joining_date=employee.joining_date,
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def get_leave_balance(db: Session, employee_id: int):
    employee = get_employee(db, employee_id)
    if not employee:
        return None
    return employee.total_leaves - employee.used_leaves

def overlapping_leaves(db: Session, employee_id: int, start: date, end: date):
    return db.query(models.Leave).filter(
        models.Leave.employee_id == employee_id,
        or_(
            and_(models.Leave.start_date <= start, models.Leave.end_date >= start),
            and_(models.Leave.start_date <= end, models.Leave.end_date >= end),
            and_(models.Leave.start_date >= start, models.Leave.end_date <= end),
        ),
        models.Leave.approved != False  # Only consider pending/approved
    ).first()

def apply_leave(db: Session, leave: schemas.LeaveCreate):
    employee = get_employee(db, leave.employee_id)
    if not employee:
        raise ValueError("Employee not found")

    if leave.start_date < employee.joining_date:
        raise ValueError("Cannot apply leave before joining date")

    if leave.end_date < leave.start_date:
        raise ValueError("End date cannot be before start date")

    days = (leave.end_date - leave.start_date).days + 1
    balance = get_leave_balance(db, leave.employee_id)
    if days > balance:
        raise ValueError("Not enough leave balance")

    if overlapping_leaves(db, leave.employee_id, leave.start_date, leave.end_date):
        raise ValueError("Overlapping leave request exists")

    db_leave = models.Leave(
        start_date=leave.start_date,
        end_date=leave.end_date,
        employee_id=leave.employee_id,
        approved=None  # Pending
    )
    db.add(db_leave)
    db.commit()
    db.refresh(db_leave)
    return db_leave

def decide_leave(db: Session, leave_id: int, approved: bool):
    leave = db.query(models.Leave).filter(models.Leave.id == leave_id).first()
    if not leave:
        raise ValueError("Leave request not found")
    if leave.approved is not None:
        raise ValueError("Leave already processed")
    if approved:
        days = (leave.end_date - leave.start_date).days + 1
        employee = get_employee(db, leave.employee_id)
        if days > (employee.total_leaves - employee.used_leaves):
            raise ValueError("Not enough leave balance at approval time")
        employee.used_leaves += days
    leave.approved = approved
    db.commit()
    db.refresh(leave)
    return leave