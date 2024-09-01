from http.client import HTTPException
import time as time_module
import traceback
from flask import Flask, g, jsonify, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restx import Api, Resource, Namespace
from config import Config
import platform
import logging
import pkg_resources

db = SQLAlchemy()
jwt = JWTManager()
api = Api(
    title='Flask API Boilerplate',
    version='1.0',
    description='A boilerplate for Flask APIs with Swagger UI',
    doc='/swagger/',
    prefix='/api'
)

# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)
logger = logging.getLogger(__name__)

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

    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/privacy')
    def privacy():
        return render_template('privacy.html')

    @app.route('/terms')
    def terms():
        return render_template('terms.html')

    @app.route('/api/waitlist', methods=['POST'])
    def join_waitlist():
        email = request.json.get('email')
        # TODO: Add email to the database
        # For now, we'll just store it in the session
        session['waitlist_email'] = email
        print(f"Email added to waitlist: {email}")
        return jsonify({"message": "Thank you for joining our waitlist!"})

    @api.route('/home')
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
        
    @app.before_request
    def before_request():
        g.start_time = time_module.time()

    @app.after_request
    def after_request(response):
        # Calculate request duration
        duration = time_module.time() - g.start_time
        
        # Log request and response details
        log_data = {
            'method': request.method,
            'path': request.path,
            'status_code': response.status_code,
            'duration': f"{duration:.4f}s",
            'ip': request.remote_addr,
            'user_agent': request.user_agent.string,
            'referrer': request.referrer,
            'request_headers': dict(request.headers),
            'response_headers': dict(response.headers)
        }
        
        logger.info(f"Request-Response: {log_data}")
        
        return response

    @app.errorhandler(Exception)
    def handle_exception(e):
        # Capture all exceptions
        if isinstance(e, HTTPException):
            # Handle HTTP errors
            response = e.get_response()
            error_data = {
                'code': e.code,
                'name': e.name,
                'description': e.description,
            }
        else:
            # Handle non-HTTP errors
            response = app.response_class(
                response=str(e),
                status=500,
            )
            error_data = {
                'error': str(e),
                'traceback': traceback.format_exc()
            }
        
        # Log error details
        log_data = {
            'method': request.method,
            'path': request.path,
            'error': error_data,
            'ip': request.remote_addr,
            'user_agent': request.user_agent.string,
            'referrer': request.referrer,
            'request_headers': dict(request.headers)
        }
        
        logger.error(f"Error: {log_data}")
        
        return response    

    return app

# This line ensures that the create_app function is importable
__all__ = ['create_app', 'db']