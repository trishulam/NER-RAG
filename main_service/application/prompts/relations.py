person_to_person_system_message = """You are tasked with identifying relationships between persons based on the input text and the provided list of person entities. The relationships to identify include:

                                    - **Knows**: When one person knows another.
                                    - **Witnessed Event With**: When two persons witnessed the same event together.

                                    **Instructions**:
                                    1. For each relationship, provide:
                                      - **type**: The specific relationship type (choose from "Knows" or "Witnessed Event With").
                                      - **source_id**: The ID of the source person (must match an ID from the provided list of persons).
                                      - **target_id**: The ID of the target person (must match an ID from the provided list of persons).
                                      - **note**: A short explanation or context for the relationship (optional).

                                    2. **Important Constraints**:
                                      - Use only the **IDs from the provided person entities**. Do not create or infer IDs.
                                      - If a valid `source_id` or `target_id` is unavailable in the list, exclude the relationship from the output.

                                    3. Respond in the following JSON format:
                                    ```json
                                    {
                                      "person_to_person_relations": [
                                        {
                                          "type": "Knows",
                                          "source_id": 1,
                                          "target_id": 2,
                                          "note": "Carlos Ramirez and Elena Torres were partners in the trafficking operation."
                                        }
                                      ]
                                    }
                                """

person_to_event_system_message = """You are tasked with identifying relationships between persons and events. Focus on the following relationships:
                                    - "Suspect In": When a person is suspected of involvement in an event.
                                    - "Witnessed": When a person witnessed an event.
                                    - "Victim In": When a person was a victim in an event.

                                    For each relationship, provide:
                                    1. The `type` of relationship.
                                    2. The `source_id` (ID of the person).
                                    3. The `target_id` (ID of the event).
                                    4. A `note` explaining the relationship.

                                    Respond in JSON format:
                                    {
                                    "person_to_event": [
                                        {
                                        "type": string, #REQUIRED
                                        "source_id": int, #REQUIRED
                                        "target_id": int, #REQUIRED
                                        "note": string #OPTIONAL
                                        }
                                    ]
                                    }

                                    If you cant satisfy the request, respond with an empty list.
                                    """

person_to_vehicle_system_message = """You are tasked with identifying relationships between persons and vehicles. Focus on the following relationship:
                                    - "Involved In Vehicle": When a person is involved with a vehicle (e.g., as an owner, driver, or suspect).

                                    For each relationship, provide:
                                    1. The `type` of relationship.
                                    2. The `source_id` (ID of the person).
                                    3. The `target_id` (ID of the vehicle).
                                    4. A `note` explaining the relationship.

                                    Respond in JSON format:
                                    {
                                    "person_to_vehicle": [
                                        {
                                        "type": string, #REQUIRED
                                        "source_id": int, #REQUIRED
                                        "target_id": int, #REQUIRED
                                        "note": string #OPTIONAL
                                        }
                                    ]
                                    }

                                    If you cant satisfy the request, respond with an empty list.
                                    """

location_to_event_system_message = """You are tasked with identifying relationships between locations and events. Focus on the following relationship:
                                    - "Scene Of": When a location is associated with an event (e.g., a crime scene).

                                    For each relationship, provide:
                                    1. The `type` of relationship. 
                                    2. The `source_id` (ID of the location).
                                    3. The `target_id` (ID of the event).
                                    4. A `note` explaining the relationship.

                                    Respond in JSON format:
                                    {
                                    "location_to_event": [
                                        {
                                        "type": string, #REQUIRED
                                        "source_id": int, #REQUIRED
                                        "target_id": int,  #REQUIRED
                                        "note": string #OPTIONAL
                                        }
                                    ]
                                    }

                                    If you cant satisfy the request, respond with an empty list.
                                    """

vehicle_to_event_system_message = """You are tasked with identifying relationships between vehicles and events. Focus on the following relationships:
                                    - "Involved In Event": When a vehicle is involved in an event (e.g., as stolen or used in a crime).
                                    - "Abandoned At": When a vehicle is abandoned at a specific location.

                                    For each relationship, provide:
                                    1. The `type` of relationship.
                                    2. The `source_id` (ID of the vehicle).
                                    3. The `target_id` (ID of the event or location).
                                    4. A `note` explaining the relationship.

                                    Respond in JSON format:
                                    {
                                    "vehicle_to_event": [
                                        {
                                        "type": string, #REQUIRED
                                        "source_id": int, #REQUIRED
                                        "target_id": int, #REQUIRED
                                        "note": string #OPTIONAL
                                        }
                                    ]
                                    }

                                    If you cant satisfy the request, respond with an empty list.
                                    """

check_for_relations_system_message = """
{
  "task": "Determine the existence of specific relationship types in the given text.",
  "relationships_to_check": [
    "Person-to-Person: Relationships like 'Knows' or 'Witnessed Event With' between two persons.",
    "Person-to-Event: Relationships like 'Suspect In', 'Witnessed', or 'Victim In' between a person and an event.",
    "Person-to-Vehicle: Relationships like 'Involved In Vehicle' between a person and a vehicle.",
    "Location-to-Event: Relationships like 'Scene Of' between a location and an event.",
    "Vehicle-to-Event: Relationships like 'Involved In Event' or 'Abandoned At' between a vehicle and an event or location."
  ],
  "instructions": "Analyze the text and determine whether each of the relationship types exists in the context. Provide a JSON response with true or false for each relationship type.",
  "format": {
    "person_to_person": "true or false",
    "person_to_event": "true or false",
    "person_to_vehicle": "true or false",
    "location_to_event": "true or false",
    "vehicle_to_event": "true or false"
  }
}
"""
