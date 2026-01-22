// Ensure main.js is loaded before running
let accessToken = null;
let allInvoices = [];
let allBookings = [];
let currentInvoiceId = null;

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
    setupEventListeners();
});

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
    
    container.innerHTML = invoices.map(invoice => `
        <div class="invoice-row" ${invoice.is_deleted ? 'style="opacity: 0.6; border: 2px solid #ff6b6b;"' : ''}>
            <div class="invoice-info">
                <div class="invoice-number-section">
                    <i class="fas fa-file-invoice"></i>
                    <div class="invoice-details">
                        <h3 class="invoice-number">
                            ${invoice.invoice_number || 'N/A'}
                            ${invoice.is_deleted ? '<span style="color: red; font-size: 0.8rem; margin-left: 0.5rem;">(Deleted)</span>' : ''}
                        </h3>
                        <p class="invoice-guest">${invoice.guest_name || 'N/A'}</p>
                    </div>
                </div>
                <div class="invoice-booking">
                    <span class="booking-code">${invoice.booking_confirmation || 'N/A'}</span>
                </div>
                <div class="invoice-amounts">
                    <div class="amount-item">
                        <span class="amount-label">Subtotal:</span>
                        <span class="amount-value">₦${parseFloat(invoice.subtotal).toLocaleString()}</span>
                    </div>
                    ${invoice.discount_amount > 0 ? `
                    <div class="amount-item">
                        <span class="amount-label">Discount:</span>
                        <span class="amount-value">₦${parseFloat(invoice.discount_amount).toLocaleString()}</span>
                    </div>
                    ` : ''}
                    ${invoice.tax > 0 ? `
                    <div class="amount-item">
                        <span class="amount-label">Tax:</span>
                        <span class="amount-value">₦${parseFloat(invoice.tax).toLocaleString()}</span>
                    </div>
                    ` : ''}
                    <div class="amount-item" style="font-weight: bold;">
                        <span class="amount-label">Total:</span>
                        <span class="amount-value">₦${parseFloat(invoice.total).toLocaleString()}</span>
                    </div>
                </div>
                ${invoice.notes ? `
                <div class="invoice-notes">
                    <span class="notes-label">Notes:</span>
                    <span class="notes-value">${invoice.notes}</span>
                </div>
                ` : ''}
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
                <div class="date-item">
                    <span class="date-label">Nights:</span>
                    <span class="date-value">${invoice.nights || 'N/A'}</span>
                </div>
                <div class="date-item">
                    <span class="date-label">Due:</span>
                    <span class="date-value">${invoice.due_date ? new Date(invoice.due_date).toLocaleDateString() : 'N/A'}</span>
                </div>
                ${invoice.payment_date ? `
                <div class="date-item">
                    <span class="date-label">Paid:</span>
                    <span class="date-value">${new Date(invoice.payment_date).toLocaleDateString()}</span>
                </div>
                ` : ''}
                <div class="date-item">
                    <span class="date-label">Created:</span>
                    <span class="date-value">${humanizeDate(invoice.created_at)}</span>
                </div>
            </div>
            <div class="invoice-status-section">
                <span class="status-badge status-${invoice.payment_status?.toLowerCase()}">
                    <i class="fas fa-circle"></i>
                    ${invoice.payment_status?.charAt(0).toUpperCase() + invoice.payment_status?.slice(1).toLowerCase() || 'Pending'}
                </span>
            </div>
            <div class="invoice-actions">
                <button class="icon-btn print-invoice-btn" title="Print" onclick="printInvoice(${invoice.id})">
                    <i class="fas fa-print"></i>
                </button>
            </div>
        </div>
    `).join('');
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
