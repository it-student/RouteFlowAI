"""
This module will define the API by defining routes and their allowed methods, etc.
"""
from fastapi import HTTPException
import db.schemas as schemas
import models
from db.db_operations import engine, SessionLocal
from sqlalchemy.orm import Session


def users_fetchall(db: Session):
    """
    get all users
    :rtype: list[type[User]]
    :param db: Session object for database access
    :return users: All users existing.
    """
    users = db.query(schemas.User).all()
    return users

def users_get(user_id: int, db: Session):
    """
    get a user by its id
    :param user_id: the unique id of the user
    :param db: Session object for database access
    :return:
    """
    user = db.query(schemas.User).filter(schemas.User.id == user_id).first()
    return user

def users_create(user: models.UserCreate, db: Session):
    """
    create a new user
    :param user: UserCreate object
    :param db: Session object for database access
    :return user: UserResponse object
    """
    new_user = schemas.User(name = user.name,
                            family_name = user.family_name,
                            address = user.address,
                            gps_coordinates = user.gps_coordinates)
    db.add(new_user)
    db.commit()
    return new_user

