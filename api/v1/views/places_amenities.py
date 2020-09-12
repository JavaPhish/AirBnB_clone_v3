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
def all_amenities_by_place(place_id):
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


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity_by_place(place_id, amenity_id):
    """delete amenity for
    given place
    """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if request.method == 'DELETE':
            place = storage.get(Place, place_id)
            if place is not None:
                for amenity in place.amenities:
                    if amenity.id == amenity_id:
                        amenity.delete()
                        storage.save()
                        return make_response(jsonify({}), 200)
                abort(404)
            else:
                abort(404)
    else:
        if request.method == 'DELETE':
            place = storage.get(Place, place_id)
            if place is not None:
                for amenity in place.amenity_ids:
                    if amenity.id == amenity_id:
                        amenity.delete()
                        storage.save()
                        return make_response(jsonify({}), 200)
                abort(404)
            else:
                abort(404)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=['POST'])
def post_amenity_by_place(place_id, amenity_id):
    """add amenity for
    given place
    """
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if request.method == 'POST':
            place = storage.get(Place, place_id)
            if place is not None:
                check_amenity = storage.get(Amenity, amenity_id)
                for amenity in place.amenities:
                    if amenity.id == amenity_id:
                        return make_response(jsonify(amenity.to_dict()), 200)
                if check_amenity is not None:
                    place.amenities.append(check_amenity)
                    storage.save()
                    return make_response(jsonify(check_amenity.to_dict()), 201)
                else:
                    abort(404)
            else:
                abort(404)
    else:
        if request.method == 'POST':
            place = storage.get(Place, place_id)
            if place is not None:
                check_amenity = storage.get(Amenity, amenity_id)
                for amenity in place.amenity_ids:
                    if amenity.id == amenity_id:
                        return make_response(jsonify(amenity.to_dict()), 200)
                if check_amenity is not None:
                    place.amenity_ids.append(check_amenity)
                    storage.save()
                    return make_response(jsonify(check_amenity.to_dict()), 201)
                else:
                    abort(404)
            else:
                abort(404)
