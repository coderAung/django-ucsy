document.addEventListener('DOMContentLoaded', () => {
    const chatLog = document.getElementById('chatLog');
    const chatInput = document.getElementById('chatInput');
    const chatSendBtn = document.getElementById('chatSendBtn');
    const customerId = chatLog.dataset['customerId'];
    const userType = chatLog.dataset['userType'];

    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/' + customerId + '/'
    );

    const scrollToBottom = () => {
        chatLog.scrollTop = chatLog.scrollHeight;
    };

    chatSocket.onmessage = e => {
        const data = JSON.parse(e.data);
        const isSent = data.sender_type === userType;
        const msgDiv = createMsg(data.message, isSent);
        chatLog.appendChild(msgDiv);
        scrollToBottom();
    };

    const sendMessage = () => {
        const message = chatInput.value.trim();
        if (!message) return;
        chatSocket.send(JSON.stringify({
            "message": message,
            "sender_type": userType
        }));
        chatInput.value = "";
        chatInput.focus();
    };

    chatSendBtn.onclick = sendMessage;

    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Scroll to bottom on page load
    scrollToBottom();
});

function createMsg(message, isSent) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add(
        'message',
        isSent ? 'sent' : 'received',
        'p-2', 'rounded', 'shadow-sm', 'mb-3', 'bg-white'
    );
    msgDiv.textContent = message;
    return msgDiv;
}
