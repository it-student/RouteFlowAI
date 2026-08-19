"""
Business Logic according Gemini calls.
"""
import os
from dotenv import load_dotenv
from google import genai
import models
from db import schemas
from db.db_operations import SessionLocal

load_dotenv()

client = genai.Client()

api_key = os.getenv("GEMINI_API_KEY")

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

def structure_output(unstructured_results):
    """
    Structure the output of unstructured search results.
    :param unstructured_results: A prior LLM Google-Search result output text.
    :return suggestions: A models.SuggestionList object.
    """
    prompt = "Please extract the relevant information from given input below. \n" + unstructured_results
    interaction = client.interactions.create(
        model="gemini-3.1-flash-lite",
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": models.SuggestionList.model_json_schema()
        },
    )
    print(interaction.output_text, "\n\n")
    suggestions = models.SuggestionList.model_validate_json(interaction.output_text)
    return suggestions

def prepare_recommendation_prompt(prompt_params):

    recommendation_prompt = f"""
Do a google search for a trip starting from {prompt_params.starting_point} and max distance of {prompt_params.distance} 
together with other given attributes below and present me with up to 5 search results found on google.
(example for clarification: 
 - starting_point: Address to start the route/plan towards destinations in reach.
 - distance: Max Distance in km from starting_point to travel towards a destination one way, only allowed to be exceeded by max 10%, not more.
 - traveltime: The time traveling until reaching back to the starting point in minutes,
   can be in conflict with distance. If so, prefer traveltime over distance.
 - theme: A biref description of a theme, that reflects the tour somehow, (i.e. 'Badetour am See mit Landstraßen Tour'
   should lead to a lake, sea, public bathing area (= Badetour am See) and include only country roads and no highways
   (= mit Landstraßen Tour).
 - transport_type: The transportation type, i.e. one of the following 'Motorcycle', 'Car', 'Bicycle', 'public transport'.
 - group_size: The amount of people to travel with, i.e. 1 = alone, 2 = group of two, 3 = group of three, etc.)

    {prompt_params}
"""
    return recommendation_prompt
"""
    "starting_point": "Breitensteinweg 21B, 14165 Berlin",
    "distance": 80,
    "traveltime": 120,
    "theme": "Badetour am See mit Landstraßen Tour",
    "transport_type": "Motorcycle",
    "group_size": 1
"""

#  Adresse des Users abfragen. Wenn keine Adresse gegeben
#  -> Fallback zu eingetragener Adresse in Users-table, wenn dort immer noch keine Adresse
#  -> Error: Keine Startadresse gegeben.
def get_address(search_obj):
    starting_point = search_obj.starting_point
    if not starting_point:
        user = SessionLocal.query(schemas.User).filter(schemas.User.id == search_obj.user_id).first()
        if not user:
            raise Exception(f"User with id {search_obj.user_id} does not exist")
        else:
            if user.address:
                starting_point = user.address
            else:
                raise Exception(f"User with id {search_obj.user_id} does not contain an address.")

    return starting_point


#  Google Suche starten und auf Ergebnis warten (mit Anzahl an Vorschlägen)
#   Zu vermeidende Ziele (Bei ersten Anfrage leer, ab der zweiten Abfrage mit drin)
def do_search(prompt):
    interaction = client.interactions.create(
        model="gemini-3.1-flash-lite",
        tools=[{"type": "google_search"}],
        input=prompt,
    )
    print(interaction, "\n\n")
    search_results = interaction.output_text
    # suggestions = models.SearchCreate.model_validate_json(interaction.output_text)
    # suggestions = client.interactions.create(
    #     model="gemini-3.1-flash-lite",
    #     tools=[{"type": "google_search"}],
    #     input=prompt
    # )
    print(search_results)
    return search_results

#  Ergebnis-einholen, Suche abspeichern und Suggestions zum Schluss abspeichern.

