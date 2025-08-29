document.addEventListener('DOMContentLoaded', () => {
    const paginationBtns = document.getElementsByClassName('paginationBtn')
    const searchBtn = document.getElementById('searchBtn')
    const pageInput = document.getElementById('pageInput')
    const statusInput = document.getElementById('statusInput')
    const statusBtns = document.getElementsByClassName('statusBtn')
    if(paginationBtns && searchBtn && pageInput && statusInput && statusBtns) {
        Array.from(paginationBtns).forEach(btn => {
            btn.addEventListener('click', () => {
                if(btn.classList.contains('active')) return
                const page = btn.dataset['page']
                pageInput.value = page
                searchBtn.click()
            })
        })

        Array.from(statusBtns).forEach(btn => {
            btn.addEventListener('click', () => {
                if(btn.classList.contains('active')) return
                if(btn.dataset['status']) statusInput.value = btn.dataset['status']
                else statusInput.value = ''
                searchBtn.click()
            })
        })
    }

    const fromDatePicker = flatpickr('#fromDateInput', {
        altInput: true,
        altFormat: 'M j, Y',
        dateFormat: 'Y-m-d',
    })

    const toDatePicker = flatpickr('#toDateInput', {
        altInput: true,
        altFormat: 'M j, Y',
        dateFormat: 'Y-m-d',
    })
    const nextDayOf = (date) => {
        const newDate = new Date(date)
        newDate.setDate(newDate.getDate() + 1)
        return newDate
    }

    const dateValidation = (from, to) => {
        if(from.selectedDates.length > 0) {
            to.set('minDate', nextDayOf(from.selectedDates[0]))
        }
    }

    fromDatePicker.set('onChange', [
        function(selectedDates) {
            if(selectedDates.length > 0) {
                dateValidation(fromDatePicker, toDatePicker)
            }
        }
    ])

    const searchForm = document.getElementById('searchForm')
    const clearBtn = document.getElementById('clearBtn')
    if(clearBtn) {
        clearBtn.addEventListener('click', () => {
            searchForm.querySelectorAll('input, select, textarea').forEach(input => {
                switch(input.type) {
                case 'checkbox':
                case 'radio':
                    input.checked = false
                    break
                default:
                    input.value = ''
                }
            })
            fromDatePicker.clear()
            toDatePicker.clear()
        })
    }
})