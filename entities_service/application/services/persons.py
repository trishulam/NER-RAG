from application.models import Person, PersonInputText
from application.database import db

def save_person_entity(value, type, input_text_id):
    """
    Save a person entity to the database.
    """
    existing_person = Person.query.filter_by(value=value).first()
    if existing_person:
        existing_link = PersonInputText.query.filter_by(
            person_id=existing_person.id, 
            input_text_id=input_text_id
        ).first()
        if not existing_link:
            person_input_text = PersonInputText(
                person_id=existing_person.id, 
                input_text_id=input_text_id
            )
            db.session.add(person_input_text)
            db.session.commit()
        return existing_person.id
    
    person = Person(value=value, type=type)
    db.session.add(person)
    db.session.commit()
    person_input_text = PersonInputText(person_id=person.id, input_text_id=input_text_id)
    db.session.add(person_input_text)
    db.session.commit()
    return person.id

def get_person_entities(input_text_id=None):
    """
    Get all person entities as dictionaries.
    """
    persons = Person.query.all()
    return [person.to_dict() for person in persons]


def get_person_entity_by_id(id):
    """
    Get a person entity by its ID as dictionary.
    """
    person = Person.query.filter_by(id=id).first()
    return person.to_dict() if person else None

def get_person_entities_by_input_text_id(input_text_id):
    """
    Get all person entities associated with an input text as dictionaries.
    """
    person_ids = PersonInputText.query.filter_by(input_text_id=input_text_id).all()
    return [get_person_entity_by_id(person_id.person_id) for person_id in person_ids]
