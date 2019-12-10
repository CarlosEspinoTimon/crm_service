from flask import jsonify

def check_schema(data, schema):
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
