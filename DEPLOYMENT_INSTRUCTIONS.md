# Layla AI - Fixed Deployment Instructions

## Issues Fixed:
1. ✅ Market data display now works correctly
2. ✅ Mobile responsiveness improved
3. ✅ Copper prices displayed in tonnes (not pounds)
4. ✅ Error handling for market data API
5. ✅ Touch-friendly mobile interface

## Railway Deployment:

1. **Upload this entire folder to Railway**
   - Connect your GitHub repository
   - Or use Railway CLI: `railway deploy`

2. **Set Environment Variables in Railway Dashboard:**
   ```
   OPENAI_API_KEY=your_actual_openai_api_key
   OPENAI_API_BASE=https://api.openai.com/v1
   ```

3. **Deploy**
   - Railway will automatically detect the configuration
   - The app will start with `gunicorn --bind 0.0.0.0:$PORT app:app`

## Files Changed:
- `src/static/index.html` - Fixed market data JavaScript and mobile CSS
- `app.py` - New Railway-compatible startup script
- `requirements.txt` - Updated dependencies
- `Procfile` - Railway deployment configuration
- `railway.json` - Railway build configuration

## Testing:
After deployment, the market data should load automatically and display:
- Copper prices in USD/tonne
- Real-time price changes
- Mobile-responsive design
- Touch-friendly interface

## Support:
If you encounter any issues, check the Railway logs for error messages.
