document.addEventListener('DOMContentLoaded', () => {
  const refundForm = document.getElementById('refundForm')
  const bookingCodeInput = document.getElementById('bookingCodeInput')

  const refundConfirmBtns = document.getElementsByClassName('refundConfirmBtn')
  if(refundConfirmBtns) {
    Array.from(refundConfirmBtns).forEach(btn => {
      btn.addEventListener('click', () => {
        const bookingCode = btn.dataset['code']
        bookingCodeInput.value = bookingCode
        // console.log(bookingCodeInput.value);
        // console.log(refundForm);
        
        refundForm.submit()
      })
    })
  }
})