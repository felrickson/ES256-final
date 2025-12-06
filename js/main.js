// Main Interactivity for ES256 Project

document.addEventListener('DOMContentLoaded', () => {
    console.log('ES256 Presentation Loaded');

    // Navbar scroll effect
    const nav = document.querySelector('nav');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            nav.classList.add('shadow-lg');
            nav.classList.replace('bg-brand-dark/80', 'bg-brand-dark/95');
        } else {
            nav.classList.remove('shadow-lg');
            nav.classList.replace('bg-brand-dark/95', 'bg-brand-dark/80');
        }
    });

    // Smooth scroll for anchor links (fallback for older browsers)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});
