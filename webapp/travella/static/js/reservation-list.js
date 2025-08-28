document.addEventListener('DOMContentLoaded', () => {
    const requestingTab = document.getElementById('requestingTab')
    const requesting = document.getElementById('requesting')
    const reservedTab = document.getElementById('reservedTab')
    const reserved = document.getElementById('reserved')
    const searchBtn = document.getElementById('searchBtn')
    if(requestingTab && reservedTab && searchBtn && requesting && reserved) {
        const search = paymentStatusInput => {
            if(paymentStatusInput.checked) return
            paymentStatusInput.checked = true
            searchBtn.click()
        }
        requestingTab.addEventListener('click', () => search(requesting))
        reservedTab.addEventListener('click', () => search(reserved))
    }

    const paginationBtns = document.getElementsByClassName('paginationBtn')
    const pageInput = document.getElementById('pageInput')
    if(paginationBtns && pageInput) {
        Array.from(paginationBtns).forEach(btn => {
            btn.addEventListener('click', () => {
                if(!btn.classList.contains('active')) {
                    const page = btn.dataset['page']
                    pageInput.value = page
                    searchBtn.click()
                }
            })
        })
    }
})