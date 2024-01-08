#!/usr/bin/python3
"""
View for User objects that Handles all default RESTFul API
actions
"""
from models import storage
from models.user import User
from flask import abort, jsonify, request
from api.v1.views import app_views


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def get_users():
    """
    """
    if request.method == 'GET':
        all_objs = storage.all(User)
        return jsonify([obj.to_dict() for obj in all_objs.values()]), 200

    if request.method == 'POST':
        data = request.get_json()

        if not data:
            abort(400, "Not a JSON")
        elif 'email' not in data.keys():
            abort(400, 'Missing email')
        elif 'password' not in data.keys():
            abort(400, 'Missing password')

        obj = User(**data)
        storage.new(obj)
        storage.save()

        return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def method_users(user_id):
    """
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if request.method == 'GET':
        return jsonify(user.to_dict()), 200

    if request.method == 'DELETE':
        user.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")

        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(user, key, value)

        storage.save()
        return jsonify(user.to_dict()), 200
