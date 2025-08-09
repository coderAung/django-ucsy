document.addEventListener('DOMContentLoaded', async () => {
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
})

async function fetchNewCode(cid) {
    const resp = await fetch(`http://127.0.0.1:8000/admins/packages/new-code?cid=${cid}`)
    const data = await resp.json()
    return data.newCode
}