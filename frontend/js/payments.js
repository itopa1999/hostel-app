// Ensure main.js is loaded before running
let accessToken = null;
let allPayments = [];
let currentPaymentId = null;
let userRole = null;
let isAdmin = false;

if (typeof CookieManager === 'undefined') {
    console.error('CookieManager not found. Make sure main.js is loaded before payments.js');
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
    loadPayments();
    loadInvoices();
    setupEventListeners();
});

function setupEventListeners() {
    // Create button
    document.getElementById('createPaymentBtn')?.addEventListener('click', openCreateModal);
    
    // Modal controls
    document.getElementById('closePaymentModal')?.addEventListener('click', closePaymentModal);
    document.getElementById('cancelPaymentBtn')?.addEventListener('click', closePaymentModal);
    document.getElementById('savePaymentBtn')?.addEventListener('click', savePayment);
    
    // Delete modal controls
    document.getElementById('closeDeleteModal')?.addEventListener('click', closeDeleteModal);
    document.getElementById('cancelDeleteBtn')?.addEventListener('click', closeDeleteModal);
    document.getElementById('confirmDeleteBtn')?.addEventListener('click', confirmDelete);
    
    // Search
    document.getElementById('paymentSearchInput')?.addEventListener('keyup', searchPayments);
}

async function loadInvoices() {
    try {        
        const response = await APIInterceptor.fetch(`${ADMIN_URL}invoice/list/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        if (data.is_success && data.data) {
            populateInvoiceSelect(data.data);
        }
    } catch (error) {
        console.error('Error fetching invoices:', error);
    }
}

function populateInvoiceSelect(invoices) {
    const select = document.getElementById('invoiceSelect');
    if (!select) return;
    
    const options = invoices.map(invoice => {
        const label = `Invoice #${invoice.invoice_number} - ${invoice.guest_name || 'N/A'}${invoice.is_deleted ? ' (Deleted)' : ''}`;
        return `<option value="${invoice.id}" ${invoice.is_deleted ? 'disabled' : ''}>${label}</option>`;
    }).join('');
    
    select.innerHTML = '<option value="">Select an invoice</option>' + options;
}

async function loadPayments() {
    try {        
        const response = await APIInterceptor.fetch(`${ADMIN_URL}payment/list/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success && data.data) {
            console.log('Payments data:', data.data);
            allPayments = data.data;
            displayPaymentsAsCards(data.data);
        } else {
            console.error('Failed to load payments:', data.message);
            showModal('Failed to load payments. Please refresh the page.', 'fail');
        }
    } catch (error) {
        console.error('Error fetching payments:', error);
        showModal('Error loading payments. Please check your connection.', 'fail');
    }
}

function displayPaymentsAsCards(payments) {
    const container = document.getElementById('paymentsContainer');
    if (!container) return;
    
    if (payments.length === 0) {
        container.style.display = 'flex';
        container.style.alignItems = 'center';
        container.style.justifyContent = 'center';
        container.style.minHeight = '400px';
        container.innerHTML = `
            <div style="text-align: center; color: var(--text-muted); padding: 3rem;">
                <i class="fas fa-credit-card" style="font-size: 3rem; margin-bottom: 1rem; display: block; color: var(--text-muted);"></i>
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">No payments found</p>
                <p style="margin-bottom: 1.5rem; color: var(--text-muted);">Create a new payment to get started.</p>
                <button class="btn btn-primary" onclick="openCreateModal()"><i class="fas fa-plus" style="margin-right: 0.5rem;"></i>Create Payment</button>
            </div>
        `;
        return;
    }
    
    container.innerHTML = payments.map(payment => `
        <div class="payment-card" style="${payment.is_deleted ? 'opacity: 0.6; border: 2px solid #ff6b6b;' : ''}">
            <div class="payment-header">
                <div class="payment-info">
                    <div class="payment-invoice-number">Invoice #${payment.invoice_number || 'N/A'}</div>
                    <div class="payment-booking-code">${payment.booking_confirmation || 'N/A'}</div>
                </div>
                <div style="display: flex; gap: 0.75rem; align-items: center;">
                    ${payment.is_deleted ? '<span style="color: #ff6b6b; font-size: 0.8em; font-weight: 600;">(Deleted)</span>' : ''}
                    <span class="payment-status-badge status-${payment.payment_status?.toLowerCase()}">
                        ${payment.payment_status?.charAt(0).toUpperCase() + payment.payment_status?.slice(1).toLowerCase() || 'Pending'}
                    </span>
                </div>
            </div>
            
            <div class="payment-amount">₦${parseFloat(payment.amount).toLocaleString()}</div>
            
            <div class="payment-details">
                <div class="detail-row">
                    <span class="label">Method:</span>
                    <span class="value">${payment.method || 'N/A'}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Transaction ID:</span>
                    <span class="value">${payment.transaction_id || 'N/A'}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Receipt Number:</span>
                    <span class="value">${payment.receipt_number || 'N/A'}</span>
                </div>
                ${payment.reference ? `
                <div class="detail-row">
                    <span class="label">Reference:</span>
                    <span class="value">${payment.reference}</span>
                </div>
                ` : ''}
                ${payment.refund_amount > 0 ? `
                <div class="detail-row">
                    <span class="label">Refund Amount:</span>
                    <span class="value" style="color: #ff6b6b;">₦${parseFloat(payment.refund_amount).toLocaleString()}</span>
                </div>
                <div class="detail-row">
                    <span class="label">Refund Date:</span>
                    <span class="value">${payment.refund_date ? new Date(payment.refund_date).toLocaleDateString() : 'N/A'}</span>
                </div>
                ` : ''}
                <div class="detail-row">
                    <span class="label">Created:</span>
                    <span class="value">${humanizeDate(payment.created_at)}</span>
                </div>
            </div>
            
            ${payment.notes ? `
            <div class="payment-notes">
                <span class="notes-label">Notes</span>
                <span class="notes-value">${payment.notes}</span>
            </div>
            ` : ''}
            
            <div class="payment-actions">
                <button class="icon-btn edit-payment-btn" title="Edit" onclick="openEditModal(${payment.id})" ${payment.is_deleted ? 'disabled style="opacity: 0.5; cursor: not-allowed;"' : ''}>
                    <i class="fas fa-edit"></i>
                </button>
                ${isAdmin ? `
                <button class="icon-btn ${payment.is_deleted ? 'reactivate-payment-btn' : 'delete-payment-btn'}" title="${payment.is_deleted ? 'Reactivate' : 'Delete'}" onclick="openDeleteModal(${payment.id})">
                    <i class="fas fa-${payment.is_deleted ? 'undo' : 'trash'}"></i>
                </button>
                ` : ''}
            </div>
        </div>
    `).join('');
}

function getPaymentStatusClass(status) {
    switch(status) {
        case 'COMPLETED':
            return 'completed';
        case 'PENDING':
            return 'pending';
        case 'FAILED':
            return 'failed';
        default:
            return 'pending';
    }
}

function openCreateModal() {
    currentPaymentId = null;
    document.getElementById('modalTitle').textContent = 'Create New Payment';
    document.getElementById('paymentForm').reset();
    
    // Show invoice select, hide status field
    const invoiceGroup = document.getElementById('invoiceSelect')?.closest('div');
    const statusGroup = document.getElementById('statusGroup');
    if (invoiceGroup) invoiceGroup.style.display = 'block';
    if (statusGroup) statusGroup.style.display = 'none';
    
    document.getElementById('paymentModal').classList.add('active');
}

function openEditModal(paymentId) {
    const payment = allPayments.find(p => p.id === paymentId);
    if (!payment) return;
    
    currentPaymentId = paymentId;
    document.getElementById('modalTitle').textContent = 'Update Payment Status';
    
    // Hide invoice select, show status field
    const invoiceGroup = document.getElementById('invoiceSelect')?.closest('div');
    const statusGroup = document.getElementById('statusGroup');
    if (invoiceGroup) invoiceGroup.style.display = 'none';
    if (statusGroup) statusGroup.style.display = 'block';
    
    document.getElementById('paymentStatus').value = payment.payment_status || 'PENDING';
    
    document.getElementById('paymentModal').classList.add('active');
}

function closePaymentModal() {
    document.getElementById('paymentModal').classList.remove('active');
    currentPaymentId = null;
}

function openDeleteModal(paymentId) {
    const payment = allPayments.find(p => p.id === paymentId);
    if (!payment) return;
    
    currentPaymentId = paymentId;
    if (payment.is_deleted) {
        document.getElementById('deleteMessage').textContent = `Are you sure you want to reactivate payment for invoice "${payment.invoice_number}"? It will be available again.`;
        document.getElementById('confirmDeleteBtn').textContent = 'Reactivate';
    } else {
        document.getElementById('deleteMessage').textContent = `Are you sure you want to delete payment for invoice "${payment.invoice_number}"? You can reactivate it later.`;
        document.getElementById('confirmDeleteBtn').textContent = 'Delete';
    }
    document.getElementById('deletePaymentModal').classList.add('active');
}

function closeDeleteModal() {
    document.getElementById('deletePaymentModal').classList.remove('active');
    currentPaymentId = null;
}

async function savePayment() {
    const invoiceId = document.getElementById('invoiceSelect').value;
    const paymentStatus = document.getElementById('paymentStatus').value;
    
    // Validate based on operation type
    if (!currentPaymentId) {
        // Creating - require invoiceId
        if (!invoiceId) {
            showModal('Please select an invoice.', 'fail');
            return;
        }
    } else {
        // Updating - require paymentStatus
        if (!paymentStatus) {
            showModal('Please select a payment status.', 'fail');
            return;
        }
    }
    
    try {
        let response;
        if (currentPaymentId) {
            // Update existing payment - only status
            const payload = {
                payment_status: paymentStatus
            };
            
            response = await APIInterceptor.fetch(`${ADMIN_URL}payment/${currentPaymentId}/update-status/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                },
                body: JSON.stringify(payload)
            });
        } else {
            // Create new payment - only invoice
            const payload = {
                invoice: parseInt(invoiceId)
            };
            
            response = await APIInterceptor.fetch(`${ADMIN_URL}payment/create/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                },
                body: JSON.stringify(payload)
            });
        }
        
        const data = await response.json();
        
        if (data.is_success || response.ok) {
            showModal(currentPaymentId ? 'Payment updated successfully!' : 'Payment created successfully!', 'success');
            closePaymentModal();
            loadPayments();
        } else {
            showModal(data.message || 'Failed to save payment.', 'fail');
        }
    } catch (error) {
        console.error('Error saving payment:', error);
        showModal('Error saving payment. Please try again.', 'fail');
    }
}

async function confirmDelete() {
    if (!currentPaymentId) return;
    
    try {
        const response = await APIInterceptor.fetch(`${ADMIN_URL}payment/${currentPaymentId}/delete/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success || response.ok) {
            const payment = allPayments.find(p => p.id === currentPaymentId);
            const message = payment.is_deleted ? 'Payment reactivated successfully!' : 'Payment deleted successfully!';
            showModal(message, 'success');
            closeDeleteModal();
            loadPayments();
        } else {
            showModal(data.message || 'Failed to delete payment.', 'fail');
        }
    } catch (error) {
        console.error('Error deleting payment:', error);
        showModal('Error deleting payment. Please try again.', 'fail');
    }
}

function searchPayments(e) {
    const searchTerm = e.target.value.toLowerCase();
    
    if (!searchTerm) {
        displayPaymentsAsCards(allPayments);
        return;
    }
    
    const filteredPayments = allPayments.filter(payment => 
        payment.invoice_number?.toLowerCase().includes(searchTerm) ||
        payment.booking_confirmation?.toLowerCase().includes(searchTerm) ||
        payment.transaction_id?.toLowerCase().includes(searchTerm) ||
        payment.receipt_number?.toLowerCase().includes(searchTerm) ||
        payment.payment_status?.toLowerCase().includes(searchTerm) ||
        payment.method?.toLowerCase().includes(searchTerm)
    );
    
    displayPaymentsAsCards(filteredPayments);
}
