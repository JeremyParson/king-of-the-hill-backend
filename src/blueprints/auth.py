from flask import Blueprint, Response, jsonify, request
from ..models import Users
import bcrypt
import jwt

bp = Blueprint('auth', __name__, url_prefix="/auth")


@bp.route('/', methods=["POST"])
# generate a JWT token for user
def index():
    json = request.get_json(True)
    user = Users.query.filter_by(email=json["email"]).first()
    if user == None:
        return Response(u'Authentication failed', mimetype='application/json', status=400)

    password = json["password"].encode()
    if not bcrypt.checkpw(password, user.password_digest.encode()):
        return Response(u'Authentication failed', mimetype='application/json', status=400)

    token = jwt.encode({"id": user.id}, "secret", algorithm="HS256")
    return token

@bp.route('/profile')
def profile ():
    if request.environ['user'] == None:
        return Response(u'User is not logged in', mimetype='application/json', status=400)
    user = Users.query.get(request.environ['user']["id"])
    return jsonify({
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": "user"
        })
