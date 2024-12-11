from application.models import Email, EmailInputText
from application.database import db

def save_email_entity(value, input_text_id):
    """
    Save an email entity to the database.
    """
    # Check if email already exists
    existing_email = Email.query.filter_by(value=value).first()
    if existing_email:
        # Create association if it doesn't exist
        existing_link = EmailInputText.query.filter_by(
            email_id=existing_email.id, 
            input_text_id=input_text_id
        ).first()
        if not existing_link:
            email_input_text = EmailInputText(
                email_id=existing_email.id, 
                input_text_id=input_text_id
            )
            db.session.add(email_input_text)
            db.session.commit()
        return existing_email.id

    # If email doesn't exist, create new one
    email = Email(value=value)
    db.session.add(email)
    db.session.commit()
    email_input_text = EmailInputText(email_id=email.id, input_text_id=input_text_id)
    db.session.add(email_input_text)
    db.session.commit()
    return email.id

def get_email_entities(input_text_id=None):
    """
    Get all email entities as dictionaries.
    """
    emails = Email.query.all()
    return [email.to_dict() for email in emails]

def get_email_entity_by_id(id):
    """
    Get an email entity by its ID as dictionary.
    """
    email = Email.query.filter_by(id=id).first()
    return email.to_dict() if email else None

def get_email_entities_by_input_text_id(input_text_id):
    """
    Get all email entities associated with an input text as dictionaries.
    """
    email_ids = EmailInputText.query.filter_by(input_text_id=input_text_id).all()
    return [get_email_entity_by_id(email_id.email_id) for email_id in email_ids]