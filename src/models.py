"""
This module serves the schemas used within API interaction/communication
"""
from datetime import datetime

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

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Max",
                    "family_name": "Mustermann",
                    "address": "Musterstr. 12, 12345 Musterstadt",
                    "gps_coordinates": ""
                }
            ]
        }
    }

# For data going OUT (Responses)
class UserResponse(BaseModel):
    id: int
    name: str | None
    family_name: str
    address: str

    # Getting SQLAlchemy database object, read attributes directly
    model_config = ConfigDict(from_attributes=True)

# # # # # # # # # # End of USERS - Table related # # # # # # # # # #
# # # # # # # # # # SEARCHHISTORIES - Table related # # # # # # # # # #

# For data coming in (POST, PUT requests)
class SearchCreate(BaseModel):
    starting_point: str = Field(examples=["Musterstarsse 1, 12345 Musterstadt"])
    distance: float | int = Field(examples=[80.0]) # in km
    traveltime: int = Field(examples=[100]) # in Minutes (?)
    theme: str = Field(examples=["Bekannte Orte", "Noch nicht besuchte Orte"])
    transport_type: str = Field(examples=["Motorcycle", "public transport", "Bicycle"])
    group_size: int = Field(default=1, examples=[5], ge=1, lt=30)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "starting_point": "Musterstarsse 1, 12345 Musterstadt",
                    "distance": 80.0,
                    "traveltime": 100,
                    "theme": "Neue Orte entdecken",
                    "transport_type": "Motorcycle",
                    "group_size": 1
                }
            ]
        }
    }

# For data going out (Response)
class SearchResponse(BaseModel):
    id: int = Field(examples=[5], ge=1)
    starting_point: str | None = Field(examples=["Musterstarsse 1, 12345 Musterstadt"])
    distance: float = Field(examples=[80.0])
    traveltime: int = Field(examples=[100])  # in Minutes
    theme: str = Field(examples=["Bekannte Orte", "Noch nicht besuchte Orte"])
    transport_type: str = Field(examples=["Motorcycle", "public transport", "Bicycle"])
    group_size: int = Field(default=1, examples=[5], ge=1, lt=30)
    user_id: int = Field(examples=[5], ge=1)

    # Getting SQLAlchemy database object, read attributes directly
    model_config = ConfigDict(from_attributes=True)

# # # # # # # # # # End of SEARCHHISTORIES - Table related # # # # # # # # # #
# # # # # # # # # # SUGGESTIONS - Table related # # # # # # # # # #

# For data coming in (POST, PUT requests)
class SuggestionCreate(BaseModel):
    title: str = Field(examples=["Trip to new lands"])
    description: str = Field(examples=["A Trip to unknown territory, for an adventurous day!"])
    sug_transport_type: str = Field(examples=["Motorcycle", "public transport", "Bicycle"])
    destination_coordinates: str | None = Field(examples=[""])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "description": "A Trip to unknown territory, for an adventurous day!",
                    "destination_coordinates": "",
                    "sug_transport_type": "Motorcycle",
                    "title": "Trip to new lands"
                },
                {
                    "description": "A Trip mixed with known and unknown grounds!",
                    "destination_coordinates": "",
                    "sug_transport_type": "Motorcycle",
                    "title": "A mix of both"
                },
            ]
        }
    }

class SuggestionList(BaseModel):
    suggestions: list[SuggestionCreate]

# For data going out (Responses)
class SuggestionResponse(BaseModel):
    id: int = Field(examples=[5], ge=1)
    title: str = Field(examples=["Trip to new lands"])
    description: str = Field(examples=["A Trip to unknown territory, for an adventurous day!"])
    sug_transport_type: str = Field(examples=["Motorcycle", "public transport", "Bicycle"])
    destination_coordinates: str | None = Field(examples=[""])
    user_id: int = Field(examples=[5], ge=1)
    history_id: int = Field(examples=[5], ge=1)

    # Getting SQLAlchemy database object, read attributes directly
    model_config = ConfigDict(from_attributes=True)

# # # # # # # # # # End of SUGGESTIONS - Table related # # # # # # # # # #
# # # # # # # # # # TRIPPLAN - Table related # # # # # # # # # #

# For data coming in (POST, PUT request)
class TripplanCreate(BaseModel):
    title: str = Field(examples=["Trip to new lands"])
    start_time: datetime = Field(examples=[datetime(1900, 1, 1), datetime(2000, 1, 1)])
    end_time: datetime = Field(examples=[datetime(1900, 1, 1), datetime(2000, 1, 1)])
    stopps: int  = Field(default=1, examples=[5], ge=1)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Trip to new lands",
                    "start_time": datetime(2026, 7, 17, 10, 15),
                    "end_time": datetime(2026, 7, 17, 19, 30),
                    "stopps": 5,
                }
            ]
        }
    }

# For data going out (Response)
class TripplanResponse(BaseModel):
    id: int = Field(examples=[5], ge=1)
    start_time: datetime = Field(examples=[datetime(1900, 1, 1), datetime(2000, 1, 1)])
    end_time: datetime = Field(examples=[datetime(1900, 1, 1), datetime(2000, 1, 1)])
    stopps: int = Field(default=1, examples=[5], ge=1)
    suggestion_id: int = Field(examples=[5], ge=1)
    search_id: int = Field(examples=[5], ge=1)
    user_id: int = Field(examples=[5], ge=1)

    # Getting SQLAlchemy databse object, read attributes directly
    model_config = ConfigDict(from_attributes=True)

# # # # # # # # # # End of TRIPPLAN - Table related # # # # # # # # # #
