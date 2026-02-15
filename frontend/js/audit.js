// Ensure main.js is loaded before running
let accessToken = null;
let allAudits = [];
let currentStartDate = null;
let currentEndDate = null;

if (typeof CookieManager === 'undefined') {
    console.error('CookieManager not found. Make sure main.js is loaded before audit.js');
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
    initializeDateRange();
    loadAudits();
    setupEventListeners();
});

function setupEventListeners() {
    document.getElementById('filterDateBtn')?.addEventListener('click', openDateFilterModal);
    document.getElementById('auditSearchInput')?.addEventListener('keyup', searchAudits);
}

function initializeDateRange() {
    // Set today as default
    const today = new Date();
    const todayStr = today.toISOString().split('T')[0];
    
    currentStartDate = todayStr;
    currentEndDate = todayStr;
    
    updateDateRangeDisplay();
}

function updateDateRangeDisplay() {
    const displayEl = document.getElementById('dateRangeDisplay');
    if (displayEl) {
        const startDate = new Date(currentStartDate);
        const endDate = new Date(currentEndDate);
        
        if (currentStartDate === currentEndDate) {
            displayEl.textContent = startDate.toLocaleDateString();
        } else {
            displayEl.textContent = `${startDate.toLocaleDateString()} - ${endDate.toLocaleDateString()}`;
        }
    }
}

async function loadAudits(startDate = null, endDate = null) {
    try {
        let url = `${ADMIN_URL}audit/list/`;
        
        // Use provided dates or current date range
        const start = startDate || currentStartDate;
        const end = endDate || currentEndDate;
        
        if (start && end) {
            url += `?start_date=${start}&end_date=${end}`;
        }
        
        const response = await APIInterceptor.fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success && data.data) {
            allAudits = data.data;
            renderAuditsTable(allAudits);
        } else {
            showModal('Failed to load audit logs', 'fail');
        }
    } catch (error) {
        console.error('Error loading audit logs:', error);
        showModal('Error loading audit logs. Please try again.', 'fail');
    }
}

function renderAuditsTable(audits) {
    const tableBody = document.getElementById('auditTableBody');
    const countSpan = document.getElementById('auditCount');
    const totalCountSpan = document.getElementById('totalCount');
    
    // Update counts
    if (countSpan) {
        countSpan.textContent = audits ? audits.length : 0;
    }
    if (totalCountSpan) {
        totalCountSpan.textContent = audits ? audits.length : 0;
    }
    
    if (!audits || audits.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="7" style="padding: 2rem; text-align: center; color: var(--text-muted);">
                    <i class="fas fa-inbox" style="font-size: 2rem; margin-bottom: 0.5rem;"></i>
                    <p>No audit logs found</p>
                </td>
            </tr>
        `;
        return;
    }
    
    tableBody.innerHTML = audits.map(audit => {
        const timestamp = new Date(audit.created_at).toLocaleString();
        const actionColor = getActionColor(audit.action);
        const statusColor = getStatusColor(audit.status);
        const statusDisplay = audit.status.charAt(0).toUpperCase() + audit.status.slice(1);
        const actionDisplay = audit.action.replace(/_/g, ' ').toUpperCase();
        
        return `
            <tr style="border-bottom: 1px solid var(--border-color); transition: background-color 0.2s;">
                <td style="padding: 1rem;">
                    <span style="display: inline-block; padding: 0.25rem 0.75rem; background: ${actionColor}20; color: ${actionColor}; border-radius: 4px; font-size: 0.85rem; font-weight: 600;">
                        ${actionDisplay}
                    </span>
                </td>
                <td style="padding: 1rem;">
                    <strong>${audit.entity}</strong>
                </td>
                <td style="padding: 1rem;">
                    <span style="color: ${statusColor}; font-weight: 600;">
                        <i class="fas fa-circle" style="font-size: 0.5rem; margin-right: 0.5rem;"></i>${statusDisplay}
                    </span>
                </td>
                <td style="padding: 1rem;">
                    <small>${audit.performed_by}</small>
                </td>
                <td style="padding: 1rem;">
                    <small>${audit.target_user || '-'}</small>
                </td>
                <td style="padding: 1rem;">
                    <small style="color: var(--text-muted);">${timestamp}</small>
                </td>
                <td style="padding: 1rem; text-align: center;">
                    <button class="btn btn-sm btn-primary" onclick="viewAuditDetail(${audit.id})" style="padding: 0.5rem 1rem; font-size: 0.85rem;">
                        <i class="fas fa-eye"></i> View
                    </button>
                </td>
            </tr>
        `;
    }).join('');
}

function getActionColor(action) {
    const colors = {
        'CREATE': '#28a745',
        'READ': '#17a2b8',
        'UPDATE': '#ffc107',
        'DELETE': '#dc3545',
        'LOGIN': '#007bff',
        'LOGOUT': '#6c757d',
        'CHANGE_PASSWORD': '#fd7e14',
        'TOGGLE_DELETE': '#dc3545',
    };
    return colors[action] || '#6c757d';
}

function getStatusColor(status) {
    const colors = {
        'SUCCESS': '#28a745',
        'FAILED': '#dc3545',
        'PENDING': '#ffc107',
    };
    return colors[status] || '#6c757d';
}

function searchAudits() {
    const searchTerm = document.getElementById('auditSearchInput').value.toLowerCase();
    
    const filtered = allAudits.filter(audit => 
        audit.action.toLowerCase().includes(searchTerm) ||
        audit.entity.toLowerCase().includes(searchTerm) ||
        audit.performed_by.toLowerCase().includes(searchTerm) ||
        (audit.target_user && audit.target_user.toLowerCase().includes(searchTerm)) ||
        (audit.description && audit.description.toLowerCase().includes(searchTerm))
    );
    
    renderAuditsTable(filtered);
}

function openDateFilterModal() {
    const existingModal = document.getElementById('dateFilterModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    const modal = document.createElement('div');
    modal.id = 'dateFilterModal';
    modal.className = 'modal active';
    
    modal.innerHTML = `
        <div class="modal-content" style="max-width: 500px;">
            <div class="modal-header">
                <h2>Filter Audit Logs by Date</h2>
                <button class="modal-close" id="closeDateFilterModal">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <form id="dateFilterForm">
                    <div class="form-group">
                        <label for="filterStartDate" style="display: block; margin-bottom: 0.5rem; font-weight: 500;">Start Date</label>
                        <input type="date" id="filterStartDate" name="start_date" class="form-control" 
                               value="${currentStartDate}"
                               style="padding: 0.75rem; border: 1px solid var(--border-color); border-radius: 8px; width: 100%;" required>
                    </div>
                    <div class="form-group" style="margin-top: 1rem;">
                        <label for="filterEndDate" style="display: block; margin-bottom: 0.5rem; font-weight: 500;">End Date</label>
                        <input type="date" id="filterEndDate" name="end_date" class="form-control" 
                               value="${currentEndDate}"
                               style="padding: 0.75rem; border: 1px solid var(--border-color); border-radius: 8px; width: 100%;" required>
                    </div>
                    <small style="color: var(--text-muted); display: block; margin-top: 0.5rem;">
                        <i class="fas fa-info-circle"></i> Select date range to view audit logs from that period
                    </small>
                </form>
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" id="cancelFilterBtn">Cancel</button>
                <button class="btn btn-primary" id="applyFilterBtn">
                    <i class="fas fa-filter"></i> Apply Filter
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    document.getElementById('closeDateFilterModal').addEventListener('click', closeDateFilterModal);
    document.getElementById('cancelFilterBtn').addEventListener('click', closeDateFilterModal);
    document.getElementById('applyFilterBtn').addEventListener('click', applyDateFilter);
}

function closeDateFilterModal() {
    const modal = document.getElementById('dateFilterModal');
    if (modal) {
        modal.classList.remove('active');
        setTimeout(() => modal.remove(), 300);
    }
}

async function applyDateFilter() {
    const startDate = document.getElementById('filterStartDate').value;
    const endDate = document.getElementById('filterEndDate').value;
    
    if (!startDate || !endDate) {
        showModal('Please select both start and end dates', 'fail');
        return;
    }
    
    if (new Date(endDate) < new Date(startDate)) {
        showModal('End date must be after start date', 'fail');
        return;
    }
    
    try {
        const button = document.getElementById('applyFilterBtn');
        button.disabled = true;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Filtering...';
        
        currentStartDate = startDate;
        currentEndDate = endDate;
        updateDateRangeDisplay();
        
        closeDateFilterModal();
        await loadAudits(startDate, endDate);
        
    } catch (error) {
        console.error('Error applying filter:', error);
        showModal('Error applying filter. Please try again.', 'fail');
    } finally {
        const button = document.getElementById('applyFilterBtn');
        if (button) {
            button.disabled = false;
            button.innerHTML = '<i class="fas fa-filter"></i> Apply Filter';
        }
    }
}

async function viewAuditDetail(auditId) {
    try {
        const response = await APIInterceptor.fetch(`${ADMIN_URL}audit/${auditId}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success && data.data) {
            const audit = data.data;
            showAuditDetailModal(audit);
        } else {
            showModal('Failed to load audit details', 'fail');
        }
    } catch (error) {
        console.error('Error loading audit detail:', error);
        showModal('Error loading audit details. Please try again.', 'fail');
    }
}

function showAuditDetailModal(audit) {
    const existingModal = document.getElementById('auditDetailModal');
    if (existingModal) {
        existingModal.remove();
    }
    
    const modal = document.createElement('div');
    modal.id = 'auditDetailModal';
    modal.className = 'modal active';
    
    const actionColor = getActionColor(audit.action);
    const statusColor = getStatusColor(audit.status);
    const oldValuesStr = audit.old_values ? JSON.stringify(audit.old_values, null, 2) : 'None';
    const newValuesStr = audit.new_values ? JSON.stringify(audit.new_values, null, 2) : 'None';
    
    modal.innerHTML = `
        <div class="modal-content" style="max-width: 800px; max-height: 90vh; overflow-y: auto;">
            <div class="modal-header">
                <h2>Audit Log Details</h2>
                <button class="modal-close" id="closeDetailModal">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="modal-body">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; margin-bottom: 1.5rem;">
                    <div>
                        <label style="font-weight: 600; color: var(--text-muted); font-size: 0.85rem;">Action</label>
                        <span style="display: inline-block; margin-top: 0.5rem; padding: 0.25rem 0.75rem; background: ${actionColor}20; color: ${actionColor}; border-radius: 4px; font-weight: 600;">
                            ${audit.action}
                        </span>
                    </div>
                    <div>
                        <label style="font-weight: 600; color: var(--text-muted); font-size: 0.85rem;">Entity</label>
                        <p style="margin-top: 0.5rem; font-weight: 500;">${audit.entity}</p>
                    </div>
                    <div>
                        <label style="font-weight: 600; color: var(--text-muted); font-size: 0.85rem;">Status</label>
                        <span style="margin-top: 0.5rem; color: ${statusColor}; font-weight: 600;">
                            <i class="fas fa-circle" style="font-size: 0.5rem; margin-right: 0.5rem;"></i>${audit.status}
                        </span>
                    </div>
                    <div>
                        <label style="font-weight: 600; color: var(--text-muted); font-size: 0.85rem;">Timestamp</label>
                        <p style="margin-top: 0.5rem; font-size: 0.9rem;">${new Date(audit.created_at).toLocaleString()}</p>
                    </div>
                    <div>
                        <label style="font-weight: 600; color: var(--text-muted); font-size: 0.85rem;">Performed By</label>
                        <p style="margin-top: 0.5rem; font-weight: 500;">${audit.performed_by}</p>
                    </div>
                    <div>
                        <label style="font-weight: 600; color: var(--text-muted); font-size: 0.85rem;">Target User</label>
                        <p style="margin-top: 0.5rem; font-weight: 500;">${audit.target_user || 'N/A'}</p>
                    </div>
                </div>
                
                ${audit.description ? `
                <div style="margin-bottom: 1.5rem;">
                    <label style="font-weight: 600; color: var(--text-muted); font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Description</label>
                    <p style="background: var(--card-bg); padding: 1rem; border-radius: 8px; border-left: 3px solid var(--primary);">${audit.description}</p>
                </div>
                ` : ''}
                
                ${audit.old_values ? `
                <div style="margin-bottom: 1.5rem;">
                    <label style="font-weight: 600; color: var(--text-muted); font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">Old Values</label>
                    <pre style="background: var(--card-bg); padding: 1rem; border-radius: 8px; overflow-x: auto; font-size: 0.85rem;">${oldValuesStr}</pre>
                </div>
                ` : ''}
                
                ${audit.new_values ? `
                <div>
                    <label style="font-weight: 600; color: var(--text-muted); font-size: 0.85rem; display: block; margin-bottom: 0.5rem;">New Values</label>
                    <pre style="background: var(--card-bg); padding: 1rem; border-radius: 8px; overflow-x: auto; font-size: 0.85rem;">${newValuesStr}</pre>
                </div>
                ` : ''}
            </div>
            <div class="modal-footer">
                <button class="btn btn-secondary" id="closeDetailBtn">Close</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    document.getElementById('closeDetailModal').addEventListener('click', closeAuditDetailModal);
    document.getElementById('closeDetailBtn').addEventListener('click', closeAuditDetailModal);
}

function closeAuditDetailModal() {
    const modal = document.getElementById('auditDetailModal');
    if (modal) {
        modal.classList.remove('active');
        setTimeout(() => modal.remove(), 300);
    }
}
