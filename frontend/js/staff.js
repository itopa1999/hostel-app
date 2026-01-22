// Ensure main.js is loaded before running
let accessToken = null;

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
    loadStaff();
});

async function loadStaff() {
    try {        
        const response = await APIInterceptor.fetch(`${HOSTEL_URL}staff/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success && data.data) {
            console.log('Staff data:', data.data);
            populateStaffTable(data.data);
        } else {
            console.error('Failed to load staff:', data.message);
            showModal('Failed to load staff. Please refresh the page.', 'fail');
        }
    } catch (error) {
        console.error('Error fetching staff:', error);
        showModal('Error loading staff. Please check your connection.', 'fail');
    }
}

function populateStaffTable(staffMembers) {
    const tbody = document.getElementById('staff-tbody');
    if (!tbody) return;
    
    if (staffMembers.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; padding: 3rem;"><div style="color: var(--text-muted);"><i class="fas fa-users" style="font-size: 2rem; margin-bottom: 1rem; display: block; color: var(--text-muted);"></i><p style="font-size: 1.1rem; margin-bottom: 1rem;">No staff found</p><p style="margin-bottom: 1.5rem; color: var(--text-muted);">Add a new staff member to get started.</p></div></td></tr>`;
        return;
    }
    
    tbody.innerHTML = staffMembers.map(staff => `
        <tr>
            <td>${staff.name || staff.first_name + ' ' + staff.last_name || '-'}</td>
            <td>${staff.email || '-'}</td>
            <td>${staff.position || '-'}</td>
            <td>${staff.department || '-'}</td>
            <td><span class="badge ${staff.status === 'active' ? 'checked-in' : 'checked-out'}">${staff.status || 'inactive'}</span></td>
            <td>${staff.hire_date ? new Date(staff.hire_date).toLocaleDateString() : '-'}</td>
            <td>
                <button class="action-btn" style="padding: 0.4rem 0.8rem; gap: 0.3rem; font-size: 0.8rem;">
                    <i class="fas fa-edit"></i>
                </button>
            </td>
        </tr>
    `).join('');
}
