document.addEventListener('DOMContentLoaded', () => {
    const saveAndAddBtn = document.getElementById('saveAndAddBtn')
    const imgInput = document.getElementById('imgInput')
    const dayInput = document.getElementById('dayInput')
    const titleInput = document.getElementById('titleInput')
    const descriptionInput = document.getElementById('descriptionInput')
    const itineraryForm = document.getElementById('itineraryForm')

    const validateInput = (input, prefix) => {
        if(!input.value) {
            const errorMessage = document.getElementById(`${prefix}Error`)
            if(errorMessage.classList.contains('d-none')) {
                errorMessage.classList.remove('d-none')
            }
            return false
        }
        return true
    }
    const validateForm = () => {
        return validateInput(dayInput, 'day') &&
        validateInput(titleInput, 'title') &&
        validateInput(descriptionInput, 'description') &&
        validateInput(imgInput, 'img')
    }

    const imgWrapper = document.getElementById('imgWrapper')
    const imgDisplay = document.getElementById('imgDisplay')
    const uploadBtn = document.getElementById('uploadBtn')
    if(saveAndAddBtn && imgInput && dayInput && titleInput && descriptionInput &&
        uploadBtn && imgDisplay &&
        itineraryForm) {

        uploadBtn.addEventListener('click', () => {
            imgInput.click()
        })
        const imgChangeBtn = document.getElementById('imgChangeBtn')
        imgChangeBtn.addEventListener('click', () => {
            imgInput.click()
        })
        const imgRemoveBtn = document.getElementById('imgRemoveBtn')
        imgRemoveBtn.addEventListener('click', () => {
            imgDisplay.src = ''
            imgInput.value = ''
            imgWrapper.classList.add('d-none')
            uploadBtn.classList.remove('d-none')
        })

        imgInput.addEventListener('change', () => {
            imgDisplay.src = URL.createObjectURL(imgInput.files[0])

            if (imgWrapper.classList.contains('d-none')) {
                imgWrapper.classList.remove('d-none')
                uploadBtn.classList.add('d-none')
            }
        })

        saveAndAddBtn.addEventListener('click', () => {
            if(validateForm()) {
                itineraryForm.submit()
            }
        })
    }

    const deleteBtns = document.getElementsByClassName('deleteBtn')
    const idToDeleteInput = document.getElementById('idToDeleteInput')
    const deleteForm = document.getElementById('deleteForm')
    if(deleteBtns && idToDeleteInput && deleteForm) {
        Array.from(deleteBtns).forEach(btn => {
            btn.addEventListener('click', () => {
                idToDeleteInput.value = btn.dataset['dayId']
                deleteForm.submit()
            })
        })
    }
})