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
            <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <p style="font-weight: 600; margin-bottom: 0.25rem;">${rt.room_type}</p>
                        <p style="color: var(--text-muted); font-size: 0.9rem;">Total: ${rt.total} | Occupied: ${rt.occupied} | Available: ${rt.available}</p>
                    </div>
                    <span class="badge checked-in">${formatPercentage(rt.occupancy_rate)}</span>
                </div>
            </div>
        `).join('');
    }
    
    output.innerHTML = `
        <div>
            <h3 style="margin-bottom: 1rem; color: var(--primary);">📊 Occupancy Report</h3>
            <p style="color: var(--text-muted); margin-bottom: 1rem;">Report Date: <strong>${report.report_date}</strong></p>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
                <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 8px; text-align: center;">
                    <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 0.5rem;">Total Rooms</p>
                    <p style="font-size: 1.8rem; font-weight: 700; color: var(--primary);">${report.total_rooms}</p>
                </div>
                <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 8px; text-align: center;">
                    <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 0.5rem;">Occupied</p>
                    <p style="font-size: 1.8rem; font-weight: 700; color: #ff9800;">${report.occupied_rooms}</p>
                </div>
                <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 8px; text-align: center;">
                    <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 0.5rem;">Available</p>
                    <p style="font-size: 1.8rem; font-weight: 700; color: #4caf50;">${report.available_rooms}</p>
                </div>
                <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 8px; text-align: center;">
                    <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 0.5rem;">Occupancy Rate</p>
                    <p style="font-size: 1.8rem; font-weight: 700; color: var(--success);">${formatPercentage(report.occupancy_rate)}</p>
                </div>
            </div>
            
            ${roomTypesHTML ? `
                <h4 style="margin-top: 1.5rem; margin-bottom: 1rem;">Room Type Breakdown</h4>
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
            <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <p style="font-weight: 600; margin-bottom: 0.25rem;">${rt.room_type}</p>
                        <p style="color: var(--text-muted); font-size: 0.9rem;">Bookings: ${rt.number_of_bookings}</p>
                    </div>
                    <span class="badge" style="background: var(--primary); color: white;">${formatCurrency(rt.total_revenue)}</span>
                </div>
            </div>
        `).join('');
    }
    
    output.innerHTML = `
        <div>
            <h3 style="margin-bottom: 1rem; color: var(--primary);">💰 Revenue Report</h3>
            <p style="color: var(--text-muted); margin-bottom: 1rem;">Report Date: <strong>${report.report_date}</strong></p>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
                <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 8px; text-align: center;">
                    <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 0.5rem;">Completed Bookings</p>
                    <p style="font-size: 1.8rem; font-weight: 700; color: var(--primary);">${report.total_completed_bookings}</p>
                </div>
                <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 8px; text-align: center;">
                    <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 0.5rem;">Subtotal</p>
                    <p style="font-size: 1.1rem; font-weight: 700; color: var(--text-primary); word-break: break-word;">${formatCurrency(report.total_subtotal)}</p>
                </div>
                <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 8px; text-align: center;">
                    <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 0.5rem;">Discount</p>
                    <p style="font-size: 1.1rem; font-weight: 700; color: #ff6b6b; word-break: break-word;">-${formatCurrency(report.total_discount)}</p>
                </div>
                <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 8px; text-align: center;">
                    <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 0.5rem;">Tax</p>
                    <p style="font-size: 1.1rem; font-weight: 700; color: #4caf50; word-break: break-word;">+${formatCurrency(report.total_tax)}</p>
                </div>
                <div style="background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%); padding: 1rem; border-radius: 8px; text-align: center; color: white; grid-column: auto;">
                    <p style="font-size: 0.9rem; margin-bottom: 0.5rem;">Total Revenue</p>
                    <p style="font-size: 1.3rem; font-weight: 700; word-break: break-word;">${formatCurrency(report.total_revenue)}</p>
                </div>
            </div>
            
            ${roomTypesHTML ? `
                <h4 style="margin-top: 1.5rem; margin-bottom: 1rem;">Revenue by Room Type</h4>
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
            <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <p style="font-weight: 600; margin-bottom: 0.25rem;">${pm.payment_method}</p>
                        <p style="color: var(--text-muted); font-size: 0.9rem;">Transactions: ${pm.number_of_transactions}</p>
                    </div>
                    <span class="badge checked-in">${formatCurrency(pm.total_amount)}</span>
                </div>
            </div>
        `).join('');
    }
    
    let statusHTML = '';
    if (report.new_bookings_by_status && report.new_bookings_by_status.length > 0) {
        statusHTML = report.new_bookings_by_status.map(bs => `
            <div style="background: var(--bg-secondary); padding: 0.75rem; border-radius: 8px; margin-bottom: 0.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <p style="font-weight: 600;">${bs.status}</p>
                    <span class="badge">${bs.count}</span>
                </div>
            </div>
        `).join('');
    }
    
    output.innerHTML = `
        <div>
            <h3 style="margin-bottom: 1rem; color: var(--primary);">📈 Sales Report</h3>
            <p style="color: var(--text-muted); margin-bottom: 1rem;">Report Date: <strong>${report.report_date}</strong></p>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">
                <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 8px; text-align: center;">
                    <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 0.5rem;">New Bookings</p>
                    <p style="font-size: 1.8rem; font-weight: 700; color: var(--primary);">${report.new_bookings}</p>
                </div>
                <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 8px; text-align: center;">
                    <p style="color: var(--text-muted); font-size: 0.9rem; margin-bottom: 0.5rem;">Completed Payments</p>
                    <p style="font-size: 1.8rem; font-weight: 700; color: #4caf50;">${report.completed_payments}</p>
                </div>
                <div style="background: linear-gradient(135deg, #4caf50 0%, #388e3c 100%); padding: 1rem; border-radius: 8px; text-align: center; color: white; grid-column: span 2;">
                    <p style="font-size: 0.9rem; margin-bottom: 0.5rem;">Total Sales</p>
                    <p style="font-size: 1.8rem; font-weight: 700;">${formatCurrency(report.total_sales)}</p>
                </div>
            </div>
            
            ${paymentMethodsHTML ? `
                <h4 style="margin-top: 1.5rem; margin-bottom: 1rem;">Payment Methods</h4>
                ${paymentMethodsHTML}
            ` : ''}
            
            ${statusHTML ? `
                <h4 style="margin-top: 1.5rem; margin-bottom: 1rem;">New Bookings by Status</h4>
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
        <div>
            <h3 style="margin-bottom: 0.5rem; color: var(--primary);">📋 Comprehensive Export Report</h3>
            <p style="color: var(--text-muted); margin-bottom: 1rem;">Generated: <strong>${report.generated_at}</strong></p>
            
            <!-- OCCUPANCY SECTION -->
            <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
                <h4 style="margin-bottom: 0.75rem; color: var(--primary);">📊 Occupancy Summary</h4>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.75rem;">
                    <div>
                        <p style="color: var(--text-muted); font-size: 0.85rem;">Occupied Rooms</p>
                        <p style="font-weight: 700;">${occupancy.occupied_rooms} / ${occupancy.total_rooms}</p>
                    </div>
                    <div>
                        <p style="color: var(--text-muted); font-size: 0.85rem;">Occupancy Rate</p>
                        <p style="font-weight: 700; color: var(--primary);">${formatPercentage(occupancy.occupancy_rate)}</p>
                    </div>
                </div>
            </div>
            
            <!-- REVENUE SECTION -->
            <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
                <h4 style="margin-bottom: 0.75rem; color: var(--primary);">💰 Revenue Summary</h4>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.75rem;">
                    <div>
                        <p style="color: var(--text-muted); font-size: 0.85rem;">Total Revenue</p>
                        <p style="font-weight: 700; color: #4caf50;">${formatCurrency(revenue.total_revenue)}</p>
                    </div>
                    <div>
                        <p style="color: var(--text-muted); font-size: 0.85rem;">Completed Bookings</p>
                        <p style="font-weight: 700;">${revenue.total_completed_bookings}</p>
                    </div>
                </div>
            </div>
            
            <!-- SALES SECTION -->
            <div style="background: var(--bg-secondary); padding: 1rem; border-radius: 8px;">
                <h4 style="margin-bottom: 0.75rem; color: var(--primary);">📈 Sales Summary</h4>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.75rem;">
                    <div>
                        <p style="color: var(--text-muted); font-size: 0.85rem;">New Bookings</p>
                        <p style="font-weight: 700;">${sales.new_bookings}</p>
                    </div>
                    <div>
                        <p style="color: var(--text-muted); font-size: 0.85rem;">Total Sales</p>
                        <p style="font-weight: 700;">${formatCurrency(sales.total_sales)}</p>
                    </div>
                </div>
            </div>
        </div>
    `;
}
