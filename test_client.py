import os
import sys
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

print("Starting OpenAI API test...")

# Load environment variables
print("Loading environment variables...")
_ = find_dotenv("openai.env")
load_dotenv("openai.env")

# Get the API key
api_key = os.getenv("openai_api_key")
if not api_key:
    print("ERROR: API key not found in openai.env file!")
    sys.exit(1)

print(f"API key found: {'*' * 10}")

# Initialize client
print("Initializing OpenAI client...")
client = OpenAI(api_key=api_key)

# Send a test request
print("Sending test request...")
try:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello, please respond with the word 'SUCCESS'"}],
        temperature=0.7,
        max_tokens=10
    )
    
    # Print response
    response_content = response.choices[0].message.content
    print(f"Response received: {response_content}")
    
    if "SUCCESS" in response_content:
        print("TEST PASSED: Received expected response.")
    else:
        print(f"TEST WARNING: Received unexpected response content: {response_content}")
        
    print("API test completed successfully!")
    
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {str(e)}")
    print("API test failed!")
    sys.exit(1) 