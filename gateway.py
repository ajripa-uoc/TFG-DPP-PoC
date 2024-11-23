from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from flask_cors import CORS
from main_functions import get_dpp_history, get_dpp_first, get_dpp_last, add_dpp, update_dpp
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Helper function for date validation
def validate_date(value):
    try:
        # Parse the date string
        return int(datetime.strptime(value, '%Y-%m-%d').timestamp())
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD")

# Initialize Flask-RESTx
api = Api(app, version="1.0", title="Digital Product Passport API", description="API for managing Digital Product Passports", doc="/docs", prefix="/api")

# Namespace for DPP
dpp_ns = api.namespace("dpp", description="Operations related to Digital Product Passports")

# Models for Swagger (used for request/response validation)
dpp_model = api.model("Digital Product Password", {
    "companyName": fields.String(required=True, description="Company Name"),
    "productType": fields.String(required=True, description="Type of Product"),
    "productDetail": fields.String(required=True, description="Details about the product"),
    "manufactureDate": fields.String(required=True, description="Manufacture date in YYYY-MM-DD format")
})

# Response model for CreateDPP
dpp_response_model = api.model("DPP Response", {
   "dppId": fields.String(description="DPP identifier returned by the smart contract")
})

update_dpp_model = api.model("Update DPP", {
    "dppId": fields.Integer(required=True, description="Unique Identifier for the DPP"),
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
    @api.doc(params={"dppId": "Unique Identifier for the DPP"})
    def get(self):
        """Get the history of a DPP by its ID"""
        dpp_id = request.args.get("dppId")
        if not dpp_id:
            api.abort(400, "Missing 'dppId' query parameter")
        try:
            dpp = get_dpp_history(int(dpp_id))
            return jsonify(dpp)
        except Exception as e:
            api.abort(500, str(e))


@dpp_ns.route("/first")
class DPPFirst(Resource):
    @api.doc(params={"dppId": "Unique Identifier for the DPP"})
    def get(self):
        """Get the first record of a DPP by its ID"""
        dpp_id = request.args.get("dppId")
        if not dpp_id:
            api.abort(400, "Missing 'dppId' query parameter")
        try:
            dpp = get_dpp_first(int(dpp_id))
            return jsonify(dpp)
        except Exception as e:
            api.abort(500, str(e))


@dpp_ns.route("/last")
class DPPLast(Resource):
    @api.doc(params={"dppId": "Unique Identifier for the DPP"})
    def get(self):
        """Get the last record of a DPP by its ID"""
        dpp_id = request.args.get("dppId")
        if not dpp_id:
            api.abort(400, "Missing 'dppId' query parameter")
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

        # Convert date string to timestamp
        manufactureTimestamp = validate_date(json_data["manufactureDate"])
        try:
            dpp = add_dpp(
                json_data["companyName"],
                json_data["productType"],
                json_data["productDetail"],
                manufactureTimestamp
            )
            return {"dppId": str(dpp)}, 200
        except Exception as e:
            api.abort(500, str(e))


@dpp_ns.route("/update")
class UpdateDPP(Resource):
    @api.expect(update_dpp_model)
    @api.response(200, "Success", transaction_response)
    def put(self):
        """Update an existing DPP"""
        json_data = request.get_json()

        # Convert date string to timestamp
        manufactureTimestamp = validate_date(json_data["manufactureDate"])
        try:
            dpp = update_dpp(
                int(json_data["dppId"]),
                json_data["companyName"],
                json_data["productType"],
                json_data["productDetail"],
                manufactureTimestamp
            )
            if dpp:
                return {
                    'status': 'success',
                    'transaction': {
                        'transaction_hash': dpp['transactionHash'].hex(),
                        'block_number': dpp['blockNumber']
                    }
                }, 200
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
