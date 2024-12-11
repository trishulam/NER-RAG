# Microservices-Based AI-Powered Entity Extraction and Relationship Management System

## Project Overview
This project implements a microservices architecture to extract entities and relationships from input text using an AI-powered model (LLM) and a vector database (Pinecone) for RAG (Retrieval Augmented Generation). The system is designed to parse entities like persons, vehicles, locations, and events, and map relationships between them.

### Key Features:
- **Entities Service**: Extracts entities like persons, vehicles, locations, etc., from input text.
- **Relations Service**: Maps relationships between the extracted entities.
- **Main Service**: Acts as the central API gateway, orchestrating requests to other services and handling RAG queries.

---

## Directory Structure
```plaintext
.
├── README.md               # This README file
├── docker-compose.yaml     # Docker Compose file for running all services
├── entities_service        # Handles entity extraction
│   ├── application
│   │   ├── services        # Entity-specific logic (persons, vehicles, etc.)
│   │   ├── models.py       # Database models for entities
│   │   ├── api.py          # API routes for entity service
│   │   ├── database.py     # Database configuration
│   │   ├── config.py       # Service configuration
│   └── main.py             # Entry point for the entities service
├── main_service            # Orchestrates the system and handles RAG
│   ├── application
│   │   ├── prompts         # LLM prompt templates
│   │   ├── schema          # Pydantic schemas for validation
│   │   ├── services        # Core logic for RAG, entities, etc.
│   │   ├── utils           # Utilities (LLM client, Pinecone client)
│   │   ├── api.py          # Main API routes
│   │   ├── database.py     # Database configuration
│   ├── main.py             # Entry point for the main service
├── relations_service       # Handles relationships between entities
│   ├── application
│   │   ├── services        # Logic for relationship mapping
│   │   ├── models.py       # Database models for relationships
│   │   ├── api.py          # API routes for relations service
│   └── main.py             # Entry point for the relations service
```

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Install Docker and Docker Compose
Ensure Docker and Docker Compose are installed on your machine:
- [Docker Installation Guide](https://docs.docker.com/get-docker/)
- [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

### 3. Set Up Environment Variables
Create a `.env` file in the root directory with the following:
```env
OPENAI_API_KEY=<your_openai_api_key>
PINECONE_API_KEY=<your_pinecone_api_key>
PINECONE_ENVIRONMENT=<your_pinecone_environment>
PINECONE_INDEX=<your_pinecone_index_name>
```

### 4. Build and Run the Docker Containers
Use Docker Compose to build and run all services:
```bash
docker-compose up --build
```

### 5. Access the Services
- **Main Service**: http://localhost:8080
- **Entities Service**: http://localhost:5001
- **Relations Service**: http://localhost:5002

---

## API Endpoints

### **Main Service**
| Endpoint         | Method | Description                           |
|------------------|--------|---------------------------------------|
| `/`              | GET    | Health check for the main service     |
| `/rag`           | POST   | Handle RAG queries                   |
| `/get_entities`  | POST   | Extract entities from input text     |
| `/check_services`| GET    | Check connectivity with other services|

### **Entities Service**
| Endpoint       | Method | Description                        |
|----------------|--------|------------------------------------|
| `/entities`    | POST   | Extract entities from input text  |
| `/entities/id` | GET    | Retrieve entities by input text ID|

### **Relations Service**
| Endpoint        | Method | Description                       |
|-----------------|--------|-----------------------------------|
| `/relations`    | POST   | Map relationships between entities|
| `/relations/id` | GET    | Retrieve relationships by input ID|

---

## Technologies Used
- **Programming Language**: Python 3.12
- **Web Framework**: Flask
- **Database**: SQLite (local), Pinecone (vector database)
- **AI Models**: Llama 3.2, OpenAI's `text-embedding-3-small`
- **Containerization**: Docker, Docker Compose

---

## Future Enhancements
- Add support for anomaly detection service.
- Improve RAG responses with more contextual data.
- Introduce a front-end visualization for entities and relationships.

---

## Contribution Guidelines
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit changes: `git commit -m 'Add feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

---