document.addEventListener('DOMContentLoaded', () => {
    let currentSettingId = 'accountSetting'
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
    }

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