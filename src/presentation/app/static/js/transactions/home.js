import {showToast} from "../toast.js";

let transactions = [];

async function fetchTransactions() {
    try {
        document.getElementById('loaderContainer').classList.remove('hidden');
        document.getElementById('transactionTable').classList.add('hidden');

        const response = await fetch('/api/v1/transaction/me');
        if (!response.ok) {
            console.error('Fetch error:', response);
            showToast('Помилка завантаження даних', 'error');
            return;
        } else {
            const data = await response.json();
            transactions = data.transactions;
        }
        populateTable();
    } catch (error) {
        console.error('Fetch error:', error);
        showToast('Помилка завантаження даних', 'error');
    } finally {
        document.getElementById('loaderContainer').classList.add('hidden');
        document.getElementById('transactionTable').classList.remove('hidden');
    }
}

async function deleteTransaction(transactionId) {
    try {
        const response = await fetch(`/api/v1/transaction/${transactionId}`, {
            method: 'DELETE'
        });
        if (response.ok) {
            showToast('Транзакцію успішно видалено', 'success');
            return true;
        }
        console.error('Fetch error:', response);
        showToast('Помилка видалення транзакції', 'error');
        return false;
    } catch (error) {
        console.error('Fetch error:', error);
        showToast('Помилка видалення транзакції', 'error');
        return false;
    }
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('uk-UA', {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric'
    });
}

function createTransactionRow(transaction) {
    const row = document.createElement('tr');
    row.id = `transaction-${transaction.transaction_id}`;
    row.innerHTML = `
                <td data-label="Дата">${formatDate(transaction.date)}</td>
                <td data-label="Операція">
                    <span class="badge badge-${transaction.operation_is_income ? 'income' : 'expense'}">
                        ${transaction.operation_is_income ? '↑' : '↓'} ${transaction.operation_name}
                    </span>
                </td>
                <td data-label="Категорія">${transaction.category_name}</td>
                <td data-label="Сума" class="amount-${transaction.operation_is_income ? 'income' : 'expense'}">
                    ${transaction.operation_is_income ? '+' : '-'}${transaction.amount} ${transaction.currency_symbol}
                </td>
                <td data-label="Опис">
                    <button class="description-button" data-id="${transaction.transaction_id}">
                        ▼
                    </button>
                </td>
                <td data-label="Дії">
                    <button class="delete-btn" data-id="${transaction.transaction_id}">
                        <i class="fas fa-trash"></i>
                    </button>
                    <div class="delete-loader hidden" id="delete-loader-${transaction.transaction_id}"></div>
                </td>
            `;
    return row;
}

function createDescriptionRow(transaction) {
    const row = document.createElement('tr');
    row.className = 'description-row';
    row.id = `description-${transaction.transaction_id}`;
    row.innerHTML = `
                <td colspan="6">
                    <div class="description-content">${transaction.description}</div>
                </td>
            `;
    return row;
}

function populateTable() {
    const tableBody = document.querySelector('#transactionTable tbody');
    tableBody.innerHTML = '';

    transactions.forEach(transaction => {
        tableBody.appendChild(createTransactionRow(transaction));
        tableBody.appendChild(createDescriptionRow(transaction));
    });

    setupDescriptionToggle();
    setupDeleteButtons();
}

function setupDescriptionToggle() {
    document.querySelectorAll('.description-button').forEach(button => {
        button.addEventListener('click', function () {
            const id = this.getAttribute('data-id');
            const descriptionRow = document.getElementById(`description-${id}`);
            if (descriptionRow.style.display === 'table-row') {
                descriptionRow.style.display = 'none';
                this.textContent = '▼';
            } else {
                descriptionRow.style.display = 'table-row';
                this.textContent = '▲';
            }
        });
    });
}

function setupDeleteButtons() {
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', async function () {
            const id = this.getAttribute('data-id');
            const deleteLoader = document.getElementById(`delete-loader-${id}`);
            const trashIcon = this.querySelector('i');
            const deleteButton = this;

            trashIcon.classList.add('hidden');
            deleteLoader.classList.remove('hidden');
            deleteButton.disabled = true;
            deleteButton.classList.add('hidden');

            const isDeleted = await deleteTransaction(id);
            if (isDeleted) {
                transactions = transactions.filter(t => t.transaction_id !== id);
                document.getElementById(`transaction-${id}`).remove();
                document.getElementById(`description-${id}`).remove();
            } else {
                trashIcon.classList.remove('hidden');
                deleteButton.disabled = false;
                deleteButton.classList.remove('hidden');
                deleteLoader.classList.add('hidden');
            }
        });
    });
}

function initTable() {
    fetchTransactions();
}

document.addEventListener('DOMContentLoaded', initTable);