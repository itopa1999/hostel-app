// Ensure main.js is loaded before running
let accessToken = null;
let userRole = null;
let isAdmin = false;

if (typeof CookieManager === 'undefined') {
    console.error('CookieManager not found. Make sure main.js is loaded before settings.js');
    window.location.href = "auth.html";
} else {
    accessToken = CookieManager.get("access_token");
    userRole = CookieManager.get("user_group");
    isAdmin = !userRole || userRole === 'Admin';
    
    if (!accessToken) {
        window.location.href = "auth.html";
    }
}

document.addEventListener('DOMContentLoaded', function() {
    hidePreloader();
    setupSettingsButtons();
    setupRoleBasedAccess();
});

function setupRoleBasedAccess() {
    if (!isAdmin) {
        // Hide System Settings section for staff users
        const rightColumn = document.querySelector('.right-column');
        if (rightColumn) {
            rightColumn.style.display = 'none';
        }
    }
}

function setupSettingsButtons() {
    const settingButtons = document.querySelectorAll('.action-btn');
    
    settingButtons.forEach(button => {
        button.addEventListener('click', function() {
            const text = this.innerText;
            handleSettingClick(text);
        });
    });
}

function handleSettingClick(settingName) {
    switch(settingName.toLowerCase()) {
        case 'profile settings':
            openProfileSettingsModal();
            break;
        case 'change password':
            openChangePasswordModal();
            break;
        case 'notifications':
            showModal('Notification settings feature coming soon!', 'info');
            break;
        case 'general settings':
            openGeneralSettingsModal();
            break;
        case 'backup & restore':
            showModal('Backup & restore feature coming soon!', 'info');
            break;
        case 'system information':
            showSystemInfo();
            break;
        default:
            showModal(`${settingName} feature coming soon!`, 'info');
    }
}

function showSystemInfo() {
    const info = `
        <strong>HotelOS Admin Dashboard</strong><br>
        Version: 1.0.0<br>
        Build: 2026.01<br>
        Last Updated: ${new Date().toLocaleDateString()}<br>
        <br>
        All systems operational ✓
    `;
    showModal(info, 'info');
}

// API calls for settings updates
async function updateProfileSettings(data) {
    try {
        const response = await APIInterceptor.fetch(`${USER_URL}profile/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.is_success) {
            showModal('Profile updated successfully!', 'success');
        } else {
            showModal('Failed to update profile.', 'fail');
        }
    } catch (error) {
        console.error('Error updating profile:', error);
        showModal('Error updating profile. Please try again.', 'fail');
    }
}

async function changePassword(oldPassword, newPassword) {
    try {
        const response = await APIInterceptor.fetch(`${USER_URL}change-password/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify({
                old_password: oldPassword,
                new_password: newPassword
            })
        });
        
        const result = await response.json();
        
        if (result.is_success) {
            showModal('Password changed successfully!', 'success');
        } else {
            showModal('Failed to change password.', 'fail');
        }
    } catch (error) {
        console.error('Error changing password:', error);
        showModal('Error changing password. Please try again.', 'fail');
    }
}

// General Settings Modal Functions
async function openGeneralSettingsModal() {
    try {        
        // Fetch current settings
        const response = await APIInterceptor.fetch(`${ADMIN_URL}settings/general/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success && data.data) {
            const settings = data.data;
            showSettingsModal(settings);
        } else {
            showModal('Failed to load settings.', 'fail');
        }
    } catch (error) {
        console.error('Error loading settings:', error);
        showModal('Error loading settings. Please try again.', 'fail');
    }
}

function showSettingsModal(settings) {
    // Remove existing modal if present
    const existingModal = document.getElementById('generalSettingsModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Create modal
    const modal = document.createElement('div');
    modal.id = 'generalSettingsModal';
    modal.className = 'modal active';
    
    modal.innerHTML = `
        <div class="modal-content" style="max-width: 500px;">
            <div class="modal-header">
                <h2>General Settings</h2>
                <button class="modal-close" id="closeSettingsModal">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <form id="generalSettingsForm">
                    <div class="form-group">
                        <label for="taxPercentage" style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Tax Percentage (%)</label>
                        <input type="number" id="taxPercentage" name="tax_percentage" step="0.01" min="0" max="100" 
                               value="${settings.tax_percentage || 0}" class="form-control" 
                               style="padding: 0.75rem; border: 1px solid var(--border-color); border-radius: 8px; width: 100%;">
                        <small style="color: var(--text-muted); display: block; margin-top: 0.25rem;">e.g., 10 for 10%</small>
                    </div>
                    <div class="form-group" style="margin-top: 1.5rem;">
                        <label for="discountPercentage" style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Default Discount Percentage (%)</label>
                        <input type="number" id="discountPercentage" name="default_discount_percentage" step="0.01" min="0" max="100" 
                               value="${settings.default_discount_percentage || 0}" class="form-control" 
                               style="padding: 0.75rem; border: 1px solid var(--border-color); border-radius: 8px; width: 100%;">
                        <small style="color: var(--text-muted); display: block; margin-top: 0.25rem;">e.g., 5 for 5%</small>
                    </div>
                    <div class="form-group" style="margin-top: 1.5rem;">
                        <label for="description" style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Description</label>
                        <textarea id="description" name="description" class="form-control" 
                                  style="padding: 0.75rem; border: 1px solid var(--border-color); border-radius: 8px; width: 100%; min-height: 80px; resize: vertical;">${settings.description || ''}</textarea>
                        <small style="color: var(--text-muted); display: block; margin-top: 0.25rem;">Optional notes about these settings</small>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" id="cancelSettingsBtn">Cancel</button>
                <button class="btn btn-primary" id="saveSettingsBtn">Save Settings</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Add event listeners
    document.getElementById('closeSettingsModal').addEventListener('click', closeSettingsModal);
    document.getElementById('cancelSettingsBtn').addEventListener('click', closeSettingsModal);
    document.getElementById('saveSettingsBtn').addEventListener('click', saveGeneralSettings);
}

function closeSettingsModal() {
    const modal = document.getElementById('generalSettingsModal');
    if (modal) {
        modal.classList.remove('active');
        setTimeout(() => {
            if (modal.parentNode) {
                modal.remove();
            }
        }, 300);
    }
}

async function saveGeneralSettings() {
    try {
        const taxPercentage = document.getElementById('taxPercentage').value;
        const discountPercentage = document.getElementById('discountPercentage').value;
        const description = document.getElementById('description').value;
        
        // Validate inputs
        if (!taxPercentage || !discountPercentage) {
            showModal('Please fill in all required fields.', 'fail');
            return;
        }
        
        const taxNum = parseFloat(taxPercentage);
        const discountNum = parseFloat(discountPercentage);
        
        if (taxNum < 0 || taxNum > 100 || discountNum < 0 || discountNum > 100) {
            showModal('Tax and discount percentages must be between 0 and 100.', 'fail');
            return;
        }
        
        const response = await APIInterceptor.fetch(`${ADMIN_URL}settings/general/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify({
                tax_percentage: taxNum,
                default_discount_percentage: discountNum,
                description: description
            })
        });
        
        const data = await response.json();
        
        if (data.is_success) {
            showModal('Settings saved successfully!', 'success');
            closeSettingsModal();
        } else {
            showModal(data.message || 'Failed to save settings.', 'fail');
        }
    } catch (error) {
        console.error('Error saving settings:', error);
        showModal('Error saving settings. Please try again.', 'fail');
    }
}

// Profile Settings Modal Functions
async function openProfileSettingsModal() {
    try {
        showPreloader();
        
        const response = await APIInterceptor.fetch(`${USER_URL}detail/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        console.log('Profile data:', data);
        hidePreloader();
        
        if (data.is_success && data.data) {
            showProfileModal(data.data);
        } else {
            hidePreloader();
            showModal(data.message || 'Failed to load profile.', 'fail');
        }
    } catch (error) {
        hidePreloader();
        console.error('Error loading profile:', error);
        showModal('Error loading profile. Please try again.', 'fail');
    }
}

function showProfileModal(user) {
    const existingModal = document.getElementById('profileSettingsModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    const modal = document.createElement('div');
    modal.id = 'profileSettingsModal';
    modal.className = 'modal active';
    
    const emailValue = (user.email && user.email.trim()) ? user.email : '';
    const firstNameValue = (user.first_name && user.first_name.trim()) ? user.first_name : '';
    const lastNameValue = (user.last_name && user.last_name.trim()) ? user.last_name : '';
    
    modal.innerHTML = `
        <div class="modal-content" style="max-width: 500px;">
            <div class="modal-header">
                <h2>Edit Profile</h2>
                <button class="modal-close" id="closeProfileModal">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <form id="profileEditForm">
                    <div class="form-group">
                        <label for="profileEmail" style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Email</label>
                        <input type="email" id="profileEmail" name="email" class="form-control" 
                               placeholder="Enter your email address"
                               style="padding: 0.75rem; border: 1px solid var(--border-color); border-radius: 8px; width: 100%;">
                    </div>
                    <div class="form-group" style="margin-top: 1rem;">
                        <label for="profileFirstName" style="display: block; margin-bottom: 0.5rem; font-weight: 500;">First Name</label>
                        <input type="text" id="profileFirstName" name="first_name" class="form-control" 
                               placeholder="Enter your first name"
                               style="padding: 0.75rem; border: 1px solid var(--border-color); border-radius: 8px; width: 100%;">
                    </div>
                    <div class="form-group" style="margin-top: 1rem;">
                        <label for="profileLastName" style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Last Name</label>
                        <input type="text" id="profileLastName" name="last_name" class="form-control" 
                               placeholder="Enter your last name"
                               style="padding: 0.75rem; border: 1px solid var(--border-color); border-radius: 8px; width: 100%;">
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" id="cancelProfileBtn">Cancel</button>
                <button class="btn btn-primary" id="saveProfileBtn">Save Changes</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Populate form fields after DOM is ready
    setTimeout(() => {
        const emailInput = document.getElementById('profileEmail');
        const firstNameInput = document.getElementById('profileFirstName');
        const lastNameInput = document.getElementById('profileLastName');
        
        if (emailInput) emailInput.value = emailValue;
        if (firstNameInput) firstNameInput.value = firstNameValue;
        if (lastNameInput) lastNameInput.value = lastNameValue;
        
        console.log('Form populated with:', { email: emailValue, first_name: firstNameValue, last_name: lastNameValue });
    }, 10);
    
    document.getElementById('closeProfileModal').addEventListener('click', closeProfileModal);
    document.getElementById('cancelProfileBtn').addEventListener('click', closeProfileModal);
    document.getElementById('saveProfileBtn').addEventListener('click', saveProfileSettings);
}

function closeProfileModal() {
    const modal = document.getElementById('profileSettingsModal');
    if (modal) {
        modal.classList.remove('active');
        setTimeout(() => {
            if (modal.parentNode) {
                modal.remove();
            }
        }, 300);
    }
}

async function saveProfileSettings() {
    try {
        const email = document.getElementById('profileEmail').value.trim();
        const firstName = document.getElementById('profileFirstName').value.trim();
        const lastName = document.getElementById('profileLastName').value.trim();
        
        if (!email) {
            showModal('Email is required.', 'fail');
            return;
        }
        
        
        const response = await APIInterceptor.fetch(`${USER_URL}update/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify({
                email: email,
                first_name: firstName,
                last_name: lastName
            })
        });
        
        const data = await response.json();
        
        if (data.is_success) {
            showModal('Profile updated successfully!', 'success');
            closeProfileModal();
        } else {
            showModal(data.message || 'Failed to update profile.', 'fail');
        }
    } catch (error) {
        console.error('Error saving profile:', error);
        showModal('Error saving profile. Please try again.', 'fail');
    }
}

// Change Password Modal Functions
function openChangePasswordModal() {
    const existingModal = document.getElementById('changePasswordModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    const modal = document.createElement('div');
    modal.id = 'changePasswordModal';
    modal.className = 'modal active';
    
    modal.innerHTML = `
        <div class="modal-content" style="max-width: 500px;">
            <div class="modal-header">
                <h2>Change Password</h2>
                <button class="modal-close" id="closePasswordModal">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <form id="changePasswordForm">
                    <div class="form-group">
                        <label for="oldPassword" style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Current Password</label>
                        <input type="password" id="oldPassword" name="old_password" class="form-control" 
                               placeholder="Enter your current password"
                               style="padding: 0.75rem; border: 1px solid var(--border-color); border-radius: 8px; width: 100%;" required>
                    </div>
                    <div class="form-group" style="margin-top: 1rem;">
                        <label for="newPassword" style="display: block; margin-bottom: 0.5rem; font-weight: 500;">New Password</label>
                        <input type="password" id="newPassword" name="new_password" class="form-control" 
                               placeholder="Enter your new password"
                               style="padding: 0.75rem; border: 1px solid var(--border-color); border-radius: 8px; width: 100%;" required>
                        <small style="color: var(--text-muted); display: block; margin-top: 0.25rem;">Minimum 6 characters</small>
                    </div>
                    <div class="form-group" style="margin-top: 1rem;">
                        <label for="confirmPassword" style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Confirm Password</label>
                        <input type="password" id="confirmPassword" name="confirm_password" class="form-control" 
                               placeholder="Re-enter your new password"
                               style="padding: 0.75rem; border: 1px solid var(--border-color); border-radius: 8px; width: 100%;" required>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" id="cancelPasswordBtn">Cancel</button>
                <button class="btn btn-primary" id="savePasswordBtn">Change Password</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    document.getElementById('closePasswordModal').addEventListener('click', closePasswordModal);
    document.getElementById('cancelPasswordBtn').addEventListener('click', closePasswordModal);
    document.getElementById('savePasswordBtn').addEventListener('click', changePassword);
}

function closePasswordModal() {
    const modal = document.getElementById('changePasswordModal');
    if (modal) {
        modal.classList.remove('active');
        setTimeout(() => {
            if (modal.parentNode) {
                modal.remove();
            }
        }, 300);
    }
}

async function changePassword() {
    try {
        const oldPassword = document.getElementById('oldPassword').value;
        const newPassword = document.getElementById('newPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        if (!oldPassword || !newPassword || !confirmPassword) {
            showModal('All fields are required.', 'fail');
            return;
        }
        
        if (newPassword.length < 6) {
            showModal('New password must be at least 6 characters long.', 'fail');
            return;
        }
        
        if (newPassword !== confirmPassword) {
            showModal('Passwords do not match.', 'fail');
            return;
        }
        
        if (oldPassword === newPassword) {
            showModal('New password must be different from current password.', 'fail');
            return;
        }
        
        
        const response = await APIInterceptor.fetch(`${USER_URL}change-password/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify({
                old_password: oldPassword,
                new_password: newPassword
            })
        });
        
        const data = await response.json();
        
        if (data.is_success) {
            showModal('Password changed successfully!', 'success');
            closePasswordModal();
        } else {
            showModal(data.message || 'Failed to change password.', 'fail');
        }
    } catch (error) {
        console.error('Error changing password:', error);
        showModal('Error changing password. Please try again.', 'fail');
    }
}


