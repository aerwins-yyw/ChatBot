import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

print("==== OpenAI API Key Validation Script ====")

# Load environment variables
script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_dir, "openai.env")
_ = find_dotenv("openai.env")
load_dotenv(dotenv_path)

# Get API key
api_key = os.getenv("openai_api_key")
print(f"API key type: {type(api_key)}")
print(f"API key length: {len(api_key) if api_key else 0}")
print(f"API key: [REDACTED]")

# Try direct reading of the file
try:
    with open(dotenv_path, "r") as f:
        env_content = f.read().strip()
        print(f"File content length: {len(env_content)}")
        print(f"File content: {env_content}")
except Exception as e:
    print(f"Error reading file: {e}")

# Test the key
if api_key:
    try:
        print("\nAttempting to connect to OpenAI API...")
        client = OpenAI(api_key=api_key)
        models = client.models.list()
        print(f"Connection successful! Available models: {len(models.data)}")
        print("First few models:")
        for model in models.data[:3]:
            print(f" - {model.id}")
        print("\nAPI KEY IS VALID ✓")
    except Exception as e:
        print(f"\nAPI connection error: {type(e).__name__}: {e}")
        print("\nAPI KEY IS INVALID ✗")
else:
    print("\nNo API key found ✗")

print("\n==== End of Validation ====") 