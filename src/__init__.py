from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/king-of-the-hill'


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # import model
    from . import models
    models.db.init_app(app)
    migrate = Migrate(app, models.db)

    # register hill blueprint
    from .blueprints import hill
    app.register_blueprint(hill.bp)
    from .blueprints import user
    app.register_blueprint(user.bp)
    from .blueprints import auth
    app.register_blueprint(auth.bp)
    from .blueprints import character
    app.register_blueprint(character.bp)

    # middleware
    from .middleware.define_user import middleware
    app.wsgi_app = middleware(app.wsgi_app)

    @app.route('/')
    def index():
        return "King of the Hill API"

    return app
