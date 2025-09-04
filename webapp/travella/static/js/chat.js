// document.addEventListener('DOMContentLoaded', () => {
//     const chatLog = document.getElementById('chatLog')

//     const customerId = chatLog.dataset['customerId']
//     const userType = chatLog.dataset['userType']
    
//     const chatSocket = new WebSocket(
//         'ws://' + window.location.host + '/ws/chat/' + customerId + '/'
//     )

//     chatSocket.onmessage = e => {
//         const data = JSON.parse(e.data)
//         const isSent = data.sender_type === userType
//         const msgDiv = createMsg(data.message, isSent)
//         chatLog.appendChild(msgDiv)
//         chatLog.scrollTop = chatLog.scrollHeight
//     }

//     document.getElementById('chatSendBtn').onclick = function () {
//         const input = document.getElementById("chatInput")
//         const message = input.value.trim()
//         if (message.length === 0) return
//         chatSocket.send(JSON.stringify({
//             "message": message,
//             "sender_type": userType
//         }));
//         input.value = "";
//     }
// })

// function createMsg(message, isSent) {
//     const msgDiv = document.createElement("div")
//     msgDiv.classList.add("message", isSent ? "sent" : "received", "shadow", "rounded", "p-2", "bg-white")
//     msgDiv.innerHTML = `${message}`
//     return msgDiv
// }