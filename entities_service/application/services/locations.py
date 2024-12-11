from application.models import Location, LocationInputText
from application.database import db

def save_location_entity(value, input_text_id):
    """
    Save a location entity to the database.
    """
    existing_location = Location.query.filter_by(value=value).first()
    if existing_location:
        existing_link = LocationInputText.query.filter_by(
            location_id=existing_location.id, 
            input_text_id=input_text_id
        ).first()
        if not existing_link:
            location_input_text = LocationInputText(
                location_id=existing_location.id, 
                input_text_id=input_text_id
            )
            db.session.add(location_input_text)
            db.session.commit()
        return existing_location.id
    
    location = Location(value=value)
    db.session.add(location)
    db.session.commit()
    location_input_text = LocationInputText(location_id=location.id, input_text_id=input_text_id)
    db.session.add(location_input_text)
    db.session.commit()
    return location.id

def get_location_entities(input_text_id=None):
    """
    Get all location entities as dictionaries.
    """
    locations = Location.query.all()
    return [location.to_dict() for location in locations]

def get_location_entity_by_id(id):
    """
    Get a location entity by its ID as dictionary.
    """
    location = Location.query.filter_by(id=id).first()
    return location.to_dict() if location else None

def get_location_entities_by_input_text_id(input_text_id):
    """
    Get all location entities associated with an input text as dictionaries.
    """
    location_ids = LocationInputText.query.filter_by(input_text_id=input_text_id).all()
    return [get_location_entity_by_id(location_id.location_id) for location_id in location_ids]


