from flask import jsonify, request
from application.services.relations import save_relationships, get_relationships, get_relationships_by_input_text_id, get_relationships_by_type
from main import app

@app.route('/relations/hello', methods=['GET'])
def hello_entities():
    return jsonify({"message": "Hello from Relations Service!"}), 200

@app.route('/relations/save', methods=['POST'])
def save_relations():
    """
    Save the extracted relationships to the database.
    """
    print("Saving relationships")
    relations = request.get_json().get("relations", [])
    input_text_id = request.get_json().get("input_text_id", "")
    response = save_relationships(relations, input_text_id)
    if response:
        return jsonify({"message": "Relationships saved successfully"}), 200
    else:
        return jsonify({"error": "Failed to save relationships"}), 500

@app.route('/relations/get', methods=['GET'])
def get_relations():
    """
    Get all relationships from the database.
    """
    print("Getting relationships")
    relationships = get_relationships()
    return jsonify(relationships), 200

@app.route('/relations/get_by_input_text_id', methods=['GET'])
def get_relations_by_input_text_id():
    """
    Get all relationships by input text id from the database.
    """
    input_text_id = request.args.get("input_text_id", "")
    print("Getting relationships by input text id")
    relationships = get_relationships_by_input_text_id(input_text_id)
    return jsonify(relationships), 200

@app.route('/relations/get_by_type', methods=['GET'])
def get_relations_by_type():
    """
    Get all relationships by type from the database.
    """
    relation_type = request.args.get("type", "")
    print("Getting relationships by type")
    relationships = get_relationships_by_type(relation_type)
    return jsonify(relationships), 200

