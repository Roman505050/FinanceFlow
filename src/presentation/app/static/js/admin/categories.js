import {showToast} from "../toast.js";

const categoryItemsContainer = document.getElementById('categoryItems');
const categoryForm = document.getElementById('categoryForm');
const operationTypeSelect = document.getElementById('operationType');
const newCategoryInput = document.getElementById('newCategory');

async function fetchOperations() {
    try {
        operationTypeSelect.innerHTML = '<option value="" disabled selected>Завантаження...</option>';
        operationTypeSelect.disabled = true;

        const response = await fetch('/api/v1/operations/autocomplete');
        if (!response.ok) {
            console.error('Error fetching operation types:', response);
            showToast('Помилка завантаження типів категорій', 'error');
            operationTypeSelect.innerHTML = '<option value="" disabled selected>Помилка при завантаженні</option>';
            operationTypeSelect.disabled = true;
            return;
        }

        const data = await response.json();
        operationTypeSelect.innerHTML = '<option value="" disabled selected>Виберіть тип</option>';
        operationTypeSelect.disabled = false;

        data.forEach(item => {
            const option = document.createElement('option');
            option.value = item.value;
            option.textContent = item.label;
            operationTypeSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error fetching operation types:', error);
        showToast('Помилка завантаження типів категорій', 'error');
    }
}

async function createCategory(newCategory, operationType) {
    try {
        const response = await fetch('/api/v1/categories', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                category_name: newCategory,
                operation_id: operationType,
            }),
        });

        if (response.status === 201) {
            showToast('Категорію успішно додано', 'success');
            fetchCategories();
            categoryForm.reset();
        } else {
            console.error('Error creating category:', response);
            showToast('Помилка при створенні категорії', 'error');
        }
    } catch (error) {
        console.error('Error creating category:', error);
        showToast('Помилка при створенні категорії', 'error');
    }
}

async function fetchCategories() {
    try {
        document.getElementById('loaderСontainer').classList.remove('hidden');
        document.getElementById('categoriesList').classList.add('hidden');

        const response = await fetch('/api/v1/categories');
        if (!response.ok) {
            console.error('Error fetching categories:', response);
            showToast('Помилка при завантаженні категорій', 'error');
            return;
        }

        const data = await response.json();
        const categories = data.categories || [];

        categoryItemsContainer.innerHTML = '';
        const noCategoriesMessage = document.querySelector('.no-categories-message');

        if (categories.length === 0) {
            noCategoriesMessage.style.display = 'block';
        } else {
            noCategoriesMessage.style.display = 'none';
            categories.forEach(category => {
                const categoryItem = document.createElement('tr');
                categoryItem.classList.add('category-item');
                categoryItem.id = `category-${category.category_id}`;
                categoryItem.innerHTML = `
                    <td class="category-name">${category.category_name}</td>
                    <td class="category-type">${category.operation_name}</td>
                    <td class="category-actions">
                        <button class="delete-btn" data-id="${category.category_id}">
                            <i class="fas fa-trash"></i>
                        </button>
                        <div class="delete-loader hidden" id="delete-loader-${category.category_id}"></div>
                    </td>
                `;
                categoryItemsContainer.appendChild(categoryItem);
            });
        }
    } catch (error) {
        console.error('Error fetching categories:', error);
        showToast('Помилка при завантаженні категорій', 'error');
    } finally {
        // Hide loader and show categories list
        document.getElementById('loaderСontainer').classList.add('hidden');
        document.getElementById('categoriesList').classList.remove('hidden');
    }
}

categoryForm.addEventListener('submit', async function (e) {
    e.preventDefault();

    if (!categoryForm.checkValidity()) {
        showToast('Будь ласка, заповніть всі обов\'язкові поля', 'info');
        return;
    }

    const newCategory = newCategoryInput.value.trim();
    const operationType = operationTypeSelect.value;

    await createCategory(newCategory, operationType);
});

categoryItemsContainer.addEventListener('click', async (event) => {
    if (event.target.closest('.delete-btn')) {
        const deleteBtn = event.target.closest('.delete-btn');
        const categoryId = deleteBtn.dataset.id;

        const deleteLoader = document.getElementById(`delete-loader-${categoryId}`);
        const trashIcon = deleteBtn.querySelector('i');

        trashIcon.classList.add('hidden');
        deleteLoader.classList.remove('hidden');
        deleteBtn.disabled = true;
        deleteBtn.classList.add('hidden');

        try {
            const response = await fetch(`/api/v1/categories/${categoryId}`, {
                method: 'DELETE'
            });

            if (response.status === 200) {
                const categoryItem = document.getElementById(`category-${categoryId}`);
                categoryItem.remove();
                showToast('Категорію успішно видалено', 'success');
            } else {
                showToast('Помилка видалення категорії', 'error');
            }
        } catch (error) {
            console.error('Error deleting category:', error);
            showToast('Помилка видалення категорії', 'error');
        } finally {
            trashIcon.classList.remove('hidden');
            deleteBtn.disabled = false;
            deleteBtn.classList.remove('hidden');
            deleteLoader.classList.add('hidden');
        }
    }
});

fetchOperations();
fetchCategories();
