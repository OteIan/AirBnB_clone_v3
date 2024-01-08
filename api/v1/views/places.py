#!/usr/bin/python3
"""
View for Place objects that Handles all default RESTFul API
actions
"""
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import abort, jsonify, request
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_places(city_id):
    """
    places with city ids
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        all_objs = storage.all(Place)
        places = [obj.to_dict() for obj in all_objs.values()]
        return jsonify(places), 200

    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        elif 'user_id' not in data.keys():
            abort(400, 'Missing user_id')
        elif 'name' not in data.keys():
            abort(400, 'Missing name')

        if not storage.get(User, data['user_id']):
            abort(404)

        obj = Place(city_id=city_id, **data)
        storage.new(obj)
        storage.save()

        return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def methods_places(place_id):
    """
    Places with IDs methods
    """
    place = storage.get(Place, place_id)
    if place is None or not place:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict()), 200

    if request.method == 'DELETE':
        place.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")

        for key, value in data.items():
            if key not in ['id', 'created_at',
                           'updated_at', 'user_id', 'place_id']:
                setattr(place, key, value)

        storage.save()
        return jsonify(place.to_dict()), 200
