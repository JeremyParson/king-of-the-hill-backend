from flask import Blueprint, request, Response, jsonify
from sqlalchemy import exc
from .. import models
import bcrypt

bp = Blueprint('user', __name__, url_prefix="/users")

# Index users


@bp.route('/')
def index():
    try:
        all_users = models.Users.query.all()
        json = [{
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role.name
        } for user in all_users]
        return jsonify(json)
    except exc.SQLAlchemyError:
        return Response(u'The server ran into an error', mimetype='text/plain', status=401)

# Create a new user


@bp.route('/', methods=['POST'])
def create_user():
    try:
        json = request.get_json(True)
        password = json["password"].encode()
        password_digest = bcrypt.hashpw(password, bcrypt.gensalt())
        new_user = models.Users(
            email=json["email"],
            username=json["username"],
            password_digest=password_digest.decode(),
            role="user"
        )
        models.db.session.add(new_user)
        models.db.session.commit()
        return jsonify({
            "id": new_user.id,
            "email": new_user.email,
            "username": new_user.username,
            "role": "user"
        })
    except exc.SQLAlchemyError:
        return Response(u'The server ran into an error', mimetype='text/plain', status=401)


# Delete a user


@bp.route('/<id>', methods=['DELETE'])
def delete_user(id):
    try:
        to_delete = models.Users.query.get(id)
        models.db.session.delete(to_delete)
        models.db.session.commit()
    except exc.SQLAlchemyError:
        return Response(u'The server ran into an error', mimetype='text/plain', status=401)

    return Response(u'User successfully deleted', mimetype='text/plain', status=200)
