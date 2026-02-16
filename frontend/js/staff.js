// Ensure main.js is loaded before running
let accessToken = null;
let allStaff = [];
let allGroups = [];
let currentStaffId = null;

if (typeof CookieManager === 'undefined') {
    console.error('CookieManager not found. Make sure main.js is loaded before staff.js');
    window.location.href = "auth.html";
} else {
    accessToken = CookieManager.get("access_token");
    if (!accessToken) {
        window.location.href = "auth.html";
    }
}

document.addEventListener('DOMContentLoaded', function() {
    hidePreloader();
    loadGroups();
    loadStaff();
    setupEventListeners();
});

function setupEventListeners() {
    // Search functionality
    const searchInput = document.getElementById('staffSearchInput');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => searchStaff(e));
    }

    // Add Staff button
    const addStaffBtn = document.getElementById('addStaffBtn');
    if (addStaffBtn) {
        addStaffBtn.addEventListener('click', openCreateStaffModal);
    }

    // Create Staff modal close buttons
    const closeCreateStaffModal = document.getElementById('closeCreateStaffModal');
    const closeCreateBtn = document.getElementById('closeCreateBtn');
    if (closeCreateStaffModal) {
        closeCreateStaffModal.addEventListener('click', closeCreateModal);
    }
    if (closeCreateBtn) {
        closeCreateBtn.addEventListener('click', closeCreateModal);
    }

    // Save Staff button
    const saveStaffBtn = document.getElementById('saveStaffBtn');
    if (saveStaffBtn) {
        saveStaffBtn.addEventListener('click', createNewStaff);
    }

    // Details modal
    document.getElementById('closeDetailsModal')?.addEventListener('click', closeDetailsModal);

    // Change Group modal buttons
    const closeChangeGroupModal = document.getElementById('closeChangeGroupModal');
    if (closeChangeGroupModal) {
        closeChangeGroupModal.addEventListener('click', closeChangeGroupModalFn);
    }
    
    const cancelChangeGroupBtn = document.getElementById('cancelChangeGroupBtn');
    if (cancelChangeGroupBtn) {
        cancelChangeGroupBtn.addEventListener('click', closeChangeGroupModalFn);
    }
    
    const saveChangeGroupBtn = document.getElementById('saveChangeGroupBtn');
    if (saveChangeGroupBtn) {
        saveChangeGroupBtn.addEventListener('click', function() {
            const modal = document.getElementById('changeGroupModal');
            const userId = parseInt(modal.dataset.userId);
            updateStaffGroup(userId);
        });
    }

    // Delete modal controls
    const closeDeleteModal = document.getElementById('closeDeleteModal');
    if (closeDeleteModal) {
        closeDeleteModal.addEventListener('click', closeDeleteStaffModal);
    }
    
    const cancelDeleteBtn = document.getElementById('cancelDeleteBtn');
    if (cancelDeleteBtn) {
        cancelDeleteBtn.addEventListener('click', closeDeleteStaffModal);
    }
    
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener('click', confirmDeleteStaff);
    }
}

async function loadGroups() {
    try {
        const response = await APIInterceptor.fetch(`${USER_URL}groups/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        const data = await response.json();
        if (data.is_success && data.data && Array.isArray(data.data.groups)) {
            allGroups = data.data.groups;
            console.log('Groups loaded:', allGroups);
        } else {
            console.warn('Invalid groups data:', data.data);
            allGroups = [];
        }
    } catch (error) {
        console.error('Error loading groups:', error);
        allGroups = [];
    }
}

async function loadStaff() {
    try {        
        const response = await APIInterceptor.fetch(`${USER_URL}list/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success && data.data) {
            console.log('Staff data:', data.data);
            allStaff = data.data;
            displayStaffAsCards(data.data);
        } else {
            console.error('Failed to load staff:', data.message);
            showModal('Failed to load staff. Please refresh the page.', 'fail');
        }
    } catch (error) {
        console.error('Error fetching staff:', error);
        showModal('Error loading staff. Please check your connection.', 'fail');
    }
}

function displayStaffAsCards(staff) {
    const container = document.getElementById('staffContainer');
    if (!container) return;
    
    if (staff.length === 0) {
        container.style.display = 'flex';
        container.style.alignItems = 'center';
        container.style.justifyContent = 'center';
        container.style.minHeight = '400px';
        container.innerHTML = `
            <div style="text-align: center; color: var(--text-muted); padding: 3rem;">
                <i class="fas fa-users" style="font-size: 3rem; margin-bottom: 1rem; display: block; color: var(--text-muted);"></i>
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">No staff found</p>
                <p style="margin-bottom: 1.5rem; color: var(--text-muted);">Add a new staff member to get started.</p>
            </div>
        `;
        return;
    }
    
    container.style.display = 'grid';
    container.innerHTML = staff.map(user => `
        <div class="staff-card" style="${user.is_deleted ? 'opacity: 0.6; border: 2px solid #ff6b6b;' : ''}">
            <div class="staff-card-header">
                <div class="staff-number">
                    <span class="number-label">${user.full_name || user.username}${user.is_deleted ? ' <span style="color: #ff6b6b; font-size: 0.8em;">(Deleted)</span>' : ''}</span>
                </div>
                <div class="staff-status-badge">
                    <i class="fas fa-user-tie"></i>
                    Staff
                </div>
                <div class="staff-actions">
                    <button class="icon-btn" title="View Details" onclick="openDetailsModal(${user.id})" style="color: var(--primary-color);">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="icon-btn edit-staff-btn" title="Change Group" data-id="${user.id}" onclick="openChangeGroupModal(${user.id}, '${user.username}')">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="icon-btn ${user.is_deleted ? 'reactivate-staff-btn' : 'delete-staff-btn'}" title="${user.is_deleted ? 'Reactivate' : 'Delete'}" data-id="${user.id}" onclick="toggleDeleteStaff(${user.id})">
                        <i class="fas fa-${user.is_deleted ? 'undo' : 'trash'}"></i>
                    </button>
                </div>
            </div>
            <div class="staff-card-body">
                <div class="staff-info">
                    <span class="info-label">Username:</span>
                    <span class="info-value">${user.username}</span>
                </div>
                <div class="staff-info">
                    <span class="info-label">Email:</span>
                    <span class="info-value">${user.email || 'N/A'}</span>
                </div>
                <div class="staff-info">
                    <span class="info-label">Groups:</span>
                    <span class="info-value">${user.groups?.length > 0 ? user.groups.join(', ') : 'N/A'}</span>
                </div>
                <div class="staff-info">
                    <span class="info-label">Joined:</span>
                    <span class="info-value">${user.date_joined ? new Date(user.date_joined).toLocaleDateString() : 'N/A'}</span>
                </div>
            </div>
        </div>
    `).join('');
}

function openChangeGroupModal(userId, username) {
    const user = allStaff.find(u => u.id === userId);
    const currentGroups = user?.groups || [];
    const modal = document.getElementById('changeGroupModal');
    
    if (!modal) return;
    
    const groupsHTML = Array.isArray(allGroups) && allGroups.length > 0 
        ? allGroups.map(group => `
            <label class="group-checkbox-label">
                <div class="checkbox-wrapper">
                    <input type="checkbox" class="group-checkbox" value="${group.id}" ${currentGroups.includes(group.name) ? 'checked' : ''} 
                           style="width: 18px; height: 18px; cursor: pointer; accent-color: #667eea;">
                    <span class="group-name">${group.name}</span>
                </div>
            </label>
        `).join('')
        : '<p style="color: var(--text-muted); text-align: center; padding: 1rem;">No groups available</p>';
    
    // Update modal header
    const header = modal.querySelector('.modal-header h2');
    if (header) header.textContent = `Manage Groups - ${username}`;
    
    // Update modal body
    const body = modal.querySelector('.modal-body');
    if (body) {
        body.innerHTML = `
            <div style="display: flex; flex-direction: column; gap: 1rem;">
                <div class="form-group">
                    <label for="updatePasswordInput" style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Change Password (Optional)</label>
                    <input type="password" id="updatePasswordInput" placeholder="Enter new password (min 6 characters)" class="form-control" style="padding: 0.75rem; border: 1px solid var(--border-color); border-radius: 8px;">
                    <small style="color: var(--text-muted); display: block; margin-top: 0.25rem;">Leave empty to keep current password</small>
                </div>
                <div style="border-top: 1px solid var(--border-color); padding-top: 1rem;">
                    <h4 style="margin-bottom: 0.75rem;">Groups:</h4>
                    ${groupsHTML}
                </div>
            </div>
        `;
    }
    
    // Store userId for use in updateStaffGroup
    modal.dataset.userId = userId;
    
    modal.classList.add('active');
}

async function updateStaffGroup(userId) {
    const modal = document.getElementById('changeGroupModal');
    if (!modal) return;
    
    const checkboxes = modal.querySelectorAll('input[type="checkbox"]:checked');
    const selectedGroupIds = Array.from(checkboxes).map(cb => parseInt(cb.value));
    const passwordInput = document.getElementById('updatePasswordInput');
    const newPassword = passwordInput ? passwordInput.value.trim() : '';
    
    if (selectedGroupIds.length === 0) {
        showModal('Please select at least one group', 'fail');
        return;
    }
    
    // Validate password if provided
    if (newPassword && newPassword.length < 6) {
        showModal('Password must be at least 6 characters long', 'fail');
        return;
    }
    
    try {        
        const payload = { groups: selectedGroupIds };
        if (newPassword) {
            payload.password = newPassword;
        }
        
        const response = await APIInterceptor.fetch(`${USER_URL}${userId}/update-groups/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        
        if (data.is_success) {
            const message = newPassword ? 'Group and password updated successfully!' : 'Group updated successfully!';
            showModal(message, 'success');
            modal.classList.remove('active');
            loadStaff(); // Refresh the list
        } else {
            showModal(data.message || 'Failed to update group.', 'fail');
        }
    } catch (error) {
        console.error('Error updating group:', error);
        showModal('Error updating group. Please try again.', 'fail');
    }
}

async function toggleDeleteStaff(userId) {
    const user = allStaff.find(u => u.id === userId);
    if (!user) return;
    
    currentStaffId = userId;
    const action = user.is_deleted ? 'reactivate' : 'delete';
    
    // Update modal based on action
    const modal = document.getElementById('deleteStaffModal');
    const header = modal.querySelector('.modal-header h2');
    const message = document.getElementById('deleteMessage');
    const confirmBtn = document.getElementById('confirmDeleteBtn');
    
    if (user.is_deleted) {
        header.textContent = 'Reactivate Staff';
        message.textContent = `Are you sure you want to reactivate ${user.full_name || user.username}? They will be able to login again.`;
        confirmBtn.textContent = 'Reactivate';
        confirmBtn.className = 'btn btn-primary';
    } else {
        header.textContent = 'Delete Staff';
        message.textContent = `Are you sure you want to delete ${user.full_name || user.username}? They will not be able to login.`;
        confirmBtn.textContent = 'Delete';
        confirmBtn.className = 'btn btn-danger';
    }
    
    modal.classList.add('active');
}

function closeDeleteStaffModal() {
    document.getElementById('deleteStaffModal').classList.remove('active');
    currentStaffId = null;
}

async function confirmDeleteStaff() {
    if (!currentStaffId) return;
    
    const user = allStaff.find(u => u.id === currentStaffId);
    const action = user?.is_deleted ? 'restore' : 'delete';
    
    try {        
        const response = await APIInterceptor.fetch(`${USER_URL}${currentStaffId}/delete/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success) {
            showModal(`Staff member ${action === 'delete' ? 'deleted' : 'restored'} successfully!`, 'success');
            closeDeleteStaffModal();
            loadStaff(); // Refresh the list
        } else {
            showModal(data.message || `Failed to ${action} staff member.`, 'fail');
        }
    } catch (error) {
        console.error(`Error ${action}ing staff:`, error);
        showModal(`Error ${action}ing staff. Please try again.`, 'fail');
    }
}

function searchStaff(e) {
    const searchTerm = e.target.value.toLowerCase();
    
    if (!searchTerm) {
        displayStaffAsCards(allStaff);
        return;
    }
    
    const filtered = allStaff.filter(user => {
        const fullName = (user.full_name || user.username || '').toLowerCase();
        const username = (user.username || '').toLowerCase();
        const email = (user.email || '').toLowerCase();
        const idNumber = (user.id_number || '').toLowerCase();
        
        return (
            fullName.includes(searchTerm) ||
            username.includes(searchTerm) ||
            email.includes(searchTerm) ||
            idNumber.includes(searchTerm)
        );
    });
    
    displayStaffAsCards(filtered);
}

function openCreateStaffModal() {
    const modal = document.getElementById('createStaffModal');
    if (!modal) return;
    
    // Reset form
    const form = document.getElementById('createStaffForm');
    if (form) form.reset();
    
    // Populate group checkboxes
    const groupCheckboxes = document.getElementById('groupCheckboxes');
    if (groupCheckboxes && allGroups.length > 0) {
        groupCheckboxes.innerHTML = allGroups.map(group => `
            <label class="group-checkbox-create-label">
                <div class="group-checkbox-create-wrapper">
                    <input type="checkbox" id="group_${group.id}" name="group_${group.id}" value="${group.id}" class="group-checkbox-create">
                    <span class="group-checkbox-create-name">${group.name}</span>
                </div>
            </label>
        `).join('');
    } else if (groupCheckboxes) {
        groupCheckboxes.innerHTML = '<p style="color: var(--text-muted);">No groups available</p>';
    }
    
    modal.classList.add('active');
}

function closeCreateModal() {
    const modal = document.getElementById('createStaffModal');
    if (modal) {
        modal.classList.remove('active');
    }
}

function closeChangeGroupModalFn() {
    const modal = document.getElementById('changeGroupModal');
    if (modal) {
        modal.classList.remove('active');
    }
}

async function createNewStaff() {
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    const email = document.getElementById('email').value.trim();
    const firstName = document.getElementById('firstName').value.trim();
    const lastName = document.getElementById('lastName').value.trim();
    
    // Validate required fields
    if (!username) {
        showModal('Username is required', 'fail');
        return;
    }
    if (!password) {
        showModal('Password is required', 'fail');
        return;
    }
    
    // Get selected groups
    const selectedGroups = Array.from(document.querySelectorAll('.group-checkbox-create:checked'))
        .map(checkbox => parseInt(checkbox.value));
    
    const staffData = {
        username: username,
        password: password,
        email: email || null,
        first_name: firstName,
        last_name: lastName,
        groups: selectedGroups,
        is_active: true,
        is_staff: true
    };
    
    try {
        const response = await APIInterceptor.fetch(`${USER_URL}create/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify(staffData)
        });
        
        const data = await response.json();
        
        if (data.is_success) {
            showModal('Staff member created successfully!', 'success');
            closeCreateModal();
            loadStaff(); // Refresh the list
        } else {
            showModal(data.message || 'Failed to create staff member.', 'fail');
        }
    } catch (error) {
        console.error('Error creating staff:', error);
        showModal('Error creating staff. Please try again.', 'fail');
    }
}

function openDetailsModal(userId) {
    const user = allStaff.find(u => u.id === userId);
    if (!user) return;
    
    document.getElementById('detailsFullName').textContent = user.full_name || 'N/A';
    document.getElementById('detailsUsername').textContent = user.username || 'N/A';
    document.getElementById('detailsEmail').textContent = user.email || 'N/A';
    document.getElementById('detailsIdNumber').textContent = user.id_number || 'N/A';
    document.getElementById('detailsGroups').textContent = user.groups?.length > 0 ? user.groups.join(', ') : 'No groups assigned';
    document.getElementById('detailsDateJoined').textContent = user.date_joined ? new Date(user.date_joined).toLocaleDateString() : 'N/A';
    document.getElementById('detailsLastLogin').textContent = user.last_login ? new Date(user.last_login).toLocaleDateString() : 'Never';
    
    if (user.created_by) {
        document.getElementById('detailsCreatedBySection').style.display = 'block';
        document.getElementById('detailsCreatedBy').textContent = user.created_by;
    } else {
        document.getElementById('detailsCreatedBySection').style.display = 'none';
    }
    
    if (user.is_deleted && user.deleted_at) {
        document.getElementById('detailsDeletedSection').style.display = 'block';
        document.getElementById('detailsDeletedAt').textContent = new Date(user.deleted_at).toLocaleDateString();
        document.getElementById('detailsDeletedBy').textContent = user.deleted_by || 'N/A';
    } else {
        document.getElementById('detailsDeletedSection').style.display = 'none';
    }
    
    document.getElementById('detailsStaffModal').classList.add('active');
}

function closeDetailsModal() {
    document.getElementById('detailsStaffModal').classList.remove('active');
}

