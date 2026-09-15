"""
This module is for crdu functionality outside routes.
"""
from idlelib import history

from db.db_operations import SessionLocal
from db.schemas import User, Suggestion
from models import SuggestionList, SuggestionResponse


def get_user_address(user_id) -> str:
    """
    returns the address of the user saved in the database.
    :param user_id: Valid user_id to find the right user-entry.
    :return address: str of the address of the user saved in the database.
    """
    address = ""
    with SessionLocal() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            address = user.address

    return address


def save_recommendations(user_id: int, search_id: int, suggestion_list: SuggestionList):
    """
    Saves recommendations to database for user with user_id and search with search id.
    :param user_id: int user id to find the right user-entry.
    :param search_id: search id of current llm-web-search, that got saved to the database.
    :param suggestion_list: List
    :return:
    """
    with SessionLocal() as db:
        if suggestion_list:
            for suggestion in suggestion_list.suggestions:
                new_suggestion = Suggestion(
                    title=suggestion.title,
                    description=suggestion.description,
                    sug_transport_type=suggestion.sug_transport_type,
                    destination_coordinates=suggestion.destination_coordinates if suggestion.destination_coordinates else '',
                    user_id=user_id,
                    history_id=search_id
                )
                db.add(new_suggestion)
            db.commit()
        else:
            # Raise exceptioon here:
            print("No suggestions saved")


def get_suggestion(user_id: int, suggest_id: int) -> SuggestionResponse:
    """
    returns the suggestion saved to the database.
    :param user_id:
    :param suggest_id:
    :return: Suggestion object:
    """
    with SessionLocal() as db:
        suggestion = db.query(Suggestion).filter(Suggestion.id == suggest_id).first()
        if suggestion.user_id == user_id:
            return SuggestionResponse.model_validate(suggestion)
        else:
            print("Suggestion not found for user with id: {}".format(user_id))
            return object.__new__(SuggestionResponse)
