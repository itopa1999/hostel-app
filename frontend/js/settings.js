// Ensure main.js is loaded before running
let accessToken = null;

if (typeof CookieManager === 'undefined') {
    console.error('CookieManager not found. Make sure main.js is loaded before settings.js');
    window.location.href = "auth.html";
} else {
    accessToken = CookieManager.get("access_token");
    if (!accessToken) {
        window.location.href = "auth.html";
    }
}

document.addEventListener('DOMContentLoaded', function() {
    hidePreloader();
    setupSettingsButtons();
});

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
            showModal('Profile settings feature coming soon!', 'info');
            break;
        case 'change password':
            showModal('Change password feature coming soon!', 'info');
            break;
        case 'notifications':
            showModal('Notification settings feature coming soon!', 'info');
            break;
        case 'general settings':
            showModal('General settings feature coming soon!', 'info');
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
