#!/usr/bin/python3
"""
View for Amenity objects that Handles all default RESTFul API
actions
"""
from models import storage
from models.amenity import Amenity
from flask import abort, jsonify, request
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def list_amenity_objects():
    """
    Retrieve a list of all Amenity objects.

    Returns:
    - JSON representation of the list of Amenity objects.

    Example:
    $ curl http://127.0.0.1:5000/api/v1/amenities
    Output: JSON representation of all Amenity objects
    """
    all_obj = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in all_obj.values()]), 200


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_object(amenity_id):
    """
    Retrieve a specific Amenity object based on its ID.

    Parameters:
    - amenity_id: The ID of the Amenity object to retrieve.

    Returns:
    - JSON representation of the specified Amenity object.

    Example:
    $ curl http://127.0.0.1:5000/api/v1/amenities/1
    Output: JSON representation of the Amenity object with ID 1
    """
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)

    return jsonify(obj.to_dict()), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_object(amenity_id):
    """
    Delete a specific Amenity object based on its ID.

    Parameters:
    - amenity_id: The ID of the Amenity object to delete.

    Returns:
    - Empty JSON response with HTTP status code 200 upon successful deletion.

    Example:
    $ curl -X DELETE http://127.0.0.1:5000/api/v1/amenities/1
    Output: {}
    """
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)

    obj.delete()
    del obj
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity_object():
    """
    Create a new Amenity object.

    Returns:
    - JSON representation of the newly created Amenity object.
    - HTTP status code 201 upon successful creation.

    Example:
    $ curl -X POST -H "Content-Type: application/json" \
      -d '{"name": "New Amenity"}' http://127.0.0.1:5000/api/v1/amenities
    Output: JSON representation of the newly created Amenity object
    """
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    elif 'name' not in data.keys():
        abort(400, 'Missing name')

    obj = Amenity(**data)
    storage.new(obj)
    storage.save()

    return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity_object(amenity_id):
    """
    Update a specific Amenity object based on its ID.

    Parameters:
    - amenity_id: The ID of the Amenity object to update.

    Returns:
    - JSON representation of the updated Amenity object.
    - HTTP status code 200 upon successful update.

    Example:
    $ curl -X PUT -H "Content-Type: application/json" \
      -d '{"name": "Updated Amenity"}' http://127.0.0.1:5000/api/v1/amenities/1
    Output: JSON representation of the updated Amenity object
    """
    obj = storage.get(Amenity, amenity_id)
    if not obj or obj is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)

    storage.save()

    return jsonify(obj.to_dict()), 200
