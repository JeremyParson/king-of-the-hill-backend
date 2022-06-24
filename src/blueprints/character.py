from flask import Blueprint, Response, request
from sqlalchemy import exc
from sqlalchemy.inspection import inspect
from ..models import Character, Hill
from .. import models
from flask import jsonify

bp = Blueprint('character', __name__, url_prefix="/characters")


@bp.route('/')
def index():
    try:
        all_characters = Character.query.all()
        json = [{
            "id": character.id,
            "hill_id": character.hill_id,
            "name": character.name,
            "description": character.description,
        } for character in all_characters]
        return jsonify(json)
    except exc.SQLAlchemyError:
        return Response(u'The server ran into an error', mimetype='text/plain', status=401)

# Create a hill


@bp.route('/<hill_id>', methods=["POST"])
def create_character(hill_id):
    try:
        user = request.environ.get("user")
        if not user or not user['id']:
            return Response(u'Must be logged in to update a hill', mimetype="application/json", status=400)
        hill = Hill.query.get(hill_id)
        if user['id'] != hill.user_id:
            return Response(u'You are not authorized to update this hill', mimetype="application/json", status=400)        
        json = request.get_json(True)
        new_character = Character(
            hill_id=hill_id,
            name=json["name"],
            description=json["description"],
            image = json["image"]
        )
        models.db.session.add(new_character)
        models.db.session.commit()
        return jsonify({
            'id': new_character.id,
            'hill_id':new_character.hill_id,
            'name': new_character.name,
            'description': new_character.description,
            'image' : new_character.image
        })
    except exc.SQLAlchemyError:
        return Response(u'The server ran into an error', mimetype='text/plain', status=401)

# Update a hill


@bp.route('/<id>', methods=["PATCH"])
def update_character(id):
    try:
        user = request.environ.get("user")
        if not user or not user['id']:
            return Response(u'Must be logged in to update a hill', mimetype="application/json", status=400)
        json = request.get_json(True)
        character = Character.query.get(id)
        hill = Hill.query.get(character.hill_id)
        if user['id'] != hill.user_id:
            return Response(u'You are not authorized to update this hill', mimetype="application/json", status=400)
        for key in json:
            if json[key] != '':
                setattr(character, key, json[key])
                models.db.session.commit()
        return jsonify({
            'id': character.id,
            'hill_id':character.hill_id,
            'name': character.name,
            'description': character.description,
            'image' : character.image
        })
    except exc.SQLAlchemyError:
        return Response(u'The server ran into an error', mimetype='text/plain', status=401)

# Delete a hill


@bp.route('/<id>', methods=['DELETE'])
def delete_character(id):
    try:
        user = request.environ.get("user")
        if not user or not user['id']:
            return Response(u'Must be logged in to update a hill', mimetype="application/json", status=400)
        to_delete = Character.query.get(id)
        hill = Hill.query.get(to_delete.hill_id)
        if user['id'] != hill.user_id:
            return Response(u'You are not authorized to update this hill', mimetype="application/json", status=400)
        models.db.session.delete(to_delete)
        models.db.session.commit()
    except exc.SQLAlchemyError:
        return Response(u'The server ran into an error', mimetype='text/plain', status=401)

    return Response(u'Character successfully deleted', mimetype='text/plain', status=200)
