// Ensure main.js is loaded before running
let accessToken = null;

if (typeof CookieManager === 'undefined') {
    console.error('CookieManager not found. Make sure main.js is loaded before dashboard.js');
    window.location.href = "auth.html";
} else {
    accessToken = CookieManager.get("access_token");
    if (!accessToken) {
        window.location.href = "auth.html";
    }
}

document.addEventListener('DOMContentLoaded', function() {
    loadDashboardMetrics();
    setupQuickActionButtons();
    hidePreloader();
});

/**
 * Setup quick action button click handlers
 */
function setupQuickActionButtons() {
    const actionButtons = document.querySelectorAll('.action-btn');
    
    // New Booking button
    if (actionButtons[0]) {
        actionButtons[0].addEventListener('click', function() {
            sessionStorage.setItem('openNewBookingModal', 'true');
            window.location.href = 'bookings.html';
        });
    }
    
    // Add Guest button
    if (actionButtons[1]) {
        actionButtons[1].addEventListener('click', function() {
            sessionStorage.setItem('openNewGuestModal', 'true');
            window.location.href = 'guests.html';
        });
    }
    
    // Generate Report button
    if (actionButtons[2]) {
        actionButtons[2].addEventListener('click', function() {
            sessionStorage.setItem('openReportModal', 'true');
            window.location.href = 'reports.html';
        });
    }
}
async function loadDashboardMetrics() {
    try {        
        const response = await APIInterceptor.fetch(`${ADMIN_URL}hotel/dashboard/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        console.log('Dashboard response data:', data);
        
        if (data.is_success && data.data) {
            console.log('Dashboard metrics:', data.data);
            populateDashboard(data.data);
        } else {
            console.error('Failed to load dashboard metrics:', data.message);
            showModal('Failed to load dashboard metrics. Please refresh the page.', 'fail');
        }
    } catch (error) {
        console.error('Error fetching dashboard metrics:', error);
        showModal('Error loading dashboard. Please check your connection.', 'fail');
    }
}

/**
 * Update dashboard UI with fetched data
 */
function populateDashboard(dashboardData) {
    // Summary Metrics - KPI Cards
    document.getElementById('total-rooms').textContent = dashboardData.summary.total_rooms;
    document.getElementById('total-guests').textContent = dashboardData.summary.total_guests;
    document.getElementById('total-bookings').textContent = dashboardData.summary.total_bookings;
    document.getElementById('total-hotels').textContent = dashboardData.summary.total_hotels;
    document.getElementById('total-floors').textContent = dashboardData.summary.total_floors;
    document.getElementById('total-invoices').textContent = dashboardData.summary.total_invoices;
    document.getElementById('total-payments').textContent = dashboardData.summary.total_payments;
    
    // Calculate occupancy rate
    const occupancyRate = dashboardData.summary.total_rooms > 0 
        ? Math.round((dashboardData.room_status.occupied / dashboardData.summary.total_rooms) * 100)
        : 0;
    document.getElementById('occupancy-rate').textContent = occupancyRate + '% occupancy';
    
    // Financial metrics
    const totalRevenue = dashboardData.financial.total_revenue.toLocaleString('en-NG', {
        style: 'currency',
        currency: 'NGN',
        minimumFractionDigits: 0
    });
    document.getElementById('total-revenue').textContent = totalRevenue;
    
    const pendingPayments = dashboardData.financial.pending_payments.toLocaleString('en-NG', {
        style: 'currency',
        currency: 'NGN',
        minimumFractionDigits: 0
    });
    document.getElementById('pending-payments').textContent = pendingPayments + ' pending';
    
    // Room Status
    document.getElementById('available-rooms').textContent = dashboardData.room_status.available;
    document.getElementById('occupied-rooms').textContent = dashboardData.room_status.occupied;
    document.getElementById('dirty-rooms').textContent = dashboardData.room_status.dirty;
    document.getElementById('maintenance-rooms').textContent = dashboardData.room_status.maintenance;
    
    // Calculate progress bar widths based on total rooms
    const totalRooms = dashboardData.summary.total_rooms || 1;
    const availablePercent = (dashboardData.room_status.available / totalRooms) * 100;
    const occupiedPercent = (dashboardData.room_status.occupied / totalRooms) * 100;
    const maintenancePercent = (dashboardData.room_status.maintenance / totalRooms) * 100;
    const dirtyPercent = (dashboardData.room_status.dirty / totalRooms) * 100;
    
    // Update progress bar widths
    const progressAvailable = document.getElementById('progress-available');
    const progressOccupied = document.getElementById('progress-occupied');
    const progressMaintenance = document.getElementById('progress-maintenance');
    const progressCleaning = document.getElementById('progress-cleaning');
    
    if (progressAvailable) progressAvailable.style.width = availablePercent + '%';
    if (progressOccupied) progressOccupied.style.width = occupiedPercent + '%';
    if (progressMaintenance) progressMaintenance.style.width = maintenancePercent + '%';
    if (progressCleaning) progressCleaning.style.width = dirtyPercent + '%';
    
    // Booking Status
    document.getElementById('reserved-bookings').textContent = dashboardData.booking_status.reserved;
    document.getElementById('checked-in-bookings').textContent = dashboardData.booking_status.checked_in;
    document.getElementById('checked-out-bookings').textContent = dashboardData.booking_status.checked_out;
    document.getElementById('cancelled-bookings').textContent = dashboardData.booking_status.cancelled;
    
    // Payment Status
    document.getElementById('pending-payment-stat').textContent = dashboardData.payment_status.pending;
    document.getElementById('completed-payment').textContent = dashboardData.payment_status.completed;
    document.getElementById('failed-payment').textContent = dashboardData.payment_status.failed;
    document.getElementById('refunded-payment').textContent = dashboardData.payment_status.refunded;
    
    // Populate Recent Bookings
    populateRecentBookings(dashboardData.recent_bookings);
    
    // Populate Recent Payments
    populateRecentPayments(dashboardData.recent_payments);
    
    // Populate Hotels
    populateHotelsCards(dashboardData.hotels);
    
    // Update user greeting
    updateUserGreeting();
}

function populateRecentBookings(bookings) {
    const container = document.getElementById('recent-bookings-list');
    if (!container) return;
    
    if (!bookings || bookings.length === 0) {
        container.innerHTML = '<div style="text-align: center; padding: 1.5rem; color: var(--text-muted);">No recent bookings</div>';
        return;
    }
    
    container.innerHTML = bookings.map(booking => {
        const guestName = booking.guest__name || 'N/A';
        const initials = guestName.split(' ').map(n => n.charAt(0)).join('').toUpperCase() || 'NB';
        const checkIn = new Date(booking.check_in).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        const checkOut = new Date(booking.check_out).toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        const nights = Math.ceil((new Date(booking.check_out) - new Date(booking.check_in)) / (1000 * 60 * 60 * 24));
        const statusClass = booking.status.toLowerCase();
        
        return `
            <div class="booking-item">
                <div class="booking-avatar">${initials}</div>
                <div class="booking-details">
                    <p class="booking-name">${guestName}</p>
                    <p class="booking-date">${checkIn} - ${checkOut} • ${nights} night${nights > 1 ? 's' : ''}</p>
                </div>
                <div class="booking-status">
                    <span class="badge ${statusClass === 'reserved' ? 'reserved' : statusClass === 'checked_in' ? 'checked-in' : 'checked-out'}">${booking.status}</span>
                </div>
            </div>
        `;
    }).join('');
}

function populateRecentPayments(payments) {
    const container = document.getElementById('recent-payments-list');
    if (!container) return;
    
    if (!payments || payments.length === 0) {
        container.innerHTML = '<div style="text-align: center; padding: 1.5rem; color: var(--text-muted);">No recent payments</div>';
        return;
    }
    
    container.innerHTML = payments.map(payment => {
        const amount = payment.amount.toLocaleString('en-NG', {
            style: 'currency',
            currency: 'NGN',
            minimumFractionDigits: 0
        });
        const paymentDate = new Date(payment.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: '2-digit' });
        const statusClass = payment.payment_status.toLowerCase();
        
        return `
            <div class="payment-item">
                <div class="payment-info">
                    <p class="payment-amount">${amount}</p>
                    <p class="payment-method">${payment.method}</p>
                </div>
                <div class="payment-meta">
                    <p class="payment-date">${paymentDate}</p>
                </div>
                <div class="payment-status">
                    <span class="badge ${statusClass === 'pending' ? 'reserved' : statusClass === 'completed' ? 'checked-in' : 'checked-out'}">${payment.payment_status}</span>
                </div>
            </div>
        `;
    }).join('');
}

function populateHotelsCards(hotels) {
    const container = document.getElementById('hotels-container');
    if (!container) return;
    
    if (!hotels || hotels.length === 0) {
        container.innerHTML = '<div style="text-align: center; padding: 2rem; color: var(--text-muted);">No hotels found</div>';
        return;
    }
    
    container.innerHTML = hotels.map(hotel => {
        const occupancyPercent = hotel.total_rooms > 0 
            ? Math.round((hotel.occupied_rooms / hotel.total_rooms) * 100)
            : 0;
        
        return `
            <div style="background: linear-gradient(135deg, rgba(110, 68, 255, 0.1) 0%, rgba(110, 68, 255, 0.05) 100%); border: 1px solid rgba(110, 68, 255, 0.2); border-radius: 12px; padding: 1.5rem; transition: all 0.3s ease; display: flex; flex-direction: column; gap: 1.2rem;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem;">
                    <h3 style="font-size: 1.3rem; font-weight: 700; color: var(--text); margin: 0;">${hotel.name}</h3>
                    <div style="background: linear-gradient(135deg, #6e44ff 0%, #8b5cf6 100%); color: white; padding: 0.5rem 1rem; border-radius: 20px; text-align: center; flex-shrink: 0; min-width: fit-content;">
                        <span style="font-weight: 700; font-size: 1.1rem; display: block;">${hotel.occupancy_rate}%</span>
                    </div>
                </div>
                
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                    <div style="display: flex; align-items: center; gap: 0.8rem; padding: 0.8rem; background: rgba(110, 68, 255, 0.05); border-radius: 8px;">
                        <div style="width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 1rem; background: linear-gradient(135deg, #6e44ff 0%, #8b5cf6 100%); flex-shrink: 0;">
                            <i class="fas fa-door-open"></i>
                        </div>
                        <div style="flex: 1;">
                            <p style="font-size: 0.75rem; color: var(--text-muted); margin: 0; text-transform: uppercase; letter-spacing: 0.5px;">Total Rooms</p>
                            <p style="font-size: 1.3rem; font-weight: 700; color: var(--text); margin: 0.2rem 0 0 0;">${hotel.total_rooms}</p>
                        </div>
                    </div>
                    
                    <div style="display: flex; align-items: center; gap: 0.8rem; padding: 0.8rem; background: rgba(110, 68, 255, 0.05); border-radius: 8px;">
                        <div style="width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 1rem; background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); flex-shrink: 0;">
                            <i class="fas fa-user"></i>
                        </div>
                        <div style="flex: 1;">
                            <p style="font-size: 0.75rem; color: var(--text-muted); margin: 0; text-transform: uppercase; letter-spacing: 0.5px;">Occupied</p>
                            <p style="font-size: 1.3rem; font-weight: 700; color: var(--text); margin: 0.2rem 0 0 0;">${hotel.occupied_rooms}</p>
                        </div>
                    </div>
                    
                    <div style="display: flex; align-items: center; gap: 0.8rem; padding: 0.8rem; background: rgba(110, 68, 255, 0.05); border-radius: 8px;">
                        <div style="width: 40px; height: 40px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 1rem; background: linear-gradient(135deg, #10b981 0%, #059669 100%); flex-shrink: 0;">
                            <i class="fas fa-check-circle"></i>
                        </div>
                        <div style="flex: 1;">
                            <p style="font-size: 0.75rem; color: var(--text-muted); margin: 0; text-transform: uppercase; letter-spacing: 0.5px;">Available</p>
                            <p style="font-size: 1.3rem; font-weight: 700; color: var(--text); margin: 0.2rem 0 0 0;">${hotel.available_rooms}</p>
                        </div>
                    </div>
                </div>
                
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; font-size: 0.85rem; color: var(--text-muted);">
                        <span>Room Status</span>
                        <span>${hotel.occupied_rooms}/${hotel.total_rooms}</span>
                    </div>
                    <div style="width: 100%; height: 8px; background: rgba(110, 68, 255, 0.1); border-radius: 4px; overflow: hidden;">
                        <div style="height: 100%; background: linear-gradient(90deg, #6e44ff 0%, #8b5cf6 100%); border-radius: 4px; transition: width 0.3s ease; width: ${occupancyPercent}%;"></div>
                    </div>
                </div>
                
                <a href="hotels.html" style="display: flex; align-items: center; justify-content: center; gap: 0.5rem; padding: 0.8rem 1rem; background: linear-gradient(135deg, #6e44ff 0%, #8b5cf6 100%); color: white; text-decoration: none; border-radius: 8px; font-weight: 600; transition: all 0.3s ease; cursor: pointer; border: none; font-size: 0.95rem;">
                    <span>View Details</span>
                    <i class="fas fa-arrow-right"></i>
                </a>
            </div>
        `;
    }).join('');
}

function updateUserGreeting() {
    const userSpan = document.getElementById('user');
    if (userSpan) {
        const userName = CookieManager.get('admin_username');
        if (userName) {
            userSpan.textContent = userName;
        }
    }
}