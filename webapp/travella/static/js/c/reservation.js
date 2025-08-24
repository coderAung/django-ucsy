document.addEventListener('DOMContentLoaded', () => {
    const uploadSlipBtn = document.getElementById('uploadSlipBtn')
    const slipImageWrapper = document.getElementById('slipImageWrapper')
    const slipImage = document.getElementById('slipImage')
    const paymentRequestForm = document.getElementById('paymentRequestForm')
    const paymentSlipInput = document.getElementById('paymentSlipInput')
    const cancelSlipBtn = document.getElementById('cancelSlipBtn')

    if(uploadSlipBtn &&
        slipImageWrapper &&
        slipImage &&
        paymentRequestForm &&
        paymentSlipInput &&
        cancelSlipBtn
    ) {
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
    }
})