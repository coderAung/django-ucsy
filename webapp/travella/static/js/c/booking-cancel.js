document.addEventListener('DOMContentLoaded', () => {
    // const bookingCancelForm = document.getElementById('bookingCancelForm')
    // const bookingCancelBtn = document.getElementById('bookingCancelBtn')
    // if(bookingCancelForm && bookingCancelBtn) {
    //     bookingCancelBtn.onclick = () => bookingCancelForm.submit()
    // }
    const paymentTypeInput = document.getElementById('paymentTypeInput')
    const paymentSuggestions = document.getElementsByClassName('paymentSuggestion')
    if(paymentSuggestions && paymentTypeInput) {
        Array.from(paymentSuggestions).forEach(i => {
            i.addEventListener('click', () => {
                const value = i.dataset['value']
                paymentTypeInput.value = value
            })
        })
    }
})