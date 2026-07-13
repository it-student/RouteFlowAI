"""
starting the fastAPI app.
"""
from fastapi import FastAPI, Depends, HTTPException
from db.db_operations import engine, SessionLocal
from sqlalchemy.orm import Session
import db.schemas as models

def get_db():
    """
    get db session
    :yield: the db session:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

# Creates the tables in Postgres if they don't exist yet
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def hello_world():
    return {"message": "Hello World"}

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    """
    get all users
    :param db:
    :return: All users existing.
    """
    users = db.query(models.User).all()
    return users

# @app.post("/users/")
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     pass
