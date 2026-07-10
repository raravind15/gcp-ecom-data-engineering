from flask import Blueprint, jsonify, request

from services.platform_jobs.handlers.run_procedure import execute
from shared.core.logger import get_logger

logger = get_logger(__name__)

run_procedure_bp = Blueprint("run_procedure", __name__)


@run_procedure_bp.post("/run-procedure")
def run_procedure():

    request_json = request.get_json(silent=True) or {}

    dataset = request_json.get("dataset")
    procedure_name = request_json.get("procedure_name")

    if not dataset or not procedure_name:

        return (
            jsonify(
                {
                    "status": "FAILED",
                    "message": "dataset and procedure_name are mandatory."
                }
            ),
            400,
        )

    try:

        response = execute(dataset, procedure_name)

        return jsonify(response), 200

    except ValueError as ex:

        logger.error(str(ex))

        return (
            jsonify(
                {
                    "status": "FAILED",
                    "message": str(ex)
                }
            ),
            400,
        )

    except Exception:

        logger.exception("Unexpected Error")

        return (
            jsonify(
                {
                    "status": "FAILED",
                    "message": "Internal Server Error"
                }
            ),
            500,
        )