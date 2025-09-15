class LMEDataProvider:
    def __init__(self):
        pass
        
    def get_current_prices(self):
        """Get current LME prices with proper units"""
        return {
            "copper": {"price": 10380.45, "change": 1.21, "unit": "USD/tonne"},
            "aluminum": {"price": 2657.00, "change": 0.95, "unit": "USD/tonne"},
            "zinc": {"price": 2890.00, "change": 0.15, "unit": "USD/tonne"},
            "lead": {"price": 2050.00, "change": -0.32, "unit": "USD/tonne"},
            "nickel": {"price": 17116.12, "change": 0.11, "unit": "USD/tonne"},
            "tin": {"price": 30607.60, "change": -0.15, "unit": "USD/tonne"}
        }
