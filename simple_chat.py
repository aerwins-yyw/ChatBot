import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

# Load the .env file
env_path = find_dotenv("openai.env")
load_dotenv(env_path)

# Get the API key
api_key = os.getenv("openai_api_key")
print(f"API Key loaded: {'*' * 10}" if api_key else "API key not found")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Chat history
messages = []

def get_gpt4o_response(user_input):
    # Add user message to history
    messages.append({"role": "user", "content": user_input})
    
    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            stream=True,
        )
        
        # Print assistant response
        print("\nGPT-4o: ", end="")
        full_response = ""
        
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_response += content
                print(content, end="", flush=True)
        
        print("\n")
        
        # Add assistant response to history
        messages.append({"role": "assistant", "content": full_response})
        
    except Exception as e:
        print(f"\nError: {str(e)}\n")

# Main chat loop
print("Welcome to Elegant AI Chat (Console Version)!")
print("Type 'exit' to end the conversation")
print("-" * 50)

while True:
    user_input = input("You: ")
    
    if user_input.lower() in ["exit", "quit", "bye"]:
        print("Goodbye!")
        break
        
    get_gpt4o_response(user_input) 