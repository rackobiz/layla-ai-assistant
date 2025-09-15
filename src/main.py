import os
from flask import Flask, render_template_string
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
CORS(app)
db = SQLAlchemy(app)

# Import and register blueprints
from src.routes.user import user_bp
from src.routes.layla import layla_bp

app.register_blueprint(user_bp, url_prefix='/api/users')
app.register_blueprint(layla_bp, url_prefix='/')

# Add a simple health check route directly in main.py
@app.route('/health')
def health_check():
    """Health check endpoint"""
    from flask import jsonify
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'api_key_configured': bool(os.getenv('OPENAI_API_KEY')),
        'service': 'Layla AI Trading Assistant'
    })

# Root route
@app.route('/')
def index():
    return render_template_string(open('src/static/index.html').read())

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
