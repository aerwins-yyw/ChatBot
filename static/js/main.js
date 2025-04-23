document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const chatContainer = document.getElementById('chat-container');
    const loadingIndicator = document.getElementById('loading-indicator');
    const resetButton = document.getElementById('reset-chat');
    
    // Settings elements
    const modelSelect = document.getElementById('model-select');
    const systemMessage = document.getElementById('system-message');
    const temperatureSlider = document.getElementById('temperature-slider');
    const temperatureValue = document.getElementById('temperature-value');
    const modelDescription = document.getElementById('model-description');
    
    // Sidebar toggle
    const openSidebarButton = document.getElementById('open-sidebar');
    const closeSidebarButton = document.getElementById('close-sidebar');
    const sidebar = document.getElementById('sidebar');
    
    // Templates
    const userMessageTemplate = document.getElementById('user-message-template');
    const assistantMessageTemplate = document.getElementById('assistant-message-template');
    
    // State
    let messages = [
        {
            role: "system", 
            content: systemMessage.value
        }
    ];
    let isProcessing = false;
    
    // Initialize the app
    init();
    
    function init() {
        // Focus on input
        userInput.focus();
        
        // Initialize event listeners
        initEventListeners();
        
        // Initialize settings
        updateModelDescription();
        
        // Auto-resize textarea
        userInput.addEventListener('input', autoResizeTextarea);
    }
    
    function initEventListeners() {
        // Send message on button click
        sendButton.addEventListener('click', sendMessage);
        
        // Send message on Enter (without shift)
        userInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
        
        // Reset chat
        resetButton.addEventListener('click', resetChat);
        
        // Update temperature value display
        temperatureSlider.addEventListener('input', () => {
            temperatureValue.textContent = temperatureSlider.value;
        });
        
        // Update model description when model changes
        modelSelect.addEventListener('change', updateModelDescription);
        
        // Sidebar toggle
        openSidebarButton.addEventListener('click', () => {
            sidebar.classList.add('active');
        });
        
        closeSidebarButton.addEventListener('click', () => {
            sidebar.classList.remove('active');
        });
    }
    
    function updateModelDescription() {
        const selectedModel = modelSelect.value;
        
        if (selectedModel === 'gpt-4o-mini') {
            modelDescription.textContent = 'Fastest, most cost-effective';
        } else if (selectedModel === 'gpt-3.5-turbo') {
            modelDescription.textContent = 'Balanced performance';
        } else if (selectedModel === 'gpt-4o') {
            modelDescription.textContent = 'Most capable, slower';
        }
    }
    
    function autoResizeTextarea() {
        // Reset height to auto to get the correct scrollHeight
        userInput.style.height = 'auto';
        
        // Set new height based on scrollHeight (with max-height handled by CSS)
        userInput.style.height = Math.min(userInput.scrollHeight, 120) + 'px';
    }
    
    function sendMessage() {
        // Get and trim message
        const message = userInput.value.trim();
        
        // Don't send empty messages or if already processing
        if (!message || isProcessing) return;
        
        // Add user message to UI
        addMessage('user', message);
        
        // Add user message to the message list
        messages.push({
            role: 'user',
            content: message
        });
        
        // Clear input and reset height
        userInput.value = '';
        userInput.style.height = 'auto';
        
        // Focus back on input
        userInput.focus();
        
        // Add a thinking indicator message
        const thinkingMessageElement = addThinkingIndicator();
        
        // Get response from API
        getAIResponse(thinkingMessageElement);
    }
    
    function addMessage(role, content, timestamp = getCurrentTime()) {
        // Clone appropriate template
        const template = role === 'user' ? userMessageTemplate : assistantMessageTemplate;
        const messageElement = document.importNode(template.content, true);
        
        // Set message content
        const messageText = messageElement.querySelector('.message-text');
        messageText.textContent = content;
        
        // Set timestamp
        const messageTimestamp = messageElement.querySelector('.message-timestamp');
        messageTimestamp.textContent = timestamp;
        
        // Add class to message content
        const messageContent = messageElement.querySelector('.message-content');
        if (messageContent) {
            messageContent.classList.add(role);
        }
        
        // Add message to chat container
        chatContainer.appendChild(messageElement);
        
        // Scroll to bottom
        scrollToBottom();
        
        // Return the message element's text container for possible later updates
        return messageText;
    }
    
    function addThinkingIndicator() {
        // Clone the assistant message template
        const messageElement = document.importNode(assistantMessageTemplate.content, true);
        
        // Get the message text element
        const messageText = messageElement.querySelector('.message-text');
        
        // Create the thinking indicator
        const thinkingIndicator = document.createElement('div');
        thinkingIndicator.className = 'thinking-dots';
        thinkingIndicator.innerHTML = '<span></span><span></span><span></span>';
        
        // Clear existing content and append thinking indicator
        messageText.textContent = '';
        messageText.appendChild(thinkingIndicator);
        
        // Set timestamp
        const messageTimestamp = messageElement.querySelector('.message-timestamp');
        messageTimestamp.textContent = getCurrentTime();
        
        // Add class to message content
        const messageContent = messageElement.querySelector('.message-content');
        if (messageContent) {
            messageContent.classList.add('assistant');
        }
        
        // Add message to chat container
        chatContainer.appendChild(messageElement);
        
        // Scroll to bottom
        scrollToBottom();
        
        // Return the message text element so we can replace it later
        return messageText;
    }
    
    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    function showLoadingIndicator() {
        loadingIndicator.classList.add('active');
        isProcessing = true;
        sendButton.disabled = true;
    }
    
    function hideLoadingIndicator() {
        loadingIndicator.classList.remove('active');
        isProcessing = false;
        sendButton.disabled = false;
    }
    
    function resetChat() {
        // Clear chat UI
        chatContainer.innerHTML = '';
        
        // Reset messages array, keeping system message
        messages = [
            {
                role: "system", 
                content: systemMessage.value
            }
        ];
    }
    
    function getCurrentTime() {
        const now = new Date();
        const hours = now.getHours().toString().padStart(2, '0');
        const minutes = now.getMinutes().toString().padStart(2, '0');
        return `${hours}:${minutes}`;
    }
    
    // Function to simulate text streaming effect
    function typeText(element, text, speed = 10) {
        return new Promise(resolve => {
            let i = 0;
            element.textContent = '';
            
            function type() {
                if (i < text.length) {
                    element.textContent += text.charAt(i);
                    i++;
                    scrollToBottom();
                    setTimeout(type, speed);
                } else {
                    resolve();
                }
            }
            
            type();
        });
    }
    
    async function getAIResponse(thinkingIndicator) {
        // Update system message
        messages[0].content = systemMessage.value;
        
        // Get settings
        const model = modelSelect.value;
        const temperature = parseFloat(temperatureSlider.value);
        
        // Show loading indicator
        showLoadingIndicator();
        
        try {
            console.log('Sending request to /api/chat...');
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    messages: messages,
                    model: model,
                    temperature: temperature
                })
            });
            
            // Check if response is JSON
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                throw new Error(`Server returned non-JSON response: ${contentType}`);
            }
            
            const data = await response.json();
            
            if (response.ok) {
                if (data.response) {
                    // Remove thinking indicator
                    if (thinkingIndicator && thinkingIndicator.parentNode) {
                        thinkingIndicator.parentNode.removeChild(thinkingIndicator);
                    }
                    
                    // Add assistant message to UI with typing effect
                    const messageText = addMessage('assistant', '', getCurrentTime());
                    await typeText(messageText, data.response, 5);
                    
                    // Add to messages array
                    messages.push({
                        role: 'assistant',
                        content: data.response
                    });
                } else {
                    throw new Error('Response missing expected data');
                }
            } else {
                // Show error message from the server
                const errorMsg = data.error || 'Unknown server error';
                console.error('Server error:', errorMsg);
                
                // Remove thinking indicator
                if (thinkingIndicator && thinkingIndicator.parentNode) {
                    thinkingIndicator.parentNode.removeChild(thinkingIndicator);
                }
                
                addMessage('assistant', `Error: ${errorMsg}`, getCurrentTime());
            }
        } catch (error) {
            console.error('Chat request failed:', error);
            
            // Remove thinking indicator
            if (thinkingIndicator && thinkingIndicator.parentNode) {
                thinkingIndicator.parentNode.removeChild(thinkingIndicator);
            }
            
            addMessage('assistant', `Error: ${error.message || 'Could not connect to the server. Please try again.'}`, getCurrentTime());
        } finally {
            hideLoadingIndicator();
        }
    }
}); 