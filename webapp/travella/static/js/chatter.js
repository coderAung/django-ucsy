document.addEventListener('DOMContentLoaded', () => {
    const chatters = document.getElementsByClassName('chat');
    const chatLog = document.getElementById('chatLog')
    if (chatters.length) {
        Array.from(chatters).forEach(chat => {

            if(chatLog && chat.dataset.customerId == chatLog.dataset.customerId) {
                chat.classList.add('active')
            }
            chat.addEventListener('click', () => {
                const customerId = chat.dataset.customerId;
                const chatLog = document.getElementById('chatLog');

                // Only redirect if chatLog is undefined or different
                if (chatLog && chatLog.dataset.customerId === customerId) return;

                window.location.href = `/admins/chats/${customerId}/`; // or whatever URL you need
            });
        });
    }
});
