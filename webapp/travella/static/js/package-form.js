let images = []

document.addEventListener('DOMContentLoaded', () => {
    const continueBtn = document.getElementById('continueBtn')
    const setSelected = (cid) => {
        continueBtn.dataset['cid'] = cid
    }
    const clearActive = () => {
        cid = continueBtn.dataset['cid']
        if(cid !== '0') {
            const item = document.getElementById(`cid${cid}`)
            item.classList.remove('active')
        }
    }

    const categoryContainer = document.getElementById('categoryContainer')
    const codeInput = document.getElementById('codeInput')

    if(continueBtn && categoryContainer && codeInput) {
        categoryContainer.addEventListener('click', e => {
            const t = e.target
            if(!t.classList.contains('categoryItem')) {
                return
            }
            if(! t.classList.contains('active')) {
                clearActive()
                t.classList.add('active')
                setSelected(t.dataset['cid'])
            }
        })

        continueBtn.addEventListener('click', async () => {
            const cid = continueBtn.dataset['cid']
            if(cid == '0') return
            const newCode = await fetchNewCode(cid)
            codeInput.value = newCode
            const modalEl = document.getElementById('categoryModal');
            const modal = bootstrap.Modal.getInstance(modalEl)
            modal.hide()
        })
    }

    const uploadPictureBtnContainer = document.getElementById('uploadPictureBtnContainer')
    const uploadPictureBtn = document.getElementById('uploadPictureBtn')
    const imageInput = document.getElementById('imageInput')
    let pictureContainer = document.getElementById('pictureContainer')
    const gallery = document.getElementById('gallery')
    if(uploadPictureBtn && imageInput && gallery) {
        imageInput.addEventListener('change', () => {
            const data = imageInput.files
            if(!pictureContainer) {
                pictureContainer = generatePictureContainer()
                gallery.innerHTML = ''
                gallery.appendChild(pictureContainer)
            }
            pictureContainer.innerHTML = ''
            images = images.concat(Array.from(data))
            images.forEach((i, index) => {
                const col = generatePictureCol(URL.createObjectURL(i), index, e => {
                    pictureContainer.removeChild(col)
                    images = images.filter(d => d !== i)
                    if(images.length === 0)  imageInput.value = ''
                })
                pictureContainer.appendChild(col)
            })
            if(!document.getElementById('uploadPictureBtn')) {
                card = generateUploadPictureCard(() => imageInput.click())
                card.id = 'uploadPictureBtn'
                pictureContainer.appendChild(card)
            }
        })
        uploadPictureBtn.addEventListener('click', () => imageInput.click())
    }

    const packageForm = document.getElementById('packageForm')
    if(packageForm) {
        packageForm.addEventListener('submit', e => {
            e.preventDefault()
            const formData = new FormData(packageForm)
            images.forEach(i => formData.append('images[]', i))
            fetch(packageForm.action, {
                method: 'POST',
                body: formData,
            }).then(res => res.json())
        })
    }
})

async function fetchNewCode(cid) {
    const resp = await fetch(`http://127.0.0.1:8000/admins/packages/new-code?cid=${cid}`)
    const data = await resp.json()
    return data.newCode
}

function generatePictureContainer() {
    const div = document.createElement('div')
    div.classList.add('row')
    div.classList.add('row-cols-2')
    div.classList.add('row-gap-3')
    return div
}

function generatePictureCol(imgSrc, index = 0, removeFunc) {
    const div = document.createElement('div')
    div.id = `i${index}`
    div.classList.add(...'col pictureCol d-flex justify-content-center align-items-center'.split(' '))
    const div2 = document.createElement('div')
    div2.classList.add('d-flex')
    div2.classList.add('justify-content-center')
    div2.classList.add('align-items-center')
    div.classList.add('position-relative')
    div2.classList.add('imgPreview')
    div.style.minHeight = '100px'
    div.appendChild(div2)
    const img = document.createElement('img')
    img.classList.add('img-fluid')
    img.classList.add('rounded')
    img.src = imgSrc
    div2.appendChild(img)

    // removeBtn = document.createElement('div')
    // removeBtn.classList.add(...'position-absolute shadow d-flex align-items-center justify-content-center rounded-circle top-0 end-0 glass-remove'.split(' '))
    // removeBtn.style.width = '25px'
    // removeBtn.style.height = '25px'
    // removeBtn.innerHTML = '<i class="bi bi-dash df-text-red fs-3"/>'
    // div2.appendChild(removeBtn)

    // hover removal feat
    const removal = document.createElement('div')
    removal.classList.add(...'removal rounded'.split(' '))
    const icon = document.createElement('i')
    icon.classList.add(...'bi bi-dash-circle fs-4 me-2'.split(' '))
    removal.appendChild(icon)
    removal.appendChild(document.createTextNode('Removal'))
    removal.dataset['index'] = `i${index}`
    div.appendChild(removal)

    removal.addEventListener('click', e => removeFunc(e))
    return div
}

function generateUploadPictureCard(onClick) {
    const col = document.createElement('div')
    col.classList.add(...'col d-flex align-items-center'.split(' '))
    const div = document.createElement('div')
    div.classList.add(...'uploadPictureCard w-100 rounded d-flex justify-content-center align-items-center pointer'.split(' '))
    div.id = 'uploadPictureBtn'
    div.style.minHeight = '100px'
    div.style.border = '2px dashed #0d6efd'
    col.appendChild(div)
    div.addEventListener('click', onClick)
    div.innerText = 'Upload Photo'
    return col
}