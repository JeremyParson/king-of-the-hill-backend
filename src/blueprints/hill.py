from flask import Blueprint, Response, request
from sqlalchemy import exc
from ..models import Hill, Character
from .. import models
from flask import jsonify
from flask_cors import cross_origin

bp = Blueprint('hill', __name__, url_prefix="/hills")

# Index all hills


@bp.route('/')
def index():
    try:
        all_hills = Hill.query.all()
        json = [{
            "id": hill.id,
            "user_id": hill.user_id,
            "name": hill.name,
            "description": hill.description,
            "image": hill.image
        } for hill in all_hills]
        return jsonify(json)
    except exc.SQLAlchemyError:
        return Response(u'The server ran into an error', mimetype='text/plain', status=401)


# Detail of hill


@bp.route('/<id>')
@cross_origin()
def detail(id):
    try:
        hill = Hill.query.get(id)
        all_characters = Character.query.filter_by(hill_id=hill.id)

        character_json = [{
            "id": character.id,
            "hill_id": character.hill_id,
            "name": character.name,
            "image": character.image,
            "description": character.description,
        } for character in all_characters]

        hill_json = {
            "id": hill.id,
            "user_id": hill.user_id,
            "name": hill.name,
            "description": hill.description,
            "image": hill.image,
            "characters": character_json
        }

        return jsonify(hill_json)
    except exc.SQLAlchemyError:
        return Response(u'The server ran into an error', mimetype='text/plain', status=401)

# Create a hill


@bp.route('/', methods=["POST"])
@cross_origin()
def create_hill():
    try:
        json = request.get_json(True)
        user = request.environ.get("user")
        if not user or user['id'] == None:
            return Response(u'Must be logged in to delete a hill', mimetype="application/json", status=400)
        new_hill = Hill(
            name=json["name"],
            description=json["description"],
            user_id=user["id"],
            image=json["image"]
        )
        models.db.session.add(new_hill)
        models.db.session.commit()
        return jsonify({
            'id': new_hill.id,
            'user_id': new_hill.user_id,
            'name': new_hill.name,
            'description': new_hill.description,
            'image': new_hill.image,
        })
    except exc.SQLAlchemyError as e:
        return Response(u'The server ran into an error', mimetype='text/plain', status=401)

# Update a hill


@bp.route('/<id>', methods=["PATCH"])
def update_hill(id):
    try:
        user = request.environ.get("user")
        if not user or not user['id']:
            return Response(u'Must be logged in to update a hill', mimetype="application/json", status=400)
        json = request.get_json(True)
        hill = Hill.query.get(id)
        if user['id'] != hill.user_id:
            return Response(u'You are not authorized to update this hill', mimetype="application/json", status=400)
        for key in json:
            if request.form.get(key) != '':
                setattr(hill, key, json[key])
                models.db.session.commit()
        return jsonify({
            'id': hill.id,
            'user_id': hill.user_id,
            'name': hill.name,
            'description': hill.description,
            'image': hill.image,
        })
    except exc.SQLAlchemyError:
        return Response(u'The server ran into an error', mimetype='text/plain', status=401)

# Delete a hill


@bp.route('/<id>', methods=['DELETE'])
def delete_hill(id):
    try:
        user = request.environ.get("user")
        if not user or not user['id']:
            return Response(u'Must be logged in to delete a hill', mimetype="application/json", status=400)
        to_delete = Hill.query.get(id)
        if user['id'] != to_delete.user_id:
            return Response(u'You are not authorized to update this hill', mimetype="application/json", status=400)
        all_characters = Character.query.filter_by(hill_id=id)
        for character in all_characters:
            models.db.session.delete(character)
        models.db.session.delete(to_delete)
        models.db.session.commit()
    except exc.SQLAlchemyError:
        return Response(u'The server ran into an error', mimetype='text/plain', status=401)

    return Response(u'Hill successfully deleted', mimetype='text/plain', status=200)

@bp.route('/admin/<id>', methods=['DELETE'])
def delete_hill_admin(id):
    try:
        to_delete = Hill.query.get(id)
        models.db.session.delete(to_delete)
        models.db.session.commit()
    except exc.SQLAlchemyError:
        return Response(u'The server ran into an error', mimetype='text/plain', status=401)

    return Response(u'Hill successfully deleted', mimetype='text/plain', status=200)