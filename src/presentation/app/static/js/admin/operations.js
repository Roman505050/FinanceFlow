import {showToast} from "../toast.js";

const operationsList = document.querySelector('.operations-body');
const operationForm = document.getElementById('operationForm');
const newOperationInput = document.getElementById('newOperation');
operationForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    if (!operationForm.checkValidity()) {
        showToast('Будь ласка, введіть назву операції', 'info');
        return;
    }

    const name = newOperationInput.value.trim();
    const type = document.querySelector('input[name="operationType"]:checked').value;

    try {
        const response = await fetch('/api/v1/operations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                operation_name: name,
                operation_type: type,
            }),
        });

        if (response.status === 201) {
            newOperationInput.value = '';
            document.querySelector('input[name="operationType"][value="income"]').checked = true;
            getOperations();
        } else {
            console.error('Error creating operation:', response);
            showToast('Помилка при створенні операції', 'error');
        }
    } catch (error) {
        console.error('Error creating operation:', error);
        showToast('Помилка при створенні операції', 'error');
    }
});


async function getOperations() {
    try {
        document.getElementById('loaderСontainer').classList.remove('hidden');
        document.getElementById('operationsList').classList.add('hidden');

        const response = await fetch('/api/v1/operations');
        if (!response.ok) {
            console.error('Error fetching operations:', response);
            showToast('Помилка завантаження даних', 'error');
            return;
        }
        const data = await response.json();
        const operations = Array.isArray(data) ? data : data.operations || [];

        operationsList.innerHTML = '';
        const noOperationsMessage = document.querySelector('.no-operations-message');

        if (operations.length === 0) {
            noOperationsMessage.style.display = 'block';
        } else {
            noOperationsMessage.style.display = 'none';
            operations.forEach(operation => {
                const operationItem = document.createElement('tr');
                operationItem.classList.add('operation-item');
                operationItem.id = `operation-${operation.operation_id}`;
                operationItem.innerHTML = `
                    <td class="operation-name">${operation.operation_name}</td>
                    <td class="operation-type">${operation.operation_type === "income" ? 'Дохід' : operation.operation_type === "expense" ? 'Витрата' : 'Інвестиція'}</td>
                    <td class="operation-actions">
                        <button class="delete-btn" data-id="${operation.operation_id}">
                            <i class="fas fa-trash"></i>
                        </button>
                        <div class="delete-loader hidden" id="delete-loader-${operation.operation_id}"></div>
                    </td>
                `;
                operationsList.appendChild(operationItem);
            });
        }
    } catch (error) {
        console.error('Error fetching operations:', error);
    } finally {
        document.getElementById('loaderСontainer').classList.add('hidden');
        document.getElementById('operationsList').classList.remove('hidden');
    }
}

operationsList.addEventListener('click', async (event) => {
    if (event.target.closest('.delete-btn')) {
        const deleteBtn = event.target.closest('.delete-btn');
        const operationId = deleteBtn.dataset.id;

        const deleteLoader = document.getElementById(`delete-loader-${operationId}`);
        const trashIcon = deleteBtn.querySelector('i');

        trashIcon.classList.add('hidden');
        deleteLoader.classList.remove('hidden');
        deleteBtn.disabled = true;
        deleteBtn.classList.add('hidden');

        try {
            const response = await fetch(`/api/v1/operations/${operationId}`, {
                method: 'DELETE'
            });

            if (response.status === 200) {
                const operationItem = document.getElementById(`operation-${operationId}`);
                operationItem.remove();
                showToast('Операцію успішно видалено', 'success');
            } else {
                showToast('Помилка видалення операції', 'error');
            }
        } catch (error) {
            console.error('Error deleting operation:', error);
            showToast('Помилка видалення операції', 'error');
        } finally {
            trashIcon.classList.remove('hidden');
            deleteBtn.disabled = false;
            deleteBtn.classList.remove('hidden');
            deleteLoader.classList.add('hidden');
        }
    }
});

getOperations();
