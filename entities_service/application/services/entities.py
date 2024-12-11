from application.services.persons import *
from application.services.phone_numbers import *
from application.services.emails import *
from application.services.locations import *
from application.services.vehicles import *
from application.services.events import *

def save_entities(entities, input_text_id):
    """
    Save the extracted entities to the database.
    """
    try:
        print("Saving entities to the database")
        # Save the entities to the database
        for key in entities.keys():
            if not entities[key]:
                continue
            if key == "persons":
                for person in entities['persons']:
                    save_person_entity(person['name'], person['type'], input_text_id)
            elif key == "phone_numbers":
                for phone_number in entities['phone_numbers']:
                    save_phone_number_entity(phone_number, input_text_id)
            elif key == "emails":
                for email in entities['emails']:
                    save_email_entity(email, input_text_id)
            elif key == "locations":
                for location in entities['locations']:
                    save_location_entity(location, input_text_id)
            elif key == "vehicles":
                for vehicle in entities['vehicles']:
                    save_vehicle_entity(
                        vehicle['license_plate'],
                        vehicle['make'],
                        vehicle['model'],
                        vehicle['color'],
                        vehicle['status'],
                        input_text_id,
                    )
            elif key == "event":
                save_event_entity(entities['event'], input_text_id)

        return {"message": "Entities saved successfully!"}
    except Exception as e:
        return {"error": str(e)}
    
def get_entities():
    """
    Get the entities for the given input text ID.
    """
    try:
        print("Getting entities from the database")
        # Get the entities from the database
        persons=get_person_entities()
        phone_numbers=get_phone_number_entities()
        emails=get_email_entities()
        locations=get_location_entities()
        vehicles=get_vehicle_entities()
        events=get_event_entities()

        return {
            "persons": persons,
            "phone_numbers": phone_numbers,
            "emails": emails,
            "locations": locations,
            "vehicles": vehicles,
            "events": events,
        }
    except Exception as e:
        return {"error": str(e)}

def get_entities_by_input_text_id(input_text_id):
    """
    Get the entities for the given input text ID.
    """
    try:
        print("Getting entities from the database")
        # Get the entities from the database
        persons=get_person_entities_by_input_text_id(input_text_id)
        phone_numbers=get_phone_number_entities_by_input_text_id(input_text_id)
        emails=get_email_entities_by_input_text_id(input_text_id)
        locations=get_location_entities_by_input_text_id(input_text_id)
        vehicles=get_vehicle_entities_by_input_text_id(input_text_id)
        events=get_event_entities_by_input_text_id(input_text_id)

        return {
            "persons": persons,
            "phone_numbers": phone_numbers,
            "emails": emails,
            "locations": locations,
            "vehicles": vehicles,
            "events": events,
        }
    except Exception as e:
        return {"error": str(e)}
