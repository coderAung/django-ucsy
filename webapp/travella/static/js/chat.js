document.addEventListener('DOMContentLoaded', () => {
    const chatLog = document.getElementById('chatLog');
    const chatInput = document.getElementById('chatInput');
    const chatSendBtn = document.getElementById('chatSendBtn');
    const customerId = chatLog.dataset['customerId'];
    const userType = chatLog.dataset['userType'];
    const chatWrapper = document.getElementById('chatWrapper')

    const chatSocket = new WebSocket(
        'ws://' + window.location.host + '/ws/chat/' + customerId + '/'
    );

    const scrollToBottom = () => {
        chatWrapper.scrollTop = chatWrapper.scrollHeight;
    };

    chatSocket.onmessage = e => {
        const data = JSON.parse(e.data);
        const isSent = data.sender_type === userType;
        
        const msgDiv = createMsg(data.message, data.created_at, isSent);
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

function createMsg(message, created_at, isSent) {


    const mainDiv = document.createElement('div')
    const msgDiv = document.createElement('div');
    mainDiv.classList.add(
        'message',
        isSent ? 'sent' : 'received',
        'p-2', 'rounded', 'shadow-sm', 'mb-3', 'bg-white'
    );
    msgDiv.textContent = message;
    const span = document.createElement('div')
    span.classList.add('df-fs-sm', 'text-muted', 'mt-2')
    // span.textContent = formatDate(created_at)

    const date = new Date(created_at);
    span.textContent = new Intl.DateTimeFormat('en-US', {
        month: 'short',   // Sep
        day: 'numeric',   // 5
        year: 'numeric',  // 2025
        hour: 'numeric',  // 8
        minute: '2-digit', // 22
        hour12: true      // a.m./p.m.
    }).format(date);
    mainDiv.appendChild(msgDiv)
    mainDiv.appendChild(span)
    return mainDiv;
}

function formatDate(isoString) {
    const d = new Date(isoString);
    if (isNaN(d.getTime())) return isoString; // fallback if invalid
    return d.toLocaleString([], { dateStyle: 'short', timeStyle: 'short' });
}
