#!/usr/bin/python3
"""import app_views State views
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State

@app_views.route('/states/', methods=['GET', 'POST', 'DELETE', 'PUT'])
def states():
    json_repr = []
    if request.method == 'POST':
        if request.get_json():
            if 'name' in request.get_json().keys():
                new_state_instance = State()
                new_state_instance.name = request.get_json().get('name')
                new_state_instance.save()
                storage.save()
                return jsonify(new_state_instance.to_dict()), 201
            else:
                abort(400, "Missing name")
        else:
            abort(400, "Not a JSON")
    for v in storage.all(State).values():
        json_repr.append(v.to_dict())
    return jsonify(json_repr)


@app_views.route('/states/<state_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def states_id(state_id):
    selected_state = storage.get(State, state_id)
    if selected_state is not None:
        if request.method == 'GET':
            return selected_state.to_dict()
        if request.method == 'DELETE':
            selected_state.delete()
            storage.save()
            return jsonify({}), 200
    else:
        abort(404)
