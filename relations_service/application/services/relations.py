from application.models import Relationship, RelationshipToInputText
from application.database import db

def save_relationships(relations, input_text_id):
    """
    Save the extracted relationships to the database.
    """
    try:
        print("Saving relationships to the database")
        # Save the relationships to the database
        for key in relations.keys():
            for relation in relations[key]:
                relation["relationship_type"] = key
                save_relationship(relation, input_text_id)
        return True
    except Exception as e:
        print(e)
        return False

def save_relationship(relation, input_text_id):
    """
    Save a relationship to the database.
    """
    try:
        existing_relationship = Relationship.query.filter_by(
            type=relation["type"],
            relationship_type=relation["relationship_type"],
            source_id=relation["source_id"],
            target_id=relation["target_id"],
        ).first()
        if existing_relationship:
            existing_link = RelationshipToInputText.query.filter_by(
                relationship_id=existing_relationship.id,
                input_text_id=input_text_id,
            ).first()
            if not existing_link:
                relationship_input_text = RelationshipToInputText(
                    relationship_id=existing_relationship.id,
                    input_text_id=input_text_id,
                )
                db.session.add(relationship_input_text)
                db.session.commit()
            return existing_relationship.id

        relationship = Relationship(
            type=relation["type"],
            relationship_type=relation["relationship_type"],
            source_id=relation["source_id"],
            target_id=relation["target_id"],
            note=relation["note"],
        )
        db.session.add(relationship)
        db.session.commit()
        relationship_input_text = RelationshipToInputText(
            relationship_id=relationship.id,
            input_text_id=input_text_id,
        )
        db.session.add(relationship_input_text)
        db.session.commit()
        return relationship.id
    except Exception as e:
        print(e)
        return False

def get_relationships():
    """
    Get all relationships.
    """
    try:
        print("Getting all relationships")
        relationships = Relationship.query.all()
        return [relationship.to_dict() for relationship in relationships]
    except Exception as e:
        print(e)
        return False

def get_relationships_by_input_text_id(input_text_id):
    """
    Get the relationships for a given input text.
    """
    try:
        print("Getting relationships for input text")
        relationships = Relationship.query.join(RelationshipToInputText).filter(
            RelationshipToInputText.input_text_id == input_text_id
        ).all()
        return [relationship.to_dict() for relationship in relationships]
    except Exception as e:
        print(e)
        return False
    

def get_relationships_by_type(relationship_type):
    """
    Get relationships by type.
    """
    try:
        print("Getting relationships by type")
        relationships = Relationship.query.filter_by(relationship_type=relationship_type).all()
        return [relationship.to_dict() for relationship in relationships]
    except Exception as e:
        print(e)
        return False

