#!/usr/bin/python3
"""amenities app_view
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'])
def all_amenites():
    """list all amenites
    """
    if request.method == 'GET':
        all_amenites = []
        for amenity in storage.all(Amenity).values():
            all_amenites.append(amenity.to_dict())
        return make_response(jsonify(all_amenites))


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def one_amenity(amenity_id):
    """get amenity by id
    """
    if request.method == 'GET':
        for value in storage.all(Amenity).values():
            if value.id == amenity_id:
                return make_response(jsonify(value.to_dict()))
        return abort(404)
