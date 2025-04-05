document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;

    // Check localStorage for theme preference
    const savedTheme = localStorage.getItem('theme') || 'light-mode';
    if (savedTheme === 'dark-mode') {
        body.classList.add('dark-mode');
        updateThemeIcon(true);
    } else {
        body.classList.remove('dark-mode');
        updateThemeIcon(false);
    }

    // Toggle theme
    themeToggle.addEventListener('click', function() {
        const isDarkMode = body.classList.contains('dark-mode');
        body.classList.toggle('dark-mode');
        localStorage.setItem('theme', isDarkMode ? 'light-mode' : 'dark-mode');
        updateThemeIcon(!isDarkMode);
    });

    function updateThemeIcon(isDarkMode) {
        const icon = themeToggle.querySelector('i');
        if (icon) {
            icon.className = isDarkMode ? 'fas fa-sun' : 'fas fa-moon';
        }
    }

    // Scroll animations
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    }, { threshold: 0.1 });

    animateElements.forEach(element => {
        observer.observe(element);
    });
});