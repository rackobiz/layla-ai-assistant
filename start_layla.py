import os
from dotenv import load_dotenv

load_dotenv()

import sys
sys.path.append('src')
from main import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
