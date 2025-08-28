document.addEventListener('DOMContentLoaded', () => {
    const paginationBtns = document.getElementsByClassName('paginationBtn')
    const searchBtn = document.getElementById('searchBtn')
    const pageInput = document.getElementById('pageInput')
    if(paginationBtns && searchBtn && pageInput) {
        Array.from(paginationBtns).forEach(btn => {
            btn.addEventListener('click', () => {
                if(btn.classList.contains('active')) return
                const page = btn.dataset['page']
                pageInput.value = page
                searchBtn.click()
            })
        })
    }
})