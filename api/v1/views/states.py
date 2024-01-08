#!/usr/bin/python3
"""
View for State objects that Handles all default RESTFul API
actions
"""
from models import storage
from models.state import State
from flask import abort, jsonify, request
from api.v1.views import app_views



@app_views.route('/states', methods=['GET', 'POST'])
def get_states():
    """
    """
    if request.method == 'GET':
        all_objs = storage.all(State)
        return jsonify([obj.to_dict() for obj in all_objs.values()]), 200

    if request.method == 'POST':
        data = request.get_json()

        if not data:
            abort(400, "Not a JSON")
        elif 'name' not in data.keys():
            abort(400, 'Missing name')

        obj = State(**data)
        storage.new(obj)
        storage.save()

        return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'])
def method_states(state_id):
    """
    """
    states = storage.get(State, state_id)
    if not states:
        abort(404)

    if request.method == 'GET':
        return jsonify(states.to_dict()), 200

    if request.method == 'DELETE':
        states.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")

        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(states, key, value)

        storage.save()
        return jsonify(states.to_dict()), 200
