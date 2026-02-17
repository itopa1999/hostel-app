// Ensure main.js is loaded before running
let accessToken = null;

if (typeof CookieManager === 'undefined') {
    console.error('CookieManager not found. Make sure main.js is loaded before reports.js');
    window.location.href = "auth.html";
} else {
    accessToken = CookieManager.get("access_token");
    if (!accessToken) {
        window.location.href = "auth.html";
    }
}

document.addEventListener('DOMContentLoaded', function() {
    hidePreloader();
    initializeReportPage();
    
    // Check if report generator should be opened from dashboard quick action
    if (sessionStorage.getItem('openReportModal') === 'true') {
        sessionStorage.removeItem('openReportModal');
        // Scroll to the report section or focus on date input
        setTimeout(() => {
            const reportDate = document.getElementById('reportDate');
            if (reportDate) {
                reportDate.focus();
                reportDate.scrollIntoView({ behavior: 'smooth' });
            }
        }, 300);
    }
});

function initializeReportPage() {
    // Set today's date as default
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('reportDate').value = today;
}

function getSelectedDate() {
    const dateInput = document.getElementById('reportDate').value;
    return dateInput ? dateInput : new Date().toISOString().split('T')[0];
}

function formatCurrency(value) {
    return parseFloat(value).toLocaleString('en-NG', {
        style: 'currency',
        currency: 'NGN',
        minimumFractionDigits: 2
    });
}

function formatPercentage(value) {
    return parseFloat(value).toFixed(2) + '%';
}

// Occupancy Report
async function generateAndDisplayOccupancyReport() {
    const date = getSelectedDate();
    
    try {        
        const response = await APIInterceptor.fetch(`${ADMIN_URL}reports/occupancy/?date=${date}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success && data.data) {
            displayOccupancyReport(data.data);
            showModal('Occupancy Report generated successfully!', 'success');
        } else {
            showModal(data.message || 'Failed to generate report.', 'fail');
        }
    } catch (error) {
        console.error('Error generating occupancy report:', error);
        showModal('Error generating report. Please try again.', 'fail');
    }
}

function displayOccupancyReport(report) {
    const output = document.getElementById('reportOutput');
    
    let roomTypesHTML = '';
    if (report.room_types_breakdown && report.room_types_breakdown.length > 0) {
        roomTypesHTML = report.room_types_breakdown.map(rt => `
            <div class="breakdown-container">
                <div class="breakdown-header">
                    <div>
                        <p class="breakdown-title">${rt.room_type}</p>
                        <p class="breakdown-subtitle">Total: ${rt.total} | Occupied: ${rt.occupied} | Available: ${rt.available}</p>
                    </div>
                    <span class="badge checked-in">${formatPercentage(rt.occupancy_rate)}</span>
                </div>
            </div>
        `).join('');
    }
    
    output.innerHTML = `
        <div class="report-output-container">
            <h3 class="report-title">📊 Occupancy Report</h3>
            <p class="report-date-text">Report Date: <strong>${report.report_date}</strong></p>
            
            <div class="report-cards-grid">
                <div class="report-card">
                    <p class="report-card-label">Total Rooms</p>
                    <p class="report-card-value">${report.total_rooms}</p>
                </div>
                <div class="report-card">
                    <p class="report-card-label">Occupied</p>
                    <p class="report-card-value occupied">${report.occupied_rooms}</p>
                </div>
                <div class="report-card">
                    <p class="report-card-label">Available</p>
                    <p class="report-card-value available">${report.available_rooms}</p>
                </div>
                <div class="report-card">
                    <p class="report-card-label">Occupancy Rate</p>
                    <p class="report-card-value success">${formatPercentage(report.occupancy_rate)}</p>
                </div>
            </div>
            
            ${roomTypesHTML ? `
                <h4 class="report-section-header">Room Type Breakdown</h4>
                ${roomTypesHTML}
            ` : ''}
        </div>
    `;
}

// Revenue Report
async function generateAndDisplayRevenueReport() {
    const date = getSelectedDate();
    
    try {
        
        const response = await APIInterceptor.fetch(`${ADMIN_URL}reports/revenue/?date=${date}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success && data.data) {
            displayRevenueReport(data.data);
            showModal('Revenue Report generated successfully!', 'success');
        } else {
            showModal(data.message || 'Failed to generate report.', 'fail');
        }
    } catch (error) {
        console.error('Error generating revenue report:', error);
        showModal('Error generating report. Please try again.', 'fail');
    }
}

function displayRevenueReport(report) {
    const output = document.getElementById('reportOutput');
    
    let roomTypesHTML = '';
    if (report.room_type_breakdown && report.room_type_breakdown.length > 0) {
        roomTypesHTML = report.room_type_breakdown.map(rt => `
            <div class="breakdown-container">
                <div class="breakdown-header">
                    <div>
                        <p class="breakdown-title">${rt.room_type}</p>
                        <p class="breakdown-subtitle">Bookings: ${rt.number_of_bookings}</p>
                    </div>
                    <span class="badge" style="background: var(--primary); color: white;">${formatCurrency(rt.total_revenue)}</span>
                </div>
            </div>
        `).join('');
    }
    
    output.innerHTML = `
        <div class="report-output-container">
            <h3 class="report-title">💰 Revenue Report</h3>
            <p class="report-date-text">Report Date: <strong>${report.report_date}</strong></p>
            
            <div class="report-cards-grid wide">
                <div class="report-card">
                    <p class="report-card-label">Completed Bookings</p>
                    <p class="report-card-value">${report.total_completed_bookings}</p>
                </div>
                <div class="report-card">
                    <p class="report-card-label">Subtotal</p>
                    <p class="report-card-value small break-word">${formatCurrency(report.total_subtotal)}</p>
                </div>
                <div class="report-card">
                    <p class="report-card-label">Discount</p>
                    <p class="report-card-value small break-word" style="color: #ff6b6b;">-${formatCurrency(report.total_discount)}</p>
                </div>
                <div class="report-card">
                    <p class="report-card-label">Tax</p>
                    <p class="report-card-value small break-word" style="color: #4caf50;">+${formatCurrency(report.total_tax)}</p>
                </div>
                <div class="report-card-gradient">
                    <p class="report-card-gradient-label">Total Revenue</p>
                    <p class="report-card-gradient-value break-word">${formatCurrency(report.total_revenue)}</p>
                </div>
            </div>
            
            ${roomTypesHTML ? `
                <h4 class="report-section-header">Revenue by Room Type</h4>
                ${roomTypesHTML}
            ` : ''}
        </div>
    `;
}

// Sales Report
async function generateAndDisplaySalesReport() {
    const date = getSelectedDate();
    
    try {
        
        const response = await APIInterceptor.fetch(`${ADMIN_URL}reports/sales/?date=${date}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success && data.data) {
            displaySalesReport(data.data);
            showModal('Sales Report generated successfully!', 'success');
        } else {
            showModal(data.message || 'Failed to generate report.', 'fail');
        }
    } catch (error) {
        console.error('Error generating sales report:', error);
        showModal('Error generating report. Please try again.', 'fail');
    }
}

function displaySalesReport(report) {
    const output = document.getElementById('reportOutput');
    
    let paymentMethodsHTML = '';
    if (report.payment_method_breakdown && report.payment_method_breakdown.length > 0) {
        paymentMethodsHTML = report.payment_method_breakdown.map(pm => `
            <div class="breakdown-container">
                <div class="breakdown-header">
                    <div>
                        <p class="breakdown-title">${pm.payment_method}</p>
                        <p class="breakdown-subtitle">Transactions: ${pm.number_of_transactions}</p>
                    </div>
                    <span class="badge checked-in">${formatCurrency(pm.total_amount)}</span>
                </div>
            </div>
        `).join('');
    }
    
    let statusHTML = '';
    if (report.new_bookings_by_status && report.new_bookings_by_status.length > 0) {
        statusHTML = report.new_bookings_by_status.map(bs => `
            <div class="breakdown-container" style="padding: 0.75rem;">
                <div class="breakdown-header">
                    <p class="breakdown-title">${bs.status}</p>
                    <span class="badge">${bs.count}</span>
                </div>
            </div>
        `).join('');
    }
    
    output.innerHTML = `
        <div class="report-output-container">
            <h3 class="report-title">📈 Sales Report</h3>
            <p class="report-date-text">Report Date: <strong>${report.report_date}</strong></p>
            
            <div class="report-cards-grid">
                <div class="report-card">
                    <p class="report-card-label">New Bookings</p>
                    <p class="report-card-value">${report.new_bookings}</p>
                </div>
                <div class="report-card">
                    <p class="report-card-label">Completed Payments</p>
                    <p class="report-card-value available">${report.completed_payments}</p>
                </div>
                <div class="report-card-gradient sales grid-span-2">
                    <p class="report-card-gradient-label">Total Sales</p>
                    <p class="report-card-gradient-value large">${formatCurrency(report.total_sales)}</p>
                </div>
            </div>
            
            ${paymentMethodsHTML ? `
                <h4 class="report-section-header">Payment Methods</h4>
                ${paymentMethodsHTML}
            ` : ''}
            
            ${statusHTML ? `
                <h4 class="report-section-header">New Bookings by Status</h4>
                ${statusHTML}
            ` : ''}
        </div>
    `;
}

// Export Report
async function generateAndDisplayExportReport() {
    const date = getSelectedDate();
    
    try {
        
        const response = await APIInterceptor.fetch(`${ADMIN_URL}reports/export/?date=${date}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success && data.data) {
            displayExportReport(data.data);
            showModal('Export Report generated successfully!', 'success');
        } else {
            showModal(data.message || 'Failed to generate report.', 'fail');
        }
    } catch (error) {
        console.error('Error generating export report:', error);
        showModal('Error generating report. Please try again.', 'fail');
    }
}

function displayExportReport(report) {
    const output = document.getElementById('reportOutput');
    
    const occupancy = report.occupancy_report;
    const revenue = report.revenue_report;
    const sales = report.sales_report;
    
    output.innerHTML = `
        <div class="report-output-container">
            <h3 style="margin-bottom: 0.5rem; color: var(--primary);">📋 Comprehensive Export Report</h3>
            <p class="report-date-text">Generated: <strong>${report.generated_at}</strong></p>
            
            <!-- OCCUPANCY SECTION -->
            <div class="export-section">
                <h4 class="export-section-title">📊 Occupancy Summary</h4>
                <div class="export-grid">
                    <div class="export-grid-item">
                        <p class="export-grid-item-label">Occupied Rooms</p>
                        <p class="export-grid-item-value">${occupancy.occupied_rooms} / ${occupancy.total_rooms}</p>
                    </div>
                    <div class="export-grid-item">
                        <p class="export-grid-item-label">Occupancy Rate</p>
                        <p class="export-grid-item-value primary">${formatPercentage(occupancy.occupancy_rate)}</p>
                    </div>
                </div>
            </div>
            
            <!-- REVENUE SECTION -->
            <div class="export-section">
                <h4 class="export-section-title">💰 Revenue Summary</h4>
                <div class="export-grid">
                    <div class="export-grid-item">
                        <p class="export-grid-item-label">Total Revenue</p>
                        <p class="export-grid-item-value success">${formatCurrency(revenue.total_revenue)}</p>
                    </div>
                    <div class="export-grid-item">
                        <p class="export-grid-item-label">Completed Bookings</p>
                        <p class="export-grid-item-value">${revenue.total_completed_bookings}</p>
                    </div>
                </div>
            </div>
            
            <!-- SALES SECTION -->
            <div class="export-section">
                <h4 class="export-section-title">📈 Sales Summary</h4>
                <div class="export-grid">
                    <div class="export-grid-item">
                        <p class="export-grid-item-label">New Bookings</p>
                        <p class="export-grid-item-value">${sales.new_bookings}</p>
                    </div>
                    <div class="export-grid-item">
                        <p class="export-grid-item-label">Total Sales</p>
                        <p class="export-grid-item-value">${formatCurrency(sales.total_sales)}</p>
                    </div>
                </div>
            </div>
        </div>
    `;
}
