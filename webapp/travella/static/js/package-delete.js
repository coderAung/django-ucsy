document.addEventListener('DOMContentLoaded', () => {
    const deletePackageForm = document.getElementById('deletePackageForm')
    const codeInput = document.getElementById('codeInput')
    const deleteConfirmBtn = document.getElementById('deleteConfirmBtn')
    if(deletePackageForm && codeInput && deleteConfirmBtn) {
        Array.from(document.getElementsByClassName('deleteBtn'))
        .forEach(btn => {
            btn.addEventListener('click', () => {
                const code = btn.dataset['code']
                document.getElementById('packageCode').innerText = code
                const modal = new bootstrap.Modal('#deletePackage')
                modal.show()
                deleteConfirmBtn.dataset['code'] = code
            })
        })
        deleteConfirmBtn.addEventListener('click', () => {
            codeInput.value = deleteConfirmBtn.dataset['code']
            deletePackageForm.submit()
        })
    }
})