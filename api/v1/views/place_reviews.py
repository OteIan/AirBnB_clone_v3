#!/usr/bin/python3
"""
View for Review objects that Handles all default RESTFul API
actions
"""
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from flask import abort, jsonify, request, make_response
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def list_review_objects(place_id):
    """
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    all_objs = storage.all(Review)
    return jsonify([obj.to_dict() for obj in all_objs.values() if obj.place_id == place_id])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_objects(review_id):
    """
    """
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review_objects(review_id):
    """
    
    """
    obj = storage.get(Review, review_id)
    if obj is None or not obj:
        abort(404)

    obj.delete()
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    elif 'user_id' not in data.keys():
        abort(400, 'Missing user_id')
    elif 'text' not in data.keys():
        abort(400, 'Missing text')

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    obj = Review(place_id=place_id, **data)
    storage.new(obj)
    storage.save()

    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review_objects(review_id):
    """
    """
    obj = storage.get(Review, review_id)
    if obj is None or not obj:
        abort(404)

    data = request.get_json()
    if not data:
        abort(404, "Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'user_id', 'place_id']:
            setattr(obj, key, value)

    storage.save()

    return make_response(jsonify(obj.to_dict()), 200)
