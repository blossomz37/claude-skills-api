// Global state
let sessionId = generateSessionId();
let attachedFiles = [];
let totalTokens = 0;
let messageCount = 0;

// DOM elements
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const attachBtn = document.getElementById('attachBtn');
const fileInput = document.getElementById('fileInput');
const attachmentPreview = document.getElementById('attachmentPreview');
const skillSelect = document.getElementById('skillSelect');
const temperature = document.getElementById('temperature');
const tempValue = document.getElementById('tempValue');
const maxTokens = document.getElementById('maxTokens');
const exportBtn = document.getElementById('exportBtn');
const clearBtn = document.getElementById('clearBtn');
const messageCountEl = document.getElementById('messageCount');
const tokenCountEl = document.getElementById('tokenCount');
const settingsBtn = document.getElementById('settingsBtn');
const settingsModal = document.getElementById('settingsModal');
const apiKeyInput = document.getElementById('apiKeyInput');
const defaultSkillInput = document.getElementById('defaultSkillInput');
const settingsStatus = document.getElementById('settingsStatus');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadSettingsFromStorage();
    checkApiKey();
    loadSkills();
    setupEventListeners();
    autoResizeTextarea();
});

function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

function setupEventListeners() {
    sendBtn.addEventListener('click', sendMessage);
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    attachBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);
    
    temperature.addEventListener('input', (e) => {
        tempValue.textContent = e.target.value;
    });
    
    exportBtn.addEventListener('click', exportChat);
    clearBtn.addEventListener('click', clearChat);
    settingsBtn.addEventListener('click', openSettings);
    
    messageInput.addEventListener('input', autoResizeTextarea);
}

function autoResizeTextarea() {
    messageInput.style.height = 'auto';
    messageInput.style.height = messageInput.scrollHeight + 'px';
}

// Settings Management
function loadSettingsFromStorage() {
    const apiKey = localStorage.getItem('anthropic_api_key');
    const defaultSkill = localStorage.getItem('default_skill_id');
    
    if (apiKey) {
        apiKeyInput.value = apiKey;
    }
    if (defaultSkill) {
        defaultSkillInput.value = defaultSkill;
    }
}

function checkApiKey() {
    const apiKey = localStorage.getItem('anthropic_api_key');
    if (!apiKey) {
        openSettings();
        setTimeout(() => {
            showSettingsMessage('Please enter your Anthropic API key to get started.', 'error');
        }, 300);
    }
}

function openSettings() {
    settingsModal.classList.add('active');
    settingsStatus.className = 'settings-status';
    settingsStatus.textContent = '';
}

function closeSettings() {
    settingsModal.classList.remove('active');
}

function saveSettings() {
    const apiKey = apiKeyInput.value.trim();
    
    if (!apiKey) {
        showSettingsMessage('API key is required.', 'error');
        return;
    }
    
    if (!apiKey.startsWith('sk-ant-')) {
        showSettingsMessage('Invalid API key format. Should start with "sk-ant-"', 'error');
        return;
    }
    
    // Save to localStorage
    localStorage.setItem('anthropic_api_key', apiKey);
    localStorage.setItem('default_skill_id', defaultSkillInput.value.trim());
    
    showSettingsMessage('✓ Settings saved successfully!', 'success');
    
    // Reload skills with new API key
    loadSkills();
    
    setTimeout(() => {
        closeSettings();
    }, 1500);
}

function showSettingsMessage(message, type) {
    settingsStatus.className = `settings-status ${type}`;
    settingsStatus.textContent = message;
}

function getApiKey() {
    return localStorage.getItem('anthropic_api_key');
}

function getDefaultSkillId() {
    return localStorage.getItem('default_skill_id') || '';
}


async function loadSkills() {
    const apiKey = getApiKey();
    if (!apiKey) return;
    
    try {
        const response = await fetch('/api/skills', {
            headers: {
                'X-API-Key': apiKey
            }
        });
        
        const data = await response.json();
        
        // Clear existing options except first
        skillSelect.innerHTML = '<option value="">No Skill (Standard Claude)</option>';
        
        data.skills.forEach(skill => {
            const option = document.createElement('option');
            option.value = skill.id;
            option.textContent = `${skill.name} (${skill.type})`;
            skillSelect.appendChild(option);
        });
        
        // Set default skill if configured
        const defaultSkill = getDefaultSkillId();
        if (defaultSkill) {
            skillSelect.value = defaultSkill;
        }
    } catch (error) {
        console.error('Failed to load skills:', error);
        addSystemMessage('Failed to load skills. Please check your API key in settings.');
    }
}

async function handleFileSelect(e) {
    const files = Array.from(e.target.files);
    
    for (const file of files) {
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            attachedFiles.push(data);
            displayAttachment(data);
        } catch (error) {
            console.error('Upload failed:', error);
            addSystemMessage(`Failed to upload ${file.name}`);
        }
    }
    
    fileInput.value = '';
}

function displayAttachment(file) {
    const item = document.createElement('div');
    item.className = 'attachment-item';
    item.innerHTML = `
        <span>📎 ${file.filename}</span>
        <button onclick="removeAttachment('${file.filename}')">✕</button>
    `;
    attachmentPreview.appendChild(item);
}

function removeAttachment(filename) {
    attachedFiles = attachedFiles.filter(f => f.filename !== filename);
    const items = attachmentPreview.querySelectorAll('.attachment-item');
    items.forEach(item => {
        if (item.textContent.includes(filename)) {
            item.remove();
        }
    });
}

async function sendMessage() {
    const apiKey = getApiKey();
    if (!apiKey) {
        openSettings();
        setTimeout(() => {
            showSettingsMessage('Please enter your API key first.', 'error');
        }, 300);
        return;
    }
    
    const message = messageInput.value.trim();
    if (!message) return;
    
    // Disable input
    sendBtn.disabled = true;
    messageInput.disabled = true;
    
    // Add user message to chat
    addMessage('user', message);
    messageInput.value = '';
    autoResizeTextarea();
    
    // Clear attachments display
    attachmentPreview.innerHTML = '';
    
    // Show typing indicator
    const typingId = showTypingIndicator();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-Key': apiKey
            },
            body: JSON.stringify({
                message: message,
                skill_id: skillSelect.value || null,
                session_id: sessionId,
                temperature: parseFloat(temperature.value),
                max_tokens: parseInt(maxTokens.value),
                attachments: attachedFiles
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Request failed');
        }
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        // Add assistant response
        addMessage('assistant', data.response);
        
        // Update stats
        totalTokens += data.usage.input_tokens + data.usage.output_tokens;
        messageCount += 2; // user + assistant
        updateStats();
        
        // Clear attached files
        attachedFiles = [];
        
    } catch (error) {
        removeTypingIndicator(typingId);
        console.error('Chat error:', error);
        addSystemMessage('Failed to send message: ' + error.message);
    } finally {
        sendBtn.disabled = false;
        messageInput.disabled = false;
        messageInput.focus();
    }
}

function addMessage(role, content) {
    // Remove welcome message if it exists
    const welcome = chatMessages.querySelector('.welcome-message');
    if (welcome) welcome.remove();
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const roleDiv = document.createElement('div');
    roleDiv.className = 'message-role';
    roleDiv.textContent = role === 'user' ? 'You' : 'Assistant';
    
    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    textDiv.textContent = content;
    
    contentDiv.appendChild(roleDiv);
    contentDiv.appendChild(textDiv);
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function addSystemMessage(content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message system';
    messageDiv.style.textAlign = 'center';
    messageDiv.style.color = 'var(--text-secondary)';
    messageDiv.style.fontSize = '0.9rem';
    messageDiv.style.padding = '1rem';
    messageDiv.textContent = content;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTypingIndicator() {
    const id = 'typing_' + Date.now();
    const messageDiv = document.createElement('div');
    messageDiv.id = id;
    messageDiv.className = 'message assistant';
    messageDiv.innerHTML = `
        <div class="message-content">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return id;
}

function removeTypingIndicator(id) {
    const element = document.getElementById(id);
    if (element) element.remove();
}

function updateStats() {
    messageCountEl.textContent = messageCount;
    tokenCountEl.textContent = totalTokens.toLocaleString();
}

async function exportChat() {
    try {
        const response = await fetch(`/api/export/${sessionId}`);
        const data = await response.json();
        
        // Create download link
        const blob = new Blob([data.markdown], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = data.filename;
        a.click();
        URL.revokeObjectURL(url);
        
        addSystemMessage('Chat exported successfully!');
    } catch (error) {
        console.error('Export failed:', error);
        addSystemMessage('Failed to export chat.');
    }
}

function clearChat() {
    if (confirm('Clear all messages? This cannot be undone.')) {
        chatMessages.innerHTML = `
            <div class="welcome-message">
                <h2>👋 Welcome to Claude Skills</h2>
                <p>Select a skill from the sidebar and start chatting!</p>
            </div>
        `;
        sessionId = generateSessionId();
        totalTokens = 0;
        messageCount = 0;
        updateStats();
        addSystemMessage('Chat cleared. New session started.');
    }
}

// Make functions globally accessible for onclick handlers
window.openSettings = openSettings;
window.closeSettings = closeSettings;
window.saveSettings = saveSettings;
window.removeAttachment = removeAttachment;
