from application.models import Event, EventInputText
from application.database import db

def save_event_entity(value, input_text_id):
    """
    Save an event entity to the database.
    """
    existing_event = Event.query.filter_by(value=value).first()
    if existing_event:
        existing_link = EventInputText.query.filter_by(
            event_id=existing_event.id, 
            input_text_id=input_text_id
        ).first()
        if not existing_link:
            event_input_text = EventInputText(
                event_id=existing_event.id, 
                input_text_id=input_text_id
            )
            db.session.add(event_input_text)
            db.session.commit()
        return existing_event.id
    
    event = Event(value=value)
    db.session.add(event)
    db.session.commit()
    event_input_text = EventInputText(event_id=event.id, input_text_id=input_text_id)
    db.session.add(event_input_text)
    db.session.commit()
    return event.id

def get_event_entities(input_text_id=None):
    """
    Get all event entities as dictionaries.
    """
    events = Event.query.all()
    return [event.to_dict() for event in events]

def get_event_entity_by_id(id):
    """
    Get an event entity by its ID as dictionary.
    """
    event = Event.query.filter_by(id=id).first()
    return event.to_dict() if event else None

def get_event_entities_by_input_text_id(input_text_id):
    """
    Get all event entities associated with an input text as dictionaries.
    """
    event_ids = EventInputText.query.filter_by(input_text_id=input_text_id).all()
    return [get_event_entity_by_id(event_id.event_id) for event_id in event_ids]
