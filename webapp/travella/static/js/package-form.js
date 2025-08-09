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
                console.log('created');
                pictureContainer = generatePictureContainer()
                gallery.appendChild(pictureContainer)
            }
            pictureContainer.innerHTML = ''
            Array.from(data).forEach(i => {
                const col = generatePictureCol(URL.createObjectURL(i))
                pictureContainer.appendChild(col)
            })
        })
        uploadPictureBtn.addEventListener('click', () => imageInput.click())
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
function generatePictureCol(imgSrc) {
    const div = document.createElement('div')
    div.classList.add('col')
    const div2 = document.createElement('div')
    div2.classList.add('d-flex')
    div2.classList.add('justify-content-center')
    div2.classList.add('align-items-center')
    div.appendChild(div2)
    const img = document.createElement('img')
    img.classList.add('img-fluid')
    img.classList.add('rounded')
    img.src = imgSrc
    div2.appendChild(img)
    return div
}
