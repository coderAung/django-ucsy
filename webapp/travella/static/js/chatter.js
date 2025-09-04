document.addEventListener('DOMContentLoaded', () => {
    const chatters = document.getElementsByClassName('chat');
    console.log(chatters);

    if (chatters.length) {
        Array.from(chatters).forEach(chat => {
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
