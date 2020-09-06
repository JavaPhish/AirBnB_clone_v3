#!/usr/bin/python3
"""import app_views State views
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET', 'POST', 'DELETE', 'PUT'])
def states():
    json_repr = []
    for v in storage.all(State).values():
        json_repr.append(v.to_dict())
        if request.method == 'POST':
            state = request.get_json()
            return state
    return jsonify(json_repr)


@app_views.route('/states/<state_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def states_id(state_id):
    selected_state = storage.get(State, state_id)
    if selected_state is not None:
        if request.method == 'GET':
            return selected_state.to_dict()
        if request.method == 'DELETE':
            selected_state.delete()
            return jsonify({}), 200
    else:
        abort(404)
