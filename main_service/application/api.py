from flask import Flask, jsonify, request
from main import app
from application.prompts.entities import *
from application.schema.entities import *
from application.utils.llm_client import LLMClient
from application.services.entities import extract_entities, check_for_entities, send_to_entities_service, entities_get, entities_get_by_input_text_id
from application.services.relations import extract_relations, check_for_relations, send_to_relations_service, get_relationships_by_input_text_id, get_relationships_by_type, get_relationships
from application.services.input import save_input_text, get_input_text_by_id, get_all_input_texts
from application.config import LLAMA_URL
from application.services.rag import add_document, query_documents, call_model
from application.services.services_check import services_check
import requests
from dotenv import load_dotenv
import os

load_dotenv()

@app.route('/', methods=['GET'])
def hello_main():
    """
    A simple hello world route for the main service.
    """
    return jsonify({"message": "Hello from Main Service!"}), 200

@app.route('/check_services', methods=['GET'])
def check_services():
    """
    Check if other services are reachable by calling their /hello endpoints.
    """
    try:
        response = services_check()
        return jsonify(response), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to connect to one or more services: {str(e)}"}), 500

@app.route('/parse_entities', methods=['POST'])
def parse_entities():
    """
    Call the LLM model to extract entities from a given text.
    """
    user_message = request.get_json().get("user_message", "")
    provider = request.get_json().get("provider", "llama")
    print(provider)

    if provider == "openai":
        llm_client = LLMClient(
            base_url="",
            model="gpt-4o-mini",
            provider="openai",
        )
    else:
        llm_client = LLMClient(
            base_url=f"http://{LLAMA_URL}:11434/v1",
            model="phi3",
            provider="llama",
        )

    try:
        check_entities_response = check_for_entities(user_message, llm_client)
        print("Checked for entities")
        print(check_entities_response)
        response = extract_entities(user_message, llm_client, check_entities_response)
        print("Extracted entities")
        print(response)
        input_text_id=save_input_text(user_message)
        print(add_document(str(input_text_id), user_message))
        send_to_entities_service(response, input_text_id)
        final_response = {
            "entities": response,
            "input_text_id": input_text_id
        }
        return jsonify(final_response), 200

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/get_entities', methods=['GET'])
def get_entities():
    """
    Get all entities from the database.
    """
    try:
        print("Getting entities from the database")
        entities = entities_get()
        return jsonify(entities), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/get_entities/<input_text_id>', methods=['GET'])
def get_entities_by_input_text_id(input_text_id):
    """
    Get all entities from the database.
    """
    try:
        print("Getting entities from the database")
        entities = entities_get_by_input_text_id(input_text_id)
        return jsonify(entities), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/parse_relations', methods=['POST'])
def parse_relations():
    """
    Call the LLM model to extract relationships from a given input text id
    """
    input_text_id = request.get_json().get("input_text_id", "")
    provider = request.get_json().get("provider", "llama")
    print(input_text_id)
    print(provider)

    user_text = get_input_text_by_id(input_text_id)

    entities = entities_get_by_input_text_id(input_text_id)
    
    # return entities
    if provider == "openai":

        llm_client = LLMClient(
            base_url="",
            model="gpt-4o-mini",
            provider="openai",
        )
    else:
        llm_client = LLMClient(
            base_url=f"http://{LLAMA_URL}:11434/v1",
            model="phi3",
            provider="llama",
        )

    try:
        check_relations_response = check_for_relations(user_text, llm_client, entities)
        print("Checked for relations")
        print(check_relations_response)
        response = extract_relations(user_text, llm_client, check_relations_response, entities)
        print("Extracted relations")   
        send_to_relations_service(response, input_text_id)
        return jsonify(response), 200

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_relations', methods=['GET'])
def get_relations():
    """
    Get all relationships from the database.
    """
    try:
        print("Getting relationships from the database")
        relationships = get_relationships()
        return jsonify(relationships), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/get_relations/<input_text_id>', methods=['GET'])
def get_relations_by_input_text_id(input_text_id):
    """
    Get all relationships from the database.
    """
    try:
        print("Getting relationships from the database")
        relationships = get_relationships_by_input_text_id(input_text_id)
        return jsonify(relationships), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/get_relations_by_type', methods=['GET'])
def get_relations_by_type():
    """
    Get all relationships by type from the database.
    """
    relation_type = request.get_json().get("type", "")
    try:
        print("Getting relationships by type from the database")
        relationships = get_relationships_by_type(relation_type)
        return jsonify(relationships), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/get_all_inputs', methods=['GET'])
def get_all_inputs():
    """
    Get all input texts from the database.
    """
    try:
        print("Getting input texts from the database")
        inputs = get_all_input_texts()
        return jsonify(inputs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/rag', methods=['POST'])
def rag():
    """
    Call the RAG model to generate a response for a given query.
    """
    query = request.get_json().get("query", "")
    provider = request.get_json().get("provider", "openai")
    try:
        results = query_documents(query)
        input_text_id = results['matches'][0]['id']
        text= get_input_text_by_id(input_text_id)
        entities=entities_get_by_input_text_id(input_text_id)
        relationships=get_relationships_by_input_text_id(input_text_id)
        response = call_model(query, text, entities, relationships, provider)
        response = response.dict()
        response['document']=text
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500