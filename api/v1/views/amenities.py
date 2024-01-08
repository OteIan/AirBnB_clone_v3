#!/usr/bin/python3
"""
View for Amenity objects that Handles all default RESTFul API
actions
"""
from models import storage
from models.amenity import Amenity
from flask import abort, jsonify, request
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def get_amenities():
    """
    Get all amenities or create a new amenity.
    GET: Returns a JSON response with all amenities.
    POST: Creates a new amenity based on the provided JSON data.
    """
    if request.method == 'GET':
        all_obj = storage.all(Amenity)
        return jsonify([obj.to_dict() for obj in all_obj.values()]), 200

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        elif 'name' not in data.keys():
            abort(400, 'Missing name')

        obj = Amenity(**data)
        storage.new(obj)
        storage.save()

        return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def methos_amenities(amenity_id):
    """
    Retrieve, delete, or update an amenity.
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict()), 200

    if request.method == 'DELETE':
        amenity.delete()
        del amenity
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')

        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)

        storage.save()
        return jsonify(amenity.to_dict()), 200
