from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from flask_cors import CORS
from main_functions import get_dpp_history, get_dpp_first, get_dpp_last, add_dpp, update_dpp
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Helpers
# Helper function for date validation
def validate_date(value):
    try:
        # Parse the date string
        return int(datetime.strptime(value, '%Y-%m-%d').timestamp())
    except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD")


# Helper function to convert DPP tuple to structured JSON
def process_dpp_data(dpp):
    if isinstance(dpp, tuple):
        # If it's a single tuple, wrap it in a list for uniform processing
        dpp = [dpp]

    #Convert DPP tuple to structured JSON
    return [{
        "companyName": dpp_tuple[0],
        "productType": dpp_tuple[1],
        "productDetail": dpp_tuple[2],
        "manufactureDate": datetime.fromtimestamp(dpp_tuple[3]).strftime('%Y-%m-%d'),
        "allowedAddresses": dpp_tuple[4],
        "isMerged": dpp_tuple[5],
        "mergedFrom": dpp_tuple[6]
    }
    for dpp_tuple in dpp]

# Initialize Flask-RESTx
api = Api(app,
        version="1.0",
        title="Digital Product Passport API",
        description="API for managing Digital Product Passports",
        doc="/docs",
        prefix="/api")

# Namespace for DPP
dpp_ns = api.namespace("dpp", description="Operations related to Digital Product Passports")

# Models for Swagger (used for request/response validation)
dpp_create_model = api.model("CreateDPP", {
    "companyName": fields.String(required=True, description="Company Name", example="Apple"),
    "productType": fields.String(required=True, description="Type of Product", example="iPhone"),
    "productDetail": fields.String(required=True, description="Details about the product", example="iPhone 12 Pro"),
    "manufactureDate": fields.String(required=True, description="Manufacture date in YYYY-MM-DD format", example="2021-01-01")
})

dpp_update_model = api.model("UpdateDPP", {
    "companyName": fields.String(required=True, description="Company Name", example="Apple"),
    "productType": fields.String(required=True, description="Type of Product", example="iPhone"),
    "productDetail": fields.String(required=True, description="Details about the product", example="Battery change"),
    "manufactureDate": fields.String(required=True, description="Manufacture date in YYYY-MM-DD format", example="2024-01-01")
})

dpp_event_response_model = api.model("DPPEvent", {
    "companyName": fields.String(description="Company Name"),
    "productType": fields.String(description="Type of Product"),
    "productDetail": fields.String(description="Details about the product"),
    "manufactureDate": fields.String(description="Manufacture date in YYYY-MM-DD format"),
    "allowedAddresses": fields.List(fields.String, description="List of allowed addresses"),
    "isMerged": fields.Boolean(description="Whether the DPP is merged"),
    "mergedFrom": fields.List(fields.String, description="List of DPP IDs this was merged from")
},description="DPP event details")

dpp_events_list_response_model = api.model("DPPEventsList", {
    "events": fields.List(fields.Nested(dpp_event_response_model), description="List of DPP records")
})

dpp_create_response_model = api.model("CreateDPPResponse", {
   "dppId": fields.String(description="DPP identifier returned by the smart contract")
})

dpp_update_response_model = api.model("UpdateDppResponse", {
    "status": fields.String(description="Status of the operation"),
    "transaction": fields.Nested(api.model("Transaction", {
        "transaction_hash": fields.String(description="Transaction hash"),
        "block_number": fields.Integer(description="Block number")
    }))
})

# Routes
@dpp_ns.route("/<string:dppId>/history")
class DPPHistory(Resource):
    @api.doc(params={"dppId": "Unique Identifier for the DPP"})
    @api.response(200, "Success", dpp_events_list_response_model)
    def get(self, dppId):
        if not dppId:
            api.abort(400, "Missing 'dppId' parameter")
        try:
            dpp = get_dpp_history(int(dppId))
            return jsonify({"events": process_dpp_data(dpp)})
        except Exception as e:
            api.abort(500, str(e))


@dpp_ns.route("/<string:dppId>/first")
class DPPFirst(Resource):
    @api.doc(params={"dppId": "Unique Identifier for the DPP"})
    @api.response(200, "Success", dpp_events_list_response_model)
    def get(self, dppId):
        if not dppId:
            api.abort(400, "Missing 'dppId'  parameter")
        try:
            dpp = get_dpp_first(int(dppId))
            return jsonify({"events": process_dpp_data(dpp)})
        except Exception as e:
            api.abort(500, str(e))


@dpp_ns.route("/<string:dppId>/last")
class DPPLast(Resource):
    @api.doc(params={"dppId": "Unique Identifier for the DPP"})
    @api.response(200, "Success", dpp_events_list_response_model)
    def get(self,dppId):
        if not dppId:
            api.abort(400, "Missing 'dppId' parameter")
        try:
            dpp = get_dpp_last(int(dppId))
            return jsonify({"events": process_dpp_data(dpp)})
        except Exception as e:
            api.abort(500, str(e))

@dpp_ns.route("")
class CreateDPP(Resource):
    @api.expect(dpp_create_model)
    @api.response(200, "Success", dpp_create_response_model)
    def post(self):
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


@dpp_ns.route("/<string:dppId>")
class UpdateDPP(Resource):
    @api.expect(dpp_update_model)
    @api.response(200, "Success", dpp_update_response_model)
    @api.doc(params={"dppId": "Unique Identifier for the DPP"})
    def put(self,dppId):
        """Update an existing DPP"""
        json_data = request.get_json()

        # Convert date string to timestamp
        manufactureTimestamp = validate_date(json_data["manufactureDate"])
        try:
            dpp = update_dpp(
                int(dppId),
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
