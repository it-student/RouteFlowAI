"""
This module will define the API by defining routes and their allowed methods, etc.
"""
from typing import Annotated, List
import db.schemas as schemas
import models
from db.db_operations import SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status


router = APIRouter()

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

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/")
def hello_world():
    return {"message": "Hello World"}

@router.get("/users/", response_model=List[models.UserResponse])
def read_all_users(db: db_dependency):
    """
    - Get all users.
    - :return users: list of UserResponse objects:
    """
    users = db.query(schemas.User).all()
    if not users or len(users) == 0:
        raise HTTPException(status_code=404, detail="Users not found")
    return users


@router.get("/users/{user_id}", response_model=models.UserResponse)
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
    user = db.query(schemas.User).filter(schemas.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users/", response_model=models.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      user: models.UserCreate = Body(
                          description="UserCreate object",
                      )):
    """
    - create a new user
    - :param user: UserCreate object
    - :return db_user: UserResponse object
    """
    new_user = schemas.User(name=user.name if user.name is not None else '',
                            family_name=user.family_name,
                            address=user.address,
                            gps_coordinates=user.gps_coordinates if user.gps_coordinates is not None else '')
    db.add(new_user)
    db.commit()
    return new_user

@router.put("/users/{user_id}", response_model=models.UserResponse)
async def update_user(db: db_dependency,
                      user_id: Annotated[int,Path(
                          description="The unique ID of the user",
                          examples=[40451]
                      )],

                      user: Annotated[models.UserCreate, Body(
                          description="UserCreate object"
                      )]
    ):
    """
    - update a user, finding it by its ID.
    - :param user_id: unique id of the user (int)
    - :return user: UserResponse object:
    """
    db_user = db.get(schemas.User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get only UserCreate Fields, that actually got send within the request
    user_update = user.model_dump(exclude_unset=True)

    # Map through the dictionary to update the database entry
    for key, value in user_update.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user

@router.delete("/users/{user_id}", response_model=models.UserResponse)
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
    db_user = db.get(schemas.User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user