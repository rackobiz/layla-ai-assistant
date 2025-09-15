import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the Flask app
from main import app

# For Railway deployment
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

# Add missing API endpoints
from flask import request, jsonify
import openai

@app.route('/api/layla/chat', methods=['POST'] )
def layla_chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        history = data.get('history', [])
        
        messages = [{
            "role": "system", 
            "content": "You are Layla, an AI trading assistant for Sharif Metals Group specializing in non-ferrous metals trading. You help with market analysis, supplier recommendations, and trading strategies across UAE, GCC, India, China, and European markets."
        }]
        
        messages.extend(history[-10:])
        messages.append({"role": "user", "content": message})
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        return jsonify({
            "response": response.choices[0].message.content,
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500

@app.route('/api/layla/market-data', methods=['GET'])
def market_data():
    return jsonify({
        "lme_prices": {
            "copper": {"price_usd_per_tonne": 8450, "change_percent": 2.3},
            "aluminum": {"price_usd_per_tonne": 2180, "change_percent": -0.8},
            "zinc": {"price_usd_per_tonne": 2890, "change_percent": 0.5},
            "lead": {"price_usd_per_tonne": 2050, "change_percent": 1.2}
        }
    })
