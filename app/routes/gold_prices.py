from flask import Blueprint, jsonify
from app.services.gold_price_service import GoldPriceService

gold_prices_bp = Blueprint('gold_prices', __name__)
gold_price_service = GoldPriceService()

@gold_prices_bp.route('/gold-prices', methods=['GET'])
def get_gold_prices():
    prices = gold_price_service.get_gold_prices()
    return jsonify(prices)