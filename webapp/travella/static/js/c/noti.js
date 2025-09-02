document.addEventListener('DOMContentLoaded', () => {
    const notiDeleteForm = document.getElementById('notiDeleteForm')
    const notiIdInput = document.getElementById('notiIdInput')
    const notiDeleteBtns = document.getElementsByClassName('notiDeleteBtn')

    if(notiDeleteForm && notiIdInput && notiDeleteBtns) {
        Array.from(notiDeleteBtns).forEach(btn => {
            btn.addEventListener('click', () => {
                notiIdInput.value = btn.dataset['id']
                console.log(btn.dataset['id']);
                notiDeleteForm.submit()
            })
        })
    }
})