#!/usr/bin/python3
"""amenities app_view
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users/', strict_slashes=False,
                 methods=['GET'])
def all_users():
    """list all users
    """
    all_users = []
    for user in storage.all(User).values():
        all_users.append(user.to_dict())
    return make_response(jsonify(all_users))


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET'])
def one_user(user_id):
    """get user by id
    """
    for value in storage.all(User).values():
        if value.id == user_id:
            return make_response(jsonify(value.to_dict()))
    return abort(404)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """delete user by id
    """
    for value in storage.all(User).values():
        if value.id == user_id:
            value.delete()
            storage.save()
            return make_response(jsonify({}), 200)
    return abort(404)


@app_views.route('/users/', strict_slashes=False,
                 methods=['POST'])
def post_user():
    """post new user data
    """
    data = request.get_json()
    if data is None:
        return make_response(jsonify(error="Not a JSON"), 400)

    if 'email' not in data.keys():
        return make_response(jsonify(error="Missing email"), 400)
    if 'password' not in data.keys():
        return make_response(jsonify(error="Missing password"), 400)

    for key, value in data.items():
        if key not in ignore_keys and hasattr(User, key):
            if key == 'name':
                new_user = User()
                setattr(new_user, key, value)
                new_user.save()
                return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def put_user(user_id):
    """update user instance
    """

    data = request.get_json()
    if data is None:
        return make_response(jsonify(error="Not a JSON"), 400)

    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for value in storage.all(User).values():
        if value.id == user_id:
            for k, v in data.items():
                if k not in ignore_keys and hasattr(User, k):
                    setattr(value, k, v)
                    value.save()
                    return make_response(jsonify(value.to_dict()), 200)
                else:
                    return abort(404)
    return abort(404)
