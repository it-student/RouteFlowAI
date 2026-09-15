"""
This module is for the final planning steps getting from a suggestion to a full trip plan.
"""
from db.crud import get_suggestion
from models import TripplanCreate


def schedule_flow(user_id: int, suggestion_id: int):
    """
    This function is for the final planning steps getting from a suggestion to a full trip plan
    :return: TripplanCreate object
    calls get_suggestion() to get suggestion details.
    """
    base_suggestion = get_suggestion(user_id=user_id, suggest_id=suggestion_id)
    return base_suggestion