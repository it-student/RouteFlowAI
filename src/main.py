"""
starting the fastAPI app.
"""
from typing import Annotated, List

from fastapi import FastAPI, Depends, HTTPException, Path, Body
from db.db_operations import engine, SessionLocal
from sqlalchemy.orm import Session
import db.schemas as models
import models as schemas
from api import users_fetchall, users_create, users_get, users_update, users_delete



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

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
def hello_world():
    return {"message": "Hello World"}

@app.get("/users/", response_model=List[schemas.UserResponse])
def read_all_users(db: db_dependency):
    """
    - Get all users, if no user_id given, user with user_id otherwise
    - :return users: list of UserResponse objects:
    """
    users = users_fetchall(db)
    if not users or len(users) == 0:
        raise HTTPException(status_code=404, detail="Users not found")
    return users


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(db: db_dependency,
              user_id: int = Path(
                  description="The unique ID of the user",
                  examples=[40451]  # Populates the path input field
              )):
    """
    - Retrieves a user by its ID.
    - :param user_id: unique id of the user (int)
    - :return user: UserResponse object:
    """
    user = users_get(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: db_dependency):
    """
    - create a new user
    - :param user: UserCreate object
    - :return user: UserResponse object
    """
    return users_create(user=user, db=db)

@app.put("/users/{user_id}", response_model=schemas.UserResponse)
async def update_user(db: db_dependency,
                      user_id: int = Path(
                          description="The unique ID of the user",
                          examples=[40451]
                      ),

                      user: schemas.UserCreate = Body(
                          description="UserCreate object",
                          examples=[
                              {"name": "Max",
                               "family_name": "Mustermann",
                               "address": "Musterstr. 12, 12345 Musterstadt",
                               "gps_coordinates": ""}
                          ])):
    """
    - update a user, finding it by its ID.
    - :param user_id: unique id of the user (int)
    - :return user: UserResponse object:
    """
    return users_update(db=db, user_id=user_id, user=user)

@app.delete("/users/{user_id}", response_model=schemas.UserResponse)
async def delete_user(db: db_dependency,
                      user_id: int = Path(
                          description="The unique ID of the user",
                          examples=[40451]  # Populates the path input field
                      )):
    """
    - delete a user by its ID.
    - :param user_id: unique id of the user (int)
    - :return user: UserResponse object:
    """
    return users_delete(db=db, user_id=user_id)

