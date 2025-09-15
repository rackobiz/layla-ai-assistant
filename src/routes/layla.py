from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import json
import os
from datetime import datetime
import openai

layla_bp = Blueprint('layla', __name__)

# Initialize OpenAI client
client = openai.OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_API_BASE')
)

class LaylaAgent:
    def __init__(self):
        self.name = "Layla"
        
    def get_current_lme_prices(self):
        """Get current LME prices"""
        return {
            "copper": {"price": 10380.45, "change": 1.21, "unit": "USD/tonne"},
            "aluminum": {"price": 2657.00, "change": 0.95, "unit": "USD/tonne"},
            "zinc": {"price": 2890.00, "change": 0.15, "unit": "USD/tonne"},
            "lead": {"price": 2050.00, "change": -0.32, "unit": "USD/tonne"},
            "nickel": {"price": 17116.12, "change": 0.11, "unit": "USD/tonne"},
            "tin": {"price": 30607.60, "change": -0.15, "unit": "USD/tonne"}
        }
    
    def generate_response(self, user_message: str) -> str:
        try:
            current_prices = self.get_current_lme_prices()
            
            system_prompt = f"""You are Layla, senior metals trading advisor for Sharif Metals Group.

COMMUNICATION STYLE:
- Direct and straightforward - no unnecessary details
- Expert-level knowledge - assume user understands trading
- Results-focused - always provide actionable insights

CORE EXPERTISE:
- Non-ferrous metals trading (Cu, Al, Zn, Pb, Ni, Sn)
- LME, SHFE, COMEX market dynamics
- BMR (Bureau of International Recycling) standards
- ISRI (Institute of Scrap Recycling Industries) specifications
- Regional arbitrage opportunities

CURRENT LME PRICES:
- Copper: ${current_prices['copper']['price']:,.0f}/tonne ({current_prices['copper']['change']:+.1f}%)
- Aluminum: ${current_prices['aluminum']['price']:,.0f}/tonne ({current_prices['aluminum']['change']:+.1f}%)
- Zinc: ${current_prices['zinc']['price']:,.0f}/tonne ({current_prices['zinc']['change']:+.1f}%)
- Lead: ${current_prices['lead']['price']:,.0f}/tonne ({current_prices['lead']['change']:+.1f}%)
- Nickel: ${current_prices['nickel']['price']:,.0f}/tonne ({current_prices['nickel']['change']:+.1f}%)
- Tin: ${current_prices['tin']['price']:,.0f}/tonne ({current_prices['tin']['change']:+.1f}%)

Always reference these current prices when discussing market conditions."""

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I apologize, but I'm experiencing technical difficulties. Error: {str(e)}"

layla_agent = LaylaAgent()

@layla_bp.route('/status', methods=['GET'])
@cross_origin()
def get_status():
    return jsonify({
        "status": "online",
        "name": "Layla",
        "timestamp": datetime.now().isoformat()
    })

@layla_bp.route('/chat', methods=['POST'])
@cross_origin()
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        response = layla_agent.generate_response(user_message)
        
        return jsonify({
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "agent": "Layla"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@layla_bp.route('/market-data', methods=['GET'])
@cross_origin()
def get_market_data():
    try:
        prices = layla_agent.get_current_lme_prices()
        return jsonify(prices)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
