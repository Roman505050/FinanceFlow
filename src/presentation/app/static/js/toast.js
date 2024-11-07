function showToast(message, type) {
    const toastContainer = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    toast.innerHTML = `
        <span class="toast-icon" aria-hidden="true"></span>
        <span class="toast-message">${message}</span>
        <button class="toast-close" aria-label="Закрити повідомлення">&times;</button>
    `;

    toastContainer.appendChild(toast);


    setTimeout(() => toast.classList.add('show'), 10);

    const timeout = setTimeout(() => {
        removeToast(toast);
    }, 5000);

    toast.querySelector('.toast-close').addEventListener('click', () => {
        clearTimeout(timeout);
        removeToast(toast);
    });
}

function removeToast(toast) {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
}


window.handleFlashedMessages = function (messages) {
    if (!messages || !Array.isArray(messages)) {
        console.error('No messages or invalid messages format');
        return;
    }

    messages.forEach(([category, message]) => {
        const toastCategory = category || 'info';
        showToast(message, toastCategory);
    });
};
