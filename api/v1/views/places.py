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
        """ If we found data, delete it within storage
            then tell storage to update the changes.
            After that, return a 200 indicating it worked
        """
        selected_place.delete()
        storage.save()
        return make_response(jsonify({}), 200)

    """ Only reaches here if nothing was found (So 404
        to make the user feel inferior
    """
    abort(404)


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=['POST'])
def post_place(city_id):
    """ post or create a new place in storage """
    selected_city = storage.get(City, city_id)
    if selected_city is not None:

        """ Ensure the json is valid (or exists to begin with) """
        data = request.get_json()
        if data is None:
            return make_response(jsonify(error="Not a JSON"), 400)

        """ The next if statements validate that required keys are present """
        if 'user_id' not in data.keys():
            return make_response(jsonify(error="Missing user_id"), 400)

        if 'name' not in data.keys():
            return make_response(jsonify(error="Missing name"), 400)

        """ Get the user, if it returns none, it doesnt exist (Return 404) """
        user_id = data.get('user_id')
        get_user = storage.get(User, user_id)
        if get_user is None:
            abort(404)

        """ if all data is present, create the new place
            object, fill in data and tell the storage engine
            to update (via .save(), return 201 on success
        """
        if 'user_id' and 'name' in data.keys():
            new_place = Place()
            for name, value in data.items():
                if hasattr(new_place, name):
                    setattr(new_place, name, value)
            new_place.city_id = city_id
            new_place.save()
            return make_response(jsonify(new_place.to_dict()), 201)

    """ If we made it here, it couldnt be found (so 404) """
    abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=['PUT'])
def put_place(place_id):
    """ Update place """

    """ Holberton wants this, but keys to ignore :) """
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    selected_place = storage.get(Place, place_id)
    if selected_place is not None:
        data = request.get_json()

        """ Validate were given actual usable data """
        if data is None:
            return make_response(jsonify(error="Not a JSON"), 400)

        """ Find the matching place and update its attributes
            to the new values. After updating, save() to 'commit' the
            changes to the storage engine
        """
        for name, value in data.items():
            if name not in ignore_keys and hasattr(selected_place, name):
                setattr(selected_place, name, value)
                selected_place.save()
                put_response = jsonify(selected_place.to_dict())
                return make_response(put_response, 200)
    """ if we made it this far we couldnt find anything so 404 """
    abort(404)
