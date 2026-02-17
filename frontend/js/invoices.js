// Ensure main.js is loaded before running
let accessToken = null;
let allInvoices = [];
let allBookings = [];
let currentInvoiceId = null;
let pendingActionBookingId = null;
let pendingActionType = null;

if (typeof CookieManager === 'undefined') {
    console.error('CookieManager not found. Make sure main.js is loaded before invoices.js');
    window.location.href = "auth.html";
} else {
    accessToken = CookieManager.get("access_token");
    if (!accessToken) {
        window.location.href = "auth.html";
    }
}

document.addEventListener('DOMContentLoaded', function() {
    hidePreloader();
    loadBookings();
    loadInvoices();
    createConfirmationModal();
    setupConfirmationModalListeners();
    setupEventListeners();
});

function createConfirmationModal() {
    // Check if modal already exists
    if (document.getElementById('confirmationModalOverlay')) {
        return;
    }
    
    const modalHTML = `
        <div id="confirmationModalOverlay" class="modal-overlay" style="display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); z-index: 1000; align-items: center; justify-content: center;">
            <div class="confirmation-modal" style="background: white; border-radius: 8px; box-shadow: 0 4px 20px rgba(0,0,0,0.15); max-width: 400px; width: 90%; padding: 0; overflow: hidden;">
                <div style="padding: 24px; border-bottom: 1px solid #e0e0e0;">
                    <h2 id="confirmationTitle" style="margin: 0; font-size: 18px; color: #333; font-weight: 600;">Confirm Action</h2>
                </div>
                <div style="padding: 20px;">
                    <p id="confirmationMessage" style="margin: 0 0 20px 0; color: #666; font-size: 14px; line-height: 1.6;">Are you sure?</p>
                </div>
                <div style="padding: 16px 24px; border-top: 1px solid #e0e0e0; display: flex; gap: 10px; justify-content: flex-end;">
                    <button id="confirmationCancelBtn" class="btn" style="padding: 8px 16px; background: #f0f0f0; color: #333; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; font-weight: 500;">Cancel</button>
                    <button id="confirmationConfirmBtn" class="btn btn-primary" style="padding: 8px 16px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; font-weight: 500;">Confirm</button>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
}

function setupConfirmationModalListeners() {
    const overlay = document.getElementById('confirmationModalOverlay');
    const cancelBtn = document.getElementById('confirmationCancelBtn');
    const confirmBtn = document.getElementById('confirmationConfirmBtn');
    
    if (cancelBtn) {
        cancelBtn.addEventListener('click', closeConfirmationModal);
    }
    
    if (confirmBtn) {
        confirmBtn.addEventListener('click', async () => {
            await executeConfirmedAction();
            closeConfirmationModal();
        });
    }
    
    if (overlay) {
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                closeConfirmationModal();
            }
        });
    }
}

function showConfirmationModal(title, message, actionType, bookingId) {
    document.getElementById('confirmationTitle').textContent = title;
    document.getElementById('confirmationMessage').textContent = message;
    document.getElementById('confirmationModalOverlay').style.display = 'flex';
    
    pendingActionType = actionType;
    pendingActionBookingId = bookingId;
}

function closeConfirmationModal() {
    document.getElementById('confirmationModalOverlay').style.display = 'none';
    pendingActionType = null;
    pendingActionBookingId = null;
}

async function executeConfirmedAction() {
    if (pendingActionType === 'checkout') {
        await performCheckOut(pendingActionBookingId);
    } else if (pendingActionType === 'checkin') {
        await performCheckIn(pendingActionBookingId);
    }
}

function displayDefaultInvoices() {
    // Default data removed - fetching from backend
}

function setupEventListeners() {
    // Create button
    document.getElementById('createInvoiceBtn')?.addEventListener('click', openCreateModal);
    
    // Modal controls
    document.getElementById('closeInvoiceModal')?.addEventListener('click', closeInvoiceModal);
    document.getElementById('cancelInvoiceBtn')?.addEventListener('click', closeInvoiceModal);
    document.getElementById('saveInvoiceBtn')?.addEventListener('click', saveInvoice);
    
    // Details modal controls
    document.getElementById('closeDetailsModal')?.addEventListener('click', closeDetailsModal);
    
    // Search
    document.getElementById('invoiceSearchInput')?.addEventListener('keyup', searchInvoices);
}

async function loadBookings() {
    try {
        const response = await APIInterceptor.fetch(`${ADMIN_URL}booking/list/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        const data = await response.json();
        if (data.is_success && data.data) {
            allBookings = data.data;
            populateBookingSelect();
        }
    } catch (error) {
        console.error('Error loading bookings:', error);
    }
}

function populateBookingSelect() {
    const select = document.getElementById('bookingSelect');
    if (!select) return;
    
    const options = allBookings.map(booking => {
        const label = `${booking.confirmation_code} - ${booking.guest_name}${booking.is_deleted ? ' (Deleted)' : ''}`;
        return `<option value="${booking.id}" ${booking.is_deleted ? 'disabled' : ''}>${label}</option>`;
    }).join('');
    
    select.innerHTML = '<option value="">Select a booking</option>' + options;
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
            console.log('Invoices data:', data.data);
            allInvoices = data.data;
            displayInvoicesAsRows(data.data);
        } else {
            console.error('Failed to load invoices:', data.message);
        }
    } catch (error) {
        console.error('Error fetching invoices:', error);
    }
}

function displayInvoicesAsRows(invoices) {
    const container = document.getElementById('invoicesList');
    if (!container) return;
    
    if (invoices.length === 0) {
        container.style.display = 'flex';
        container.style.alignItems = 'center';
        container.style.justifyContent = 'center';
        container.style.minHeight = '400px';
        container.innerHTML = `
            <div style="text-align: center; color: var(--text-muted); padding: 3rem;">
                <i class="fas fa-file-invoice-dollar" style="font-size: 3rem; margin-bottom: 1rem; display: block; color: var(--text-muted);"></i>
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">No invoices found</p>
                <p style="margin-bottom: 1.5rem; color: var(--text-muted);">Create a new invoice to get started.</p>
                <button class="btn btn-primary" onclick="openCreateModal()"><i class="fas fa-plus" style="margin-right: 0.5rem;"></i>Create Invoice</button>
            </div>
        `;
        return;
    }
    
    container.style.display = 'grid';
    container.innerHTML = invoices.map(invoice => {
        // Determine checkout alert styling and message
        let checkoutAlert = '';
        if (invoice.checkout_status === 'TODAY') {
            checkoutAlert = `<div class="checkout-alert checkout-today" style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 0.5rem; margin-bottom: 0.5rem; border-radius: 4px;">
                <i class="fas fa-clock" style="color: #ffc107; margin-right: 0.5rem;"></i>
                <strong>Checkout Today!</strong> Guest checkout is due today.
            </div>`;
        } else if (invoice.checkout_status === 'OVERDUE') {
            checkoutAlert = `<div class="checkout-alert checkout-overdue" style="background-color: #f8d7da; border-left: 4px solid #dc3545; padding: 0.5rem; margin-bottom: 0.5rem; border-radius: 4px;">
                <i class="fas fa-exclamation-triangle" style="color: #dc3545; margin-right: 0.5rem;"></i>
                <strong>Checkout Overdue!</strong> Guest checkout date has passed. Please follow up.
            </div>`;
        }
        
        return `
        <div class="invoice-card" style="${invoice.is_deleted ? 'opacity: 0.6; border: 2px solid #ff6b6b;' : ''}">
            <div class="invoice-card-header">
                <div class="invoice-number">
                    <span class="number-label">${invoice.invoice_number || 'N/A'}${invoice.is_deleted ? ' <span style="color: #ff6b6b; font-size: 0.8em;">(Deleted)</span>' : ''}</span>
                </div>
                <div class="status-badge status-${invoice.payment_status?.toLowerCase()}">
                    <i class="fas fa-circle"></i>
                    ${invoice.payment_status?.charAt(0).toUpperCase() + invoice.payment_status?.slice(1).toLowerCase() || 'Pending'}
                </div>
                <div class="invoice-actions">
                    <button class="icon-btn" title="View Details" onclick="openDetailsModal(${invoice.id})" style="color: var(--primary-color);">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="icon-btn print-invoice-btn" title="Print" onclick="printInvoice(${invoice.id})">
                        <i class="fas fa-print"></i>
                    </button>
                    ${(invoice.checkout_status === 'TODAY' || invoice.checkout_status === 'OVERDUE') && invoice.booking_status !== 'CHECKED_OUT' && invoice.booking_status !== 'CANCELLED' && invoice.payment_status === 'COMPLETED' ? `
                    <button class="icon-btn checkout-btn" title="Check Out Guest" onclick="checkOutGuest(${invoice.booking})" style="color: #28a745;">
                        <i class="fas fa-sign-out-alt"></i>
                    </button>
                    ` : ''}
                    ${invoice.payment_status === 'COMPLETED' && invoice.check_in && invoice.check_out && 
                      new Date(invoice.check_in) <= new Date(invoice.today) && 
                      new Date(invoice.today) <= new Date(invoice.check_out) ? `
                    <button class="icon-btn check-in-btn" title="Check In Guest" onclick="checkInGuest(${invoice.booking})">
                        <i class="fas fa-door-open"></i>
                    </button>
                    ` : ''}
                </div>
            </div>
            ${checkoutAlert}
            <div class="invoice-card-body">
                <div class="invoice-info">
                    <span class="info-label">Guest:</span>
                    <span class="info-value">${invoice.guest_name || 'N/A'}</span>
                </div>
                <div class="invoice-info">
                    <span class="info-label">Booking:</span>
                    <span class="info-value">${invoice.booking_confirmation || 'N/A'}</span>
                </div>
                <div class="invoice-dates">
                    <div class="date-item">
                        <span class="date-label">Check-in:</span>
                        <span class="date-value">${invoice.check_in ? new Date(invoice.check_in).toLocaleDateString() : 'N/A'}</span>
                    </div>
                    <div class="date-item">
                        <span class="date-label">Check-out:</span>
                        <span class="date-value">${invoice.check_out ? new Date(invoice.check_out).toLocaleDateString() : 'N/A'}</span>
                    </div>
                </div>
                <div class="invoice-amount">
                    <span class="amount-label">Total:</span>
                    <span class="amount-value">₦${parseFloat(invoice.total).toLocaleString()}</span>
                </div>
            </div>
        </div>
    `}).join('');
}

function openCreateModal() {
    currentInvoiceId = null;
    document.getElementById('modalTitle').textContent = 'Create New Invoice';
    document.getElementById('invoiceForm').reset();
    document.getElementById('invoiceModal').classList.add('active');
}

function closeInvoiceModal() {
    document.getElementById('invoiceModal').classList.remove('active');
    currentInvoiceId = null;
}

async function saveInvoice() {
    const bookingId = document.getElementById('bookingSelect').value;
    const notes = document.getElementById('notes').value;
    
    if (!bookingId) {
        showModal('Please select a booking.', 'fail');
        return;
    }
    
    const payload = {
        booking: parseInt(bookingId),
        notes: notes || ''
    };
    
    try {
        // Create new invoice
        const response = await APIInterceptor.fetch(`${ADMIN_URL}invoice/create/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify(payload)
        });
        
        const data = await response.json();
        
        if (data.is_success || response.ok) {
            showModal('Invoice created successfully!', 'success');
            closeInvoiceModal();
            loadInvoices();
        } else {
            showModal(data.message || 'Failed to save invoice.', 'fail');
        }
    } catch (error) {
        console.error('Error saving invoice:', error);
        showModal('Error saving invoice. Please try again.', 'fail');
    }
}

function openDetailsModal(invoiceId) {
    const invoice = allInvoices.find(inv => inv.id === invoiceId);
    if (!invoice) return;
    
    // Populate basic info
    document.getElementById('detailsInvoiceNumber').textContent = invoice.invoice_number || 'N/A';
    document.getElementById('detailsGuestName').textContent = invoice.guest_name || 'N/A';
    document.getElementById('detailsBookingConfirmation').textContent = invoice.booking_confirmation || 'N/A';
    
    // Populate dates
    document.getElementById('detailsCheckIn').textContent = invoice.check_in ? new Date(invoice.check_in).toLocaleDateString() : 'N/A';
    document.getElementById('detailsCheckOut').textContent = invoice.check_out ? new Date(invoice.check_out).toLocaleDateString() : 'N/A';
    document.getElementById('detailsNights').textContent = invoice.nights || 'N/A';
    document.getElementById('detailsDueDate').textContent = invoice.due_date ? new Date(invoice.due_date).toLocaleDateString() : 'N/A';
    
    // Populate amounts
    document.getElementById('detailsSubtotal').textContent = `₦${parseFloat(invoice.subtotal).toLocaleString()}`;
    document.getElementById('detailsDiscount').textContent = `₦${parseFloat(invoice.discount_amount || 0).toLocaleString()}`;
    document.getElementById('detailsTax').textContent = `₦${parseFloat(invoice.tax || 0).toLocaleString()}`;
    document.getElementById('detailsTotal').textContent = `₦${parseFloat(invoice.total).toLocaleString()}`;
    
    // Populate status and payment info
    document.getElementById('detailsPaymentStatus').textContent = invoice.payment_status?.charAt(0).toUpperCase() + invoice.payment_status?.slice(1).toLowerCase() || 'N/A';
    
    // Populate payment date if available
    const paymentDateElement = document.getElementById('detailsPaymentDate');
    const paymentSection = document.getElementById('paymentDateSection');
    if (invoice.payment_date) {
        paymentDateElement.textContent = new Date(invoice.payment_date).toLocaleDateString();
        paymentSection.style.display = 'block';
    } else {
        paymentSection.style.display = 'none';
    }
    
    // Populate notes if available
    const notesElement = document.getElementById('detailsNotes');
    const notesSection = document.getElementById('notesSection');
    if (invoice.notes) {
        notesElement.textContent = invoice.notes;
        notesSection.style.display = 'block';
    } else {
        notesSection.style.display = 'none';
    }
    
    document.getElementById('detailsInvoiceModal').classList.add('active');
}

function closeDetailsModal() {
    document.getElementById('detailsInvoiceModal').classList.remove('active');
}

async function checkOutGuest(bookingId) {
    showConfirmationModal(
        '🚪 Check Out Guest',
        'Are you sure you want to check out this guest? The room will become available.',
        'checkout',
        bookingId
    );
}

async function performCheckOut(bookingId) {
    try {
        const response = await APIInterceptor.fetch(`${ADMIN_URL}booking/${bookingId}/check-out/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success || response.ok) {
            showModal('✓ Guest checked out successfully! Room is now available.', 'success');
            loadInvoices();
        } else {
            showModal(data.message || 'Failed to check out guest.', 'fail');
        }
    } catch (error) {
        console.error('Error checking out guest:', error);
        showModal('Error checking out guest. Please try again.', 'fail');
    }
}

function printInvoice(invoiceId) {
    const invoice = allInvoices.find(i => i.id === invoiceId);
    if (!invoice) return;
    
    // Create printable invoice HTML
    const printWindow = window.open('', '', 'height=800,width=900');
    const printContent = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Invoice ${invoice.invoice_number}</title>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                body {
                    font-family: 'Arial', sans-serif;
                    color: #333;
                    line-height: 1.6;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }
                .header {
                    display: flex;
                    justify-content: space-between;
                    align-items: flex-start;
                    border-bottom: 2px solid #333;
                    padding-bottom: 20px;
                    margin-bottom: 20px;
                }
                .company-info h1 {
                    font-size: 24px;
                    margin-bottom: 5px;
                }
                .company-info p {
                    font-size: 12px;
                    color: #666;
                }
                .invoice-title {
                    text-align: right;
                }
                .invoice-title h2 {
                    font-size: 28px;
                    color: #667eea;
                    margin-bottom: 5px;
                }
                .invoice-title p {
                    font-size: 12px;
                    color: #666;
                }
                .invoice-details {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 30px;
                    margin-bottom: 30px;
                    padding: 20px;
                    background: #f9f9f9;
                    border-radius: 8px;
                }
                .detail-section h3 {
                    font-size: 12px;
                    font-weight: bold;
                    color: #667eea;
                    margin-bottom: 8px;
                    text-transform: uppercase;
                }
                .detail-section p {
                    font-size: 13px;
                    margin-bottom: 5px;
                }
                .detail-section p span {
                    font-weight: bold;
                }
                .line-separator {
                    border-top: 1px solid #ddd;
                    margin: 20px 0;
                }
                .amounts-table {
                    width: 100%;
                    margin: 20px 0;
                    border-collapse: collapse;
                }
                .amounts-table tr {
                    border-bottom: 1px solid #eee;
                }
                .amounts-table td {
                    padding: 12px;
                    font-size: 13px;
                }
                .amounts-table td:first-child {
                    text-align: left;
                    font-weight: 500;
                    width: 60%;
                }
                .amounts-table td:last-child {
                    text-align: right;
                    font-weight: 600;
                }
                .amounts-table tr.total td {
                    background: #f0f0f0;
                    font-size: 14px;
                    font-weight: bold;
                    border-top: 2px solid #333;
                }
                .status-info {
                    padding: 15px;
                    background: #f0f7ff;
                    border-left: 4px solid #667eea;
                    margin: 20px 0;
                    border-radius: 4px;
                }
                .status-info p {
                    font-size: 13px;
                    margin: 5px 0;
                }
                .status-label {
                    font-weight: bold;
                    color: #667eea;
                }
                .dates-grid {
                    display: grid;
                    grid-template-columns: 1fr 1fr 1fr;
                    gap: 15px;
                    margin: 20px 0;
                }
                .date-box {
                    padding: 12px;
                    background: #f5f5f5;
                    border-radius: 4px;
                    text-align: center;
                }
                .date-box p:first-child {
                    font-size: 11px;
                    color: #666;
                    text-transform: uppercase;
                    margin-bottom: 5px;
                }
                .date-box p:last-child {
                    font-size: 14px;
                    font-weight: bold;
                    color: #333;
                }
                .notes-section {
                    margin-top: 20px;
                    padding: 15px;
                    background: #fffef0;
                    border-left: 4px solid #f39c12;
                    border-radius: 4px;
                }
                .notes-section h4 {
                    font-size: 12px;
                    color: #f39c12;
                    margin-bottom: 8px;
                    text-transform: uppercase;
                }
                .notes-section p {
                    font-size: 13px;
                    color: #333;
                }
                .footer {
                    text-align: center;
                    margin-top: 40px;
                    padding-top: 20px;
                    border-top: 1px solid #ddd;
                    font-size: 11px;
                    color: #999;
                }
                .thank-you {
                    text-align: center;
                    margin: 20px 0;
                    font-size: 14px;
                    font-weight: bold;
                    color: #667eea;
                }
                @media print {
                    body {
                        margin: 0;
                        padding: 0;
                    }
                    .container {
                        max-width: 100%;
                        padding: 10px;
                    }
                }
                @media (max-width: 600px) {
                    .invoice-details {
                        grid-template-columns: 1fr;
                    }
                    .dates-grid {
                        grid-template-columns: 1fr;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="company-info">
                        <h1>HotelOS</h1>
                        <p>Hotel Management System</p>
                        <p>Email: info@hotelosystem.com</p>
                        <p>Phone: +234 123 456 7890</p>
                    </div>
                    <div class="invoice-title">
                        <h2>${invoice.invoice_number || 'N/A'}</h2>
                        <p>Invoice</p>
                        <p style="margin-top: 10px;">Generated: ${new Date().toLocaleDateString()}</p>
                    </div>
                </div>
                
                <div class="invoice-details">
                    <div class="detail-section">
                        <h3>Guest Information</h3>
                        <p><span>Name:</span> ${invoice.guest_name || 'N/A'}</p>
                        <p><span>Booking Code:</span> ${invoice.booking_confirmation || 'N/A'}</p>
                        <p><span>Number of Guests:</span> ${invoice.number_of_guests || 'N/A'}</p>
                    </div>
                    <div class="detail-section">
                        <h3>Room Information</h3>
                        <p><span>Room:</span> ${invoice.room || 'N/A'}</p>
                        <p><span>Room Type:</span> ${invoice.room_type || 'N/A'}</p>
                        <p><span>Total Nights:</span> ${invoice.nights || 'N/A'}</p>
                    </div>
                </div>
                
                <div class="dates-grid">
                    <div class="date-box">
                        <p>Check-in</p>
                        <p>${invoice.check_in ? new Date(invoice.check_in).toLocaleDateString() : 'N/A'}</p>
                    </div>
                    <div class="date-box">
                        <p>Check-out</p>
                        <p>${invoice.check_out ? new Date(invoice.check_out).toLocaleDateString() : 'N/A'}</p>
                    </div>
                    <div class="date-box">
                        <p>Due Date</p>
                        <p>${invoice.due_date ? new Date(invoice.due_date).toLocaleDateString() : 'N/A'}</p>
                    </div>
                </div>
                
                <div class="line-separator"></div>
                
                <table class="amounts-table">
                    <tr>
                        <td>Subtotal</td>
                        <td>₦${parseFloat(invoice.subtotal).toLocaleString()}</td>
                    </tr>
                    ${invoice.discount_amount > 0 ? `
                    <tr>
                        <td>Discount</td>
                        <td>-₦${parseFloat(invoice.discount_amount).toLocaleString()}</td>
                    </tr>
                    ` : ''}
                    ${invoice.tax > 0 ? `
                    <tr>
                        <td>Tax</td>
                        <td>₦${parseFloat(invoice.tax).toLocaleString()}</td>
                    </tr>
                    ` : ''}
                    <tr class="total">
                        <td>TOTAL AMOUNT</td>
                        <td>₦${parseFloat(invoice.total).toLocaleString()}</td>
                    </tr>
                </table>
                
                <div class="status-info">
                    <p><span class="status-label">Payment Status:</span> ${invoice.payment_status?.toUpperCase() || 'PENDING'}</p>
                    ${invoice.payment_date ? `<p><span class="status-label">Payment Date:</span> ${new Date(invoice.payment_date).toLocaleDateString()}</p>` : ''}
                </div>
                
                ${invoice.notes ? `
                <div class="notes-section">
                    <h4>Additional Notes</h4>
                    <p>${invoice.notes}</p>
                </div>
                ` : ''}
                
                <div class="thank-you">
                    Thank you for your stay!
                </div>
                
                <div class="footer">
                    <p>This is an automatically generated invoice. For inquiries, please contact our billing department.</p>
                    <p>Invoice ID: ${invoice.id} | Generated: ${new Date().toLocaleString()}</p>
                </div>
            </div>
        </body>
        </html>
    `;
    
    printWindow.document.write(printContent);
    printWindow.document.close();
    
    // Wait for content to load then print
    setTimeout(() => {
        printWindow.print();
    }, 250);
}

function searchInvoices(e) {
    const searchTerm = e.target.value.toLowerCase();
    
    if (!searchTerm) {
        displayInvoicesAsRows(allInvoices);
        return;
    }
    
    const filteredInvoices = allInvoices.filter(invoice => 
        invoice.invoice_number?.toLowerCase().includes(searchTerm) ||
        invoice.guest_name?.toLowerCase().includes(searchTerm) ||
        invoice.booking_confirmation?.toLowerCase().includes(searchTerm) ||
        invoice.payment_status?.toLowerCase().includes(searchTerm)
    );
    
    displayInvoicesAsRows(filteredInvoices);
}

async function checkInGuest(bookingId) {
    if (!bookingId) {
        showModal('Booking not found', 'fail');
        return;
    }
    
    showConfirmationModal(
        '🚪 Check In Guest',
        'Are you sure you want to check in this guest? The room will be marked as occupied.',
        'checkin',
        bookingId
    );
}

async function performCheckIn(bookingId) {
    try {        
        const response = await APIInterceptor.fetch(`${ADMIN_URL}booking/${bookingId}/check-in/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success) {
            showModal('✓ Guest checked in successfully!', 'success');
            loadInvoices();  // Refresh the list
        } else {
            showModal(data.message || 'Failed to check in guest.', 'fail');
        }
    } catch (error) {
        console.error('Error checking in guest:', error);
        showModal('Error processing check-in. Please try again.', 'fail');
    }
}
