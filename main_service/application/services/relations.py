from application.utils.llm_client import LLMClient
from application.config import RELATIONSHIPS_SERVICE_URL
from application.prompts.relations import (
    person_to_person_system_message,
    person_to_event_system_message,
    person_to_vehicle_system_message,
    location_to_event_system_message,
    vehicle_to_event_system_message,
    check_for_relations_system_message,
)
from application.schema.relations import (
    PersonToPersonRelationships,
    PersonToEventRelationships,
    PersonToVehicleRelationships,
    LocationToEventRelationships,
    VehicleToEventRelationships,
    check_for_relations_schema,
)
import pydantic
import json

import requests


def check_relation_response(response, key, source_ids, target_ids):
    """
    Check if the response from the Relations Service is valid.
    """
    print("Source IDs", source_ids)
    print("Target IDs", target_ids)
    for item in response[key]:
        if item['source_id'] == item['target_id']:
            response[key].remove(item)
        if item['source_id'] not in source_ids or item['target_id'] not in target_ids:
            response[key].remove(item)
    return response
        


def send_to_relations_service(relations, input_text_id):
    """
    Send the extracted relationships to the Relations Service for saving.
    """
    try:
        response = requests.post(
            f"{RELATIONSHIPS_SERVICE_URL}/relations/save",
            json={
                "relations": relations,
                "input_text_id": input_text_id,
            },
        )
        return response.json()

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to send relationships to the Relations Service: {str(e)}")

def check_for_relations(user_text: str, llm_client: LLMClient, entities: dict):
    """
    Check if the given user message contains any relationships using the LLM client.
    """
    try:
        user_message = f"""
                            Analyze the following text and determine if the specified relationships exist:
                            Text: "{user_text}"

                            Entities:{entities}
                        """
        try:
            response = llm_client.call_model(
                system_message=check_for_relations_system_message,
                user_message=user_message,
                response_model=check_for_relations_schema
            )
        except pydantic.ValidationError as e:
            raise RuntimeError(f"Pydantic validation error: {str(e)}")
        return response.dict()
    
    except Exception as e:
        raise RuntimeError(f"Relationship check failed: {str(e)}")
    
def extract_relations(input_text: str, llm_client: LLMClient, check_relations: check_for_relations, entities: dict):
    """
    Extract relationships from the user message using the LLM client.
    """
    responses = {
        "person_to_person_relations": [],
        "person_to_event_relations": [],
        "person_to_vehicle_relations": [],
        "location_to_event_relations": [],
        "vehicle_to_event_relations": [],
    }

    persons=entities.get("persons", [])
    events=entities.get("events", [])
    vehicles=entities.get("vehicles", [])
    locations=entities.get("locations", [])
    
    person_to_person_user_message = f"""
    Entities:
    {{
    "persons": {persons},
    "input_text": {input_text}
    }}
    """

    person_to_event_user_message = f"""
    Entities:
    {{
    "persons": {persons},
    "events": {events},
    "input_text": {input_text}
    }}
    """

    person_to_vehicle_user_message = f"""
    Entities:
    {{
    "persons": {persons},
    "vehicles": {vehicles},
    "input_text": {input_text}
    }}
    """

    location_to_event_user_message = f"""
    Entities:
    {{
    "locations": {locations},
    "events": {events},
    "input_text": {input_text}
    }}
    """

    vehicle_to_event_user_message = f"""
    Entities:
    {{
    "vehicles": {vehicles},
    "events": {events},
    "input_text": {input_text}
    }}
    """

    try:
        if check_relations["person_to_person"]:
            try:
                person_response = llm_client.call_model(
                    system_message=person_to_person_system_message,
                    user_message=person_to_person_user_message,
                    response_model=PersonToPersonRelationships,
                )
                source_ids = [item['id'] for item in persons]
                target_ids = [item['id'] for item in persons]
                person_response = check_relation_response(person_response.dict(), "person_to_person_relations", source_ids, target_ids)
            except pydantic.ValidationError as e:
                raise RuntimeError(f"Pydantic validation error: {str(e)}")
            responses.update(person_response)

        if check_relations["person_to_event"]:
            try:
                event_response = llm_client.call_model(
                    system_message=person_to_event_system_message,
                    user_message=person_to_event_user_message,
                    response_model=PersonToEventRelationships,
                )
                source_ids = [item['id'] for item in persons]
                target_ids = [item['id'] for item in events]
                event_response = check_relation_response(event_response.dict(), "person_to_event_relations", source_ids, target_ids)
            except pydantic.ValidationError as e:
                raise RuntimeError(f"Pydantic validation error: {str(e)}")
            responses.update(event_response)

        if check_relations["person_to_vehicle"]:
            try:
                vehicle_response = llm_client.call_model(
                    system_message=person_to_vehicle_system_message,
                    user_message=person_to_vehicle_user_message,
                    response_model=PersonToVehicleRelationships,
                )
                source_ids = [item['id'] for item in persons]
                target_ids = [item['id'] for item in vehicles]
                vehicle_response = check_relation_response(vehicle_response.dict(), "person_to_vehicle_relations", source_ids, target_ids)
            except pydantic.ValidationError as e:
                raise RuntimeError(f"Pydantic validation error: {str(e)}")
            responses.update(vehicle_response)

        if check_relations["location_to_event"]:
            try: 
                location_response = llm_client.call_model(
                    system_message=location_to_event_system_message,
                    user_message=location_to_event_user_message,
                    response_model=LocationToEventRelationships,
                )
                source_ids = [item['id'] for item in locations]
                target_ids = [item['id'] for item in events]
                location_response = check_relation_response(location_response.dict(), "location_to_event_relations", source_ids, target_ids)
            except pydantic.ValidationError as e:
                raise RuntimeError(f"Pydantic validation error: {str(e)}")     
            responses.update(location_response)

        if check_relations["vehicle_to_event"]:
            try:
                vehicle_event_response = llm_client.call_model(
                    system_message=vehicle_to_event_system_message,
                    user_message=vehicle_to_event_user_message,
                    response_model=VehicleToEventRelationships,
                )
                source_ids = [item['id'] for item in vehicles]
                target_ids = [item['id'] for item in events]
                vehicle_event_response = check_relation_response(vehicle_event_response.dict(), "vehicle_to_event_relations", source_ids, target_ids)
            except pydantic.ValidationError as e:
                raise RuntimeError(f"Pydantic validation error: {str(e)}")
            responses.update(vehicle_event_response)

        # Serialize results
        for key, response in responses.items():
            if response:
                if isinstance(response, list):
                    responses[key] = [item.dict() if hasattr(item, 'dict') else item for item in response]
                else:
                    responses[key] = response.dict() if hasattr(response, 'dict') else response
            else:
                responses[key] = {}

        return responses

    except Exception as e:
        raise RuntimeError(f"Relation extraction failed: {str(e)}")
    
def get_relationships():
    """
    Get all relationships from the database.
    """
    try:
        response = requests.get(f"{RELATIONSHIPS_SERVICE_URL}/relations/get")
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to get relationships from the Relations Service: {str(e)}")
    
def get_relationships_by_input_text_id(input_text_id: str):
    """
    Get all relationships by input text id from the database.
    """
    try:
        response = requests.get(f"{RELATIONSHIPS_SERVICE_URL}/relations/get_by_input_text_id?input_text_id={input_text_id}")
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to get relationships by input text id from the Relations Service: {str(e)}")
    
def get_relationships_by_type(relation_type: str):
    """
    Get all relationships by type from the database.
    """
    try:
        response = requests.get(f"{RELATIONSHIPS_SERVICE_URL}/relations/get_by_type?type={relation_type}")
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to get relationships by type from the Relations Service: {str(e)}")
    