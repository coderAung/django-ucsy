document.addEventListener('DOMContentLoaded', () => {
    const uploadSlipBtn = document.getElementById('uploadSlipBtn')
    const slipImageWrapper = document.getElementById('slipImageWrapper')
    const slipImage = document.getElementById('slipImage')
    const paymentRequestForm = document.getElementById('paymentRequestForm')
    const paymentSlipInput = document.getElementById('paymentSlipInput')
    const cancelSlipBtn = document.getElementById('cancelSlipBtn')
    const paymentSelect = document.getElementById('paymentSelect')
    const paymentKeyInput = document.getElementById('paymentKeyInput')
    const requestPaymentBtn = document.getElementById('requestPaymentBtn')
    const paymentInput = document.getElementById('paymentInput')
    const updatePaymentInput = () => {
        paymentInput.value = paymentSelect.options[paymentSelect.selectedIndex].text
    }

    if(uploadSlipBtn &&
        slipImageWrapper &&
        slipImage &&
        paymentRequestForm &&
        paymentSlipInput &&
        cancelSlipBtn &&
        paymentSelect &&
        paymentInput &&
        requestPaymentBtn &&
        paymentKeyInput
    ) {

        paymentSelect.selectedIndex = 0
        updatePaymentInput()

        uploadSlipBtn.addEventListener('click', () => paymentSlipInput.click())
        paymentSlipInput.addEventListener('change', () => {
            const file = paymentSlipInput.files[0]
            const url = URL.createObjectURL(file)
            if(!uploadSlipBtn.classList.contains('d-none')) {
                uploadSlipBtn.classList.add('d-none')
            }
            if(slipImageWrapper.classList.contains('d-none')) {
                slipImage.src = url
                slipImageWrapper.classList.remove('d-none')
            }
            const paymentSlipError = document.getElementById('paymentSlipError')
            if(! paymentSlipError.classList.contains('d-none')) {
                paymentSlipError.classList.add('d-none')
            }

        })

        cancelSlipBtn.addEventListener('click', () => {
            paymentSlipInput.value = ''
            if(!slipImageWrapper.classList.contains('d-none')) {
                slipImage.src = ''
                slipImageWrapper.classList.add('d-none')
            }
            if(uploadSlipBtn.classList.contains('d-none')) {
                uploadSlipBtn.classList.remove('d-none')
            }
        })

        paymentSelect.addEventListener('change', () => {
            paymentKeyInput.value = paymentSelect.value
            updatePaymentInput()
        })

        const validateForm = () => {
            const paymentSlipError = document.getElementById('paymentSlipError')
            if(! paymentSlipInput.files[0]) {
                if(paymentSlipError.classList.contains('d-none')) {
                    paymentSlipError.classList.remove('d-none')
                }
                return false
            } else {
                if(! paymentSlipError.classList.contains('d-none')) {
                    paymentSlipError.classList.add('d-none')
                }
            }
            return true
        }

        requestPaymentBtn.addEventListener('click', () => {
            const result = validateForm()
            const bookingIdInput = document.getElementById('bookingIdInput')
            console.log(`
                id      : ${bookingIdInput.value}
                payment : ${paymentInput.value}
                slip    : ${paymentSlipInput.files[0]}`);
            if (result) {
                paymentRequestForm.submit()
            }
        })
    }
})