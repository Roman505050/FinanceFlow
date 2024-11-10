document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('loginForm');
    const inputs = form.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            input.parentElement.classList.remove('has-error');
            input.parentElement.querySelector('.error-message').style.opacity = 0;
        });
    });
});