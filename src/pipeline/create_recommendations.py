"""
This mocule is for ...
"""
from pipeline.ai_functions import prepare_recommendation_prompt, do_search, structure_output
from db.crud import get_user_address, save_recommendations

#  Adresse des Users abfragen. Wenn keine Adresse gegeben
#  -> Fallback zu eingetragener Adresse in Users-table, wenn dort immer noch keine Adresse
#  -> Error: Keine Startadresse gegeben.
def get_address(search_obj):
    starting_point = search_obj.starting_point
    if not starting_point:
        user_address = get_user_address(search_obj.user_id)
        if not user_address:
            raise Exception(f"User with id {search_obj.user_id} does not exist")
        else:
            if user_address:
                starting_point = user_address
            else:
                raise Exception(f"User with id {search_obj.user_id} does not contain an address.")

    return starting_point

def recommendations_flow(search_obj):
    """
    creating a recommendation flow, starting from the given search object.
    Do a Google search for given search object.
    receive up to 5 suggestions according to the given search object.
    structure the search result output for following operations and return them.
    :param search_obj: A models.SeachCreate object.
    :return structured_suggestions:
    """
    prompt_params = search_obj
    prompt_params.starting_point = get_address(search_obj=search_obj)
    recommendation_prompt = prepare_recommendation_prompt(prompt_params)
    unstructured_results = do_search(recommendation_prompt)
    structured_suggestions = structure_output(unstructured_results)
    save_recommendations(user_id=prompt_params.user_id,
                         search_id=prompt_params.id,
                         suggestion_list=structured_suggestions)

    return structured_suggestions