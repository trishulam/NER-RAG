from application.config import ENTITIES_SERVICE_URL, RELATIONSHIPS_SERVICE_URL
import requests

def services_check():
    try:
        # Call Entities Service
        entities_response = requests.get(f"{ENTITIES_SERVICE_URL}/entities/hello")
        entities_message = entities_response.json().get("message", "No response")

        # # Call Relationships Service
        relationships_response = requests.get(f"{RELATIONSHIPS_SERVICE_URL}/relations/hello")
        relationships_message = relationships_response.json().get("message", "No response")

        return {
            "entities_service": entities_message,
            "relationships_service": relationships_message
        }, 200

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to connect to one or more services: {str(e)}")