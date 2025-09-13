from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from datetime import datetime
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

AIRIA_URL = 'https://prodaus.api.airia.ai/v2/PipelineExecution/eacc757c-c433-414f-90b2-e40d7710e530'
AIRIA_HEADERS = {
    'Content-Type': 'application/json',
    'X-API-KEY': 'ak-MTg1MzA4MzE2OXwxNzU3NjY1Njg1ODQwfHRpLVJGTlZJRVJsZGtoaFkyc2dWR1Z1WVc1MElERTN8MXwyMTgxMDE3OTM3'
}

# Timeout settings (in seconds)
CONNECT_TIMEOUT = 30  # Time to establish connection
READ_TIMEOUT = 180    # Time to wait for response (3 minutes)

def format_chat_response(response):
    """Extract response from API response data"""
    try:
        if isinstance(response, list):
            # Look for AIOperation step output
            for step in response:
                if isinstance(step, dict) and step.get('stepType') == 'AIOperation':
                    return str(step.get('output', '')).strip()
            return str(response[-1].get('output', '')) if response else ''
        elif isinstance(response, dict):
            if 'result' in response:
                return str(response['result'])
        return str(response)
    except Exception as e:
        logger.error(f"Error formatting response: {e}")
        return str(response)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_input = data.get('userInput', '')
        conversation_history = data.get('conversationHistory', [])
        tab_info = data.get('tabInfo', {})
        
        if not user_input:
            return jsonify({'error': 'No input provided'}), 400
        
        logger.info(f"Received chat request for URL: {tab_info.get('url', 'unknown')}")
        logger.info(f"Sending request to Airia API with input length: {len(user_input)}")
        
        # Filter conversation history
        filtered_history = [
            msg for msg in conversation_history 
            if msg.get('role') in ('user', 'assistant') and 'content' in msg
        ]
        
        # Prepare payload for Airia API
        payload = {
            "userInput": user_input,
            "asyncOutput": False,
            "context": {
                "previousMessages": filtered_history,
                "metadata": {
                    "source": "browser_extension",
                    "url": tab_info.get('url', ''),
                    "title": tab_info.get('title', '')
                }
            }
        }

        # Make request to Airia API with proper timeout handling
        try:
            response = requests.post(
                AIRIA_URL, 
                headers=AIRIA_HEADERS, 
                json=payload,
                timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
            )
            
            if not response.ok:
                logger.error(f"API request failed with status code {response.status_code}")
                logger.error(f"Response content: {response.text[:500]}...")
                return jsonify({
                    'error': f'API request failed with status code {response.status_code}'
                }), response.status_code
            
            # Format the response
            api_response_data = response.json()
            formatted_response = format_chat_response(api_response_data)
            
            if not formatted_response or formatted_response.strip() == '':
                logger.warning("Received empty response from API")
                formatted_response = "I apologize, but I received an empty response. Please try asking your question again."
            
            logger.info(f"Successfully processed request, response length: {len(formatted_response)}")
            
            return jsonify({
                'response': formatted_response,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
        except requests.exceptions.ConnectTimeout:
            logger.error("Connection to Airia API timed out")
            return jsonify({
                'error': 'Connection timeout - could not connect to AI service. Please try again.'
            }), 504
            
        except requests.exceptions.ReadTimeout:
            logger.error(f"Request to Airia API timed out ({READ_TIMEOUT} seconds)")
            return jsonify({
                'error': f'Request timeout - AI service took longer than {READ_TIMEOUT} seconds to respond. Please try a simpler question or try again later.'
            }), 504
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            return jsonify({
                'error': f'Network error: {str(e)}'
            }), 500
    
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint: {e}")
        return jsonify({
            'error': f'Internal server error: {str(e)}'
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("Starting AI Chat Assistant Server...")
    logger.info("Server will be available at: http://localhost:5000")
    logger.info("Health check endpoint: http://localhost:5000/api/health")
    logger.info(f"API timeout settings: Connect={CONNECT_TIMEOUT}s, Read={READ_TIMEOUT}s")
    
    try:
        app.run(debug=True, port=5000, host='127.0.0.1')
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)