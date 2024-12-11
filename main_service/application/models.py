from .database import db
from datetime import datetime


class SerializerMixin:
    def to_dict(self):
        return {column.name: getattr(self, column.name) 
                for column in self.__table__.columns}

class InputText(db.Model, SerializerMixin):
    __tablename__ = "InputText"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    input_text = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)