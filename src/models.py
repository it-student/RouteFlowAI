"""
This module serves the schemas used within API interaction/communication
"""
from pydantic import BaseModel, ConfigDict, Field

# # # # # # # # # # USERS - Table related # # # # # # # # # #

# General Address class
# class Address(BaseModel):
#     street_name: str = Field(examples=["Musterstr."])
#     house_number: str = Field(5, gt=0, le=5, examples=["12"])
#     city: str = Field(examples=["Musterstadt"])
#     state: str = Field(examples=["Musterland"])
#     zip_code: str = Field(examples=["10969"])

# For data coming IN (POST, PUT requests)
class UserCreate(BaseModel):
    name: str | None = Field(examples=["Max"])
    family_name: str = Field(examples=["Mustermann"])
    address: str = Field(examples=["Musterstr. 12, 12345 Musterstadt"])
    gps_coordinates: str | None = Field(examples=[""])

# For data going OUT (Responses)
class UserResponse(BaseModel):
    id: int
    name: str | None
    family_name: str

    # Getting SQLAlchemy database object, read attributes directly
    model_config = ConfigDict(from_attributes=True)

# # # # # # # # # # End of USERS - Table related # # # # # # # # # #
# # # # # # # # # # SEARCHHISTORIES - Table related # # # # # # # # # #

# For data coming in (POST, PUT requests)
class SearchCreate(BaseModel):
    distance: float = Field(examples=[80.0]) # in km
    traveltime: int = Field(examples=[100]) # in Seconds (?)
    theme: str = Field(examples=["Bekannte Orte", ""])