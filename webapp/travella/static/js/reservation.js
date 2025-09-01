document.addEventListener('DOMContentLoaded', () => {
    const reservationForm = document.getElementById('reservationForm')
    const rejectForm = document.getElementById('rejectForm')
    const confirmBtn = document.getElementById('confirmBtn')
    const rejectBtn = document.getElementById('rejectBtn')
    if(reservationForm && confirmBtn && rejectBtn && rejectForm) {
        confirmBtn.addEventListener('click', () => {
            reservationForm.submit()
        })
        
        rejectBtn.addEventListener('click', () => {
            const value = document.getElementById('rejectMessage').value
            const rejectMessageError = document.getElementById('rejectMessageError')
            console.log(rejectMessageError);
            if (value) {
                rejectForm.submit()
            } else {
                if(rejectMessageError.classList.contains('d-none')) {
                    rejectMessageError.classList.remove('d-none')
                }
            }
        })
    }
})