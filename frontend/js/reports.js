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
    setupReportButtons();
});

function setupReportButtons() {
    const reportButtons = document.querySelectorAll('.action-btn');
    
    reportButtons.forEach(button => {
        button.addEventListener('click', function() {
            const text = this.innerText;
            showModal(`${text} will be generated soon!`, 'info');
        });
    });
}

async function generateOccupancyReport() {
    try {        
        const response = await APIInterceptor.fetch(`${HOSTEL_URL}reports/occupancy/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success) {
            showModal('Occupancy report generated successfully!', 'success');
        } else {
            showModal('Failed to generate report.', 'fail');
        }
    } catch (error) {
        console.error('Error generating report:', error);
        showModal('Error generating report. Please try again.', 'fail');
    }
}

async function generateRevenueReport() {
    try {        
        const response = await APIInterceptor.fetch(`${HOSTEL_URL}reports/revenue/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success) {
            showModal('Revenue report generated successfully!', 'success');
        } else {
            showModal('Failed to generate report.', 'fail');
        }
    } catch (error) {
        console.error('Error generating report:', error);
        showModal('Error generating report. Please try again.', 'fail');
    }
}

async function generateSalesReport() {
    try {        
        const response = await APIInterceptor.fetch(`${HOSTEL_URL}reports/sales/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success) {
            showModal('Sales report generated successfully!', 'success');
        } else {
            showModal('Failed to generate report.', 'fail');
        }
    } catch (error) {
        console.error('Error generating report:', error);
        showModal('Error generating report. Please try again.', 'fail');
    }
}
