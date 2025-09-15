"""
Market Data Integration Module for Layla AI Agent
Provides real-time and historical market data for non-ferrous metals
"""

import sys
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

sys.path.append('/opt/.manus/.sandbox-runtime')
from data_api import ApiClient

class MarketDataProvider:
    """
    Provides market data for non-ferrous metals trading
    """
    
    def __init__(self):
        self.client = ApiClient()
        
        # Metal symbols mapping for different exchanges
        self.metal_symbols = {
            'copper': {
                'lme': 'HG=F',  # Copper futures
                'comex': 'HG=F',
                'yahoo': 'HG=F'
            },
            'aluminum': {
                'lme': 'ALI=F',  # Aluminum futures
                'yahoo': 'ALI=F'
            },
            'lead': {
                'lme': 'LE=F',   # Lead futures
                'yahoo': 'LE=F'
            },
            'zinc': {
                'lme': 'ZN=F',   # Zinc futures
                'yahoo': 'ZN=F'
            },
            'nickel': {
                'lme': 'NI=F',   # Nickel futures
                'yahoo': 'NI=F'
            }
        }
        
        # Related stocks for market sentiment
        self.related_stocks = {
            'mining_companies': ['FCX', 'AA', 'SCCO', 'BHP', 'RIO'],
            'metal_etfs': ['COPX', 'CPER', 'JJC', 'JJN', 'JJU']
        }
    
    def get_metal_price(self, metal: str, exchange: str = 'yahoo') -> Dict[str, Any]:
        """
        Get current price for a specific metal
        
        Args:
            metal: Metal name (copper, aluminum, lead, zinc, nickel)
            exchange: Exchange to query (yahoo, lme, comex)
            
        Returns:
            Dictionary with price data
        """
        try:
            if metal.lower() not in self.metal_symbols:
                return {'error': f'Metal {metal} not supported'}
            
            symbol = self.metal_symbols[metal.lower()].get(exchange, 
                    self.metal_symbols[metal.lower()]['yahoo'])
            
            response = self.client.call_api('YahooFinance/get_stock_chart', query={
                'symbol': symbol,
                'region': 'US',
                'interval': '1d',
                'range': '5d',
                'includeAdjustedClose': True
            })
            
            if response and 'chart' in response and 'result' in response['chart']:
                result = response['chart']['result'][0]
                meta = result['meta']
                
                # Calculate price change
                current_price = meta.get('regularMarketPrice', 0)
                previous_close = meta.get('previousClose', current_price)
                change = current_price - previous_close
                change_percent = (change / previous_close * 100) if previous_close != 0 else 0
                
                return {
                    'metal': metal,
                    'symbol': symbol,
                    'price': current_price,
                    'currency': meta.get('currency', 'USD'),
                    'change': change,
                    'change_percent': change_percent,
                    'volume': meta.get('regularMarketVolume', 0),
                    'day_high': meta.get('regularMarketDayHigh', 0),
                    'day_low': meta.get('regularMarketDayLow', 0),
                    'fifty_two_week_high': meta.get('fiftyTwoWeekHigh', 0),
                    'fifty_two_week_low': meta.get('fiftyTwoWeekLow', 0),
                    'timestamp': datetime.now().isoformat(),
                    'exchange': exchange
                }
            else:
                return {'error': f'No data available for {metal}'}
                
        except Exception as e:
            return {'error': f'Failed to fetch {metal} price: {str(e)}'}
    
    def get_all_metals_prices(self) -> Dict[str, Any]:
        """
        Get current prices for all supported metals
        
        Returns:
            Dictionary with all metal prices
        """
        metals_data = {}
        
        for metal in self.metal_symbols.keys():
            metals_data[metal] = self.get_metal_price(metal)
        
        return {
            'metals': metals_data,
            'last_updated': datetime.now().isoformat(),
            'data_source': 'Yahoo Finance'
        }
    
    def get_metal_historical_data(self, metal: str, period: str = '1mo') -> Dict[str, Any]:
        """
        Get historical price data for a metal
        
        Args:
            metal: Metal name
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y)
            
        Returns:
            Dictionary with historical data
        """
        try:
            if metal.lower() not in self.metal_symbols:
                return {'error': f'Metal {metal} not supported'}
            
            symbol = self.metal_symbols[metal.lower()]['yahoo']
            
            response = self.client.call_api('YahooFinance/get_stock_chart', query={
                'symbol': symbol,
                'region': 'US',
                'interval': '1d',
                'range': period,
                'includeAdjustedClose': True
            })
            
            if response and 'chart' in response and 'result' in response['chart']:
                result = response['chart']['result'][0]
                timestamps = result['timestamp']
                quotes = result['indicators']['quote'][0]
                
                historical_data = []
                for i, timestamp in enumerate(timestamps):
                    if i < len(quotes['close']) and quotes['close'][i] is not None:
                        historical_data.append({
                            'date': datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d'),
                            'open': quotes['open'][i],
                            'high': quotes['high'][i],
                            'low': quotes['low'][i],
                            'close': quotes['close'][i],
                            'volume': quotes['volume'][i] if quotes['volume'][i] else 0
                        })
                
                return {
                    'metal': metal,
                    'symbol': symbol,
                    'period': period,
                    'data': historical_data,
                    'data_points': len(historical_data)
                }
            else:
                return {'error': f'No historical data available for {metal}'}
                
        except Exception as e:
            return {'error': f'Failed to fetch historical data for {metal}: {str(e)}'}
    
    def get_market_sentiment(self) -> Dict[str, Any]:
        """
        Get market sentiment from related mining stocks and ETFs
        
        Returns:
            Dictionary with market sentiment data
        """
        sentiment_data = {
            'mining_companies': {},
            'metal_etfs': {},
            'overall_sentiment': 'neutral'
        }
        
        positive_count = 0
        negative_count = 0
        total_count = 0
        
        # Check mining companies
        for symbol in self.related_stocks['mining_companies']:
            try:
                response = self.client.call_api('YahooFinance/get_stock_chart', query={
                    'symbol': symbol,
                    'region': 'US',
                    'interval': '1d',
                    'range': '5d'
                })
                
                if response and 'chart' in response and 'result' in response['chart']:
                    result = response['chart']['result'][0]
                    meta = result['meta']
                    
                    current_price = meta.get('regularMarketPrice', 0)
                    previous_close = meta.get('previousClose', current_price)
                    change_percent = ((current_price - previous_close) / previous_close * 100) if previous_close != 0 else 0
                    
                    sentiment_data['mining_companies'][symbol] = {
                        'price': current_price,
                        'change_percent': change_percent,
                        'sentiment': 'positive' if change_percent > 0 else 'negative' if change_percent < 0 else 'neutral'
                    }
                    
                    if change_percent > 0:
                        positive_count += 1
                    elif change_percent < 0:
                        negative_count += 1
                    total_count += 1
                    
            except Exception as e:
                sentiment_data['mining_companies'][symbol] = {'error': str(e)}
        
        # Check metal ETFs
        for symbol in self.related_stocks['metal_etfs']:
            try:
                response = self.client.call_api('YahooFinance/get_stock_chart', query={
                    'symbol': symbol,
                    'region': 'US',
                    'interval': '1d',
                    'range': '5d'
                })
                
                if response and 'chart' in response and 'result' in response['chart']:
                    result = response['chart']['result'][0]
                    meta = result['meta']
                    
                    current_price = meta.get('regularMarketPrice', 0)
                    previous_close = meta.get('previousClose', current_price)
                    change_percent = ((current_price - previous_close) / previous_close * 100) if previous_close != 0 else 0
                    
                    sentiment_data['metal_etfs'][symbol] = {
                        'price': current_price,
                        'change_percent': change_percent,
                        'sentiment': 'positive' if change_percent > 0 else 'negative' if change_percent < 0 else 'neutral'
                    }
                    
                    if change_percent > 0:
                        positive_count += 1
                    elif change_percent < 0:
                        negative_count += 1
                    total_count += 1
                    
            except Exception as e:
                sentiment_data['metal_etfs'][symbol] = {'error': str(e)}
        
        # Calculate overall sentiment
        if total_count > 0:
            positive_ratio = positive_count / total_count
            if positive_ratio > 0.6:
                sentiment_data['overall_sentiment'] = 'bullish'
            elif positive_ratio < 0.4:
                sentiment_data['overall_sentiment'] = 'bearish'
            else:
                sentiment_data['overall_sentiment'] = 'neutral'
        
        sentiment_data['sentiment_score'] = {
            'positive': positive_count,
            'negative': negative_count,
            'total': total_count,
            'positive_ratio': positive_ratio if total_count > 0 else 0
        }
        
        return sentiment_data
    
    def get_arbitrage_opportunities(self) -> List[Dict[str, Any]]:
        """
        Identify potential arbitrage opportunities
        
        Returns:
            List of arbitrage opportunities
        """
        opportunities = []
        
        # This is a simplified example - in reality, you'd compare prices across different exchanges
        metals_data = self.get_all_metals_prices()
        
        for metal, data in metals_data.get('metals', {}).items():
            if 'error' not in data:
                # Example: Flag metals with high volatility as potential opportunities
                day_range = data.get('day_high', 0) - data.get('day_low', 0)
                current_price = data.get('price', 0)
                volatility = (day_range / current_price * 100) if current_price > 0 else 0
                
                if volatility > 2:  # More than 2% daily range
                    opportunities.append({
                        'metal': metal,
                        'type': 'high_volatility',
                        'current_price': current_price,
                        'day_range': day_range,
                        'volatility_percent': volatility,
                        'recommendation': f'Monitor {metal} for intraday trading opportunities',
                        'confidence': 'medium' if volatility > 3 else 'low'
                    })
        
        return opportunities
    
    def get_supply_demand_indicators(self) -> Dict[str, Any]:
        """
        Get supply and demand indicators for metals
        
        Returns:
            Dictionary with supply/demand analysis
        """
        # This would typically integrate with inventory data, production reports, etc.
        # For now, we'll use price trends and volume as proxies
        
        indicators = {}
        metals_data = self.get_all_metals_prices()
        
        for metal, data in metals_data.get('metals', {}).items():
            if 'error' not in data:
                change_percent = data.get('change_percent', 0)
                volume = data.get('volume', 0)
                
                # Simple heuristic based on price movement and volume
                if change_percent > 1 and volume > 1000000:
                    demand_signal = 'strong'
                elif change_percent > 0:
                    demand_signal = 'moderate'
                elif change_percent < -1:
                    demand_signal = 'weak'
                else:
                    demand_signal = 'stable'
                
                indicators[metal] = {
                    'demand_signal': demand_signal,
                    'price_trend': 'up' if change_percent > 0 else 'down' if change_percent < 0 else 'flat',
                    'volume_indicator': 'high' if volume > 5000000 else 'normal',
                    'change_percent': change_percent,
                    'volume': volume
                }
        
        return {
            'indicators': indicators,
            'analysis_timestamp': datetime.now().isoformat(),
            'note': 'Analysis based on price trends and trading volume'
        }

# Example usage and testing
if __name__ == "__main__":
    provider = MarketDataProvider()
    
    print("=== Market Data Provider Test ===")
    
    # Test single metal price
    copper_data = provider.get_metal_price('copper')
    print(f"Copper Data: {json.dumps(copper_data, indent=2)}")
    
    # Test all metals
    all_metals = provider.get_all_metals_prices()
    print(f"All Metals: {json.dumps(all_metals, indent=2)}")

