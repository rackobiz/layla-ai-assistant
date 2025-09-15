import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# For Railway deployment, the API key will be set as an environment variable
# For local development, create a .env file with your API key

# Import the app
import sys
sys.path.append('src')
from main import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 Starting Layla AI Trading Assistant...")
    
    # Check if API key is available
    if os.environ.get('OPENAI_API_KEY'):
        print("✅ API Key loaded successfully")
    else:
        print("⚠️  Warning: No API key found. Set OPENAI_API_KEY environment variable.")
    
    print(f"🌐 Access Layla at: http://localhost:{port}" )
    app.run(debug=False, host='0.0.0.0', port=port)
