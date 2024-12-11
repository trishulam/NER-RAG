from typing import List, Literal, Optional
from pydantic import BaseModel


# Person-to-Person Relationship
class PersonToPersonRelationship(BaseModel):
    type: Literal["Suspect In", "Witnessed", "Victim In"]  # Relationship types specific to Person-to-Person
    source_id: int  # ID of the source person
    target_id: int  # ID of the target person
    note: Optional[str]  # Explanation or context for the relationship

class PersonToPersonRelationships(BaseModel):
    person_to_person_relations: List[PersonToPersonRelationship]

# Person-to-Event Relationship
class PersonToEventRelationship(BaseModel):
    type: Literal["Suspect In", "Witnessed", "Victim In"]  # Relationship types specific to Person-to-Event
    source_id: int  # ID of the person
    target_id: int  # ID of the event
    note: Optional[str]  # Explanation or context for the relationship

class PersonToEventRelationships(BaseModel):
    person_to_event_relations: List[PersonToEventRelationship]

# Person-to-Vehicle Relationship
class PersonToVehicleRelationship(BaseModel):
    type: Literal["Involved In Vehicle"]  # Relationship type specific to Person-to-Vehicle
    source_id: int  # ID of the person
    target_id: int  # ID of the vehicle
    note: Optional[str]  # Explanation or context for the relationship

class PersonToVehicleRelationships(BaseModel):
    person_to_vehicle_relations: List[PersonToVehicleRelationship]

# Location-to-Event Relationship
class LocationToEventRelationship(BaseModel):
    type: Literal["Scene Of"]  # Relationship type specific to Location-to-Event
    source_id: int  # ID of the location
    target_id: int  # ID of the event
    note: Optional[str]  # Explanation or context for the relationship

class LocationToEventRelationships(BaseModel):
    location_to_event_relations: List[LocationToEventRelationship]

# Vehicle-to-Event Relationship
class VehicleToEventRelationship(BaseModel):
    type: Literal["Involved In Event", "Abandoned At"]  # Relationship types specific to Vehicle-to-Event
    source_id: int  # ID of the vehicle
    target_id: int  # ID of the event or location
    note: Optional[str] # Explanation or context for the relationship

class VehicleToEventRelationships(BaseModel):
    vehicle_to_event_relations: List[VehicleToEventRelationship]

class check_for_relations_schema(BaseModel):
    person_to_person: bool
    person_to_event: bool
    person_to_vehicle: bool
    location_to_event: bool
    vehicle_to_event: bool

