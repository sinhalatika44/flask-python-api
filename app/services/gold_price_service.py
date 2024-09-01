import requests

class GoldPriceService:
    def __init__(self):
        self.api_url = "https://api.metalpriceapi.com/v1/latest"
        self.api_key = "YOUR_METAL_PRICE_API_KEY"  # Replace with your actual API key

    def get_gold_prices(self):
        params = {
            "api_key": self.api_key,
            "base": "INR",
            "currencies": "XAU"  # XAU is the currency code for gold
        }
        
        response = requests.get(self.api_url, params=params)
        if response.status_code == 200:
            data = response.json()
            gold_price_per_oz = data["rates"]["XAU"]
            gold_price_per_gram = gold_price_per_oz / 31.1035  # Convert oz to gram

            cities = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bengaluru", "Hyderabad"]
            gold_prices = {}

            for city in cities:
                # Simulating slight price differences between cities
                price_variation = 1 + (hash(city) % 5 - 2) / 100  # -2% to +2% variation
                gold_prices[city] = round(gold_price_per_gram * price_variation, 2)

            return gold_prices
        else:
            return {"error": "Failed to fetch gold prices"}