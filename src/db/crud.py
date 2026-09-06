"""
This module is for crdu functionality outside routes.
"""
from idlelib import history

from db.db_operations import SessionLocal
from db.schemas import User, Suggestion
from models import SuggestionList, SuggestionCreate


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