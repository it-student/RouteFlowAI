"""
This module will define the API by defining routes and their allowed methods, etc.
"""
from pydantic import BaseModel, ConfigDict

# For data coming IN (POST requests)
class UserCreate(BaseModel):
    name: str | None
    family_name: str
    address: str
    gps_coordinates: str | None

# For data going OUT (Responses)
class UserResponse(BaseModel):
    id: int
    name: str | None
    family_name: str
    address: str

