#!/usr/bin/python3
"""import app_views State views
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET', 'POST'])
def states():
    """get state instance
    and post new state instance
    """
    if request.method == 'GET':
        json_repr = []
        for v in storage.all(State).values():
            json_repr.append(v.to_dict())
        return make_response(jsonify(json_repr))
    if request.method == 'POST':
        if request.is_json:
            if 'name' in request.get_json().keys():
                new_state_instance = State()
                new_state_instance.name = request.get_json().get('name')
                new_state_instance.save()
                post_response = jsonify(new_state_instance.to_dict())
                return make_response(post_response, 201)
            else:
                error_message = jsonify(error="Missing name")
                return make_response(error_message, 400)
        else:
            error_message = jsonify(error="Not a JSON")
            return make_response(error_message, 400)


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def states_id(state_id):
    """get state by id
    delete by id
    modify state instance
    """
    selected_state = storage.get(State, state_id)
    if selected_state is not None:
        if request.method == 'GET':
            return make_response(jsonify(selected_state.to_dict()))
        if request.method == 'DELETE':
            selected_state.delete()
            storage.save()
            return make_response(jsonify({}), 200)
        if request.method == 'PUT':
            ignore_keys = ['id', 'created_at', 'updated_at']
            if request.is_json:
                for name, value in request.get_json().items():
                    if name not in ignore_keys:
                        if hasattr(selected_state, name):
                            setattr(selected_state, name, value)
                            selected_state.save()
                            put_response = jsonify(selected_state.to_dict())
                            return make_response(put_response, 200)
            else:
                error_message = jsonify(error="Not a JSON")
                return make_response(error_message, 400)
    else:
        abort(404)
