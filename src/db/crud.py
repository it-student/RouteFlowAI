"""
This module is for crdu functionality outside routes.
"""
from idlelib import history

from db.db_operations import SessionLocal
from db.schemas import User, Suggestion, Searchhistory, Tripplan
from models import SuggestionList, SuggestionResponse, TripplanCreate, TripplanResponse


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


def get_starting_point(history_id: int) -> str:
    """
    returns the starting point as a string.
    :param history_id: The id of the search_history.:
    :return starting_point: string of the starting point.:
    """
    with SessionLocal() as db:
        search_history_obj = db.query(Searchhistory).filter(Searchhistory.id == history_id).first()
        return search_history_obj.starting_point if search_history_obj else ""


def save_tripplan(user_id: int, searchhistory_id: int, suggestion_id: int, tripplan: TripplanCreate):
    """
    Saves a tripplan to database for user with user_id and search with searchhistory_id as well as the chosen suggestion
    to plan with, with suggestion_id as well.
    :param user_id: The user id:
    :param searchhistory_id: The search history id:
    :param suggestion_id: The suggestion id:
    :param tripplan: A TripplanCreate object:
    :return: None.
    """
    with SessionLocal() as db:
        new_tripplan = Tripplan(
            title=tripplan.title,
            description=tripplan.description,
            highlights=tripplan.highlights,
            route_description=tripplan.route_description,
            google_maps_location_links=tripplan.google_maps_location_links,
            stopps=1,
            suggestion_id=suggestion_id,
            search_id=searchhistory_id,
            user_id=user_id
        )
        db.add(new_tripplan)
        db.commit()
        return TripplanResponse.model_validate(new_tripplan)