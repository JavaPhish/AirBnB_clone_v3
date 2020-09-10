#!/usr/bin/python3
"""import app_views Places views
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['GET'])
def all_places_in_city(city_id):
    """get all places in city
    """

    """ Fetches the city by ID and class """
    selected_city = storage.get(City, city_id)
    json_repr = []
    if selected_city is not None:
        """ Loop through all places and search for all matching
            city IDs
        """
        for v in storage.all(Place).values():
            if v.city_id == city_id:
                json_repr.append(v.to_dict())
        """ JSON the output then respond """
        return make_response(jsonify(json_repr))
    abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['GET'])
def get_place(place_id):
    """get place by id
    """
    selected_place = storage.get(Place, place_id)
    if selected_place is not None:
        """ if the get actually returned a value, JSONIFY it 
            and respond with it
        """
        return make_response(jsonify(selected_place.to_dict()))
    """ if we made it here, no relevent data was found, return 404 """
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """delete state by id
    """
    selected_place = storage.get(Place, place_id)
    if selected_place is not None:
        if request.method == 'DELETE':
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
            data = request.get_json()
            if data is None:
                return make_response(jsonify(error="Not a JSON"), 400)

            if 'user_id' not in data.keys():
                return make_response(jsonify(error="Missing user_id"), 400)

            if 'name' not in data.keys():
                return make_response(jsonify(error="Missing name"), 400)

            user_id = data.get('user_id')
            get_user = storage.get(User, user_id)
            if get_user is None:
                abort(404)

            if 'user_id' and 'name' in data.keys():
                new_place = Place()
                for name, value in data.items():
                    if hasattr(new_place, name):
                        setattr(new_place, name, value)
                new_place.city_id = city_id
                new_place.save()
                return make_response(jsonify(new_place.to_dict()), 201)
    else:
        abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['PUT'])
def put_place(place_id):
    """Update place
    """
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    selected_place = storage.get(Place, place_id)
    if selected_place is not None:
        if request.method == 'PUT':
            data = request.get_json()

            if data is None:
                return make_response(jsonify(error="Not a JSON"), 400)

            for name, value in data.items():
                if name not in ignore_keys and hasattr(selected_place, name):
                    setattr(selected_place, name, value)
                    selected_place.save()
                    put_response = jsonify(selected_place.to_dict())
                    return make_response(put_response, 200)
    else:
        abort(404)
