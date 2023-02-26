import jsonschema
import datetime
import base64

from flask import Blueprint
from flask import request

from tasks.worker import aggregator

urls_api = Blueprint('simple_page', __name__)

payload_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["device_id", "client_id", "data"],
    "properties": {
        "device_id": {
            "type": "string"
        },
        "client_id": {
            "type": "string"
        },
        "created_at": {
            "type": "string"
        },
        "data": {
            "type": "object",
            "required": ["license_id", "preds"],
            "properties": {
                "license_id": {
                    "type": "string"
                },
                "preds": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "image_frame": {
                                "type": "string"
                            },
                            "prob": {
                                "type": "number"
                            },
                            "tags": {
                                "type": "array",
                            }
                        }
                    }

                }
            }
        }
    }
}


def is_datetime(instance):
    try:
        datetime.datetime.strptime(instance, '%Y-%m-%d %H:%M:%S.%f')
        return True
    except ValueError:
        return False


def is_base64(instance):
    try:
        base64.b64decode(instance)
        return True
    except ValueError:
        return False


@urls_api.route('/')
def index():
    return 'Use /executor api'


def additional_checks(check_types):
    for check_type in check_types:
        func = check_type[0]
        value = check_type[1]
        if isinstance(value, list):
            for v in value:
                if not func(v):
                    raise ValueError(
                        'Value {} is not {}'.format(v, func.__name__))
        else:
            if not func(value):
                raise ValueError(
                    'Value {} is not {}'.format(value, func.__name__))


@urls_api.route('/executor', methods=['POST'])
def validator_executor():
    payload = request.get_json()
    try:
        jsonschema.validate(payload, payload_schema)
        image_frames = [pred['image_frame']
                        for pred in payload['data']['preds']]
        additional_checks([
            [is_datetime, payload['created_at']],
            [is_base64, image_frames]
        ])
    except Exception as e:
        return str(e), 422
    aggregator.delay(payload)
    return "Entity being processed", 202
