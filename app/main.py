from fastapi import FastAPI
from app.database import Base, engine
from app.routers import employees, leaves

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Leave Management API",
    description="A simple API to manage employees and their leave requests.",
    version="1.0.0"
)

app.include_router(employees.router, prefix="/employees", tags=["Employees"])
app.include_router(leaves.router, prefix="/leaves", tags=["Leaves"])