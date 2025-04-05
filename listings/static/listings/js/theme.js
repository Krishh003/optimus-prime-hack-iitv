document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;

    // Check localStorage for theme preference
    const savedTheme = localStorage.getItem('theme') || 'light-mode';
    body.className = savedTheme;

    // Update toggle button icon based on current theme
    updateThemeIcon(savedTheme);

    // Toggle theme
    themeToggle.addEventListener('click', function() {
        const currentTheme = body.className;
        const newTheme = currentTheme === 'light-mode' ? 'dark-mode' : 'light-mode';

        body.className = newTheme;
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });

    function updateThemeIcon(theme) {
        themeToggle.innerHTML = theme === 'dark-mode' ?
            '<i class="fas fa-sun"></i>' :
            '<i class="fas fa-moon"></i>';
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