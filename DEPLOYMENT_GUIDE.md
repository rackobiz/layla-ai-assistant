# Layla AI Trading Assistant - Deployment Guide

## Quick Start (Local Testing)

### Prerequisites
- Python 3.11+
- pip package manager

### Local Setup
1. Navigate to the project directory:
   ```bash
   cd layla_ai_agent
   ```

2. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

3. Set environment variables (already configured in sandbox):
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export OPENAI_API_BASE="your-openai-base-url"
   ```

4. Start the application:
   ```bash
   python3.11 src/main.py
   ```

5. Access the application:
   - Open browser to: http://127.0.0.1:5000
   - The application will load with live market data
   - Chat functionality is immediately available

## Production Deployment

### Option 1: Railway Platform (Recommended)
1. Create a Railway account at https://railway.app
2. Connect your GitHub repository
3. Set environment variables in Railway dashboard:
   - `OPENAI_API_KEY`
   - `OPENAI_API_BASE`
4. Deploy directly from the repository
5. Railway will automatically detect the Flask app and deploy

### Option 2: Other Cloud Platforms
The application is compatible with:
- Heroku
- AWS Elastic Beanstalk
- Google Cloud Run
- DigitalOcean App Platform

### Environment Variables Required
```
OPENAI_API_KEY=your-openai-api-key
OPENAI_API_BASE=your-openai-base-url
```

## Application Features

### 1. Live Market Data
- Real-time LME prices for Copper, Aluminum, Lead, Zinc
- Automatic updates every 30 seconds
- Price change indicators

### 2. Enhanced AI Chat
- Structured responses with market analysis
- Proactive supplier recommendations
- Actionable trading strategies
- Risk assessments and timelines

### 3. Supplier Finding
- Click "Find Suppliers" for instant supplier search
- Verified supplier database with reliability scores
- Regional supplier intelligence
- Proactive supplier recommendations

### 4. Quick Actions
- Market Analysis
- Find Suppliers
- Scenario Analysis
- Arbitrage Opportunities

## API Endpoints

### Chat Functionality
- `POST /api/layla/chat` - Main chat interface
- `GET /api/layla/status` - Check Layla's status

### Market Data
- `GET /api/layla/market-data` - Current LME prices
- `GET /api/layla/market-analysis` - Comprehensive market analysis
- `GET /api/layla/sentiment` - Market sentiment analysis

### Supplier Finding
- `POST /api/layla/find-suppliers` - Find suppliers for specific metals
- `GET /api/layla/supplier-intelligence` - Market supplier intelligence
- `POST /api/layla/validate-supplier` - Validate specific suppliers
- `POST /api/layla/supplier-recommendations` - AI-powered recommendations

### Trading Intelligence
- `GET /api/layla/recommendations` - Trading and supplier recommendations
- `GET /api/layla/arbitrage` - Arbitrage opportunities
- `GET /api/layla/alerts` - Market alerts and opportunities

## Troubleshooting

### Common Issues
1. **Module Not Found Error**
   - Ensure you're in the correct directory
   - Install requirements: `pip3 install -r requirements.txt`

2. **Port Already in Use**
   - Change port in `src/main.py`: `app.run(host='0.0.0.0', port=5001)`

3. **API Key Issues**
   - Verify environment variables are set correctly
   - Check API key validity

### Support
For technical issues or questions about deployment, refer to the application logs or contact the development team.

## Security Notes
- Always use HTTPS in production
- Keep API keys secure and never commit them to version control
- Consider implementing user authentication for production use
- Monitor API usage and implement rate limiting if needed

## Performance Optimization
- The application is optimized for real-time trading environments
- Market data updates every 30 seconds to balance freshness with performance
- AI responses are cached where appropriate
- Database queries are optimized for fast supplier lookups

