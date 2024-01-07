#!/usr/bin/python3
"""
View for Amenity objects that Handles all default RESTFul API
actions
"""
from models import storage
from models.amenity import Amenity
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def list_amenity_objects():
    """
    """
    all_obj = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in all_obj.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity_object(amenity_id):
    """
    """
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)

    return jsonify(obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity_object(amenity_id):
    """
    """
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        abort(404)

    obj.delete()
    del obj
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity_object():
    """
    """
    data = request.get_json()
    if not data:
        abort(404, 'Not a JSON')
    elif 'name' not in data.keys():
        abort(404, 'Missing name')

    obj = Amenity(**data)
    storage.new(obj)
    storage.save()

    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity_object(amenity_id):
    """
    """
    obj = storage.get(Amenity, amenity_id)
    if not obj or obj is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(404, 'Not a JSON')

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)

    return make_response(jsonify(obj), 200)

