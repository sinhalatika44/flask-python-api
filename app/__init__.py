from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restx import Api, Resource
from config import Config
import platform
import pkg_resources

db = SQLAlchemy()
jwt = JWTManager()
api = Api(
    title='Flask API Boilerplate',
    version='1.0',
    description='A boilerplate for Flask APIs with Swagger UI',
    doc='/swagger/'
)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    from app.routes import auth
    app.register_blueprint(auth.bp)

    @api.route('/')
    class Home(Resource):
        def get(self):
            """Welcome endpoint with API information"""
            flask_version = pkg_resources.get_distribution("flask").version
            return {
                "message": "Welcome to the Flask API Boilerplate!",
                "description": "This is a simple API boilerplate using Flask, Flask-SQLAlchemy, and Flask-JWT-Extended. It can be used for scalable and secure RESTful APIs.",
                "status": "operational",
                "version": "1.0.0",
                "python_version": platform.python_version(),
                "flask_version": flask_version
            }, 200

    return app

# This line ensures that the create_app function is importable
__all__ = ['create_app', 'db']