from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
import json
import os
from datetime import datetime
import sys
import openai
sys.path.append('/opt/.manus/.sandbox-runtime')
from src.lme_data_provider import LMEDataProvider
from src.supplier_finder import SupplierFinder

layla_bp = Blueprint('layla', __name__)

# Initialize OpenAI client
client = openai.OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_API_BASE')
)

# Initialize LME data provider for accurate pricing
lme_provider = LMEDataProvider()

# Initialize supplier finder for proactive supplier identification
supplier_finder = SupplierFinder()

class LaylaAgent:
    def __init__(self):
        self.personality = {
            "name": "Layla",
            "role": "Non-ferrous metals trading assistant for Sharif Metals Group",
            "traits": [
                "Sharp and confident",
                "Professional and pragmatic", 
                "Detail-driven and fast-thinking",
                "Assertive and proactive",
                "Loyal and trustworthy"
            ],
            "communication_style": "Clear, direct, professional, concise, actionable, insightful, data-driven",
            "expertise": [
                "Copper, aluminum, lead, zinc trading",
                "LME operations and pricing",
                "UAE, GCC, India, China, European markets",
                "Scrap and semi-refined materials",
                "Arbitrage opportunities",
                "Supply chain optimization"
            ]
        }
        
        self.sharif_metals_context = {
            "company": "Sharif Metals Group",
            "founded": 1963,
            "type": "Family-owned recycling company",
            "position": "Leading recycler in Middle East and North Africa",
            "scale": "650+ employees, >$500M revenue annually",
            "focus": "Circular economy, sustainability, carbon emission reduction",
            "metals": ["Copper", "Aluminum", "Lead", "Zinc", "Nickel alloys", "Brass"],
            "operations": "Procurement, processing, recycling of ferrous and non-ferrous metals",
            "certifications": "ISO 9001:2015"
        }

    def get_system_prompt(self):
        return f"""You are {self.personality['name']}, a {self.personality['role']}.

PERSONALITY TRAITS:
- {', '.join(self.personality['traits'])}

COMMUNICATION STYLE:
{self.personality['communication_style']}

EXPERTISE:
- {', '.join(self.personality['expertise'])}

SHARIF METALS GROUP CONTEXT:
- Company: {self.sharif_metals_context['company']} (founded {self.sharif_metals_context['founded']})
- Type: {self.sharif_metals_context['type']}
- Position: {self.sharif_metals_context['position']}
- Scale: {self.sharif_metals_context['scale']}
- Focus: {self.sharif_metals_context['focus']}
- Main Metals: {', '.join(self.sharif_metals_context['metals'])}
- Operations: {self.sharif_metals_context['operations']}

ENHANCED BEHAVIOR GUIDELINES:
- Be proactive and assertive in your recommendations
- Always consider Sharif Metals Group's interests and market position
- Provide actionable insights backed by data
- Identify opportunities before they become obvious
- Focus on maximizing margins and securing reliable supply
- Consider premiums, freight, FX shifts, and arbitrage opportunities
- Monitor competitor moves and market trends
- ALWAYS provide specific next steps and action items
- Include risk assessments and mitigation strategies
- Suggest concrete supplier contacts when relevant
- Provide price targets and timing recommendations
- Consider regional market dynamics (UAE, GCC, India, China, Europe)

RESPONSE STRUCTURE (ALWAYS FOLLOW):
1. **Market Analysis**: Current situation with specific data points
2. **Strategic Recommendation**: Clear buy/sell/hold recommendation with reasoning
3. **Action Items**: Specific steps Sharif Metals should take immediately
4. **Risk Assessment**: Potential risks and mitigation strategies
5. **Timeline**: When to execute recommendations
6. **Follow-up**: What to monitor and when to reassess

PROACTIVE ELEMENTS TO INCLUDE:
- Supplier recommendations with specific contact suggestions
- Arbitrage opportunities between markets
- Inventory optimization suggestions
- Hedging strategies for price protection
- Market timing for optimal entry/exit points
- Competitive intelligence insights

Remember: You are not just an assistant - you are a trusted trading partner who actively brings opportunities and insights to help Sharif Metals Group stay ahead in the non-ferrous metals market. Be specific, actionable, and always think one step ahead."""

    def get_market_data(self, symbol=None):
        """Get current LME market data for metals"""
        try:
            if symbol:
                # Get specific metal LME data
                return lme_provider.get_lme_price(symbol)
            else:
                # Get all LME metals data
                return lme_provider.get_all_lme_prices()
        except Exception as e:
            return {"error": f"Failed to fetch LME market data: {str(e)}"}

    def generate_response(self, user_message, conversation_history=None):
        """Generate Layla's response using OpenAI with enhanced context"""
        try:
            # Get current market data
            market_data = self.get_market_data()
            
            # Get additional market context
            market_context = self._get_enhanced_market_context()
            
            # Prepare conversation context
            messages = [
                {"role": "system", "content": self.get_system_prompt()},
                {"role": "system", "content": f"Current LME market data: {json.dumps(market_data)}"},
                {"role": "system", "content": f"Market intelligence: {market_context}"}
            ]
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Generate response using OpenAI
            response = client.chat.completions.create(
                model="gemini-2.5-flash",
                messages=messages,
                max_tokens=1500,  # Increased for more detailed responses
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I apologize, but I'm experiencing technical difficulties. Error: {str(e)}"

    def _get_enhanced_market_context(self):
        """Get enhanced market context for more informed responses"""
        # Get supplier intelligence
        supplier_intel = supplier_finder.get_market_supplier_intelligence()
        
        return {
            "market_sentiment": "Bullish on copper due to supply constraints and renewable energy demand",
            "key_trends": [
                "Copper supply disruptions in Chile affecting global prices",
                "Strong demand from renewable energy infrastructure projects",
                "Aluminum production costs rising due to energy prices",
                "Zinc inventory levels at 5-year lows",
                "Lead demand stable from battery sector growth"
            ],
            "regional_insights": {
                "UAE": "Strong construction demand, favorable import conditions",
                "India": "High demand, competitive pricing for scrap materials",
                "China": "Production constraints, export opportunities available",
                "Europe": "Energy costs impacting smelter operations"
            },
            "supplier_intelligence": supplier_intel["new_opportunities"],
            "supplier_alerts": supplier_intel["alerts"],
            "arbitrage_opportunities": [
                "LME-COMEX copper spread at $150/tonne - profitable for large volumes",
                "Regional aluminum price differences between UAE and India markets"
            ]
        }

    def find_suppliers_for_metal(self, metal: str, region: str = None, quantity: int = None):
        """Find suppliers for specific metal requirements"""
        return supplier_finder.find_suppliers(metal, region, quantity)

    def get_supplier_recommendations(self, metal: str, urgency: str = "normal"):
        """Get proactive supplier recommendations"""
        suppliers = self.find_suppliers_for_metal(metal)
        
        if urgency == "urgent":
            # Filter for immediate availability
            urgent_suppliers = [s for s in suppliers.get("verified_suppliers", []) 
                             if s.get("reliability_score", 0) > 8.5]
            return {
                "urgent_suppliers": urgent_suppliers[:3],
                "immediate_actions": suppliers.get("recommendations", {}).get("immediate_actions", []),
                "timeline": "Contact within 2 hours"
            }
        
        return suppliers

# Initialize Layla agent
layla_agent = LaylaAgent()

@layla_bp.route('/chat', methods=['POST'])
@cross_origin()
def chat():
    """Main chat endpoint for Layla"""
    try:
        data = request.json
        user_message = data.get('message', '')
        conversation_history = data.get('history', [])
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        # Generate Layla's response
        response = layla_agent.generate_response(user_message, conversation_history)
        
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
    """Get current market data"""
    try:
        data = layla_agent.get_market_data()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@layla_bp.route('/alerts', methods=['GET'])
@cross_origin()
def get_alerts():
    """Get market alerts and opportunities"""
    try:
        # Mock alerts for now - will be replaced with real analysis
        alerts = [
            {
                "type": "price_alert",
                "metal": "copper",
                "message": "Copper prices up 2.3% - consider securing additional supply",
                "priority": "high",
                "timestamp": datetime.now().isoformat()
            },
            {
                "type": "arbitrage",
                "message": "Arbitrage opportunity: LME-COMEX copper spread at $150/ton",
                "priority": "medium",
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        return jsonify(alerts)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@layla_bp.route('/recommendations', methods=['GET'])
@cross_origin()
def get_recommendations():
    """Get trading and supplier recommendations"""
    try:
        # Get supplier intelligence
        supplier_intel = supplier_finder.get_market_supplier_intelligence()
        
        recommendations = [
            {
                "type": "buy",
                "metal": "aluminum",
                "reason": "Strong demand from UAE construction sector, prices expected to rise",
                "target_price": 2200,
                "confidence": "high",
                "timestamp": datetime.now().isoformat()
            },
            {
                "type": "supplier",
                "metal": "copper_scrap",
                "message": "New supplier identified in Turkey - high-grade copper scrap at competitive rates",
                "action": "Contact for quote",
                "supplier_name": "Ankara Copper Industries",
                "contact": "export@ankaracopper.com.tr",
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        # Add supplier opportunities from intelligence
        for opportunity in supplier_intel["new_opportunities"]:
            recommendations.append({
                "type": "supplier_opportunity",
                "message": opportunity,
                "action": "Investigate and contact",
                "priority": "medium",
                "timestamp": datetime.now().isoformat()
            })
        
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@layla_bp.route('/scenario', methods=['POST'])
@cross_origin()
def run_scenario():
    """Run scenario analysis"""
    try:
        data = request.json
        scenario = data.get('scenario', '')
        
        if not scenario:
            return jsonify({"error": "Scenario description is required"}), 400
        
        # Generate scenario analysis using Layla
        analysis_prompt = f"Analyze this scenario for Sharif Metals Group: {scenario}. Provide detailed impact analysis on margins, operations, and recommendations."
        
        analysis = layla_agent.generate_response(analysis_prompt)
        
        return jsonify({
            "scenario": scenario,
            "analysis": analysis,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@layla_bp.route('/status', methods=['GET'])
@cross_origin()
def get_status():
    """Get Layla's status and capabilities"""
    return jsonify({
        "name": layla_agent.personality["name"],
        "role": layla_agent.personality["role"],
        "status": "online",
        "capabilities": [
            "Real-time market analysis",
            "Trading recommendations",
            "Supplier identification",
            "Scenario modeling",
            "Market alerts",
            "Communication drafting"
        ],
        "markets_monitored": ["UAE", "GCC", "India", "China", "Europe"],
        "metals_expertise": layla_agent.personality["expertise"]
    })



@layla_bp.route('/market-analysis', methods=['GET'])
@cross_origin()
def get_market_analysis():
    """Get comprehensive market analysis"""
    try:
        # Get all LME market data
        market_data = lme_provider.get_all_lme_prices()
        
        # Get LME settlement prices
        settlement_data = lme_provider.get_lme_settlement_prices()
        
        return jsonify({
            "lme_market_data": market_data,
            "settlement_data": settlement_data,
            "timestamp": datetime.now().isoformat(),
            "exchange": "London Metal Exchange"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@layla_bp.route('/sentiment', methods=['GET'])
@cross_origin()
def get_market_sentiment():
    """Get market sentiment analysis"""
    try:
        # Mock sentiment data for now - will be enhanced later
        sentiment = {
            "overall_sentiment": "bullish",
            "confidence": 0.75,
            "factors": [
                "Strong demand from construction sector",
                "Supply chain disruptions in key regions",
                "Positive economic indicators"
            ],
            "timestamp": datetime.now().isoformat()
        }
        return jsonify(sentiment)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@layla_bp.route('/arbitrage', methods=['GET'])
@cross_origin()
def get_arbitrage_opportunities():
    """Get arbitrage opportunities"""
    try:
        # Mock arbitrage opportunities for now - will be enhanced later
        opportunities = [
            {
                "type": "exchange_arbitrage",
                "metal": "copper",
                "exchanges": ["LME", "COMEX"],
                "spread": 150,
                "unit": "USD/tonne",
                "confidence": "high",
                "timestamp": datetime.now().isoformat()
            },
            {
                "type": "regional_arbitrage",
                "metal": "aluminum",
                "regions": ["UAE", "India"],
                "spread": 75,
                "unit": "USD/tonne",
                "confidence": "medium",
                "timestamp": datetime.now().isoformat()
            }
        ]
        return jsonify({"opportunities": opportunities})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@layla_bp.route('/supply-demand', methods=['GET'])
@cross_origin()
def get_supply_demand():
    """Get supply and demand indicators"""
    try:
        # Mock supply-demand indicators for now - will be enhanced later
        indicators = {
            "copper": {
                "supply_status": "tight",
                "demand_trend": "increasing",
                "inventory_level": "low",
                "key_factors": [
                    "Mine disruptions in Chile",
                    "Strong demand from renewable energy sector",
                    "Low LME warehouse stocks"
                ]
            },
            "aluminum": {
                "supply_status": "adequate",
                "demand_trend": "stable",
                "inventory_level": "normal",
                "key_factors": [
                    "Steady production from major smelters",
                    "Construction sector demand stable",
                    "Normal inventory levels"
                ]
            },
            "timestamp": datetime.now().isoformat()
        }
        return jsonify(indicators)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@layla_bp.route('/price-alert', methods=['POST'])
@cross_origin()
def create_price_alert():
    """Create a price alert"""
    try:
        data = request.json
        metal = data.get('metal')
        target_price = data.get('target_price')
        alert_type = data.get('type', 'above')  # above or below
        
        # In a real implementation, this would store the alert in a database
        # For now, we'll just return a confirmation
        
        alert = {
            "id": f"alert_{datetime.now().timestamp()}",
            "metal": metal,
            "target_price": target_price,
            "type": alert_type,
            "created": datetime.now().isoformat(),
            "status": "active"
        }
        
        return jsonify({
            "message": f"Price alert created for {metal}",
            "alert": alert
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@layla_bp.route('/trading-recommendation', methods=['POST'])
@cross_origin()
def get_trading_recommendation():
    """Get AI-powered trading recommendation"""
    try:
        data = request.json
        metal = data.get('metal', 'copper')
        investment_amount = data.get('amount', 100000)
        risk_tolerance = data.get('risk_tolerance', 'medium')
        
        # Get current market data for the metal using LME provider
        market_data = lme_provider.get_lme_price(metal)
        
        # Get market sentiment (mock data for now)
        sentiment = {
            "overall_sentiment": "bullish",
            "confidence": 0.75,
            "factors": ["Strong demand", "Supply constraints"]
        }
        
        # Generate AI recommendation
        recommendation_prompt = f"""
        As Layla, provide a trading recommendation for {metal} with the following context:
        
        Current Market Data:
        - Price: ${market_data.get('price', 0):.2f}
        - Change: {market_data.get('change_percent', 0):.2f}%
        - Volume: {market_data.get('volume', 0):,}
        
        Investment Parameters:
        - Amount: ${investment_amount:,}
        - Risk Tolerance: {risk_tolerance}
        
        Market Sentiment: {sentiment.get('overall_sentiment', 'neutral')}
        
        Provide a specific recommendation with:
        1. Buy/Hold/Sell recommendation
        2. Target price range
        3. Risk assessment
        4. Timeline
        5. Key factors to monitor
        """
        
        response = layla_agent.generate_response(recommendation_prompt)
        
        return jsonify({
            "metal": metal,
            "recommendation": response,
            "market_data": market_data,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@layla_bp.route('/find-suppliers', methods=['POST'])
@cross_origin()
def find_suppliers():
    """Find suppliers for specific metal requirements"""
    try:
        data = request.json
        metal = data.get('metal', 'copper')
        region = data.get('region')
        quantity = data.get('quantity')
        urgency = data.get('urgency', 'normal')
        
        if urgency == 'urgent':
            suppliers = layla_agent.get_supplier_recommendations(metal, urgency)
        else:
            suppliers = layla_agent.find_suppliers_for_metal(metal, region, quantity)
        
        return jsonify(suppliers)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@layla_bp.route('/supplier-intelligence', methods=['GET'])
@cross_origin()
def get_supplier_intelligence():
    """Get current supplier market intelligence"""
    try:
        intelligence = supplier_finder.get_market_supplier_intelligence()
        return jsonify(intelligence)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@layla_bp.route('/validate-supplier', methods=['POST'])
@cross_origin()
def validate_supplier():
    """Validate a specific supplier"""
    try:
        data = request.json
        supplier_name = data.get('supplier_name')
        
        if not supplier_name:
            return jsonify({"error": "Supplier name is required"}), 400
        
        validation = supplier_finder.validate_supplier(supplier_name)
        return jsonify(validation)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@layla_bp.route('/supplier-recommendations', methods=['POST'])
@cross_origin()
def get_supplier_recommendations():
    """Get AI-powered supplier recommendations"""
    try:
        data = request.json
        metal = data.get('metal', 'copper')
        urgency = data.get('urgency', 'normal')
        quantity = data.get('quantity', 1000)
        region = data.get('region')
        
        # Get supplier recommendations
        suppliers = layla_agent.get_supplier_recommendations(metal, urgency)
        
        # Generate AI analysis
        analysis_prompt = f"""
        As Layla, provide detailed supplier recommendations for {metal} with the following context:
        
        Requirements:
        - Metal: {metal}
        - Quantity: {quantity} MT
        - Region preference: {region or 'Any'}
        - Urgency: {urgency}
        
        Available suppliers: {json.dumps(suppliers.get('verified_suppliers', [])[:3])}
        
        Provide specific recommendations including:
        1. Top 3 supplier choices with reasoning
        2. Negotiation strategies
        3. Risk assessment for each supplier
        4. Payment terms recommendations
        5. Quality assurance steps
        6. Timeline for procurement
        """
        
        analysis = layla_agent.generate_response(analysis_prompt)
        
        return jsonify({
            "metal": metal,
            "suppliers": suppliers,
            "ai_analysis": analysis,
            "urgency": urgency,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

