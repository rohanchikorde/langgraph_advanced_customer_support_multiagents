// script.js
document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const chatMessages = document.getElementById('chat-messages');
    const connectionStatus = document.getElementById('connection-status');
    const serverStatus = document.getElementById('server-status');
    const clearChatBtn = document.getElementById('clear-chat');
    const exportChatBtn = document.getElementById('export-chat');

    // Configuration
    const API_BASE_URL = 'http://127.0.0.1:8000';
    const USER_ID = 'frontend_user_' + Date.now();
    let isConnected = false;
    let conversationHistory = [];

    // Initialize the application
    initializeApp();

    function initializeApp() {
        checkBackendHealth();
        setupEventListeners();
        loadConversationHistory();
        setInterval(checkBackendHealth, 30000); // Check every 30 seconds
    }

    function setupEventListeners() {
        sendButton.addEventListener('click', handleSendMessage);
        userInput.addEventListener('keypress', handleKeyPress);
        clearChatBtn.addEventListener('click', clearChat);
        exportChatBtn.addEventListener('click', exportChat);
        userInput.addEventListener('input', handleInputChange);
    }

    async function checkBackendHealth() {
        try {
            const response = await fetch(`${API_BASE_URL}/health`, {
                timeout: 5000
            });

            if (response.ok) {
                const data = await response.json();
                updateConnectionStatus(true);
                updateServerStats(data);
            } else {
                updateConnectionStatus(false);
            }
        } catch (error) {
            console.error('Health check failed:', error);
            updateConnectionStatus(false);
        }
    }

    function updateConnectionStatus(connected) {
        isConnected = connected;
        connectionStatus.textContent = connected ? '● Online' : '● Offline';
        connectionStatus.className = connected ? 'status-online' : 'status-offline';
        serverStatus.textContent = connected ? 'Connected' : 'Disconnected';
        sendButton.disabled = !connected;
    }

    function updateServerStats(data) {
        if (data && data.stats) {
            document.getElementById('total-conversations').textContent = data.stats.total_conversations || '-';
            document.getElementById('active-users').textContent = data.stats.active_users || '-';
            document.getElementById('resolution-rate').textContent = data.stats.resolution_rate ? `${data.stats.resolution_rate}%` : '-';
        }
    }

    async function handleSendMessage() {
        const message = userInput.value.trim();
        if (!message || !isConnected) return;

        // Add user message
        addMessage(message, 'user');
        conversationHistory.push({ role: 'user', content: message, timestamp: new Date() });

        // Clear input and disable send button
        userInput.value = '';
        sendButton.disabled = true;

        // Show typing indicator
        showTypingIndicator();

        try {
            const response = await fetch(`${API_BASE_URL}/api/v1/support/query`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: message,
                    user_id: USER_ID,
                    conversation_history: conversationHistory.slice(-10) // Send last 10 messages
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Hide typing indicator
            hideTypingIndicator();

            // Add bot response
            addMessage(data.response, 'bot');
            conversationHistory.push({ role: 'assistant', content: data.response, timestamp: new Date() });

            // Save to local storage
            saveConversationHistory();

        } catch (error) {
            console.error('Error sending message:', error);
            hideTypingIndicator();
            addMessage('Sorry, I encountered an error. Please try again later.', 'bot', true);
        } finally {
            sendButton.disabled = false;
            userInput.focus();
        }
    }

    function handleKeyPress(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    }

    function handleInputChange() {
        const message = userInput.value.trim();
        sendButton.disabled = !message || !isConnected;
    }

    function addMessage(content, sender, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const avatar = sender === 'user' ? '👤' : '🤖';
        const timeString = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        messageDiv.innerHTML = `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content ${isError ? 'error-message' : ''}">
                <div class="message-text">${content}</div>
                <div class="message-time">${timeString}</div>
            </div>
        `;

        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }

    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-indicator';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="message-avatar">🤖</div>
            <div class="message-content">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        chatMessages.appendChild(typingDiv);
        scrollToBottom();
    }

    function hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function clearChat() {
        if (confirm('Are you sure you want to clear the chat history?')) {
            chatMessages.innerHTML = `
                <div class="message bot-message">
                    <div class="message-avatar">🤖</div>
                    <div class="message-content">
                        <div class="message-text">Hello! I'm your AI customer support assistant. How can I help you today?</div>
                        <div class="message-time">Just now</div>
                    </div>
                </div>
            `;
            conversationHistory = [];
            localStorage.removeItem(`chat_history_${USER_ID}`);
        }
    }

    function exportChat() {
        const chatContent = conversationHistory.map(msg => {
            const time = new Date(msg.timestamp).toLocaleString();
            return `[${time}] ${msg.role.toUpperCase()}: ${msg.content}`;
        }).join('\n\n');

        const blob = new Blob([chatContent], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `chat_export_${new Date().toISOString().split('T')[0]}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

    function saveConversationHistory() {
        localStorage.setItem(`chat_history_${USER_ID}`, JSON.stringify(conversationHistory));
    }

    function loadConversationHistory() {
        const saved = localStorage.getItem(`chat_history_${USER_ID}`);
        if (saved) {
            try {
                conversationHistory = JSON.parse(saved);
                // Replay recent messages (last 10)
                const recentMessages = conversationHistory.slice(-10);
                recentMessages.forEach(msg => {
                    addMessage(msg.content, msg.role === 'user' ? 'user' : 'bot');
                });
            } catch (error) {
                console.error('Error loading conversation history:', error);
            }
        }
    }

    // Auto-resize input (optional enhancement)
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = this.scrollHeight + 'px';
    });

    // Initial focus
    userInput.focus();
});