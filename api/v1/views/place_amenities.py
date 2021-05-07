#!/usr/bin/python3
"""
    This is the places amenities page handler for Flask.
"""
from api.v1.views.places import places_id
from api.v1.views import app_views
from api.v1 import *
from models import storage
from flask import abort, jsonify, request

from models.place import Place
from models.review import Review
from models.user import User
from models.amenity import Amenity


@app_views.route('/places/<id>/amenities', methods=['GET'])
def places_id_amenities(id):
    """
        Flask route at /places/<id>/amenities.
    """
    place = storage.get(Place, id)
    if (place):
        if storage_t == 'db':
            return jsonify([r.to_dict() for r in place.amenities])
        elif storage_t == 'fs':
            pass
    abort(404)


@app_views.route('/places/<id>/amenities/<amenity_id>', methods=['DELETE', 'POST'])
def places_id_amenities_id(id, amenity_id):
    """
        Flask route at /places/<id>/amenities/<amenity_id>.
    """
    place = storage.get(Place, id)
    if (place):
        amenity = storage.get(Amenity, amenity_id)
        if storage_t == 'db':
            if (amenity):
                if (amenity in place.amenities):
                    place.amenities.remove(amenity)
                    storage.save()
                    return {}, 200
                abort(404)
            abort(404)
        elif storage_t == 'fs':
            pass
    abort(404)
