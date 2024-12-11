from application.models import PhoneNumber, PhoneNumberInputText
from application.database import db

def save_phone_number_entity(value, input_text_id):
    """
    Save a phone number entity to the database.
    """
    existing_phone_number = PhoneNumber.query.filter_by(value=value).first()
    if existing_phone_number:
        existing_link = PhoneNumberInputText.query.filter_by(
            phone_number_id=existing_phone_number.id, 
            input_text_id=input_text_id
        ).first()
        if not existing_link:
            phone_number_input_text = PhoneNumberInputText(
                phone_number_id=existing_phone_number.id, 
                input_text_id=input_text_id
            )
            db.session.add(phone_number_input_text)
            db.session.commit()
        return existing_phone_number.id
    
    phone_number = PhoneNumber(value=value)
    db.session.add(phone_number)
    db.session.commit()
    phone_number_input_text = PhoneNumberInputText(phone_number_id=phone_number.id, input_text_id=input_text_id)
    db.session.add(phone_number_input_text)
    db.session.commit()
    return phone_number.id

def get_phone_number_entities(input_text_id=None):
    """
    Get all phone number entities as dictionaries.
    """
    phone_numbers = PhoneNumber.query.all()
    return [phone_number.to_dict() for phone_number in phone_numbers]

def get_phone_number_entity_by_id(id):
    """
    Get a phone number entity by its ID as dictionary.
    """
    phone_number = PhoneNumber.query.filter_by(id=id).first()
    return phone_number.to_dict() if phone_number else None

def get_phone_number_entities_by_input_text_id(input_text_id):
    """
    Get all phone number entities associated with an input text as dictionaries.
    """
    phone_number_ids = PhoneNumberInputText.query.filter_by(input_text_id=input_text_id).all()
    return [get_phone_number_entity_by_id(phone_number_id.phone_number_id) for phone_number_id in phone_number_ids] 
