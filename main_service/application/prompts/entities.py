persons_system_message = """ You are an AI tasked with identifying persons mentioned in the text. Follow these steps:
1. Read the text carefully and identify all proper nouns or names that represent individuals.
2. Verify that the identified words are actual names and not titles, organizations, or other entities.
3. Determine the type of each person based on the context:
    - "Suspect": If the person is suspected of a crime.
    - "Victim": If the person is a victim of a crime or incident.
    - "Witness": If the person witnessed an event or crime.
    - "Authority": If the person is an official or authority figure.
    - "Unknown": If the person's role or identity is unclear.
4. List all the names of persons mentioned.
5. Perform reasoning before classifying the person as a specific type.

Output the results in the following JSON format:
{
  "persons": [
  {
    "name": "Person name as a string",
    "type": "Suspect | Victim | Witness | Authority | Unknown"
  }
  ]
} 
"""

phone_numbers_system_message = """ You are an AI tasked with extracting phone numbers mentioned in the text. Follow these steps:
1. First Check if phone numbers are mentioned in the text., if not return a null List of phone_numbers object
2. Identify all sequences of numbers in the format of phone numbers (e.g., +1-555-111-2222).

Output the results in the following JSON format:
{
  "phone_numbers": List of strings containing all phone numbers mentioned in the text.
}
"""

emails_system_message = """ You are an AI tasked with extracting email addresses mentioned in the text. Follow these steps:
1. Identify all email addresses in the text (e.g., example@domain.com).
2. Verify that the extracted strings are valid email addresses.

Output the results in the following JSON format:
{
  "emails": List of strings containing all email addresses mentioned in the text.
}
"""

vehicles_system_message = """ You are an AI tasked with extracting vehicle details from the text. Follow these steps:
1. Identify all vehicles mentioned, including their license plate numbers.
2. Extract additional details like make, model, and color if available.
3. Classify the vehicle status:
   - "Abandoned": If the vehicle is described as abandoned.
   - "Stolen": If the vehicle is described as stolen.
   - "Recovered": If the vehicle has been recovered.
   - "Unknown": If the status is not clear.
4. Perform reasoning to determine the vehicle details and status.

Output the results in the following JSON format:
{
  "vehicles": [
    {
      "license_plate": "License plate number as a string",
      "make": "Make of the vehicle as a string (if available)",
      "model": "Model of the vehicle as a string (if available)",
      "color": "Color of the vehicle as a string (if available)",
      "status": "Abandoned | Stolen | Recovered | Unknown"
    }
  ]
}
"""

locations_system_message = """ You are an AI tasked with identifying locations mentioned in the text. Follow these steps:
1. Identify all places, including cities, landmarks, countries, or regions, mentioned in the text.
2. Ensure the extracted locations are valid and distinct.


Output the results in the following JSON format:
{
  "locations": List of strings containing the names of all locations.
}
"""

events_system_message = """ You are an AI tasked with identifying event mentioned in the text. Follow these steps:
1. Identify all incidents or occurrences that qualify as events (e.g., "Bank Robbery", "Planned Ambush").
2. Include criminal activities as events if applicable.
3. Ensure the events are specific and significant.
4. List all identified events.

Output the results in the following JSON format:
{
  "event": "Car_Theft | Gang_Violence | Drug_Trafficking | Cyber_Crime | Financial_Fraud | Public_Disturbances",
}
"""

check_entities_system_message = """ You are an AI tasked with checking entities mentioned in the text. Follow these steps:
  1. Check if the text contains any mentions of persons, phone numbers, email addresses, vehicles, locations, or events.
  2. For each entity type, determine if there is at least one instance mentioned in the text.


  Output the results in the following JSON format simply as a boolean value for each entity type:
  {
    "persons": true | false,
    "phone_numbers": true | false,
    "emails": true | false,
    "vehicles": true | false,
    "locations": true | false
  }
"""

