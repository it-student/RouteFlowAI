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

    return unstructured_search_results


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


def schedule_trip(prompt: str):
    """
    Schedule a trip according to chosen suggestion.
    :param prompt: The prompt to be sent to the LLM.
    :return: unstructured_schedule_results
    """
    interaction = client.interactions.create(
        model="gemini-3.1-flash-lite",
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": models.TripplanCreate.model_json_schema()
        },
    )
    tripplan = models.TripplanCreate.model_validate_json(interaction.output_text)
    print(tripplan)
    return tripplan
