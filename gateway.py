from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from flask_cors import CORS
from main_functions import get_dpp_history, get_dpp_first, get_dpp_last, add_dpp, update_dpp
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Initialize Flask-RESTx
api = Api(app, version="1.0", title="DPP API", description="API for managing Digital Product Passports", doc="/docs")

# Namespace for DPP
dpp_ns = api.namespace("dpp", description="Operations related to Digital Product Passports")

# Models for Swagger (used for request/response validation)
dpp_model = api.model("Digital Product Password", {
    "companyName": fields.String(required=True, description="Company Name"),
    "productType": fields.String(required=True, description="Type of Product"),
    "productDetail": fields.String(required=True, description="Details about the product"),
    "manufactureDate": fields.String(required=True, description="Manufacture date in YYYY-MM-DD format")
})

update_dpp_model = api.model("Updat DPP", {
    "id": fields.Integer(required=True, description="Unique Identifier for the DPP"),
    "companyName": fields.String(required=True, description="Company Name"),
    "productType": fields.String(required=True, description="Type of Product"),
    "productDetail": fields.String(required=True, description="Details about the product"),
    "manufactureDate": fields.String(required=True, description="Manufacture date in YYYY-MM-DD format")
})

transaction_response = api.model("Transaction Response", {
    "status": fields.String(description="Status of the operation"),
    "transaction": fields.Nested(api.model("Transaction", {
        "transaction_hash": fields.String(description="Transaction hash"),
        "block_number": fields.Integer(description="Block number")
    }))
})


@dpp_ns.route("/history")
class DPPHistory(Resource):
    @api.doc(params={"id": "Unique Identifier for the DPP"})
    def get(self):
        """Get the history of a DPP by its ID"""
        dpp_id = request.args.get("id")
        if not dpp_id:
            api.abort(400, "Missing 'id' query parameter")
        try:
            dpp = get_dpp_history(int(dpp_id))
            return jsonify(dpp)
        except Exception as e:
            api.abort(500, str(e))


@dpp_ns.route("/first")
class DPPFirst(Resource):
    @api.doc(params={"id": "Unique Identifier for the DPP"})
    def get(self):
        """Get the first record of a DPP by its ID"""
        dpp_id = request.args.get("id")
        if not dpp_id:
            api.abort(400, "Missing 'id' query parameter")
        try:
            dpp = get_dpp_first(int(dpp_id))
            return jsonify(dpp)
        except Exception as e:
            api.abort(500, str(e))


@dpp_ns.route("/last")
class DPPLast(Resource):
    @api.doc(params={"id": "Unique Identifier for the DPP"})
    def get(self):
        """Get the last record of a DPP by its ID"""
        dpp_id = request.args.get("id")
        if not dpp_id:
            api.abort(400, "Missing 'id' query parameter")
        try:
            dpp = get_dpp_last(int(dpp_id))
            return jsonify(dpp)
        except Exception as e:
            api.abort(500, str(e))


@dpp_ns.route("")
class CreateDPP(Resource):
    @api.expect(dpp_model)
    def post(self):
        """Create a new DPP"""
        json_data = request.get_json()
        try:
            dpp = add_dpp(
                json_data["companyName"],
                json_data["productType"],
                json_data["productDetail"],
                json_data["manufactureDate"]
            )
            return jsonify(dpp), 201
        except Exception as e:
            api.abort(500, str(e))


@dpp_ns.route("/update")
class UpdateDPP(Resource):
    @api.expect(update_dpp_model)
    @api.response(200, "Success", transaction_response)
    def put(self):
        """Update an existing DPP"""
        json_data = request.get_json()
        try:
            dpp = update_dpp(
                int(json_data["id"]),
                json_data["companyName"],
                json_data["productType"],
                json_data["productDetail"],
                json_data["manufactureDate"]
            )
            if dpp:
                return jsonify({
                    'status': 'success',
                    'transaction': {
                        'transaction_hash': dpp['transactionHash'].hex(),
                        'block_number': dpp['blockNumber']
                    }
                })
            else:
                return jsonify({"status": "error", "error": "Transaction failed"}), 400
        except Exception as e:
            api.abort(500, str(e))


# Health check endpoint
@dpp_ns.route("/healthz")
class HealthCheck(Resource):
    def get(self):
        """Health check endpoint"""
        return ({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
