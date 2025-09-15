import re

# Read the layla.py file
with open('src/routes/layla.py', 'r') as f:
    content = f.read()

# Make sure we have a proper chat route
chat_route = '''
@layla_bp.route('/chat', methods=['POST'])
@cross_origin()
def chat():
    """Handle chat messages"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        user_message = data['message']
        
        # Get conversation history if provided
        conversation_history = data.get('conversation_history', [])
        
        # Generate response using Layla
        layla_agent = LaylaAgent()
        response = layla_agent.generate_response(user_message, conversation_history)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'error': str(e)}), 500
'''

# Check if chat route exists, if not add it
if '@layla_bp.route(\'/chat\'' not in content:
    # Add the chat route before the last route
    content = content.replace(
        '@layla_bp.route(\'/health\'',
        chat_route + '\n@layla_bp.route(\'/health\''
    )

# Write back
with open('src/routes/layla.py', 'w') as f:
    f.write(content)

print("Fixed chat route")
