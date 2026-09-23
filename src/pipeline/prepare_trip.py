"""
This module is for the final planning steps getting from a suggestion to a full trip plan.
"""
from db.crud import get_suggestion, get_starting_point, save_tripplan
from models import TripplanCreate, TripplanResponse, SuggestionResponse
from pipeline.ai_functions import schedule_trip

def prepare_prompt(suggestion_obj: SuggestionResponse, starting_point: str) -> str:
    """
    This method is completing the prompt for a trip plan.
    :param starting_point: A String of the starting point for the trip plan (i.e. "Musterstraße 12, 123456 Musterstadt").:
    :param suggestion_obj: A SuggestionResponse object:
    :return: The tripplan_prompt text:
    """
    tripplan_prompt = f"""Schedule a trip given the suggestion details below. Point out the highlights of that trip chosen
within three bullet points. Include the description given within the suggestion details below. Also keep the title given below.
At the end open up google maps with the route information between my starting point and the destination already entered
and the option to exclude highways already switched on, finally provide me with a google maps link for that route prepared. 

suggestion details: {suggestion_obj}
starting_point: {starting_point}
"""
    return tripplan_prompt


def schedule_flow(user_id: int, suggestion_id: int):
    """
    This function is for the final planning steps getting from a suggestion to a full trip plan
    :return: TripplanCreate object
    calls get_suggestion() to get suggestion details.
    """
    base_suggestion = get_suggestion(user_id=user_id, suggest_id=suggestion_id)
    suggestion_object = SuggestionResponse.model_validate(base_suggestion)
    starting_point = get_starting_point(suggestion_object.history_id)
    tripplan_create_prompt = prepare_prompt(suggestion_object, starting_point)
    tripplan_create_obj = schedule_trip(tripplan_create_prompt)
    if isinstance(tripplan_create_obj, TripplanCreate):
        tripplan_obj = save_tripplan(user_id=user_id,
                      searchhistory_id=suggestion_object.history_id,
                      suggestion_id=suggestion_id,
                      tripplan=tripplan_create_obj)
    print(type(tripplan_obj), "\n\n", tripplan_obj)
    return tripplan_obj
