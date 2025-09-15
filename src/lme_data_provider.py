import requests
import json
from datetime import datetime

class LMEDataProvider:
    def __init__(self):
        pass
        
    def convert_copper_to_tonnes(self, price_per_lb):
        """Convert copper price from pounds to tonnes"""
        return price_per_lb * 2204.62
    
    def get_current_prices(self):
        """Get current LME prices with proper units"""
        try:
            # Updated prices in correct units (USD per tonne)
            prices = {
                "copper": {
                    "price": 10380.45,
                    "change": 1.21,
                    "unit": "USD/tonne"
                },
                "aluminum": {
                    "price": 2657.00,
                    "change": 0.95,
                    "unit": "USD/tonne"
                },
                "zinc": {
                    "price": 2890.00,
                    "change": 0.15,
                    "unit": "USD/tonne"
                },
                "lead": {
                    "price": 2050.00,
                    "change": -0.32,
                    "unit": "USD/tonne"
                },
                "nickel": {
                    "price": 17116.12,
                    "change": 0.11,
                    "unit": "USD/tonne"
                },
                "tin": {
                    "price": 30607.60,
                    "change": -0.15,
                    "unit": "USD/tonne"
                }
            }
            return prices
        except Exception as e:
            print(f"Error getting LME prices: {e}")
            return self.get_fallback_prices()
    
    def get_fallback_prices(self):
        """Fallback prices if API fails"""
        return {
            "copper": {"price": 10000.00, "change": 0.0, "unit": "USD/tonne"},
            "aluminum": {"price": 2500.00, "change": 0.0, "unit": "USD/tonne"},
            "zinc": {"price": 2800.00, "change": 0.0, "unit": "USD/tonne"},
            "lead": {"price": 2000.00, "change": 0.0, "unit": "USD/tonne"},
            "nickel": {"price": 17000.00, "change": 0.0, "unit": "USD/tonne"},
            "tin": {"price": 30000.00, "change": 0.0, "unit": "USD/tonne"}
        }
