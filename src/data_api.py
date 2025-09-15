"""
Simple mock data_api for local development
"""
import requests
import json

class ApiClient:
    def __init__(self):
        pass
    
    def call_api(self, endpoint, query=None):
        """
        Mock API client that returns sample data for testing
        """
        if 'get_stock_chart' in endpoint:
            symbol = query.get('symbol', 'HG=F') if query else 'HG=F'
            
            # Return mock data structure similar to Yahoo Finance
            return {
                'chart': {
                    'result': [{
                        'meta': {
                            'symbol': symbol,
                            'regularMarketPrice': 4.65,
                            'regularMarketDayHigh': 4.70,
                            'regularMarketDayLow': 4.60,
                            'fiftyTwoWeekHigh': 5.89,
                            'fiftyTwoWeekLow': 3.97,
                            'regularMarketVolume': 50000,
                            'previousClose': 4.63
                        },
                        'timestamp': [1726387200],
                        'indicators': {
                            'quote': [{
                                'open': [4.63],
                                'high': [4.70],
                                'low': [4.60],
                                'close': [4.65],
                                'volume': [50000]
                            }]
                        }
                    }]
                }
            }
        
        return {'error': 'Mock API - endpoint not implemented'}
