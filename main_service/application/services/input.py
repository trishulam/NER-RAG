from application.models import InputText
from application.database import db

def save_input_text(user_message):
    """
    Save the input text to the database and return its ID.
    """
    input_text = InputText(input_text=user_message)
    db.session.add(input_text)
    db.session.commit()
    return input_text.id

def get_input_text_by_id(input_text_id):
    """
    Get the input text by its ID.
    """
    input_text = InputText.query.filter_by(id=input_text_id).first()
    return input_text.input_text

def get_all_input_texts():
    """
    Get all input texts from the database.
    """
    input_texts = InputText.query.all()
    return [input_text.to_dict() for input_text in input_texts]