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
    const type = document.querySelector('input[name="operationType"]:checked').value === 'true';

    try {
        const response = await fetch('/api/v1/operation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                operation_name: name,
                is_income: type,
            }),
        });

        if (response.status === 201) {
            newOperationInput.value = '';
            document.querySelector('input[name="operationType"][value="true"]').checked = true;
            getOperations();
        } else {
            console.error('Помилка при додаванні операції:', response.statusText);
        }
    } catch (error) {
        console.error('Помилка мережі:', error);
    }
});


async function getOperations() {
    try {
        document.getElementById('loaderСontainer').classList.remove('hidden');
        document.getElementById('operationsList').classList.add('hidden');

        const response = await fetch('/api/v1/operation');
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
                operationItem.innerHTML = `
                    <td class="operation-name">${operation.operation_name}</td>
                    <td class="operation-type">${operation.is_income ? 'Надходження' : 'Витрати'}</td>
                    <td class="operation-actions">
                        <button class="delete-btn" data-id="${operation.operation_id}">
                            <i class="fas fa-trash"></i>
                        </button>
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

        try {
            const response = await fetch(`/api/v1/operation/${operationId}`, {
                method: 'DELETE'
            });

            if (response.status === 200) {
                for (const operationItem of document.querySelectorAll('.operation-item')) {
                    if (operationItem.querySelector('.delete-btn').dataset.id === operationId) {
                        operationItem.remove();
                        break;
                    }
                }
            } else {
                showToast('Помилка видалення операції', 'error');
            }
        } catch (error) {
            console.error('Error deleting operation:', error);
        }
    }
});

getOperations();
