// Ensure main.js is loaded before running
let accessToken = null;
let allBackups = [];

if (typeof CookieManager === 'undefined') {
    console.error('CookieManager not found. Make sure main.js is loaded before backups.js');
    window.location.href = "auth.html";
} else {
    accessToken = CookieManager.get("access_token");
    if (!accessToken) {
        window.location.href = "auth.html";
    }
    
    // Check if user is admin
    const userGroup = CookieManager.get('user_group');
    if (userGroup && userGroup !== 'Admin') {
        // Redirect non-admin users
        window.location.href = "dashboard.html";
    }
}

document.addEventListener('DOMContentLoaded', function() {
    hidePreloader();
    loadBackups();
    setupEventListeners();
});

function setupEventListeners() {
    document.getElementById('createBackupBtn')?.addEventListener('click', openBackupModal);
    document.getElementById('backupSearchInput')?.addEventListener('keyup', searchBackups);
}

async function loadBackups() {
    try {        
        const response = await APIInterceptor.fetch(`${ADMIN_URL}backup/list/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success && data.data) {
            allBackups = data.data;
            renderBackupsTable(allBackups);
        } else {
            showModal('Failed to load backups', 'fail');
        }
    } catch (error) {
        console.error('Error loading backups:', error);
        showModal('Error loading backups. Please try again.', 'fail');
    }
}

function renderBackupsTable(backups) {
    const tableBody = document.getElementById('backupTableBody');
    const countSpan = document.getElementById('backupCount');
    
    // Update total count
    if (countSpan) {
        countSpan.textContent = backups ? backups.length : 0;
    }
    
    if (!backups || backups.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="7" style="padding: 2rem; text-align: center; color: var(--text-muted);">
                    <i class="fas fa-inbox" style="font-size: 2rem; margin-bottom: 0.5rem;"></i>
                    <p>No backups found</p>
                </td>
            </tr>
        `;
        return;
    }
    
    tableBody.innerHTML = backups.map(backup => {
        const startDate = new Date(backup.start_date).toLocaleDateString();
        const endDate = new Date(backup.end_date).toLocaleDateString();
        const createdDate = new Date(backup.created_at).toLocaleString();
        const fileSize = backup.file_size ? formatFileSize(backup.file_size) : 'N/A';
        const statusColor = getStatusColor(backup.status);
        const statusDisplay = backup.status.charAt(0).toUpperCase() + backup.status.slice(1);
        
        return `
            <tr style="border-bottom: 1px solid var(--border-color); transition: background-color 0.2s;">
                <td style="padding: 1rem;">
                    <strong>${backup.backup_name}</strong>
                    <br/>
                    <small style="color: var(--text-muted);">${createdDate}</small>
                </td>
                <td style="padding: 1rem;">
                    <small>${startDate} to ${endDate}</small>
                </td>
                <td style="padding: 1rem;">
                    <span style="background: var(--card-bg); padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem;">
                        ${backup.record_count} records
                    </span>
                </td>
                <td style="padding: 1rem;">${fileSize}</td>
                <td style="padding: 1rem;">
                    <span style="color: ${statusColor}; font-weight: 600;">
                        <i class="fas fa-circle" style="font-size: 0.5rem; margin-right: 0.5rem;"></i>${statusDisplay}
                    </span>
                </td>
                <td style="padding: 1rem;">
                    <small>${backup.requested_by_username}</small>
                </td>
                <td style="padding: 1rem; text-align: center;">
                    ${backup.status === 'completed' 
                        ? `<button class="btn btn-sm btn-primary" onclick="downloadBackup(${backup.id}, '${backup.backup_name}')" style="padding: 0.5rem 1rem; font-size: 0.85rem;">
                            <i class="fas fa-download"></i> Download
                        </button>`
                        : `<button class="btn btn-sm btn-secondary" disabled style="padding: 0.5rem 1rem; font-size: 0.85rem;">
                            <i class="fas fa-hourglass-end"></i> Processing
                        </button>`
                    }
                </td>
            </tr>
        `;
    }).join('');
}

function getStatusColor(status) {
    const colors = {
        'pending': '#ffc107',
        'processing': '#17a2b8',
        'completed': '#28a745',
        'failed': '#dc3545'
    };
    return colors[status] || '#6c757d';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

function searchBackups() {
    const searchTerm = document.getElementById('backupSearchInput').value.toLowerCase();
    
    const filtered = allBackups.filter(backup => 
        backup.backup_name.toLowerCase().includes(searchTerm) ||
        backup.requested_by_username.toLowerCase().includes(searchTerm)
    );
    
    renderBackupsTable(filtered);
}

function openBackupModal() {
    const existingModal = document.getElementById('backupModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Get today's date as default end date
    const today = new Date();
    const endDate = today.toISOString().split('T')[0];
    
    // Set start date to 7 days ago
    const startDateObj = new Date(today);
    startDateObj.setDate(startDateObj.getDate() - 7);
    const startDate = startDateObj.toISOString().split('T')[0];
    
    const modal = document.createElement('div');
    modal.id = 'backupModal';
    modal.className = 'modal active';
    
    modal.innerHTML = `
        <div class="modal-content" style="max-width: 500px;">
            <div class="modal-header">
                <h2>Create New Backup</h2>
                <button class="modal-close" id="closeBackupModal">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <form id="backupForm">
                    <div class="form-group">
                        <label for="backupStartDate" style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Start Date</label>
                        <input type="date" id="backupStartDate" name="start_date" class="form-control" 
                               value="${startDate}"
                               style="padding: 0.75rem; border: 1px solid var(--border-color); border-radius: 8px; width: 100%;" required>
                    </div>
                    <div class="form-group" style="margin-top: 1rem;">
                        <label for="backupEndDate" style="display: block; margin-bottom: 0.5rem; font-weight: 500;">End Date</label>
                        <input type="date" id="backupEndDate" name="end_date" class="form-control" 
                               value="${endDate}"
                               style="padding: 0.75rem; border: 1px solid var(--border-color); border-radius: 8px; width: 100%;" required>
                    </div>
                    <small style="color: var(--text-muted); display: block; margin-top: 0.5rem;">
                        <i class="fas fa-info-circle"></i> Backup will include all records created within this date range
                    </small>
                </form>
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" id="cancelBackupBtn">Cancel</button>
                <button class="btn btn-primary" id="startBackupBtn">
                    <i class="fas fa-download"></i> Start Backup
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    document.getElementById('closeBackupModal').addEventListener('click', closeBackupModal);
    document.getElementById('cancelBackupBtn').addEventListener('click', closeBackupModal);
    document.getElementById('startBackupBtn').addEventListener('click', submitBackup);
}

function closeBackupModal() {
    const modal = document.getElementById('backupModal');
    if (modal) {
        modal.classList.remove('active');
        setTimeout(() => modal.remove(), 300);
    }
}

async function submitBackup() {
    const startDate = document.getElementById('backupStartDate').value;
    const endDate = document.getElementById('backupEndDate').value;
    
    if (!startDate || !endDate) {
        showModal('Please select both start and end dates', 'fail');
        return;
    }
    
    if (new Date(endDate) < new Date(startDate)) {
        showModal('End date must be after start date', 'fail');
        return;
    }
    
    try {
        const button = document.getElementById('startBackupBtn');
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
        
        const response = await APIInterceptor.fetch(`${ADMIN_URL}backup/create/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify({
                start_date: startDate,
                end_date: endDate
            })
        });
        
        const result = await response.json();
        
        if (result.is_success) {
            closeBackupModal();
            showModal('Backup started successfully!', 'success');
            loadBackups();
        } else {
            showModal(result.message || 'Failed to start backup', 'fail');
        }
    } catch (error) {
        console.error('Error starting backup:', error);
        showModal('Error starting backup. Please try again.', 'fail');
    } finally {
        const button = document.getElementById('startBackupBtn');
        if (button) {
            button.disabled = false;
            button.innerHTML = '<i class="fas fa-download"></i> Start Backup';
        }
    }
}

async function downloadBackup(backupId, backupName) {
    try {
        const response = await fetch(`${ADMIN_URL}backup/${backupId}/download/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        if (!response.ok) {
            const error = await response.json();
            showModal(error.message || 'Failed to download backup', 'fail');
            return;
        }
        
        // Create blob and download
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `${backupName}.csv`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
        
        showModal('Backup downloaded successfully!', 'success');
    } catch (error) {
        console.error('Error downloading backup:', error);
        showModal('Error downloading backup. Please try again.', 'fail');
    }
}

// Auto-refresh backups every 30 seconds
setInterval(() => {
    loadBackups();
}, 30000);
