from flask import Flask, request, jsonify
from main_functions import get_dpp_history, get_dpp_first, get_dpp_last, add_dpp, update_dpp
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

#
# These are the endpoints for the frontend to call, but in real project data will come IoT devices and will be processed
#

# Get the dpp history by dpp_id
@app.route("/api/dpp/history", methods=["GET"])
def get_dpp_history_by_id():
    # Extract the dpp_id from the query parameters
    dpp_id = request.args.get("id")

    # If the dpp_id is missing, return an error
    if not dpp_id:
        return jsonify({"error": "Missing 'id' query parameter"}), 400

    # Call the get_dpp_history function from main_functions.py
    dpp = get_dpp_history(int(dpp_id))
    return jsonify(dpp), 200

# Get the first dpp by dpp_id
@app.route("/api/dpp/first", methods=["GET"])
def get_dpp_first_by_id():
    # Extract the dpp_id from the query parameters
    dpp_id = request.args.get("id")

    # If the dpp_id is missing, return an error
    if not dpp_id:
        return jsonify({"error": "Missing 'id' query parameter"}), 400

    dpp = get_dpp_first(int(dpp_id))
    return jsonify(dpp), 200

# Get the last dpp by dpp_id
@app.route("/api/dpp/last", methods=["GET"])
def get_dpp_last_by_id():
    # Extract the dpp_id from the query parameters
    dpp_id = request.args.get("id")

    # If the dpp_id is missing, return an error
    if not dpp_id:
        return jsonify({"error": "Missing 'id' query parameter"}), 400

    dpp = get_dpp_last(int(dpp_id))
    return jsonify(dpp), 200

# Create a new dpp
@app.route("/api/dpp", methods=["POST"])
def create_dpp():
    json_data = request.get_json()
    dpp = add_dpp(json_data["companyName"], json_data["productType"], json_data["productDetail"], json_data["manufactureDate"])
    return jsonify(dpp), 200

# Update an existing dpp
@app.route("/api/dpp/update", methods=["PUT"])
def update_dpp_web():
    json_data = request.get_json()
    dpp = update_dpp(int(json_data["id"]), json_data["companyName"], json_data["productType"], json_data["productDetail"], json_data["manufactureDate"])
    return jsonify(dpp), 200

# Health check endpoint
@app.route("/healthz", methods=["GET"])
def health_check():
   return jsonify({"status": "healthy"}), 200

app.run(host="0.0.0.0", debug=True)
