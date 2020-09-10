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
        """ Loop through all users in the storage engine,
            when we find one with a matching id to the user_id,
            return it in json format
        """
        if value.id == user_id:
            return make_response(jsonify(value.to_dict()))

    """ abort if nothing was found (404 OBVIOUSLY.) """
    return abort(404)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    """delete user by id
    """

    """ Loop through all Users in the storage engine,
        once we find one that matches the given id (user_id),
        delete it from the engine and .save() the engine to
        update our changes

        oh then return 200 to reflect a successful deletion
    """
    for value in storage.all(User).values():
        if value.id == user_id:
            value.delete()
            storage.save()
            return make_response(jsonify({}), 200)

    """ 404 abort if we made it here, nothing was found to delete """
    return abort(404)


@app_views.route('/users/', strict_slashes=False,
                 methods=['POST'])
def post_user():
    """post new user data
    """

    data = request.get_json()
    """ Validates the json is valid """
    if data is None:
        return make_response(jsonify(error="Not a JSON"), 400)

    """ Ensures we have the relevent keys (email and password)
        if we dont have them, yell at the user
    """
    if 'email' not in data.keys():
        return make_response(jsonify(error="Missing email"), 400)
    if 'password' not in data.keys():
        return make_response(jsonify(error="Missing password"), 400)

    """ Create a new user and use the given data (email and pass)
        as the values for the new users.

        .save() so the storage engine will update these changes
        then return 201 on success
    """
    new_user = User()
    new_user.email = data.get('email')
    new_user.password = data.get('password')
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
