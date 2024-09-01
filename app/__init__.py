from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restx import Api, Resource, Namespace
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

    # Import and initialize news and gold price services
    from app.services.news_service import NewsService
    from app.services.gold_price_service import GoldPriceService
    news_service = NewsService()
    gold_price_service = GoldPriceService()

    # Create namespaces for different API sections
    news_ns = Namespace('news', description='News operations')
    gold_ns = Namespace('gold', description='Gold price operations')

    api.add_namespace(news_ns)
    api.add_namespace(gold_ns)

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

    @news_ns.route('/')
    class NewsList(Resource):
        def get(self):
            """Get all news"""
            return news_service.get_news()

    @news_ns.route('/<string:category>')
    class NewsCategory(Resource):
        def get(self, category):
            """Get news by category"""
            return news_service.get_news(category)

    @news_ns.route('/<string:category>/<path:article_link_path>')
    class NewsArticle(Resource):
        def get(self, category, article_link_path):
            """Get full article content (placeholder)"""
            return {"message": f"Full article content for category: {category}, path: {article_link_path}"}

    @gold_ns.route('/prices')
    class GoldPrices(Resource):
        def get(self):
            """Get gold prices for major Indian cities"""
            return gold_price_service.get_gold_prices()

    return app

# This line ensures that the create_app function is importable
__all__ = ['create_app', 'db']