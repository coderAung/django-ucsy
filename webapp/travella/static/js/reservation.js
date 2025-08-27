document.addEventListener('DOMContentLoaded', () => {
    const reservationForm = document.getElementById('reservationForm')
    const confirmBtn = document.getElementById('confirmBtn')
    if(reservationForm && confirmBtn) {
        confirmBtn.addEventListener('click', () => {
            reservationForm.submit()
        })
    }
})