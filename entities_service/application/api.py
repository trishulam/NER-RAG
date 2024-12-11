# from application.models import *
from flask import jsonify, request
from main import app
from application.services.entities import save_entities, get_entities, get_entities_by_input_text_id

@app.route('/entities/hello', methods=['GET'])
def hello_entities():
    return jsonify({"message": "Hello from Entities Service!"}), 200

@app.route('/entities/save', methods=['POST'])
def entities_save():
    """
    Save the extracted entities to the database.
    """
    try:
        print("Saving entities to the database")
        entities = request.get_json().get("entities", [])
        input_text_id = request.get_json().get("input_text_id", None)

        save_entities(entities, input_text_id)

        return jsonify({"message": "Entities saved successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/entities/get', methods=['GET'])
def entities_get():
    """
    Get the all entities from the database.
    """
    try:
        entities = get_entities()
        return jsonify(entities), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/entities/get/<input_text_id>', methods=['GET'])
def entities_get_by_input_text_id(input_text_id):
    """
    Get the all entities from the database.
    """
    try:
        entities = get_entities_by_input_text_id(input_text_id)
        return jsonify(entities), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    

