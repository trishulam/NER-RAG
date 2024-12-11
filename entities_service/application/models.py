from .database import db
from datetime import datetime

class SerializerMixin:
    def to_dict(self):
        return {column.name: getattr(self, column.name) 
                for column in self.__table__.columns}

# Person Entity
class Person(db.Model, SerializerMixin):
    __tablename__ = "persons"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String, nullable=False)  # Name of the person
    type = db.Column(db.String, nullable=True)  # Type (Suspect, Witness, etc.)

# Vehicle Entity
class Vehicle(db.Model, SerializerMixin):
    __tablename__ = "vehicles"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    license_plate = db.Column(db.String, nullable=False)  # License plate number
    make = db.Column(db.String, nullable=True)  # Vehicle make
    model = db.Column(db.String, nullable=True)  # Vehicle model
    color = db.Column(db.String, nullable=True)  # Vehicle color
    status = db.Column(db.String, nullable=True)  # Vehicle status (Stolen, Abandoned, etc.)

# Location Entity
class Location(db.Model, SerializerMixin):
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String, nullable=False)  # Name of the location

# Phone Number Entity
class PhoneNumber(db.Model, SerializerMixin):
    __tablename__ = "phone_numbers"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String, nullable=False)  # Phone number

# Email Entity
class Email(db.Model, SerializerMixin):
    __tablename__ = "emails"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String, nullable=False)  # Email address

class Event(db.Model, SerializerMixin):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String, nullable=False)  # Event name

class PersonInputText(db.Model, SerializerMixin):
    __tablename__ = 'person_input_text'
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('persons.id'), nullable=False)
    input_text_id = db.Column(db.Integer,nullable=False)

class VehicleInputText(db.Model, SerializerMixin):
    __tablename__ = 'vehicle_input_text'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    input_text_id = db.Column(db.Integer, nullable=False)

class LocationInputText(db.Model, SerializerMixin):
    __tablename__ = 'location_input_text'
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    input_text_id = db.Column(db.Integer, nullable=False)

class PhoneNumberInputText(db.Model, SerializerMixin):
    __tablename__ = 'phone_number_input_text'
    id = db.Column(db.Integer, primary_key=True)
    phone_number_id = db.Column(db.Integer, db.ForeignKey('phone_numbers.id'), nullable=False)
    input_text_id = db.Column(db.Integer, nullable=False)

class EmailInputText(db.Model, SerializerMixin):
    __tablename__ = 'email_input_text'
    id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.Integer, db.ForeignKey('emails.id'), nullable=False)
    input_text_id = db.Column(db.Integer, nullable=False)

class EventInputText(db.Model, SerializerMixin):
    __tablename__ = 'event_input_text'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    input_text_id = db.Column(db.Integer,nullable=False)