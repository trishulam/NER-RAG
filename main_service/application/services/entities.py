from application.utils.llm_client import LLMClient
from application.config import ENTITIES_SERVICE_URL
from application.prompts.entities import (
    persons_system_message,
    phone_numbers_system_message,
    emails_system_message,
    vehicles_system_message,
    locations_system_message,
    check_entities_system_message,
    events_system_message,
)
from application.schema.entities import (
    PersonEntities,
    PhoneNumberEntities,
    EmailEntities,
    VehicleEntities,
    LocationEntities,
    check_entities,
    EventEntity,
)
import requests

def send_to_entities_service(entities, input_text_id):
    """
    Send the extracted entities to the Entities Service for saving.
    """
    try:
        print(f"Sending entities to the Entities Service")
        response = requests.post(
            f"{ENTITIES_SERVICE_URL}/entities/save",
            json={
                "entities": entities,
                "input_text_id": input_text_id,
            },
        )

        return response.json()

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to send entities to the Entities Service: {str(e)}")


def check_for_entities(user_message: str, llm_client: LLMClient):
    """
    Check if the given user message contains any entities using the LLM client.
    """
    try:
        return llm_client.call_model(
            system_message=check_entities_system_message,
            user_message=user_message,
            response_model=check_entities,
        ).dict()

    except Exception as e:
        raise RuntimeError(f"Entity check failed: {str(e)}")



def extract_entities(user_message: str, llm_client: LLMClient, check_entities: check_entities):
    """
    Extract all entities from the given user message using the LLM client.
    """
    responses = {
        "persons": None,
        "phone_numbers": None,
        "emails": None,
        "vehicles": None,
        "locations": None,
    }

    try:
        if check_entities["persons"]:
            persons_response = llm_client.call_model(
                system_message=persons_system_message,
                user_message=user_message,
                response_model=PersonEntities,
            )
            responses.update(persons_response)

        if check_entities["phone_numbers"]:
            phone_numbers_response = llm_client.call_model(
                system_message=phone_numbers_system_message,
                user_message=user_message,
                response_model=PhoneNumberEntities,
            )
            responses.update(phone_numbers_response)

        if check_entities["emails"]:
            emails_response = llm_client.call_model(
                system_message=emails_system_message,
                user_message=user_message,
                response_model=EmailEntities,
            )
            responses.update(emails_response)

        if check_entities["vehicles"]:
            vehicles_response = llm_client.call_model(
                system_message=vehicles_system_message,
                user_message=user_message,
                response_model=VehicleEntities,
            )
            responses.update(vehicles_response)

        if check_entities["locations"]:
            locations_response = llm_client.call_model(
                system_message=locations_system_message,
                user_message=user_message,
                response_model=LocationEntities,
            )
            responses.update(locations_response)
        event_response = llm_client.call_model(
            system_message=events_system_message,
            user_message=user_message,
            response_model=EventEntity,
        )
        responses.update(event_response)

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
        raise RuntimeError(f"Entity extraction failed: {str(e)}")
    
def entities_get():
    """
    Retrieve all entities from the Entities Service.
    """
    try:
        response = requests.get(f"{ENTITIES_SERVICE_URL}/entities/get")
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to retrieve entities from the Entities Service: {str(e)}")

def entities_get_by_input_text_id(input_text_id: str):
    """
    Retrieve entities from the Entities Service by input text ID.
    """
    try:
        response = requests.get(f"{ENTITIES_SERVICE_URL}/entities/get/{input_text_id}")
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to retrieve entities for input text ID {input_text_id} from the Entities Service: {str(e)}")