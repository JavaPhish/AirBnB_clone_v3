#!/usr/bin/python3
"""import app_views State views
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'])
def all_states():
    """get all state instance json format
    """
    if request.method == 'GET':
        json_repr = []
        for v in storage.all(State).values():
            json_repr.append(v.to_dict())
        return make_response(jsonify(json_repr))


@app_views.route('/states/', methods=['POST'])
def post_state():
    """Post or make new states
    """
    if request.method == 'POST':
        try:
            data = request.get_json()
        except Exception:
            error_message = jsonify(error="Not a JSON")
            return make_response(error_message, 400)

        if data is not None:
            if 'name' in request.get_json().keys():
                new_state_instance = State()
                new_state_instance.name = request.get_json().get('name')
                new_state_instance.save()
                post_response = jsonify(new_state_instance.to_dict())
                return make_response(post_response, 201)
            else:
                error_message = jsonify(error="Missing name")
                return make_response(error_message, 400)


@app_views.route('/states/<state_id>', methods=['GET'])
def one_state(state_id):
    """get one state by id
    """
    if request.method == 'GET':
        selected_state = storage.get(State, state_id)
        if selected_state is not None:
            return make_response(jsonify(selected_state.to_dict()))
        else:
            abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """delete state by id
    """
    if request.method == 'DELETE':
        selected_state = storage.get(State, state_id)
        if selected_state is not None:
            selected_state.delete()
            storage.save()
            empty_dict = {}
            return make_response(jsonify(empty_dict), 200)
        else:
            abort(404)


@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state(state_id):
    if request.method == 'PUT':
        try:
            data = request.get_json()
        except Exception:
            error_message = jsonify(error="Not a JSON")
            return make_response(error_message, 400)

        selected_state = storage.get(State, state_id)
        if selected_state is not None:
            ignore_keys = ['id', 'created_at', 'updated_at']
            if data is not None:
                for name, value in request.get_json().items():
                    if name not in ignore_keys:
                        try:
                            setattr(selected_state, name, value)
                            selected_state.save()
                            put_response = jsonify(selected_state.to_dict())
                            return make_response(put_response, 200)
                        except Exception:
                            put_response = jsonify(error="Not an attribute")
                            return make_response(put_response, 200)
        else:
            abort(404)
