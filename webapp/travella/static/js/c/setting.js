const settingJson = [
    {
        id: 'accountSetting',
        p: 'account',
    },
    {
        id: 'passwordSetting',
        p: 'password',
    },
    {
        id: 'accessLogSetting',
        p: 'access-log',
    },
    {
        id: 'deleteAccountSetting',
        p: 'd',
    },
]

const get_p = id => {
    return settingJson.filter(i => i.id == id)[0].p
}

document.addEventListener('DOMContentLoaded', () => {
    let currentSettingId = 'accountSetting'
    const loadCurrentSettingId = () => {
        const params = new URLSearchParams(window.location.search)
        const page = params.get('p')
        if (page) {
            const found = settingJson.find(i => i.p === page)
            if (found) {
                currentSettingId = found.id
            }
        }
    }

    const updateCurrentSetting = settingId => {        
        const settingBtn = document.getElementById(`${settingId}Btn`)
        const currentSettingBtn = document.getElementById(`${currentSettingId}Btn`)
        currentSettingBtn.classList.remove('active')
        settingBtn.classList.add('active')

        const currentSetting = document.getElementById(currentSettingId)
        if(currentSetting) {            
            currentSetting.classList.add('d-none')
        }
        const setting = document.getElementById(settingId)
        setting.classList.remove('d-none')
        currentSettingId = settingId
        const p = get_p(currentSettingId)
        history.pushState({}, '', `?p=${p}`)
    }

    loadCurrentSettingId()
    console.log(currentSettingId);
    
    updateCurrentSetting(currentSettingId)

    const settingBtns = document.getElementsByClassName('settingBtn')
    if(settingBtns) {
        Array.from(settingBtns).forEach(btn => {
            btn.addEventListener('click', () => {
                if(btn.classList.contains('active')) return
                const settingId = btn.dataset['settingId']
                updateCurrentSetting(settingId)
            })
        })
    }
})