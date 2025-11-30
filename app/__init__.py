from flask import Flask
from .config import Config
from .extensions import socketio, db, migrate ,bcrypt, jwt
from .routes import register_routes

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")

    register_routes(app)

    @app.route("/ping")
    def ping():
        return {"status": "ok", "service": "sklio-backend"}

    return app

from .extensions import socketio