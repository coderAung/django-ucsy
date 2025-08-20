document.addEventListener("DOMContentLoaded", function() {
    // Get the categories list URL from a data attribute
    const categoriesListUrl = document.body.getAttribute('data-categories-url');
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // ==================== ADD CATEGORY FUNCTIONALITY ====================
    const addForm = document.getElementById('addCategoryForm');
    if (addForm) {
        addForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const submitBtn = this.querySelector('[type="submit"]');
            const spinner = submitBtn.querySelector('.spinner-border') || createSpinner(submitBtn);
            
            // Show loading state
            submitBtn.disabled = true;
            spinner.classList.remove('d-none');
            
            try {
                const formData = new FormData(this);
                
                const response = await fetch(this.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                    }
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Hide the modal
                    bootstrap.Modal.getInstance(document.getElementById('addCategoryModal')).hide();
                    
                    // Show success toast
                    showToast('success', 'Category added successfully!');
                    
                    // Either redirect or update the table
                    if (data.redirect_url) {
                        window.location.href = data.redirect_url;
                    } else {
                        // Add new row to the table
                        const tableBody = document.querySelector('table tbody');
                        const newRow = document.createElement('tr');
                        newRow.dataset.categoryId = data.category.id;
                        newRow.innerHTML = `
                            <td>${data.category.id}</td>
                            <td>${data.category.name}</td>
                            <td class="text-center">0</td>
                            <td class="text-center">${data.category.created_by}</td>
                            <td class="text-center">${data.category.created_at}</td>
                            <td class="text-center">
                                <button class="btn btn-sm btn-outline-primary edit-category-btn" 
                                        data-bs-toggle="modal" 
                                        data-bs-target="#editCategoryModal"
                                        data-category-id="${data.category.id}"
                                        data-category-name="${data.category.name}">
                                    <i class="bi bi-pencil"></i>
                                </button>
                                <button class="btn btn-sm btn-outline-danger delete-category-btn" 
                                        data-category-id="${data.category.id}"
                                        data-category-name="${data.category.name}">
                                    <i class="bi bi-trash"></i>
                                </button>
                            </td>
                        `;
                        tableBody.appendChild(newRow);
                        
                        // Update total count
                        const totalElem = document.querySelector(".total-categories strong");
                        if (totalElem) {
                            totalElem.textContent = parseInt(totalElem.textContent) + 1;
                        }
                        
                        // Reset form
                        addForm.reset();
                    }
                } else {
                    showToast('danger', data.error || 'Failed to add category.');
                }
            } catch (error) {
                console.error('Error:', error);
                showToast('danger', 'An error occurred while adding the category.');
            } finally {
                submitBtn.disabled = false;
                spinner.classList.add('d-none');
            }
        });
    }

    // ==================== EDIT FUNCTIONALITY ====================
    const editModal = document.getElementById('editCategoryModal');
    if (editModal) {
        editModal.addEventListener('show.bs.modal', function(event) {
            const button = event.relatedTarget;
            const categoryId = button.getAttribute('data-category-id');
            const categoryName = button.getAttribute('data-category-name');
            
            // Update the modal content
            const modalTitle = editModal.querySelector('.modal-title');
            const nameInput = editModal.querySelector('#editCategoryName');
            const form = editModal.querySelector('#editCategoryForm');
            
            modalTitle.textContent = `Edit Category: ${categoryName}`;
            nameInput.value = categoryName;
            form.action = `/admins/categories/${categoryId}/edit/`;
            form.dataset.categoryId = categoryId;
        });
        
        // Handle form submission
        const editForm = document.getElementById('editCategoryForm');
        if (editForm) {
            editForm.addEventListener('submit', async function(e) {
                e.preventDefault();
                const submitBtn = this.querySelector('[type="submit"]');
                const spinner = submitBtn.querySelector('.spinner-border') || createSpinner(submitBtn);
                
                // Show loading state
                submitBtn.disabled = true;
                spinner.classList.remove('d-none');
                
                try {
                    const formData = new FormData(this);
                    const categoryId = this.dataset.categoryId;
                    
                    const response = await fetch(this.action, {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                        }
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        // Update the table row
                        const row = document.querySelector(`tr[data-category-id="${categoryId}"]`);
                        if (row) {
                            row.querySelector('td:nth-child(2)').textContent = data.category.name;
                            // Update the edit button data attribute
                            const editBtn = row.querySelector('.edit-category-btn');
                            if (editBtn) {
                                editBtn.setAttribute('data-category-name', data.category.name);
                            }
                        }
                        
                        // Hide the modal
                        bootstrap.Modal.getInstance(editModal).hide();
                        
                        // Show success toast
                        showToast('success', 'Category updated successfully!');
                    } else {
                        showToast('danger', data.error || 'Failed to update category.');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    showToast('danger', 'An error occurred while updating the category.');
                } finally {
                    submitBtn.disabled = false;
                    spinner.classList.add('d-none');
                }
            });
        }
    }

    // ==================== DELETE FUNCTIONALITY ====================
    const deleteButtons = document.querySelectorAll('.delete-category-btn');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const categoryId = this.getAttribute('data-category-id');
            const categoryName = this.getAttribute('data-category-name');
            
            // Create confirmation modal HTML
            const modalHTML = `
                <div class="modal fade" id="deleteConfirmModal" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Confirm Delete</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                Are you sure you want to delete <strong>${categoryName}</strong>?
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                                <button type="button" class="btn btn-danger" id="confirmDelete">
                                    <span class="spinner-border spinner-border-sm d-none" role="status" aria-hidden="true"></span>
                                    Delete
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Add modal to DOM
            document.body.insertAdjacentHTML('beforeend', modalHTML);
            
            // Show modal
            const deleteModal = new bootstrap.Modal(document.getElementById('deleteConfirmModal'));
            deleteModal.show();
            
            // Handle delete confirmation
            document.getElementById('confirmDelete').addEventListener('click', function() {
                const deleteBtn = this;
                const spinner = deleteBtn.querySelector('.spinner-border');
                
                // Show loading state
                deleteBtn.disabled = true;
                spinner.classList.remove('d-none');
                
                deleteCategory(categoryId, categoryName, deleteModal, deleteBtn);
            });
            
            // Clean up modal after close
            document.getElementById('deleteConfirmModal').addEventListener('hidden.bs.modal', function() {
                this.remove();
            });
        });
    });
    
    // Function to handle the actual deletion
    async function deleteCategory(categoryId, categoryName, modal, deleteBtn) {
        try {
            const response = await fetch(`/admins/categories/${categoryId}/delete/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                // Hide the modal first
                modal.hide();
                
                // Remove the row from the table
                const row = document.querySelector(`tr[data-category-id="${categoryId}"]`);
                if (row) row.remove();
                
                // Update total count
                const totalElem = document.querySelector(".total-categories strong");
                if (totalElem) {
                    totalElem.textContent = parseInt(totalElem.textContent) - 1;
                }
                
                // Show success toast
                showToast('success', `Category "${categoryName}" deleted successfully!`);
                
                // Redirect to categories list if needed
                if (categoriesListUrl) {
                    setTimeout(() => {
                        window.location.href = categoriesListUrl;
                    }, 1500);
                }
            } else {
                showToast('danger', data.error || 'Failed to delete category.');
                if (deleteBtn) {
                    deleteBtn.disabled = false;
                    deleteBtn.querySelector('.spinner-border').classList.add('d-none');
                }
            }
        } catch (error) {
            console.error('Error:', error);
            showToast('danger', 'An error occurred while deleting the category.');
            if (deleteBtn) {
                deleteBtn.disabled = false;
                deleteBtn.querySelector('.spinner-border').classList.add('d-none');
            }
        }
    }

    // ==================== HELPER FUNCTIONS ====================
    function showToast(type, message) {
        // Remove any existing toasts first
        const existingToasts = document.querySelectorAll('.toast-container');
        existingToasts.forEach(toast => toast.remove());
        
        const toastHTML = `
            <div class="toast-container position-fixed bottom-0 end-0 p-3">
                <div class="toast show" role="alert" aria-live="assertive" aria-atomic="true">
                    <div class="toast-header bg-${type} text-white">
                        <strong class="me-auto">Notification</strong>
                        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
                    </div>
                    <div class="toast-body">
                        ${message}
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', toastHTML);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            const toastEl = document.querySelector('.toast-container .toast');
            if (toastEl) {
                const toast = new bootstrap.Toast(toastEl);
                toast.hide();
                toastEl.addEventListener('hidden.bs.toast', () => {
                    toastEl.remove();
                });
            }
        }, 5000);
    }
    
    function createSpinner(button) {
        const spinner = document.createElement('span');
        spinner.className = 'spinner-border spinner-border-sm d-none';
        spinner.setAttribute('role', 'status');
        spinner.setAttribute('aria-hidden', 'true');
        button.insertBefore(spinner, button.firstChild);
        return spinner;
    }
});