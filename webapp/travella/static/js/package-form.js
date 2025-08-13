let images = []
let categories = [] // {'id': 1, 'name': 'Adventure'}
function initCategories() {
    const categoryItems = document.getElementsByClassName('categoryItem')
    Array.from(categoryItems).forEach(item => {
        const obj = {
            'id': item.dataset['cid'],
            'name': item.innerText
        }
        categories.push(obj)
    })
}
document.addEventListener('DOMContentLoaded', () => {
    const continueBtn = document.getElementById('continueBtn')
    const setSelected = (cid) => {
        continueBtn.dataset['cid'] = cid
    }
    const clearActive = () => {
        cid = continueBtn.dataset['cid']
        if(cid !== '0') {
            const item = document.getElementById(`cid${cid}`)
            if(!item) return
            item.classList.remove('active')
        }
    }
    initCategories()
    const categoryContainer = document.getElementById('categoryContainer')
    const codeInput = document.getElementById('codeInput')
    const categorySearch = document.getElementById('categorySearch')
    const cidInput = document.getElementById('cidInput')
    if(continueBtn && categoryContainer && codeInput && categorySearch && cidInput) {
        categorySearch.addEventListener('keyup', () => {
            const key = categorySearch.value
            categoryContainer.innerHTML = ''
            if(!key) {
                categories.forEach(c => {
                    const col = generateCategoryCol(c, () => c.id == continueBtn.dataset['cid'])
                    categoryContainer.appendChild(col)
                })
                return
            }
            categories.filter(c => c.name.toLowerCase().startsWith(key.toLowerCase()))
                .forEach(c => {
                    const col = generateCategoryCol(c, () => c.id == continueBtn.dataset['cid'])
                    categoryContainer.appendChild(col)
                })
        })

        categoryContainer.addEventListener('click', e => {
            const t = e.target
            if(!t.classList.contains('categoryItem')) {
                clearActive()
                setSelected('0')
                continueBtn.disabled = true
                return
            }
            if(! t.classList.contains('active')) {
                clearActive()
                t.classList.add('active')
                setSelected(t.dataset['cid'])
                continueBtn.disabled = false
            } else {
                clearActive()
                setSelected('0')
                continueBtn.disabled = true
            }
        })

        continueBtn.addEventListener('click', async () => {
            const cid = continueBtn.dataset['cid']
            if(cid == '0') return
            const [newCode, cname] = await fetchNewCode(cid)
            codeInput.value = newCode
            const modalEl = document.getElementById('categoryModal');
            const modal = bootstrap.Modal.getInstance(modalEl)
            modal.hide()
            document.getElementById('categoryBtn').innerText = cname
            cidInput.value = cid
        })
    }


    // image upload feature
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
                    const btn = document.getElementById('uploadPictureBtn')
                    if(images.length % 2 === 0 && btn && !btn.classList.contains('w-100')) btn.classList.add('w-100')
                    else btn.classList.remove('w-100')
                })
                pictureContainer.appendChild(col)
            })
            imageInput.value = ''
            if(!document.getElementById('uploadPictureBtn')) {
                card = generateUploadPictureCard(() => imageInput.click())
                card.id = 'uploadPictureBtn'
                pictureContainer.appendChild(card)
            }
            const btn = document.getElementById('uploadPictureBtn')
            if(images.length % 2 === 0 && btn && !btn.classList.contains('w-100')) btn.classList.add('w-100')
            else btn.classList.remove('w-100')
        })
        uploadPictureBtn.addEventListener('click', () => imageInput.click())
    }

    const packageForm = document.getElementById('packageForm')
    const publishBtn = document.getElementById('publishBtn')
    if(packageForm && publishBtn) {
        publishBtn.addEventListener('click', e => {
            e.preventDefault()
            const dt = new DataTransfer()
            images.forEach(i => dt.items.add(i))
            imageInput.value = ''
            imageInput.files = dt.files
            packageForm.submit()
        })
        // packageForm.addEventListener('submit', e => {
        //     e.preventDefault()
        //     const formData = new FormData(packageForm)
        //     images.forEach(i => formData.append('images[]', i))
        //     fetch(packageForm.action, {
        //         method: 'POST',
        //         body: formData,
        //     }).then(res => res.json())
        // })

    }
})

async function fetchNewCode(cid) {
    const resp = await fetch(`http://127.0.0.1:8000/admins/packages/new-code?cid=${cid}`)
    const data = await resp.json()
    return [data.newCode, data.cname]
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

    removeBtn = document.createElement('div')
    removeBtn.classList.add(...'position-absolute shadow d-flex align-items-center justify-content-center rounded-circle top-0 end-0 glass-remove'.split(' '))
    removeBtn.style.width = '25px'
    removeBtn.style.height = '25px'
    removeBtn.innerHTML = '<i class="bi bi-x fs-5"/>'
    removeBtn.addEventListener('click', e => removeFunc(e))
    div2.appendChild(removeBtn)

    // hover removal feat
    // const removal = document.createElement('div')
    // removal.classList.add(...'removal rounded'.split(' '))
    // const icon = document.createElement('i')
    // icon.classList.add(...'bi bi-dash-circle fs-4 me-2'.split(' '))
    // removal.appendChild(icon)
    // removal.appendChild(document.createTextNode('Remove'))
    // removal.dataset['index'] = `i${index}`
    // div.appendChild(removal)

    // removal.addEventListener('click', e => removeFunc(e))
    return div
}

function generateUploadPictureCard(onClick) {
    const col = document.createElement('div')
    col.classList.add(...'col d-flex align-items-center'.split(' '))
    const div = document.createElement('div')
    div.classList.add(...'uploadPictureCard w-100 rounded d-flex flex-column justify-content-center align-items-center pointer'.split(' '))
    div.id = 'uploadPictureBtn'
    div.style.minHeight = '100px'
    div.style.border = '2px dashed #0d6efd'
    col.appendChild(div)
    div.addEventListener('click', onClick)
    div.innerHTML = '<i class="bi bi-upload fs-4"></i> Upload Photo'
    return col
}

function generateCategoryCol(c, isActive = () => false) {
    const col = document.createElement('div')
    col.classList.add('col')
    const div = document.createElement('div')
    div.classList.add(...'rounded-5 categoryItem text-center glass-item border px-2 py-2'.split(' '))
    if (isActive()) div.classList.add('active')
    div.innerText = 
    div.id = `cid${c.id}`
    div.dataset['cid'] = c.id
    div.innerText = c.name
    col.appendChild(div)
    return col
}
