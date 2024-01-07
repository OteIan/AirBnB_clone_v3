#!/usr/bin/python3
"""
View for User objects that Handles all default RESTFul API
actions
"""
from models import storage
from models.user import User
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_user_objects():
    """
    Retrieve a list of all User objects.

    Returns:
    - JSON representation of the list of User objects.

    Example:
    $ curl http://127.0.0.1:5000/api/v1/users
    Output: JSON representation of all User objects
    """
    all_objs = storage.all(User)
    return jsonify([obj.to_dict() for obj in all_objs.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_objects(user_id):
    """
    Retrieve a specific User object based on its ID.

    Parameters:
    - user_id: The ID of the User object to retrieve.

    Returns:
    - JSON representation of the specified User object.

    Example:
    $ curl http://127.0.0.1:5000/api/v1/users/1
    Output: JSON representation of the User object with ID 1
    """
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user_objects(user_id):
    """
    Delete a specific User object based on its ID.

    Parameters:
    - user_id: The ID of the User object to delete.

    Returns:
    - Empty JSON response with HTTP status code 200 upon successful deletion.

    Example:
    $ curl -X DELETE http://127.0.0.1:5000/api/v1/users/1
    Output: {}
    """
    obj = storage.get(User, user_id)
    if obj is None or not obj:
        abort(404)

    obj.delete()
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Create a new User object.

    Returns:
    - JSON representation of the newly created User object.
    - HTTP status code 201 upon successful creation.

    Example:
    $ curl -X POST -H "Content-Type: application/json" \
      -d '{"name": "New User"}' http://127.0.0.1:5000/api/v1/users
    Output: JSON representation of the newly created User object
    """
    data = request.get_json()

    if not data:
        abort(404, "Not a JSON")
    elif 'email' not in data.keys():
        abort(404, 'Missing email')
    elif 'password' not in data.keys():
        abort(404, 'Missing password')

    obj = User(**data)
    storage.new(obj)
    storage.save()

    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user_objects(user_id):
    """
    Update a specific User object based on its ID.

    Parameters:
    - user_id: The ID of the User object to update.

    Returns:
    - JSON representation of the updated User object.
    - HTTP status code 200 upon successful update.

    Example:
    $ curl -X PUT -H "Content-Type: application/json" \
      -d '{"name": "Updated User"}' http://127.0.0.1:5000/api/v1/users/1
    Output: JSON representation of the updated User object
    """
    obj = storage.get(User, user_id)

    if obj is None or not obj:
        abort(404)

    data = request.get_json()
    if not data:
        abort(404, "Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)

    storage.save()

    return make_response(jsonify(obj.to_dict()), 200)
