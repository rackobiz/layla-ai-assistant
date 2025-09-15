import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the API key directly for local testing
os.environ['OPENAI_API_KEY'] = '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'
os.environ['OPENAI_API_BASE'] = 'https://api.openai.com/v1'

# Import the app
import sys
sys.path.append('src' )
from main import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 Starting Layla AI Trading Assistant...")
    print("✅ API Key loaded successfully")
    print(f"🌐 Access Layla at: http://localhost:{port}" )
    app.run(debug=False, host='0.0.0.0', port=port)
