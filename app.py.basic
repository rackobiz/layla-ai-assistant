import os
import sys
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Load environment variables
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Create Flask app
app = Flask(__name__, static_folder='src/static')
CORS(app)

# Import OpenAI
try:
    import openai
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/layla/chat', methods=['POST'])
def layla_chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        # Create messages for OpenAI
        messages = [
            {
                "role": "system", 
                "content": "You are Layla, an AI trading assistant for Sharif Metals Group specializing in non-ferrous metals trading. You help with market analysis, supplier recommendations, and trading strategies across UAE, GCC, India, China, and European markets. Keep responses concise and professional."
            },
            {"role": "user", "content": message}
        ]
        
        # Call OpenAI API with correct method
        client = openai.OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=300,
            temperature=0.7
        )
        
        return jsonify({
            "response": response.choices[0].message.content,
            "status": "success"
        })
        
    except Exception as e:
        return jsonify({
            "response": f"I apologize, but I'm experiencing technical difficulties: {str(e)}. Please try again in a moment.",
            "status": "error"
        })

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

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "openai": HAS_OPENAI})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
