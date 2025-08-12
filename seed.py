from app import models, database

models.Base.metadata.create_all(bind=database.engine)

db = database.SessionLocal()
db.add(models.Employee(name="Abishek", department="IT"))
db.commit()
db.close()
