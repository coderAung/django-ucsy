document.addEventListener('DOMContentLoaded', () => {
    const uploadBtn = document.getElementById('uploadBtn')
    const profileImageInput = document.getElementById('profileImageInput')
    const profileImageForm = document.getElementById('profileImageForm')
    const profileImage = document.getElementById('profileImage')

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value
    
    const upload = async form => {
        const response = await fetch(profileImageForm.action, {
                            method: 'POST',
                            body: form,
                            headers: {
                                'X-CSRFToken': csrfToken
                            },
                        })
        const data = await response.json()
        if(data.success) {
            profileImage.src = data.url
        } else {
            console.log(data.message);
        }
    }
    
    if(uploadBtn && profileImageInput && profileImageForm) {
        uploadBtn.onclick = () => profileImageInput.click()
        profileImageInput.onchange = () => {
            const formData = new FormData()
            formData.append('profileImage', profileImageInput.files[0])
            uploadBtn.classList.add('d-none')
            upload(formData)    
            uploadBtn.classList.remove('d-none')
        }
    }

})