from flask import Blueprint
from flask import jsonify
from flask import request

from services.event_consumer.handlers.event_handler import process_event

events_bp = Blueprint("events", __name__)


@events_bp.post("/events")
def events():

    request_json = request.get_json()

    process_event(
        request_json["message"]
    )

    return jsonify(
        {
            "status": "SUCCESS"
        }
    ), 200