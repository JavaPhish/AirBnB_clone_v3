#!/usr/bin/python3
"""linking places and amenities
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route("/places/<place_id>/amenities", strict_slashes=False,
                 methods=['GET'])
def all_amenities(place_id):
    """get all amenities for
    given place
    """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if request.method == 'GET':
            place = storage.get(Place, place_id)
            if place is not None:
                list_amenities = []
                for amenity in place.amenities:
                    list_amenities.append(amenity.to_dict())
                return make_response(jsonify(list_amenities))
            else:
                abort(404)
    else:
        if request.method == 'GET':
            place = storage.get(Place, place_id)
            if place is not None:
                list_amenities = []
                for amenity in place.amenity_ids:
                    list_amenities.append(amenity.to_dict())
                return make_response(jsonify(list_amenities))
            else:
                abort(404)
