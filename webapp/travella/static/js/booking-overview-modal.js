document.addEventListener('DOMContentLoaded', () => {
    btnList = document.getElementsByClassName('bookingOverviewBtn')
    modal = new bootstrap.Modal('#bookingOverview')
    bookingCode = document.getElementById('bookingCode')
    email = document.getElementById('email')
    tickets = document.getElementById('tickets')
    bookingStatus = document.getElementById('bookingStatus')
    bookedDate = document.getElementById('bookedDate')
    bookedTime = document.getElementById('bookedTime')
    // actionedDate = document.getElementById('actionedDate')
    // actionedTime = document.getElementById('actionedTime')
    if (btnList && modal) {
        Array.from(btnList).forEach(btn => {
            btn.addEventListener('click', async () => {
                if (
                    bookingCode &&
                    email &&
                    tickets &&
                    bookingStatus &&
                    bookedDate &&
                    bookedTime
                ) {
                    data = await fetchOverview(id=btn.dataset['bid'])
                    email.innerText = data.email
                    tickets.innerText = data.tickets
                    bookingStatus.innerText = data.status
                    if(data.status === 'Pending') {
                        bookingStatus.classList.remove('badge-red')
                        bookingStatus.classList.remove('badge-green')
                        bookingStatus.classList.add('badge-blue')
                    }
                    if(data.status === 'Reserved') {
                        bookingStatus.classList.remove('badge-red')
                        bookingStatus.classList.remove('badge-blue')
                        bookingStatus.classList.add('badge-green')
                    }
                    if(data.status === 'Cancelled') {
                        bookingStatus.classList.remove('badge-blue')
                        bookingStatus.classList.remove('badge-green')
                        bookingStatus.classList.add('badge-red')
                    }
                    bookedDate.innerText = data.bookedDate
                    bookedTime.innerText = data.bookedTime
                    modal.show()
                }
            })
        })
    }
})

async function fetchOverview(id = '2bb6db72-0b6b-4bc2-b736-5642a09eac92') {    
    const resp = await fetch(`http://127.0.0.1:8000/test/overview/${id}`)
    return await resp.json()
}