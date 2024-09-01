from flask import Blueprint, jsonify
from app.services.news_service import NewsService

news_bp = Blueprint('news', __name__)
news_service = NewsService()

@news_bp.route('/news', methods=['GET'])
def get_news():
    news = news_service.get_news()
    return jsonify(news)

@news_bp.route('/news/<category>', methods=['GET'])
def get_news_by_category(category):
    news = news_service.get_news(category)
    return jsonify(news)

@news_bp.route('/news/<category>/<path:article_link_path>', methods=['GET'])
def get_article(category, article_link_path):
    # This endpoint might be used to fetch full article content
    # For now, we'll return a placeholder response
    return jsonify({"message": f"Full article content for category: {category}, path: {article_link_path}"})