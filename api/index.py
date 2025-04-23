from flask import Flask, request, jsonify, render_template, session
import os
from dotenv import load_dotenv
from openai import OpenAI  # Import the OpenAI class directly
from datetime import datetime
import json

# Try to get API key from environment variables first (for Vercel deployment)
openai_api_key = os.environ.get("OPENAI_API_KEY")

# If not found in environment variables, try to load from .env file
if not openai_api_key:
    # Load environment variables from .env file if it exists
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    dotenv_path = os.path.join(parent_dir, "openai.env")
    load_dotenv(dotenv_path)
    
    # Try to get API key from loaded .env file
    openai_api_key = os.getenv("openai_api_key")

# Log API key status
if openai_api_key:
    print(f"API key loaded: {'*' * 10}")
else:
    print("Failed to load API key from environment variables or openai.env file")

app = Flask(__name__, static_folder='../static', template_folder='../templates')
app.secret_key = os.getenv("SECRET_KEY", "default-secret-key-replace-in-production")

# Function to generate AI response
def generate_response(messages, model="gpt-3.5-turbo"):
    if not openai_api_key:
        return "Error: OpenAI API key not found. Please add it to environment variables or the openai.env file."
        
    try:
        # Create the OpenAI client with just the API key
        client = OpenAI(api_key=openai_api_key)
        
        # Log client initialization
        print(f"Sending request to model: {model}")
        
        # Create a chat completion
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000
        )
        
        # Extract and return the response content
        return response.choices[0].message.content
        
    except Exception as e:
        error_message = str(e)
        print(f"Error generating response: {error_message}")
        
        if "insufficient_quota" in error_message.lower():
            return "Error: Your OpenAI API key has insufficient quota. Please check your usage."
        elif "invalid_api_key" in error_message.lower():
            return "Error: Invalid API key. Please check your OpenAI API key."
        else:
            return f"Error: Unable to generate response. {error_message}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400
            
        messages = data.get('messages', [])
        model = data.get('model', 'gpt-3.5-turbo')
        
        response = generate_response(messages, model)
        
        # Check if the response starts with "Error:"
        if response.startswith("Error:"):
            return jsonify({'error': response}), 500
            
        return jsonify({'response': response})
    except Exception as e:
        print(f"Chat endpoint error: {str(e)}")
        return jsonify({'error': f"Server error: {str(e)}"}), 500

@app.route('/api/models', methods=['GET'])
def get_models():
    models = [
        {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "description": "Fastest, most cost-effective"},
        {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "description": "Balanced performance"},
        {"id": "gpt-4o", "name": "GPT-4o", "description": "Most capable, slower"}
    ]
    return jsonify(models)

if __name__ == '__main__':
    app.run(debug=True) 