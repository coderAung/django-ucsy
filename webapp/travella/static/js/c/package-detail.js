document.addEventListener('DOMContentLoaded', () => {
    const images = document.querySelectorAll('.packageImageWrapper img')
    const carouselDiv = document.getElementById('imagesCarousel')
    const modalDiv = document.getElementById('imagesModal')

    if(images && carouselDiv && modalDiv) {
        const modal = bootstrap.Modal.getInstance(modalDiv) || new bootstrap.Modal(modalDiv)
        const carousel = bootstrap.Carousel.getInstance(carouselDiv) || new bootstrap.Carousel(carouselDiv, {ride: false})                
        Array.from(images).forEach(i => {
            i.addEventListener('click', () => {
                const index = i.dataset['num']
                modal.show()
                carousel.to(index - 1)
            })
        })

        document.addEventListener('keydown', (e) => {
            if(modalDiv.classList.contains('show')) {
                switch(e.key) {
                case 'ArrowLeft':
                    carousel.prev()
                    break
                case 'ArrowRight':
                    carousel.next()
                    break
                case 'Escape':
                    modal.hide()
                    break
                }
            }
        })
    }

})