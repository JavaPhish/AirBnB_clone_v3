#!/usr/bin/python3
"""import app_views City views
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities(state_id):
    """get city instance
    and post new city instance
    """
    selected_state = storage.get(State, state_id)
    json_repr = []
    if selected_state is not None:
        if request.method == 'GET':
            for v in storage.all(City).values():
                if v.state_id == state_id:
                    json_repr.append(v.to_dict())
            return jsonify(json_repr), 200
        if request.method == 'POST':
            if request.get_json():
                if 'name' in request.get_json().keys():
                    new_city_instance = City()
                    new_city_instance.state_id = state_id
                    new_city_instance.name = request.get_json().get('name')
                    new_city_instance.save()
                    storage.save()
                    return jsonify(new_city_instance.to_dict()), 201
                else:
                    error_message = jsonify(error="Missing name")
                    return make_response(error_message, 400)
            else:
                error_message = jsonify(error="Not a JSON")
                return make_response(error_message, 400)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def city_id(city_id):
    """get city by id
    delete by id
    modify city instance
    """
    selected_city = storage.get(City, city_id)
    if selected_city is not None:
        if request.method == 'GET':
            return jsonify(selected_city.to_dict())
        if request.method == 'DELETE':
            selected_city.delete()
            storage.save()
            return jsonify({}), 200
        if request.method == 'PUT':
            ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
            if request.get_json():
                for name, value in request.get_json().items():
                    if name not in ignore_keys:
                        if hasattr(selected_city, name):
                            setattr(selected_city, name, value)
                            selected_city.save()
                            storage.save()
                            return jsonify(selected_city.to_dict()), 200
            else:
                error_message = jsonify(error="Not a JSON")
                return make_response(error_message, 400)
    else:
        abort(404)
