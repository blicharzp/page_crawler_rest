import json


def build_error_message(message):
    return json.dumps({'message': message})