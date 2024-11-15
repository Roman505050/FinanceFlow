import {showToast} from "./toast.js";

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