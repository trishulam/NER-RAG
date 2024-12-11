# Backend for Text Analysis and Enrichment Pipeline

## Overview

This backend system implements a microservices-based architecture for text analysis and enrichment using a locally hosted language model (LLM). The application extracts entities, identifies relationships, and structures the data for downstream processing. It demonstrates efficient use of AI capabilities, scalable backend design, and structured data handling.

This backend is built specifically for an interview test and showcases:

- **Entity Extraction**: Identifying named entities (e.g., persons, locations, vehicles).
- **Relationship Mapping**: Establishing connections between entities.
- **RAG (Retrieval-Augmented Generation)**: Answering queries with enriched contextual data.

The backend interacts with a separate Next.js frontend application to visualize outputs like relationships on a canvas.

---

## Features

- **Microservices Architecture**:

  - `main_service`: Gateway for handling API requests, coordinating entity and relationship operations, and performing AI tasks.
  - `entities_service`: Manages CRUD operations for extracted entities.
  - `relations_service`: Manages CRUD operations for relationships between entities.

- **AI Integration**:

  - Local LLMs like Phi3 for Named Entity Recognition (NER) and Llama 3.2 for RAG.
  - Pinecone for vector-based document retrieval.
  - **Structured Outputs with Pydantic and Ollama**:
    - Pydantic schemas ensure structured outputs, providing type validation and clarity in API responses.
    - **Ollama Structured Outputs**:
      - Uses `response_format` in the `client.beta.chat.completion.parse` method from the OpenAI client library.
      - Outputs adhere to predefined JSON schemas for reliable downstream processing, as demonstrated in the [Ollama Structured Outputs blog](https://ollama.com/blog/structured-outputs).

- **Scalable Design**:

  - Modular services with isolated responsibilities.
  - Dockerized setup for easy deployment.

- **Optimized Data Handling**:

  - SQLite for persistence.
  - SQLAlchemy ORM for efficient database operations.

---

## Model Selection Rationale

Given the constraints of running on an M1 Mac with 8GB RAM, the selected models are Phi3 for Named Entity Recognition (NER) and Llama 3.2 for Retrieval-Augmented Generation (RAG). These models are lightweight and can run locally without requiring extensive computational resources. However, their performance is below average compared to larger models like GPT-4, and this trade-off ensures feasibility within the hardware limitations.

---

## Architecture

### Microservices

1. **Main Service**:

   - Acts as the gateway for the backend.
   - Coordinates between `entities_service` and `relations_service`.
   - Handles AI tasks like entity extraction and RAG.

2. **Entities Service**:

   - Stores and retrieves extracted entities.
   - CRUD operations for entities like Persons, Locations, Vehicles.

3. **Relations Service**:

   - Manages relationships between entities.
   - Supports queries by relationship type or associated input text.

---

## Directory Structure

```
.
├── README.md
├── docker-compose.yaml
├── entities_service
│   ├── Dockerfile
│   ├── application
│   │   ├── __init__.py
│   │   ├── api.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── services
│   │       ├── emails.py
│   │       ├── entities.py
│   │       ├── events.py
│   │       ├── locations.py
│   │       ├── persons.py
│   │       ├── phone_numbers.py
│   │       └── vehicles.py
│   ├── main.py
│   └── requirements.txt
├── main_service
│   ├── Dockerfile
│   ├── README.md
│   ├── application
│   │   ├── __init__.py
│   │   ├── api.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── prompts
│   │   │   ├── entities.py
│   │   │   ├── rag.py
│   │   │   └── relations.py
│   │   ├── schema
│   │   │   ├── entities.py
│   │   │   ├── rag.py
│   │   │   └── relations.py
│   │   ├── services
│   │   │   ├── entities.py
│   │   │   ├── input.py
│   │   │   ├── rag.py
│   │   │   ├── relations.py
│   │   │   └── services_check.py
│   │   └── utils
│   │       ├── llm_client.py
│   │       └── pinecone.py
│   ├── main.py
│   └── requirements.txt
└── relations_service
    ├── Dockerfile
    ├── README.md
    ├── application
    │   ├── __init__.py
    │   ├── api.py
    │   ├── config.py
    │   ├── database.py
    │   ├── models.py
    │   └── services
    │       └── relations.py
    ├── main.py
    └── requirements.txt
```

---

## Installation and Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/trishulam/S2T.git
   cd S2T
   ```

2. **Install Docker** (if not already installed):

   - [Docker Installation Guide](https://docs.docker.com/get-docker/)

3. **Run the Application**:

   ```bash
   docker-compose up --build
   ```

4. **Verify Services**:

   - Main Service: `http://localhost:8080`
   - Entities Service: `http://localhost:5001`
   - Relations Service: `http://localhost:5002`

---

## API Endpoints

### Main Service

- `GET /`: Health check for the main service.
- `GET /check_services`: Verifies connectivity with `entities_service` and `relations_service`.
- `POST /parse_entities`: Extract entities using the LLM. Requires:
  - `user_message`: The text to analyze.
  - `provider`: The LLM provider (`llama` or `openai`).
- `GET /get_entities`: Retrieve all entities from the database.
- `GET /get_entities/<input_text_id>`: Retrieve entities for a specific input text.
- `POST /parse_relations`: Extract relationships from a given input text ID. Requires:
  - `input_text_id`: ID of the input text.
  - `provider`: The LLM provider (`llama` or `openai`).
- `GET /get_relations`: Retrieve all relationships from the database.
- `GET /get_relations/<input_text_id>`: Retrieve relationships for a specific input text.
- `GET /get_relations_by_type`: Retrieve relationships filtered by type. Requires:
  - `type`: Type of the relationship.
- `GET /get_all_inputs`: Retrieve all input texts from the database.
- `POST /rag`: Perform a RAG query. Requires:
  - `query`: The question to ask.
  - `provider`: The LLM provider (`llama` or `openai`).

### Entities Service

- `GET /entities/hello`: Health check for the `entities_service`.
- `POST /entities/save`: Save extracted entities to the database. Requires:
  - `entities`: List of entities.
  - `input_text_id`: Identifier for the input text.
- `GET /entities/get`: Retrieve all entities.
- `GET /entities/get/<input_text_id>`: Retrieve entities for a specific input text.

### Relations Service

- `GET /relations/hello`: Health check for the `relations_service`.
- `POST /relations/save`: Save extracted relationships to the database. Requires:
  - `relations`: List of relationships.
  - `input_text_id`: Identifier for the input text.
- `GET /relations/get`: Retrieve all relationships.
- `GET /relations/get_by_input_text_id`: Retrieve relationships for a specific input text. Requires:
  - `input_text_id`: Identifier for the input text.
- `GET /relations/get_by_type`: Retrieve relationships filtered by type. Requires:
  - `type`: Type of the relationship to filter.

---