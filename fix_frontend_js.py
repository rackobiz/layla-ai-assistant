import re

# Read the HTML file
with open('src/static/index.html', 'r') as f:
    content = f.read()

# Fix the sendMessage function
new_send_function = '''
        function sendMessage() {
            const input = document.getElementById('chat-input');
            const message = input.value.trim();
            
            if (!message) return;
            
            // Add user message to chat
            addMessage(message, 'user');
            input.value = '';
            
            // Show loading
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'message layla';
            loadingDiv.innerHTML = `
                <div class="message-content">
                    <div class="loading">
                        <span>Layla is thinking</span>
                        <div class="loading-dots">
                            <div class="loading-dot"></div>
                            <div class="loading-dot"></div>
                            <div class="loading-dot"></div>
                        </div>
                    </div>
                </div>
            `;
            document.getElementById('chat-messages').appendChild(loadingDiv);
            scrollToBottom();
            
            // Send to backend
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    conversation_history: []
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // Remove loading message
                loadingDiv.remove();
                
                if (data.error) {
                    addMessage(`Sorry, I encountered an error: ${data.error}`, 'layla');
                } else {
                    addMessage(data.response, 'layla');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                loadingDiv.remove();
                addMessage('Sorry, I\'m having trouble connecting right now. Please try again.', 'layla');
            });
        }'''

# Replace the sendMessage function
content = re.sub(
    r'function sendMessage\(\)\s*\{[^}]*\}',
    new_send_function.strip(),
    content,
    flags=re.DOTALL
)

# Write back
with open('src/static/index.html', 'w') as f:
    f.write(content)

print("Fixed frontend JavaScript")
