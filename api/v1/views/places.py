#!/usr/bin/python3
"""import app_views City views
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['GET'])
def all_places_in_city(city_id):
    """get all places in city
    """
    selected_place = storage.get(City, city_id)
    json_repr = []
    if selected_place is not None:
        if request.method == 'GET':
            for v in storage.all(Place).values():
                if v.city_id == city_id:
                    json_repr.append(v.to_dict())
            return make_response(jsonify(json_repr))
    else:
        abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['GET'])
def get_place(place_id):
    """get place by id
    """
    selected_place = storage.get(Place, place_id)
    if selected_place is not None:
        if request.method == 'GET':
            return make_response(jsonify(selected_place.to_dict()))
    else:
        abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """delete state by id
    """
    if request.method == 'DELETE':
        selected_place = storage.get(Place, place_id)
        if selected_place is not None:
            selected_place.delete()
            storage.save()
            return make_response(jsonify({}), 200)
        else:
            abort(404)


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['POST'])
def post_place(city_id):
    """post place
    """
    selected_city = storage.get(City, city_id)
    if selected_city is not None:
        if request.method == 'POST':
            if request.get_json():
                if 'user_id' not in request.get_json().keys():
                    error_message = jsonify(error="Missing user_id")
                    return make_response(error_message, 400)
                else:
                    user_id = request.get_json().get('user_id')
                    get_user = storage.get(User, user_id)
                    if get_user is None:
                        abort(404)
                if 'name' not in request.get_json().keys():
                    error_message = jsonify(error="Missing name")
                    return make_response(error_message, 400)
                new_place_instance = Place()
                new_place_instance.city_id = city_id
                new_place_instance.user_id = user_id
                new_place_instance.name = request.get_json().get('name')
                new_place_instance.save()
                new_ins_res = jsonify(new_place_instance.to_dict())
                return make_response(new_ins_res, 201)
            else:
                error_message = jsonify(error="Not a JSON")
                return make_response(error_message, 400)
    else:
        abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['PUT'])
def put_place(place_id):
    """Update place
    """
    selected_place = storage.get(Place, place_id)
    if selected_place is not None:
        if request.method == 'PUT':
            ignore_keys = [
                'id', 'user_id', 'city_id', 'created_at', 'updated_at']
            if request.get_json():
                for name, value in request.get_json().items():
                    if name not in ignore_keys:
                        if hasattr(selected_place, name):
                            setattr(selected_place, name, value)
                            selected_place.save()
                            put_response = jsonify(selected_place.to_dict())
                            return make_response(put_response, 200)
            else:
                error_message = jsonify(error="Not a JSON")
                return make_response(error_message, 400)
    else:
        abort(404)
