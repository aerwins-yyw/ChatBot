from flask import Flask, request, jsonify, render_template, session
import os
from dotenv import load_dotenv
import openai
from datetime import datetime
import json

# Load environment variables from .env file if it exists
load_dotenv('openai.env')

# Get OpenAI API key from environment variable
openai_api_key = os.getenv("openai_api_key")
if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key
    print(f"API key loaded: {'*' * 10}")
else:
    print("Failed to load API key from openai.env file")

app = Flask(__name__, static_folder='../static', template_folder='../templates')
app.secret_key = os.getenv("SECRET_KEY", "default-secret-key-replace-in-production")

# Function to generate AI response
def generate_response(messages, model="gpt-3.5-turbo"):
    client = openai.OpenAI(api_key=openai_api_key)
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=1000,
        )
        return response.choices[0].message.content
    except Exception as e:
        error_message = str(e)
        print(f"Error: {error_message}")
        
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
    data = request.json
    messages = data.get('messages', [])
    model = data.get('model', 'gpt-3.5-turbo')
    
    response = generate_response(messages, model)
    return jsonify({'response': response})

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