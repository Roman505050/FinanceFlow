import {showToast} from "../toast.js";

const modal = document.getElementById('transactionModal');
const openModalBtn = document.getElementById('openModal');
const closeBtn = document.getElementsByClassName('close')[0];
const operationSelect = document.getElementById('operation');
const categorySelect = document.getElementById('category');
const currencySelect = document.getElementById('currency');
const form = document.getElementById('transactionForm');

openModalBtn.onclick = () => modal.style.display = 'block';

closeBtn.onclick = () => modal.style.display = 'none';
window.onclick = (event) => {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
};

function showLoader() {
    const loaderTransactionModal = document.getElementById('loaderTransactionModal');
    loaderTransactionModal.style.display = 'flex';
}

function hideLoader() {
    const loaderTransactionModal = document.getElementById('loaderTransactionModal');
    loaderTransactionModal.style.display = 'none';
}

async function fetchOperations() {
    operationSelect.innerHTML = '<option value="">Завантаження...</option>';
    operationSelect.disabled = true;

    try {
        const response = await fetch('api/v1/operation/autocomplete');
        const data = await response.json();

        operationSelect.innerHTML = '<option value="">Виберіть операцію</option>';
        data.forEach(op => {
            const option = document.createElement('option');
            option.value = op.value;
            option.textContent = op.label;
            operationSelect.appendChild(option);
        });

        operationSelect.disabled = false;
    } catch (error) {
        console.error('Error fetching operations:', error);
    }
}

async function fetchCurrencies() {
    currencySelect.innerHTML = '<option value="">Завантаження...</option>';
    currencySelect.disabled = true;

    try {
        const response = await fetch('api/v1/currency/autocomplete');
        const data = await response.json();

        currencySelect.innerHTML = '<option value="">Виберіть валюту</option>';
        data.forEach(cur => {
            const option = document.createElement('option');
            option.value = cur.value;
            option.textContent = cur.label;
            currencySelect.appendChild(option);
        });

        currencySelect.disabled = false;
    } catch (error) {
        console.error('Error fetching currencies:', error);
    }
}

async function fetchCategories(operationId) {
    categorySelect.innerHTML = '<option value="">Завантаження...</option>';
    categorySelect.disabled = true;

    try {
        const response = await fetch(`api/v1/category/autocomplete?operation_id=${operationId}`);
        const data = await response.json();

        if (operationSelect.value !== operationId) {
            categorySelect.innerHTML = '<option value="">Виберіть категорію</option>';
            return;
        }

        categorySelect.innerHTML = '<option value="">Виберіть категорію</option>';
        data.forEach(cat => {
            const option = document.createElement('option');
            option.value = cat.value;
            option.textContent = cat.label;
            categorySelect.appendChild(option);
        });

        categorySelect.disabled = false;
    } catch (error) {
        console.error('Error fetching categories:', error);
        categorySelect.innerHTML = '<option value="">Помилка завантаження</option>';
    }
}

async function saveTransaction(transaction) {
    try {
        const response = await fetch('api/v1/transaction', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(transaction)
        });

        if (response.status === 201) {
            return true;
        }
        console.error('Fetch error:', response);
        return false;
    } catch (error) {
        console.error('Fetch error:', error);
        return false;
    }
}

operationSelect.addEventListener('change', (e) => {
    if (e.target.value) {
        categorySelect.innerHTML = '<option value="">Виберіть категорію</option>';
        categorySelect.disabled = true;

        fetchCategories(e.target.value);
    } else {
        categorySelect.innerHTML = '<option value="">Виберіть категорію</option>';
        categorySelect.disabled = true;
    }
});

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    showLoader();

    const formData = new FormData(form);
    const transaction = {
        operation_id: formData.get('operation'),
        category_id: formData.get('category'),
        currency_id: formData.get('currency'),
        amount: formData.get('amount'),
        date: formData.get('date'),
        description: formData.get('description')
    }

    const success = await saveTransaction(transaction);
    if (success) {
        showToast('Транзакцію успішно збережено', 'success');
        modal.style.display = 'none';
        hideLoader();
        // Sleep for 0.5 second to allow the modal to close before reloading the page
        await new Promise(resolve => setTimeout(resolve, 500));
        window.location.reload();
    } else {
        showToast('Виникла помилка при збереженні транзакції', 'error');
        hideLoader();
    }
});


fetchOperations();
fetchCurrencies();