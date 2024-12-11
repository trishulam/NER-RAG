from typing import List, Literal, Optional
from pydantic import BaseModel

class PersonEntity(BaseModel):
    name: str  # Person name
    type: Optional[Literal["Suspect", "Victim", "Witness", "Authority", "Unknown"]]  # Person type

class PersonEntities(BaseModel):
    persons: List[PersonEntity]

class PhoneNumberEntities(BaseModel):
    phone_numbers: List[str]

class EmailEntities(BaseModel):
    emails: List[str]

# Schema for Vehicles
class VehicleEntity(BaseModel):
    license_plate: str  # License plate number
    make: Optional[str] = None  # Vehicle make
    model: Optional[str] = None  # Vehicle model
    color: Optional[str] = None  # Vehicle color
    status: Optional[Literal["Abandoned", "Stolen", "Recovered", "Unknown"]]  # Vehicle status

class VehicleEntities(BaseModel):
    vehicles: List[VehicleEntity]

# Schema for Locations
class LocationEntities(BaseModel):
    locations: List[str]  # List of location names

class EventEntity(BaseModel):
    event: Literal["Car_Theft", "Gang_Violence", "Drug_Trafficking", "Cyber_Crime", "Financial_Fraud", "Public_Disturbances"]

class check_entities(BaseModel):
    persons : bool
    phone_numbers : bool
    emails : bool
    vehicles : bool
    locations : bool

