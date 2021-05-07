#!/usr/bin/python3
"""
    This is the cities page handler for Flask.
"""
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, request

from models.city import City
from models.state import State

cities_m = ['GET', 'POST']


@app_views.route('/states/<id>/cities', methods=cities_m, strict_slashes=False)
def states_id_cities(id):
    """
        Flask route at /states/<id>/cities.
    """
    state = storage.get(State, id)
    if (state):
        if request.method == 'POST':
            try:
                kwargs = request.get_json()
            except:
                return {"error": "Not a JSON"}, 400
            if "name" not in kwargs:
                return {"error": "Missing name"}, 400
            new_city = City(state_id=id, **kwargs)
            new_city.save()
            return new_city.to_dict(), 201

        elif request.method == 'GET':
            return jsonify([c.to_dict() for c in state.cities])
    abort(404)

cities_id_m = ['GET', 'DELETE', 'PUT']


@app_views.route('/cities/<id>', methods=cities_id_m, strict_slashes=False)
def cities_id(id):
    """
        Flask route at /cities/<id>.
    """
    city = storage.get(City, id)
    if (city):
        if request.method == 'DELETE':
            city.delete()
            storage.save()
            return {}, 200

        elif request.method == 'PUT':
            try:
                kwargs = request.get_json()
            except:
                return {"error": "Not a JSON"}, 400
            for k, v in kwargs.items():
                if k not in ["id", "state_id", "created_at", "updated_at"]:
                    setattr(city, k, v)
            city.save()
        return city.to_dict()
    abort(404)
