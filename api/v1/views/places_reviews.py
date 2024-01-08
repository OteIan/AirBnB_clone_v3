#!/usr/bin/python3
"""
View for Review objects that Handles all default RESTFul API
actions
"""
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from flask import abort, jsonify, request
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_reviews(place_id):
    """
    Reviews for places with place ids
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':
        all_objs = storage.all(Review)
        x = [obj.to_dict() for obj in all_objs.values()
             if obj.place_id == place_id]
        return jsonify(x), 200

    if request.method == 'POST':
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

        return jsonify(obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT', 'GET', 'DELETE'],
                 strict_slashes=False)
def method_reviews(review_id):
    """
    Methods for reviews with ids
    """
    review = storage.get(Review, review_id)
    if review is None or not review:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict()), 200

    if request.method == 'DELETE':
        review.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(404, "Not a JSON")

        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at',
                           'user_id', 'place_id']:
                setattr(review, key, value)

        storage.save()
        return jsonify(review.to_dict()), 200
