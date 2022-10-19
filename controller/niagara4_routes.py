# type: ignore
import marshmallow
from datetime import datetime, timedelta
from typing import Tuple, Dict, Any
from werkzeug import Response
from services.niagara4_service import get_all_sites
from flask import jsonify, request
from app import app
from common.exceptions import (
    ResourceConflictError,
    ResourceNotFound,
    AuthenticationError,
)
from controller.common import login_required
from services.device_service import create_history_for_device
from serializers.user_serializers import (
    history_schema,
    get_history_schema,
    post_history_schema,
)
from models.history import History


@app.route("/sites", methods=["GET", "POST"])
@login_required
def sites() -> Tuple[Response, int]:
    buildings = get_all_sites()
    return jsonify(dict(names=list(buildings.keys())))


@app.route("/history/<string:device_name>", methods=["POST", "GET"])
@login_required
def history_for_device(device_name) -> Tuple[Response, int]:
    if request.method == "POST":
        create_history_for_device(device_name)

    history = History.get_device_history(device_name)

    result = history_schema.dump(history)
    return jsonify(result), 200


@app.route("/history", methods=["GET"])
def get_history() -> Tuple[Response, int]:
    try:
        scehma = get_history_schema.load(_get_history_schema())
        history = History.get_history(**scehma)
        result = history_schema.dump(history)
    except KeyError:
        return jsonify(error="please select Device ID"), 400

    return jsonify(result), 200


@app.route("/history", methods=["POST"])
def create_history() -> Tuple[Response, int]:
    try:
        scehma = post_history_schema.load(request.json)
        history = History.create_device_history(scehma)
        result = history_schema.dump(history)
    except marshmallow.exceptions.ValidationError as error:
        return jsonify(error=error.messages), 400
    except KeyError:
        return jsonify(error="please select Device ID"), 400

    return jsonify(result), 204


def _get_history_schema() -> Dict[str, Any]:
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    point_id = request.args["point_id"]
    from_time = request.args.get("from_time", str(yesterday.date()))
    to_time = request.args.get("to_time", str(now.date()))
    return dict(point_id=point_id, from_time=from_time, to_time=to_time)


@app.route("/building/<string:building_id>/utility", methods=["GET"])
def fake_data(building_id) -> Tuple[Response, int]:
    """TODO: remove """
    from tests.mock_data.point_history_2 import point_2
    from tests.mock_data.point_history_1 import point_1

    device_res = {
        "device_type": "Electric",
        "name": "HVAC",
        "unit": "kwh",
        "points": [{"point_1": point_1}, {"point_2": point_2}],
    }
    res = {"electric": [{"device1": device_res}]}

    return jsonify(res), 200
