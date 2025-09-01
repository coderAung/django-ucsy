// document.addEventListener('DOMContentLoaded', () => {
//     let lastScroll = 0
//     const navbar = document.getElementById('navbar')
//     if(navbar) {
//         window.addEventListener('scroll', () => {
//             const currentScroll = window.pageYOffset || document.documentElement.scrollTop
//             if(currentScroll > lastScroll) {
//                 navbar.classList.add('hidden')
//             } else {
//                 navbar.classList.remove('hidden')
//             }
//             lastScroll = currentScroll <= 0 ? 0 : currentScroll
//         })
//     }
// })

document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;

    let lastScroll = 0;

    // Wait for browser to render before adding scroll listener
    requestAnimationFrame(() => {
        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset || document.documentElement.scrollTop;

            if (currentScroll > lastScroll) {
                navbar.classList.add('hidden');
            } else {
                navbar.classList.remove('hidden');
            }

            lastScroll = currentScroll <= 0 ? 0 : currentScroll;
        });
    });
});
