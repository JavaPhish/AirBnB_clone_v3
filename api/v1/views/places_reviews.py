#!/usr/bin/python3
"""import app_views Places views
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['GET'])
def all_reviews_in_place(place_id):
    """get all places in city
    """
    selected_place = storage.get(Place, place_id)
    json_repr = []
    if selected_place is not None:
        if request.method == 'GET':
            for v in storage.all(Review).values():
                if v.place_id == place_id:
                    json_repr.append(v.to_dict())
            return make_response(jsonify(json_repr))
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=['GET'])
def get_place_reviews(review_id):
    """get place by id
    """
    selected_review = storage.get(Review, review_id)
    if selected_review is not None:
        if request.method == 'GET':
            return make_response(jsonify(selected_review.to_dict()))
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(review_id):
    """delete state by id
    """
    selected_review = storage.get(Review, review_id)
    if selected_review is not None:
        if request.method == 'DELETE':
            selected_review.delete()
            storage.save()
            return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=['POST'])
def post_review(place_id):
    """post place
    """
    selected_place = storage.get(Place, place_id)
    if selected_place is not None:
        if request.method == 'POST':
            data = request.get_json()
            if data is None:
                return make_response(jsonify(error="Not a JSON"), 400)

            if 'user_id' not in data.keys():
                return make_response(jsonify(error="Missing user_id"), 400)

            if 'text' not in data.keys():
                return make_response(jsonify(error="Missing text"), 400)

            user_id = data.get('user_id')
            get_user = storage.get(User, user_id)
            if get_user is None:
                abort(404)

            if 'user_id' and 'text' in data.keys():
                new_review = Place()
                for name, value in data.items():
                    if hasattr(new_review, name):
                        setattr(new_review, name, value)
                new_review.place_id = place_id
                new_review.save()
                return make_response(jsonify(new_review.to_dict()), 201)
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=['PUT'])
def put_place(review_id):
    """Update place
    """
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    selected_review = storage.get(Place, review_id)
    if selected_review is not None:
        if request.method == 'PUT':
            data = request.get_json()

            if data is None:
                return make_response(jsonify(error="Not a JSON"), 400)

            for name, value in data.items():
                if name not in ignore_keys and hasattr(selected_review, name):
                    setattr(selected_review, name, value)
                    selected_review.save()
                    put_response = jsonify(selected_review.to_dict())
                    return make_response(put_response, 200)
    else:
        abort(404)
