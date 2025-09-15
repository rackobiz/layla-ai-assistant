import re

# Read the current layla.py file
with open('src/routes/layla.py', 'r') as f:
    content = f.read()

# Make sure the get_market_data method actually calls the LME provider
market_data_method = '''
    def get_market_data(self):
        """Get current market data from LME provider"""
        try:
            prices = lme_provider.get_current_prices()
            return prices
        except Exception as e:
            print(f"Error getting market data: {e}")
            return {}
'''

# Replace or add the method
if 'def get_market_data(self):' in content:
    # Replace existing method
    content = re.sub(
        r'def get_market_data\(self\):.*?(?=\n    def|\nclass|\n@|\Z)',
        market_data_method.strip(),
        content,
        flags=re.DOTALL
    )
else:
    # Add the method before generate_response
    content = content.replace(
        'def generate_response(self, user_message, conversation_history=None):',
        market_data_method + '\n    def generate_response(self, user_message, conversation_history=None):'
    )

# Write back
with open('src/routes/layla.py', 'w') as f:
    f.write(content)

print("Fixed market data method")
