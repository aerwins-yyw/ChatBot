import os
import streamlit as st
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
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

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are AI-Lumina, an expert investment analyst assistant. Provide concise, data-driven insights on financial markets, investment strategies, and economic trends. Your analysis should be balanced, considering both risks and opportunities. Use professional financial terminology when appropriate."}
    ]

if "system_message" not in st.session_state:
    st.session_state.system_message = "You are AI-Lumina, an expert investment analyst assistant. Provide concise, data-driven insights on financial markets, investment strategies, and economic trends. Your analysis should be balanced, considering both risks and opportunities. Use professional financial terminology when appropriate."

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "gpt-4o-mini"

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7

if "thinking" not in st.session_state:
    st.session_state.thinking = False

# Function to generate AI response
def generate_response(messages):
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Get the response from the selected model
        response = client.chat.completions.create(
            model=st.session_state.selected_model,
            messages=messages,
            temperature=st.session_state.temperature,
            max_tokens=1000
        )
        
        # Get response content
        result = response.choices[0].message.content
        print(f"Response successfully received, length: {len(result)}")
        return result
    except Exception as e:
        error_message = str(e)
        
        # Print detailed error for debugging
        print(f"ERROR TYPE: {type(e).__name__}")
        print(f"ERROR MESSAGE: {error_message}")
        
        # Make error message more user-friendly
        if "Incorrect API key" in error_message:
            return "❌ Error: Invalid API key. Please check your OpenAI API key in the openai.env file."
        elif "Rate limit" in error_message:
            return "❌ Error: You've reached OpenAI's rate limit. Please wait a moment before trying again."
        elif "invalid_api_key" in error_message.lower():
            return "❌ Error: Your API key format is correct, but OpenAI rejected it. It may have been revoked or have insufficient credits."
        elif "Connection" in error_message or "timeout" in error_message.lower():
            return "❌ Error: Connection error. Please check your internet connection and try again."
        elif "billing" in error_message.lower():
            return "❌ Error: Billing issue. Your OpenAI account may not have a valid payment method or sufficient credits."
        else:
            return f"❌ Error: {error_message}"

# Page configuration
st.set_page_config(
    page_title="AI-Lumina", 
    page_icon="📊", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Apply BCG-style CSS
st.markdown("""
<style>
    /* BCG-style colors */
    :root {
        --bcg-dark-blue: #082A46;
        --bcg-medium-blue: #0E6BA8;
        --bcg-light-blue: #1A9ADA;
        --bcg-teal: #00A3B4;
        --bcg-light-teal: #91D2CD;
        --bcg-light-gray: #F5F7F9;
        --bcg-dark-gray: #4A4A4A;
    }
    
    /* Remove all default whitespace */
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }
    
    /* Header styling */
    h1 {
        color: var(--bcg-dark-blue);
        font-weight: 300;
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--bcg-light-gray);
        border-right: 1px solid #eaeaea;
    }
    
    [data-testid="stSidebar"] h1 {
        font-size: 1.2rem;
        padding-left: 1rem;
        color: var(--bcg-dark-blue);
    }
    
    /* Message styling */
    .chat-message {
        padding: 0.8rem 1.2rem;
        border-radius: 4px;
        margin-bottom: 0.8rem;
        max-width: 90%;
        line-height: 1.4;
    }
    
    .user {
        background-color: var(--bcg-light-gray);
        border-left: 3px solid var(--bcg-dark-blue);
        margin-left: auto;
    }
    
    .assistant {
        background-color: white;
        border-left: 3px solid var(--bcg-teal);
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    /* Message timestamp */
    .message-timestamp {
        font-size: 0.7rem;
        color: #888;
        margin-top: 0.4rem;
        text-align: right;
    }
    
    /* Input field styling */
    div[data-baseweb="input"] {
        border-radius: 4px !important;
    }
    
    div[data-baseweb="input"] input {
        font-size: 0.9rem !important;
    }
    
    /* Button styling */
    .stButton button {
        background-color: var(--bcg-teal) !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 400 !important;
    }
    
    .stButton button:hover {
        background-color: var(--bcg-medium-blue) !important;
    }
    
    /* Typing indicator */
    .typing-indicator {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
        margin-left: 5px;
    }
    
    .typing-indicator span {
        height: 8px;
        width: 8px;
        float: left;
        margin: 0 1px;
        background-color: var(--bcg-light-teal);
        display: block;
        border-radius: 50%;
        opacity: 0.4;
    }
    
    .typing-indicator span:nth-of-type(1) {
        animation: 1s blink infinite 0.3333s;
    }
    
    .typing-indicator span:nth-of-type(2) {
        animation: 1s blink infinite 0.6666s;
    }
    
    .typing-indicator span:nth-of-type(3) {
        animation: 1s blink infinite 0.9999s;
    }
    
    @keyframes blink {
        50% {
            opacity: 1;
        }
    }
    
    /* Logo area */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .logo-text {
        font-size: 1.8rem;
        font-weight: 300;
        color: var(--bcg-dark-blue);
        letter-spacing: 0.5px;
    }
    
    .logo-subtitle {
        font-size: 0.9rem;
        color: var(--bcg-dark-gray);
        font-weight: 300;
    }
    
    /* Hide Streamlit branding */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    /* Chat container styling */
    .chat-container {
        height: calc(100vh - 160px);
        overflow-y: auto;
        border: 1px solid #eaeaea;
        border-radius: 6px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with settings
with st.sidebar:
    st.title("Settings")
    
    # Model selection
    st.session_state.selected_model = st.selectbox(
        "AI Model",
        ["gpt-4o-mini", "gpt-3.5-turbo", "gpt-4o"],
        index=0
    )
    
    # System message
    st.session_state.system_message = st.text_area(
        "System Instructions",
        value=st.session_state.system_message,
        height=150
    )
    
    # Update system message in message list
    if st.session_state.messages[0]["role"] == "system":
        st.session_state.messages[0]["content"] = st.session_state.system_message
    
    # Temperature slider
    st.session_state.temperature = st.slider(
        "Response Creativity",
        min_value=0.0,
        max_value=1.0,
        value=st.session_state.temperature,
        step=0.1,
        help="Lower values provide more deterministic responses, higher values more creative ones"
    )
    
    # Clear conversation button
    if st.button("Reset Conversation", use_container_width=True):
        st.session_state.messages = [
            {"role": "system", "content": st.session_state.system_message}
        ]
        st.rerun()

# Logo and title
st.markdown("""
<div class="logo-container">
    <div>
        <div class="logo-text">AI-Lumina</div>
        <div class="logo-subtitle">Investment Analysis Assistant</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display messages
display_messages = [m for m in st.session_state.messages if m["role"] != "system"]

# Display chat messages
for message in display_messages:
    role_class = "user" if message["role"] == "user" else "assistant"
    timestamp = message.get("timestamp", "")
    
    st.markdown(f"""
    <div class="chat-message {role_class}">
        {message["content"]}
        <div class="message-timestamp">{timestamp}</div>
    </div>
    """, unsafe_allow_html=True)

# Display typing indicator when thinking
if st.session_state.thinking:
    st.markdown("""
    <div class="typing-indicator">
        <span></span>
        <span></span>
        <span></span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Simple input area
col1, col2 = st.columns([5, 1])

with col1:
    user_input = st.text_input(
        "Message",
        placeholder="Ask about investments, market trends, or financial analysis...",
        key="user_input",
        on_change=None,
        label_visibility="collapsed"
    )

with col2:
    send_button = st.button(
        "Send", 
        use_container_width=True,
        disabled=not api_key_valid
    )

# Handle enter key press with JavaScript
st.markdown("""
<script>
document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        const sendButton = document.querySelector('button[kind="primary"]');
        if (sendButton) {
            sendButton.click();
        }
    }
});
</script>
""", unsafe_allow_html=True)

# Process input and generate response
if send_button and user_input.strip() and api_key_valid:
    # Add user message to chat
    current_time = datetime.now().strftime("%H:%M")
    st.session_state.messages.append({"role": "user", "content": user_input, "timestamp": current_time})
    
    # Set thinking state and rerun to show user message
    st.session_state.thinking = True
    st.rerun()

# If in thinking state, generate response
if st.session_state.thinking and api_key_valid:
    # Prepare messages for API
    api_messages = []
    for m in st.session_state.messages:
        if m["role"] in ["user", "assistant", "system"]:
            api_messages.append({"role": m["role"], "content": m["content"]})
    
    # Generate response
    response_content = generate_response(api_messages)
    
    # Add response to chat
    current_time = datetime.now().strftime("%H:%M")
    st.session_state.messages.append(
        {"role": "assistant", "content": response_content, "timestamp": current_time}
    )
    
    # Reset thinking state
    st.session_state.thinking = False
    st.rerun() 