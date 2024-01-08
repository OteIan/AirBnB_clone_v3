#!/usr/bin/python3
"""
View for Place objects that Handles all default RESTFul API
actions
"""
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def list_place_objects(city_id):
    """
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    all_objs = storage.all(Place)
    return jsonify([obj.to_dict() for obj in all_objs.values() if obj.city_id == city_id])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_objects(place_id):
    """
    """
    obj = storage.get(Place, place_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_objects(place_id):
    """
    """
    obj = storage.get(Place, place_id)
    if obj is None or not obj:
        abort(404)

    obj.delete()
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    elif 'user_id' not in data.keys():
        abort(400, 'Missing user_id')
    elif 'name' not in data.keys():
        abort(400, 'Missing name')

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    obj = Place(city_id=city_id, **data)
    storage.new(obj)
    storage.save()

    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place_objects(place_id):
    """
    """
    obj = storage.get(Place, place_id)
    if obj is None or not obj:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'user_id', 'place_id']:
            setattr(obj, key, value)

    storage.save()

    return make_response(jsonify(obj.to_dict()), 200)
