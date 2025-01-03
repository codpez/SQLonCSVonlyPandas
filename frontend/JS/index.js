// js/index.js
document.addEventListener('DOMContentLoaded', function() {
    // Animación para el título
    const title = document.querySelector('.title');
    if (title) {
        title.style.opacity = '0';
        setTimeout(() => {
            title.style.transition = 'opacity 1s ease-in-out';
            title.style.opacity = '1';
        }, 100);
    }

    // Animación para las feature cards
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease-in-out';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 300 + (index * 200)); // Añade delay progresivo para cada carta
    });

    // Efecto hover más suave para el botón CTA
    const ctaButton = document.querySelector('.cta-button');
    if (ctaButton) {
        ctaButton.addEventListener('mouseenter', () => {
            ctaButton.style.transform = 'scale(1.05)';
            ctaButton.style.boxShadow = '0 4px 15px rgba(99, 102, 241, 0.4)';
        });

        ctaButton.addEventListener('mouseleave', () => {
            ctaButton.style.transform = 'scale(1)';
            ctaButton.style.boxShadow = 'none';
        });
    }
});