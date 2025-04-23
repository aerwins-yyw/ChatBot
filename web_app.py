import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
import base64
import time
from datetime import datetime

# Load environment variables
script_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(script_dir, "openai.env")
_ = find_dotenv("openai.env")
load_dotenv(dotenv_path)

# Set OpenAI API key
api_key = os.getenv("openai_api_key")
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
    print(f"API key loaded successfully: {'*' * 15}")
else:
    print("Failed to load API key from openai.env file")

# Check if API key is available and valid
api_key_valid = bool(api_key and len(api_key) > 10)

# Page configuration
st.set_page_config(
    page_title="ChatBot",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Function to encode image to base64
def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

# Try to load the logo image
try:
    logo_base64 = get_base64_encoded_image("logo.png")
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" style="height:100px; margin-bottom:20px;">'
except Exception:
    # Fallback if image can't be loaded
    logo_html = '<h1 style="color: #A89888;">AI Chat Assistant</h1>'

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .stTextInput, .stSelectbox {
        margin-bottom: 5px;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.75rem;
        margin-bottom: 1rem;
        display: flex;
        animation: fadeIn 0.5s;
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    .chat-message.user {
        background-color: #e3f2fd;
        color: #0d47a1;
        border-bottom-right-radius: 0.25rem;
        align-self: flex-end;
        margin-left: 40px;
    }
    .chat-message.bot {
        background-color: #f1f1f1;
        color: #333;
        border-bottom-left-radius: 0.25rem;
        align-self: flex-start;
        margin-right: 40px;
    }
    .chat-container {
        padding-bottom: 5rem;
    }
    .thinking-animation {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    .dot {
        height: 10px;
        width: 10px;
        margin-right: 5px;
        border-radius: 50%;
        background-color: #bbb;
        animation: pulse 1.5s infinite ease-in-out;
    }
    .dot:nth-child(2) {
        animation-delay: 0.3s;
    }
    .dot:nth-child(3) {
        animation-delay: 0.6s;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.5); }
    }
</style>
""", unsafe_allow_html=True)

# App title
st.title("💬 ChatBot")

# Sidebar 
with st.sidebar:
    st.header("Settings")
    
    # Model selection
    st.session_state.selected_model = st.selectbox(
        "Select Model",
        options=["gpt-3.5-turbo", "gpt-4", "gpt-4o"],
        index=0
    )
    
    # System instructions
    st.session_state.system_instructions = st.text_area(
        "System Instructions",
        "You are a helpful AI assistant.",
        height=100
    )
    
    # Temperature slider
    st.session_state.temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1
    )
    
    st.markdown("---")
    
    if not api_key_valid:
        st.error("⚠️ API Key Missing or Invalid")
        st.markdown("""
        Add your OpenAI API key to the `openai.env` file with the format:
        ```
        openai_api_key=your_api_key_here
        ```
        """)
    else:
        st.success("✅ API Key is valid")

# Display header
st.markdown(f"""
<div class="header-container">
    {logo_html}
    <p>Ask me anything and I'll do my best to help you!</p>
</div>
""", unsafe_allow_html=True)

# Display API key error if not valid
if not api_key_valid:
    st.markdown("""
    <div class="error-container">
        <h3>⚠️ API Key Missing or Invalid</h3>
        <p>Please add a valid OpenAI API key to the <code>openai.env</code> file with the format:</p>
        <p><code>openai_api_key=your_api_key_here</code></p>
        <p>You can get an API key from <a href="https://platform.openai.com/api-keys" target="_blank">OpenAI's website</a>.</p>
    </div>
    """, unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": st.session_state.system_instructions},
        {"role": "assistant", "content": "Hello! How can I help you today?"}
    ]

# Initialize thinking state
if "thinking" not in st.session_state:
    st.session_state.thinking = False

# Display chat messages
for i, message in enumerate(st.session_state.messages):
    if message["role"] == "system":
        continue
    
    with st.container():
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot">{message["content"]}</div>', unsafe_allow_html=True)

# Function for AI response
def generate_response():
    with st.spinner():
        try:
            if st.session_state.thinking:
                # Make sure system message is updated
                if st.session_state.messages and st.session_state.messages[0]["role"] == "system":
                    st.session_state.messages[0]["content"] = st.session_state.system_instructions
                
            # Print debug info
            print(f"Using model: {st.session_state.selected_model}")
            print(f"API key validity check: {api_key_valid}")
                print(f"API key: [REDACTED]")
            
            # Create clean message list for API
                messages_for_api = st.session_state.messages.copy()
            
                # Initialize API client
            client = OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=st.session_state.selected_model,
                    messages=[{"role": m["role"], "content": m["content"]} for m in messages_for_api],
                    temperature=st.session_state.temperature,
                    max_tokens=1000,
                    stream=False
                )
                
                # Add the response to the message history
                assistant_response = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        except Exception as e:
            error_message = str(e)
            print(f"Error: {error_message}")
            
            if "insufficient_quota" in error_message.lower():
                error_response = "I apologize, but the API key has insufficient quota. Please check your usage limits."
            elif "invalid_api_key" in error_message.lower():
                error_response = "I apologize, but the API key seems to be invalid. Please check your API key."
            else:
                error_response = f"I apologize, but an error occurred: {error_message}"
            
            st.session_state.messages.append({"role": "assistant", "content": error_response})
        
        st.session_state.thinking = False

# User input area
with st.container():
    st.markdown('<div class="chat-container"></div>', unsafe_allow_html=True)
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_input = st.text_input("Type your message here:", key="user_input")
    
    with col2:
        send_button = st.button("Send", key="send", disabled=not api_key_valid)
    
    # Process input and display thinking animation when Send is clicked
    if send_button and user_input.strip() and api_key_valid:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Set thinking state to trigger response generation
        st.session_state.thinking = True
    
    # When in thinking state, generate response and rerun to update UI
    if st.session_state.thinking and api_key_valid:
        with st.container():
            st.markdown(
                """
                <div class="thinking-animation">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div>
                """, 
                unsafe_allow_html=True
            )
        
        # Generate response
        generate_response()
        
        # Rerun to update UI with the new message
        st.rerun()

# Add a footer
st.markdown("""
<div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; color: #888; font-size: 12px;">
    Powered by OpenAI's API • Built with Streamlit
</div>
""", unsafe_allow_html=True) 

# Run the app
if __name__ == "__main__":
    pass  # The app is already running by Streamlit 