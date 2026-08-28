"""
This mocule is for ...
"""
from ai_functions import get_address, prepare_recommendation_prompt, do_search, structure_output

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

    return structured_suggestions