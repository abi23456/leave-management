from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    department: str
    joining_date: date

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    total_leaves: int
    used_leaves: int

    class Config:
        from_attributes = True

class LeaveBase(BaseModel):
    start_date: date
    end_date: date

class LeaveCreate(LeaveBase):
    employee_id: int

class Leave(LeaveBase):
    id: int
    approved: Optional[bool]
    employee_id: int

    class Config:
        from_attributes = True

class LeaveDecision(BaseModel):
    approved: bool