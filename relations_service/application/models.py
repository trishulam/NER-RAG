from .database import db

class SerializerMixin:
    def to_dict(self):
        return {column.name: getattr(self, column.name) 
                for column in self.__table__.columns}
    
# Relationship Table
class Relationship(db.Model, SerializerMixin):
    __tablename__ = "relationships"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String, nullable=False)  # Specific type of relationship (e.g., Knows, Suspect In)
    relationship_type = db.Column(db.String, nullable=False)  # General category (e.g., Person-to-Person, Person-to-Event)
    source_id = db.Column(db.Integer, nullable=False)  # ID of the source entity
    target_id = db.Column(db.Integer, nullable=False)  # ID of the target entity
    note = db.Column(db.String, nullable=True)  # Context or explanation of the relationship

# Relationship to Input Text Mapping Table
class RelationshipToInputText(db.Model, SerializerMixin):
    __tablename__ = "relationship_to_input_text"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    relationship_id = db.Column(db.Integer, db.ForeignKey('relationships.id'), nullable=False)
    input_text_id = db.Column(db.Integer, nullable=False)
    relationships = db.relationship("Relationship", backref="relationship_to_input_text")