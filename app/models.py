from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    department = Column(String, nullable=False)
    joining_date = Column(Date, nullable=False)
    total_leaves = Column(Integer, default=20)
    used_leaves = Column(Integer, default=0)

    leaves = relationship("Leave", back_populates="employee", cascade="all, delete-orphan")

class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    approved = Column(Boolean, default=None, nullable=True)  # None=pending, True=approved, False=rejected

    employee_id = Column(Integer, ForeignKey("employees.id"))
    employee = relationship("Employee", back_populates="leaves")