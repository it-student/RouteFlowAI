"""
Business Logic according Gemini calls.
"""
import os
from dotenv import load_dotenv
from google import genai
import models

load_dotenv()

client = genai.Client()

api_key = os.getenv("GEMINI_API_KEY")

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




#  Google Suche starten und auf Ergebnis warten (mit Anzahl an Vorschlägen)
#   Zu vermeidende Ziele (Bei ersten Anfrage leer, ab der zweiten Abfrage mit drin)
def do_search(prompt):
    interaction = client.interactions.create(
        model="gemini-3.1-flash-lite",
        tools=[{"type": "google_search"}],
        input=prompt,
    )
    unstructured_search_results = interaction.output_text
    print("Search results (unstructured): \n\n", unstructured_search_results, "\n\n")
    # suggestions = models.SearchCreate.model_validate_json(interaction.output_text)
    # suggestions = client.interactions.create(
    #     model="gemini-3.1-flash-lite",
    #     tools=[{"type": "google_search"}],
    #     input=prompt
    # )
    return unstructured_search_results

#  Ergebnis-einholen, Suche abspeichern und Suggestions zum Schluss abspeichern.
def structure_output(unstructured_results: str) -> models.SuggestionList:
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
    suggestions = models.SuggestionList.model_validate_json(interaction.output_text)
    return suggestions
