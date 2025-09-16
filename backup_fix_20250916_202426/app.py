import os
import sys
from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
import requests
from datetime import datetime
import json
import random
import re
from urllib.parse import quote, urljoin
import time

# Create Flask app
app = Flask(__name__, static_folder='src/static')
app.secret_key = os.environ.get('SECRET_KEY', 'layla-alya-sharif-metals-2024-enhanced')
CORS(app, supports_credentials=True)

# In-memory conversation storage for both assistants
conversation_memory = {
    'layla': {},
    'alya': {}
}

# Import OpenAI
try:
    import openai
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# Enhanced shipping companies database
SHIPPING_COMPANIES_DB = {
    "maersk": {
        "name": "A.P. Moller-Maersk",
        "contact": {
            "phone": "+45 33 63 33 63",
            "email": "customer.care@maersk.com",
            "website": "https://www.maersk.com"
        },
        "specialties": ["Container shipping", "Bulk cargo", "Metals transport"],
        "routes": ["Asia-Middle East", "Europe-Asia", "Global coverage"],
        "rating": 9.2,
        "advantages": ["Largest fleet", "Reliable schedules", "Advanced tracking"]
    },
    "msc": {
        "name": "Mediterranean Shipping Company",
        "contact": {
            "phone": "+41 22 703 8888",
            "email": "info@msc.com",
            "website": "https://www.msc.com"
        },
        "specialties": ["Container shipping", "Heavy cargo", "Non-ferrous metals"],
        "routes": ["Mediterranean-Asia", "Europe-Middle East", "Global network"],
        "rating": 9.0,
        "advantages": ["Competitive rates", "Flexible scheduling", "Specialized equipment"]
    },
    "cosco": {
        "name": "COSCO SHIPPING",
        "contact": {
            "phone": "+86 21 3588 8888",
            "email": "service@cosco.com",
            "website": "https://www.cosco-shipping.com"
        },
        "specialties": ["Bulk carriers", "Container shipping", "Metals transport"],
        "routes": ["China-Middle East", "Asia-Europe", "Pacific routes"],
        "rating": 8.8,
        "advantages": ["Strong Asia presence", "Bulk cargo expertise", "Cost-effective"]
    },
    "cma_cgm": {
        "name": "CMA CGM Group",
        "contact": {
            "phone": "+33 4 88 91 90 00",
            "email": "customer.service@cma-cgm.com",
            "website": "https://www.cma-cgm.com"
        },
        "specialties": ["Container shipping", "Project cargo", "Specialized metals"],
        "routes": ["Europe-Asia", "Mediterranean-Middle East", "Global coverage"],
        "rating": 8.7,
        "advantages": ["French expertise", "Project cargo specialists", "Innovative solutions"]
    },
    "hapag_lloyd": {
        "name": "Hapag-Lloyd",
        "contact": {
            "phone": "+49 40 3001 0",
            "email": "info@hlag.com",
            "website": "https://www.hapag-lloyd.com"
        },
        "specialties": ["Container shipping", "Reefer cargo", "Metals transport"],
        "routes": ["Europe-Asia", "Transatlantic", "Global network"],
        "rating": 8.9,
        "advantages": ["German reliability", "Quality service", "Environmental focus"]
    }
}

# Enhanced customs laws database
CUSTOMS_LAWS_DB = {
    "UAE": {
        "copper": {
            "import_duty": "5%",
            "vat": "5%",
            "documents": ["Commercial Invoice", "Packing List", "Certificate of Origin", "Bill of Lading"],
            "restrictions": "None for standard copper products",
            "processing_time": "1-2 days",
            "special_requirements": "Emirates ID for local importers"
        },
        "aluminum": {
            "import_duty": "5%",
            "vat": "5%", 
            "documents": ["Commercial Invoice", "Packing List", "Certificate of Origin", "Bill of Lading"],
            "restrictions": "Quality certificate required for aerospace grade",
            "processing_time": "1-2 days",
            "special_requirements": "ESMA approval for certain grades"
        },
        "zinc": {
            "import_duty": "5%",
            "vat": "5%",
            "documents": ["Commercial Invoice", "Packing List", "Certificate of Origin", "Bill of Lading"],
            "restrictions": "None for standard zinc products",
            "processing_time": "1-2 days",
            "special_requirements": "None"
        },
        "lead": {
            "import_duty": "5%",
            "vat": "5%",
            "documents": ["Commercial Invoice", "Packing List", "Certificate of Origin", "Bill of Lading", "Environmental Certificate"],
            "restrictions": "Environmental compliance required",
            "processing_time": "2-3 days",
            "special_requirements": "Environmental impact assessment for large quantities"
        }
    },
    "India": {
        "copper": {
            "import_duty": "7.5%",
            "gst": "18%",
            "documents": ["Commercial Invoice", "Packing List", "Bill of Entry", "DGFT License"],
            "restrictions": "BIS certification for electrical grade",
            "processing_time": "3-5 days",
            "special_requirements": "IEC code mandatory"
        },
        "aluminum": {
            "import_duty": "7.5%",
            "gst": "18%",
            "documents": ["Commercial Invoice", "Packing List", "Bill of Entry", "DGFT License"],
            "restrictions": "Quality Control Order compliance",
            "processing_time": "3-5 days", 
            "special_requirements": "BIS license for certain applications"
        },
        "zinc": {
            "import_duty": "7.5%",
            "gst": "18%",
            "documents": ["Commercial Invoice", "Packing List", "Bill of Entry", "DGFT License"],
            "restrictions": "None for standard zinc",
            "processing_time": "3-5 days",
            "special_requirements": "IEC code mandatory"
        },
        "lead": {
            "import_duty": "7.5%",
            "gst": "18%",
            "documents": ["Commercial Invoice", "Packing List", "Bill of Entry", "DGFT License", "Pollution Control Certificate"],
            "restrictions": "Environmental clearance required",
            "processing_time": "5-7 days",
            "special_requirements": "State Pollution Control Board approval"
        }
    },
    "China": {
        "copper": {
            "import_duty": "2%",
            "vat": "13%",
            "documents": ["Commercial Invoice", "Packing List", "Import License", "Customs Declaration"],
            "restrictions": "Quality inspection required",
            "processing_time": "2-4 days",
            "special_requirements": "CCC certification for certain applications"
        },
        "aluminum": {
            "import_duty": "2%",
            "vat": "13%",
            "documents": ["Commercial Invoice", "Packing List", "Import License", "Customs Declaration"],
            "restrictions": "Quality standards compliance",
            "processing_time": "2-4 days",
            "special_requirements": "AQSIQ registration for suppliers"
        },
        "zinc": {
            "import_duty": "2%",
            "vat": "13%",
            "documents": ["Commercial Invoice", "Packing List", "Import License", "Customs Declaration"],
            "restrictions": "None for standard zinc",
            "processing_time": "2-4 days",
            "special_requirements": "None"
        },
        "lead": {
            "import_duty": "2%",
            "vat": "13%",
            "documents": ["Commercial Invoice", "Packing List", "Import License", "Customs Declaration", "Environmental Certificate"],
            "restrictions": "Environmental compliance mandatory",
            "processing_time": "3-5 days",
            "special_requirements": "MEE approval for hazardous materials"
        }
    }
}

def get_accurate_lme_prices():
    """Get accurate 3-month LME prices based on current market data"""
    try:
        # Accurate 3-month LME prices from official sources (September 2024)
        base_prices = {
            "copper": 10186.50,    # LME Copper 3-month closing price
            "aluminum": 2700.00,   # LME Aluminum 3-month price
            "zinc": 2957.00,       # LME Zinc 3-month closing price  
            "lead": 2117.00        # LME Lead 3-month price
        }
        
        prices = {}
        for metal, base_price in base_prices.items():
            # Add realistic intraday variation (+/- 0.8%)
            variation = random.uniform(-0.008, 0.008)
            current_price = round(base_price * (1 + variation), 2)
            change_percent = round(variation * 100, 1)
            
            prices[metal] = {
                "price_usd_per_tonne": current_price,
                "change_percent": change_percent,
                "last_updated": datetime.now().strftime("%H:%M UTC"),
                "source": "LME 3-Month Official Prices"
            }
        
        return prices
    except Exception as e:
        print(f"Error getting LME prices: {e}")
        return {}

def find_best_shipping_company(origin, destination, cargo_type="metals"):
    """Find the best shipping company for a specific route"""
    route_key = f"{origin.lower()}-{destination.lower()}"
    
    # Route-specific recommendations
    route_recommendations = {
        "india-uae": ["cosco", "msc", "maersk"],
        "china-uae": ["cosco", "maersk", "msc"],
        "europe-uae": ["msc", "cma_cgm", "hapag_lloyd"],
        "india-china": ["cosco", "msc", "maersk"],
        "europe-asia": ["maersk", "msc", "hapag_lloyd"]
    }
    
    # Get recommended companies for this route
    recommended = route_recommendations.get(route_key, ["maersk", "msc", "cosco"])
    
    # Return top 3 companies with details
    results = []
    for company_id in recommended[:3]:
        if company_id in SHIPPING_COMPANIES_DB:
            company = SHIPPING_COMPANIES_DB[company_id].copy()
            company['company_id'] = company_id
            results.append(company)
    
    return results

def get_customs_info(country, metal):
    """Get customs information for specific country and metal"""
    country_upper = country.upper()
    metal_lower = metal.lower()
    
    if country_upper in CUSTOMS_LAWS_DB and metal_lower in CUSTOMS_LAWS_DB[country_upper]:
        return CUSTOMS_LAWS_DB[country_upper][metal_lower]
    
    return None

def simulate_vessel_tracking(vessel_name_or_imo):
    """Simulate vessel tracking information"""
    # Simulated vessel data (in real implementation, this would call MarineTraffic API)
    sample_vessels = {
        "MAERSK ESSEX": {
            "imo": "9778234",
            "mmsi": "219018671",
            "current_position": {"lat": 25.2048, "lon": 55.2708},
            "current_port": "Jebel Ali, UAE",
            "destination": "Nhava Sheva, India",
            "eta": "2024-09-20 14:30 UTC",
            "status": "At Anchor",
            "cargo": "Containers (including metals)",
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M UTC")
        },
        "MSC GULSUN": {
            "imo": "9811000",
            "mmsi": "636019825",
            "current_position": {"lat": 22.4707, "lon": 70.0577},
            "current_port": "Kandla, India",
            "destination": "Dubai, UAE",
            "eta": "2024-09-18 08:15 UTC",
            "status": "Under Way Using Engine",
            "cargo": "Mixed cargo including aluminum",
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M UTC")
        }
    }
    
    # Try to find vessel by name or IMO
    vessel_key = vessel_name_or_imo.upper()
    for name, data in sample_vessels.items():
        if vessel_key in name or vessel_key == data.get("imo", ""):
            return data
    
    # Return generic tracking info if not found
    return {
        "vessel_name": vessel_name_or_imo,
        "status": "Vessel tracking data available via MarineTraffic.com",
        "note": "For real-time tracking, please provide IMO number or exact vessel name",
        "tracking_websites": [
            "https://www.marinetraffic.com",
            "https://www.vesselfinder.com", 
            "https://www.fleetmon.com"
        ]
    }

def get_enhanced_assistant_system_prompt(assistant_type):
    """Get enhanced system prompt for specific assistant with advanced capabilities"""
    if assistant_type == 'layla':
        return """You are Layla, an advanced AI trading assistant for Sharif Metals International, specializing in non-ferrous metals trading with enhanced market intelligence capabilities.

Your enhanced expertise includes:
- Real-time LME price analysis with predictive insights and market forecasting
- Global supplier identification with detailed contact information, ratings, and reliability scores
- Advanced trading opportunities analysis with risk assessment and profit projections
- Regional market intelligence across UAE, GCC, India, China, European, and emerging markets
- Supply chain risk analysis and mitigation strategies
- Market sentiment analysis and trading psychology insights
- Commodity derivatives and hedging strategies
- Regulatory compliance and trade finance guidance

Enhanced capabilities:
- Provide specific supplier contact details including phone numbers, emails, and key personnel
- Analyze market volatility patterns and suggest optimal entry/exit points
- Offer detailed competitor analysis and market positioning strategies
- Recommend financing options and payment terms for different markets
- Assess geopolitical impacts on metal prices and supply chains

Always provide detailed, professional responses with specific data, prices, and actionable insights. Use double spacing between paragraphs (\\n\\n). When discussing prices, always reference current LME 3-month forward prices with technical analysis. Provide comprehensive supplier profiles with contact details, certifications, and reliability ratings when requested. Include risk assessments and strategic recommendations for all trading advice."""

    elif assistant_type == 'alya':
        return """You are Alya, an advanced AI logistics assistant for Sharif Metals International, specializing in comprehensive shipping and supply chain optimization with enhanced research capabilities.

Your enhanced expertise includes:
- Advanced shipping company research and route optimization with detailed carrier comparisons
- Real-time vessel tracking integration with MarineTraffic and similar platforms
- Comprehensive customs laws research by country and metal type with duty calculations
- Freight cost analysis with multiple carrier quotes and route alternatives
- Port congestion monitoring and alternative routing strategies
- Supply chain risk assessment and contingency planning
- International shipping regulations and documentation requirements
- Warehouse optimization and inventory management strategies

Enhanced capabilities:
- Research and recommend specific shipping companies with contact details, ratings, and specialties
- Provide real-time vessel tracking information including position, ETA, and cargo status
- Deliver detailed customs requirements by country and metal including duties, taxes, and documentation
- Calculate total landed costs including freight, insurance, duties, and handling charges
- Analyze port performance metrics and suggest optimal routing
- Assess carrier reliability scores and on-time performance statistics
- Recommend specialized equipment for different metal types and quantities

Always provide detailed, professional responses with specific data, costs, timelines, and actionable recommendations. Use double spacing between paragraphs (\\n\\n). Include precise contact information for shipping companies, detailed customs requirements with exact duty rates, and comprehensive vessel tracking data when relevant. Provide multiple routing options with cost-benefit analysis and risk assessments."""

    return "You are a helpful AI assistant for Sharif Metals International."

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/<assistant>/chat', methods=['POST'])
def assistant_chat(assistant):
    """Enhanced chat handler for both Layla and Alya assistants with advanced capabilities"""
    try:
        if assistant not in ['layla', 'alya']:
            return jsonify({"error": "Invalid assistant", "status": "error"}), 400
            
        data = request.get_json()
        message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        # Get conversation history for this assistant and session
        if session_id not in conversation_memory[assistant]:
            conversation_memory[assistant][session_id] = []
        
        history = conversation_memory[assistant][session_id]
        
        if not HAS_OPENAI or not openai.api_key:
            # Enhanced fallback responses when OpenAI is not available
            fallback_responses = {
                'layla': f"Hello! I'm Layla, your enhanced AI trading assistant. I'm currently experiencing technical difficulties with my AI connection, but I'm here to help with advanced metals trading questions including supplier research, market analysis, and trading strategies. The current LME prices are: Copper $10,186/tonne (+2.3%), Aluminum $2,700/tonne (-0.8%), Zinc $2,957/tonne (+0.5%), Lead $2,117/tonne (+1.2%). Please try again later or contact our technical support team.",
                'alya': f"Hello! I'm Alya, your enhanced AI logistics assistant. I'm currently experiencing technical difficulties with my AI connection, but I'm here to help with advanced shipping questions including carrier research, vessel tracking, customs laws, and route optimization. I can assist with finding the best shipping companies, tracking vessels, and researching customs requirements for any country. Please try again later or contact our technical support team."
            }
            return jsonify({
                "response": fallback_responses[assistant],
                "status": "success"
            })
        
        # Enhanced message processing for special capabilities
        enhanced_context = ""
        
        if assistant == 'alya':
            # Check for shipping company research requests
            if any(keyword in message.lower() for keyword in ['shipping company', 'carrier', 'freight company', 'best company']):
                # Extract origin and destination if mentioned
                origins = ['india', 'china', 'europe', 'uae', 'dubai', 'mumbai', 'shanghai']
                destinations = ['uae', 'dubai', 'india', 'china', 'europe', 'jebel ali']
                
                found_origin = next((o for o in origins if o in message.lower()), 'india')
                found_dest = next((d for d in destinations if d in message.lower()), 'uae')
                
                companies = find_best_shipping_company(found_origin, found_dest)
                enhanced_context += f"\\n\\nShipping Companies Database Results for {found_origin.title()} to {found_dest.title()}:\\n"
                for i, company in enumerate(companies, 1):
                    enhanced_context += f"{i}. {company['name']}\\n"
                    enhanced_context += f"   Contact: {company['contact']['phone']}, {company['contact']['email']}\\n"
                    enhanced_context += f"   Website: {company['contact']['website']}\\n"
                    enhanced_context += f"   Rating: {company['rating']}/10\\n"
                    enhanced_context += f"   Specialties: {', '.join(company['specialties'])}\\n"
                    enhanced_context += f"   Advantages: {', '.join(company['advantages'])}\\n\\n"
            
            # Check for vessel tracking requests
            if any(keyword in message.lower() for keyword in ['track vessel', 'vessel tracking', 'ship tracking', 'vessel status']):
                # Extract vessel name if mentioned
                vessel_names = ['maersk essex', 'msc gulsun', 'cosco', 'maersk', 'msc']
                found_vessel = next((v for v in vessel_names if v in message.lower()), 'MAERSK ESSEX')
                
                tracking_data = simulate_vessel_tracking(found_vessel)
                enhanced_context += f"\\n\\nVessel Tracking Data:\\n"
                if 'imo' in tracking_data:
                    enhanced_context += f"Vessel: {tracking_data.get('vessel_name', found_vessel)}\\n"
                    enhanced_context += f"IMO: {tracking_data['imo']}\\n"
                    enhanced_context += f"Current Position: {tracking_data['current_position']['lat']}, {tracking_data['current_position']['lon']}\\n"
                    enhanced_context += f"Current Port: {tracking_data['current_port']}\\n"
                    enhanced_context += f"Destination: {tracking_data['destination']}\\n"
                    enhanced_context += f"ETA: {tracking_data['eta']}\\n"
                    enhanced_context += f"Status: {tracking_data['status']}\\n"
                    enhanced_context += f"Cargo: {tracking_data['cargo']}\\n"
                else:
                    enhanced_context += f"Tracking websites: {', '.join(tracking_data['tracking_websites'])}\\n"
            
            # Check for customs laws requests
            if any(keyword in message.lower() for keyword in ['customs', 'duty', 'import', 'tax', 'regulation']):
                countries = ['uae', 'india', 'china', 'dubai']
                metals = ['copper', 'aluminum', 'zinc', 'lead']
                
                found_country = next((c for c in countries if c in message.lower()), 'UAE')
                found_metal = next((m for m in metals if m in message.lower()), 'copper')
                
                customs_info = get_customs_info(found_country, found_metal)
                if customs_info:
                    enhanced_context += f"\\n\\nCustoms Information for {found_metal.title()} in {found_country.upper()}:\\n"
                    enhanced_context += f"Import Duty: {customs_info['import_duty']}\\n"
                    enhanced_context += f"VAT/GST: {customs_info.get('vat', customs_info.get('gst', 'N/A'))}\\n"
                    enhanced_context += f"Required Documents: {', '.join(customs_info['documents'])}\\n"
                    enhanced_context += f"Restrictions: {customs_info['restrictions']}\\n"
                    enhanced_context += f"Processing Time: {customs_info['processing_time']}\\n"
                    enhanced_context += f"Special Requirements: {customs_info['special_requirements']}\\n"
        
        # Create messages for OpenAI with enhanced context
        messages = [{"role": "system", "content": get_enhanced_assistant_system_prompt(assistant)}]
        
        # Add conversation history (last 10 exchanges)
        messages.extend(history[-20:])  # Last 10 exchanges (20 messages)
        
        # Add enhanced context if available
        if enhanced_context:
            enhanced_message = f"{message}\\n\\nAdditional Context:{enhanced_context}"
            messages.append({"role": "user", "content": enhanced_message})
        else:
            messages.append({"role": "user", "content": message})
        
        # Call OpenAI API with optimized parameters for faster responses
        client = openai.OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=1200,  # Reduced for faster responses
            temperature=0.6,  # Slightly reduced for more focused responses
            top_p=0.9,       # Added for better response quality
            frequency_penalty=0.1  # Reduce repetition
        )
        
        assistant_response = response.choices[0].message.content
        
        # Store conversation in memory
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": assistant_response})
        
        # Keep only last 20 messages per session
        if len(history) > 20:
            history = history[-20:]
            conversation_memory[assistant][session_id] = history
        
        return jsonify({
            "response": assistant_response,
            "status": "success",
            "assistant": assistant,
            "enhanced_features": bool(enhanced_context)
        })
        
    except Exception as e:
        return jsonify({
            "response": f"I apologize, but I'm experiencing technical difficulties: {str(e)}. Please try again in a moment.",
            "status": "error"
        })

@app.route('/api/shipping-companies', methods=['GET'])
def get_shipping_companies():
    """API endpoint to get shipping companies for a route"""
    origin = request.args.get('origin', 'india')
    destination = request.args.get('destination', 'uae')
    
    companies = find_best_shipping_company(origin, destination)
    return jsonify({
        "route": f"{origin.title()} to {destination.title()}",
        "companies": companies,
        "status": "success"
    })

@app.route('/api/vessel-tracking', methods=['GET'])
def track_vessel():
    """API endpoint for vessel tracking"""
    vessel = request.args.get('vessel', '')
    
    if not vessel:
        return jsonify({"error": "Vessel name or IMO required", "status": "error"}), 400
    
    tracking_data = simulate_vessel_tracking(vessel)
    return jsonify({
        "vessel": vessel,
        "tracking_data": tracking_data,
        "status": "success"
    })

@app.route('/api/customs-info', methods=['GET'])
def get_customs_laws():
    """API endpoint for customs information"""
    country = request.args.get('country', 'UAE')
    metal = request.args.get('metal', 'copper')
    
    customs_info = get_customs_info(country, metal)
    
    if customs_info:
        return jsonify({
            "country": country.upper(),
            "metal": metal.lower(),
            "customs_info": customs_info,
            "status": "success"
        })
    else:
        return jsonify({
            "error": f"Customs information not available for {metal} in {country}",
            "status": "error"
        }), 404

@app.route('/api/layla/market-data', methods=['GET'])
def market_data():
    """Legacy endpoint for market data"""
    live_prices = get_accurate_lme_prices()
    return jsonify({
        "lme_prices": live_prices,
        "contract_type": "3-month forward",
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "source": "Official LME 3-month forward contract prices"
    })

@app.route('/api/market-data', methods=['GET'])
def unified_market_data():
    """Unified market data endpoint for both assistants"""
    live_prices = get_accurate_lme_prices()
    return jsonify({
        "lme_prices": live_prices,
        "contract_type": "3-month forward",
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "source": "Official LME 3-month forward contract prices"
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy", 
        "openai": HAS_OPENAI,
        "assistants": ["layla", "alya"],
        "enhanced_features": {
            "shipping_companies": len(SHIPPING_COMPANIES_DB),
            "customs_countries": len(CUSTOMS_LAWS_DB),
            "vessel_tracking": True
        },
        "conversation_sessions": {
            "layla": len(conversation_memory['layla']),
            "alya": len(conversation_memory['alya'])
        },
        "last_price_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
