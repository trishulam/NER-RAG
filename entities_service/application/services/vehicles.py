from application.models import Vehicle, VehicleInputText
from application.database import db

def save_vehicle_entity(license_plate, make, model, color, status, input_text_id):
    """
    Save a vehicle entity to the database.
    """
    existing_vehicle = Vehicle.query.filter_by(license_plate=license_plate).first()
    if existing_vehicle:
        existing_link = VehicleInputText.query.filter_by(
            vehicle_id=existing_vehicle.id, 
            input_text_id=input_text_id
        ).first()
        if not existing_link:
            vehicle_input_text = VehicleInputText(
                vehicle_id=existing_vehicle.id, 
                input_text_id=input_text_id
            )
            db.session.add(vehicle_input_text)
            db.session.commit()
        return existing_vehicle.id
    
    vehicle = Vehicle(license_plate=license_plate, make=make, model=model, color=color, status=status)
    db.session.add(vehicle)
    db.session.commit()
    vehicle_input_text = VehicleInputText(vehicle_id=vehicle.id, input_text_id=input_text_id)
    db.session.add(vehicle_input_text)
    db.session.commit()
    return vehicle.id

def get_vehicle_entities(input_text_id=None):
    """
    Get all vehicle entities as dictionaries.
    """
    vehicles = Vehicle.query.all()
    return [vehicle.to_dict() for vehicle in vehicles]

def get_vehicle_entity_by_id(id):
    """
    Get a vehicle entity by its ID as dictionary.
    """
    vehicle = Vehicle.query.filter_by(id=id).first()
    return vehicle.to_dict() if vehicle else None

def get_vehicle_entities_by_input_text_id(input_text_id):
    """
    Get all vehicle entities associated with an input text as dictionaries.
    """
    vehicle_ids = VehicleInputText.query.filter_by(input_text_id=input_text_id).all()
    return [get_vehicle_entity_by_id(vehicle_id.vehicle_id) for vehicle_id in vehicle_ids]
