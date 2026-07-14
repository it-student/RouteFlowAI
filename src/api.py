"""
This module will define the API by defining routes and their allowed methods, etc.
"""
import db.schemas as schemas
import models
from sqlalchemy.orm import Session

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

def users_get(user_id: int, db: Session):
    """
    get a user by its id
    :param user_id: the unique id of the user
    :param db: Session object for database access
    :return:
    """
    user = db.query(schemas.User).filter(schemas.User.id == user_id).first()
    return user

def users_update(user_id: int, user: models.UserCreate, db: Session):
    """
    Get user by its id and update it with new data.
    :param user_id: unique id of the user
    :param db: Session object for database access
    :returndb_user: UserResponse object:
    """
    db_user = db.query(schemas.User).filter(schemas.User.id == user_id).first()
    db_user.name = user.name if user.name is not None else db_user.name
    db_user.family_name = user.family_name if user.family_name is not None else db_user.family_name
    db_user.address = user.address if user.address is not None else db_user.address
    db_user.gps_coordinates = user.gps_coordinates if user.gps_coordinates is not None else user.gps_coordinates
    db.commit()
    return db_user

def users_delete(user_id: int, db: Session):
    """
    delete a user by its id
    :param user_id: unique id of the user
    :param db: Session object for database access
    :return user: UserResponse object:
    """
    db_user = db.query(schemas.User).filter(schemas.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user

def users_fetchall(db: Session):
    """
    get all users
    :rtype: list[type[User]]
    :param db: Session object for database access
    :return users: All users existing.
    """
    users = db.query(schemas.User).all()
    return users

