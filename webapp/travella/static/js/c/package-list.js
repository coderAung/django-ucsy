document.addEventListener('DOMContentLoaded', () => {
    const categoryFilter = document.getElementsByClassName('categoryFilter')
    const locationFilter = document.getElementsByClassName('locationFilter')

    const categoryInput = document.getElementById('categoryInput')
    const locationInput = document.getElementById('locationInput')

    const categoryBtn = document.getElementById('categoryBtn')
    const locationBtn = document.getElementById('locationBtn')
    const dateChooseBtn = document.getElementById('dateChooseBtn')
    const fromDateInput = document.getElementById('fromDateInput')
    const toDateInput = document.getElementById('toDateInput')
    const resetDateBtn = document.getElementById('resetDateBtn')
    const thisMonthBtn = document.getElementById('thisMonthBtn')
    const nextMonthBtn = document.getElementById('nextMonthBtn')
    const okDateBtn = document.getElementById('okDateBtn')
    const clearFilterBtn = document.getElementById('clearFilterBtn')
    const keyInput = document.getElementById('keyInput')


    if(dateChooseBtn && fromDateInput && toDateInput && resetDateBtn && thisMonthBtn && nextMonthBtn && okDateBtn) {

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
        const fromDatePicker = flatpickr('#fromDateInput', {
            altInput: true,
            altFormat: 'F j, Y',
            dateFormat: 'Y-m-d',
        })

        const toDatePicker = flatpickr('#toDateInput', {
            altInput: true,
            altFormat: 'F j, Y',
            dateFormat: 'Y-m-d',
        })

        fromDatePicker.set('onChange', [
            function(selectedDates) {
                if(selectedDates.length > 0) {
                    dateValidation(fromDatePicker, toDatePicker)
                }
            }
        ])

        const departureDisplay = document.getElementById('departureDisplay')
        const updateDepartureDisplay = (text = 'Departure Date') => departureDisplay.innerText = text

        resetDateBtn.addEventListener('click', () => {
            fromDatePicker.clear()
            toDatePicker.clear()
            updateDepartureDisplay()
        })

        okDateBtn.addEventListener('click', () => {
            if(fromDatePicker.selectedDates.length > 0 && toDatePicker.selectedDates.length > 0) {
                updateDepartureDisplay(`${fromDatePicker.altInput.value} ... ${toDatePicker.altInput.value}`)
            }
            bootstrap.Modal.getInstance('#dateChoose').hide()
        })

        const updateDates = (from, to) => {
            fromDatePicker.setDate(from, true)
            toDatePicker.setDate(to, true)
            updateDepartureDisplay(`${fromDatePicker.altInput.value} ... ${toDatePicker.altInput.value}`)
        }

        thisMonthBtn.addEventListener('click', () => {
            const now = new Date()
            const thisMonthStart = new Date(now.getFullYear(), now.getMonth(), 1)
            const thisMonthEnd = new Date(now.getFullYear(), now.getMonth() + 1, 0)
            fromDatePicker.setDate(thisMonthStart, true)
            toDatePicker.setDate(thisMonthEnd, true)
            updateDepartureDisplay(`${fromDatePicker.altInput.value} ... ${toDatePicker.altInput.value}`)
        })

        nextMonthBtn.addEventListener('click', () => {
            const now = new Date()
            const nextMonthStart = new Date(now.getFullYear(), now.getMonth() + 1, 1)
            const nextMonthEnd = new Date(now.getFullYear(), now.getMonth() + 2, 0)
            updateDates(nextMonthStart, nextMonthEnd)
        })

        const loadFilter = () => {
            const params = new URLSearchParams(window.location.search)
            const categoryId = params.get('categoryId')
            const locationId = params.get('locationId')
            const fromDate = params.get('fromDate')
            const toDate = params.get('toDate')
            const q = params.get('q')
            if(q) {
                keyInput.value = q
            }
            if(categoryId) {
                Array.from(categoryFilter).filter(cf => cf.dataset['filterValue'] == categoryId).forEach(cf => {
                    categoryInput.value = categoryId
                    categoryBtn.innerText = cf.innerText    
                })
            }
            if(locationId) {
                Array.from(locationFilter).filter(lf => lf.dataset['filterValue'] == locationId).forEach(lf => {
                    locationInput.value = locationId
                    locationBtn.innerText = lf.innerText
                })
            }
            if(fromDate && toDate) {
                updateDates(new Date(fromDate), new Date(toDate))
            }
        }

        loadFilter()

    }

    if(categoryFilter && locationFilter && categoryInput && locationInput && categoryBtn && locationBtn && clearFilterBtn) {
        const filterFunc = (btn, input, filter) => {
            btn.innerText = filter.innerText
            input.value = filter.dataset['filterValue']
        }
        Array.from(categoryFilter).forEach(c => {
            c.addEventListener('click', () => filterFunc(btn = categoryBtn, input = categoryInput, c))
        })
        Array.from(locationFilter).forEach(l => {
            l.addEventListener('click', () => filterFunc(btn = locationBtn, input = locationInput, l))
        })

        clearFilterBtn.addEventListener('click', () => {
            categoryBtn.innerText = 'Category'
            categoryInput.value = ''
            locationBtn.innerText = 'Location'
            locationInput.value = ''
            resetDateBtn.click()
            keyInput.value = ''
            filterForm.submit()
        })

    }

    const paginationBtns = document.getElementsByClassName('paginationBtn')
    const pageInput = document.getElementById('pageInput')
    const filterForm = document.getElementById('filterForm')
    if(paginationBtns && pageInput && filterForm) {
        const paginate = btn => {            
            const page = btn.dataset['page']
            pageInput.value = page
            filterForm.submit()
        }
        Array.from(paginationBtns).forEach(btn => {
            if(!btn.classList.contains('active')) {
                btn.addEventListener('click', () => paginate(btn))
            }
        })
    }
})

