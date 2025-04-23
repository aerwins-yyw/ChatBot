import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

# Try to locate the .env file
env_path = find_dotenv("openai.env")
print(f"Found .env file at: {env_path}")

# Load the .env file
load_dotenv(env_path)

# Get the API key
api_key = os.getenv("OPENAI_API_KEY")
print(f"API Key: [REDACTED]")

# Initialize the client and test
if api_key:
    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Hello, how are you?"}],
            max_tokens=50
        )
        print("API call successful. Response:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Error during API call: {e}")
else:
    print("API key not found in .env file.") 