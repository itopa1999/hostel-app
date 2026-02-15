// Ensure main.js is loaded before running
let accessToken = null;
let allBookings = [];
let allGuests = [];
let allRooms = [];
let currentBookingId = null;
let userRole = null;
let isAdmin = false;

if (typeof CookieManager === 'undefined') {
    console.error('CookieManager not found. Make sure main.js is loaded before bookings.js');
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
    loadGuestsAndRooms();
    loadBookings();
    setupEventListeners();
    
    // Check if modal should be opened from dashboard quick action
    if (sessionStorage.getItem('openNewBookingModal') === 'true') {
        sessionStorage.removeItem('openNewBookingModal');
        setTimeout(() => openCreateModal(), 500);
    }
});

function setupEventListeners() {
    // Create button
    document.getElementById('createBookingBtn')?.addEventListener('click', openCreateModal);
    
    // Modal controls
    document.getElementById('closeBookingModal')?.addEventListener('click', closeBookingModal);
    document.getElementById('cancelBookingBtn')?.addEventListener('click', closeBookingModal);
    document.getElementById('saveBookingBtn')?.addEventListener('click', saveBooking);
    
    // Delete modal controls
    document.getElementById('closeDeleteModal')?.addEventListener('click', closeDeleteModal);
    document.getElementById('cancelDeleteBtn')?.addEventListener('click', closeDeleteModal);
    document.getElementById('confirmDeleteBtn')?.addEventListener('click', confirmDelete);
    
    // Search
    document.getElementById('bookingSearchInput')?.addEventListener('keyup', searchBookings);
    
    // Cancellation reason field visibility toggle
    document.getElementById('bookingStatus')?.addEventListener('change', function() {
        const cancellationGroup = document.getElementById('cancellationReasonGroup');
        const cancellationReasonField = document.getElementById('cancellationReason');
        
        if (this.value === 'CANCELLED') {
            cancellationGroup.style.display = 'block';
            cancellationReasonField.required = true;
        } else {
            cancellationGroup.style.display = 'none';
            cancellationReasonField.required = false;
            cancellationReasonField.value = '';
        }
    });
}

async function loadGuestsAndRooms() {
    try {
        // Load guests
        const guestsResponse = await APIInterceptor.fetch(`${ADMIN_URL}guest/list/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        const guestsData = await guestsResponse.json();
        if (guestsData.is_success && guestsData.data) {
            allGuests = guestsData.data;
            populateGuestSelect();
        }

        // Load rooms
        const roomsResponse = await APIInterceptor.fetch(`${ADMIN_URL}room/list/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        const roomsData = await roomsResponse.json();
        if (roomsData.is_success && roomsData.data) {
            allRooms = roomsData.data;
            populateRoomSelect();
        }
    } catch (error) {
        console.error('Error loading guests and rooms:', error);
    }
}

function populateGuestSelect() {
    const select = document.getElementById('guestSelect');
    if (!select) return;
    
    const options = allGuests.map(guest => {
        const isDeleted = guest.is_deleted ? 'disabled' : '';
        const deletedLabel = guest.is_deleted ? ' (Deleted)' : '';
        return `<option value="${guest.id}" ${isDeleted}>${guest.name}${deletedLabel} (${guest.email})</option>`;
    }).join('');
    
    select.innerHTML = '<option value="">Select a guest</option>' + options;
}

function populateRoomSelect() {
    const select = document.getElementById('roomSelect');
    if (!select) return;
    
    const options = allRooms.map(room => {
        const isDeleted = room.is_deleted ? 'disabled' : '';
        const deletedLabel = room.is_deleted ? ' (Deleted)' : '';
        const status = room.status ? `[${room.status}]` : '';
        return `<option value="${room.id}" ${isDeleted}>Room ${room.number}${deletedLabel} (${room.room_type_name} - ₦${room.base_price?.toLocaleString() || '0'}) ${status}</option>`;
    }).join('');
    
    select.innerHTML = '<option value="">Select a room</option>' + options;
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
            console.log('Bookings data:', data.data);
            allBookings = data.data;
            displayBookingsAsCards(data.data);
        } else {
            console.error('Failed to load bookings:', data.message);
        }
    } catch (error) {
        console.error('Error fetching bookings:', error);
    }
}

function displayBookingsAsCards(bookings) {
    const container = document.getElementById('bookingsContainer');
    if (!container) return;
    
    if (bookings.length === 0) {
        container.style.display = 'flex';
        container.style.alignItems = 'center';
        container.style.justifyContent = 'center';
        container.style.minHeight = '400px';
        container.innerHTML = `
            <div style="text-align: center; color: var(--text-muted); padding: 3rem;">
                <i class="fas fa-calendar-check" style="font-size: 3rem; margin-bottom: 1rem; display: block; color: var(--text-muted);"></i>
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">No bookings found</p>
                <p style="margin-bottom: 1.5rem; color: var(--text-muted);">Create a new booking to get started.</p>
                <button class="btn btn-primary" onclick="openCreateModal()"><i class="fas fa-plus" style="margin-right: 0.5rem;"></i>Create Booking</button>
            </div>
        `;
        return;
    }
    
    container.innerHTML = bookings.map(booking => `
        <div class="booking-card" style="${booking.is_deleted ? 'opacity: 0.6; border: 2px solid #ff6b6b;' : ''}">
            <div class="booking-card-header">
                <div class="booking-code">
                    <span class="code-label">${booking.confirmation_code || 'N/A'} <span style="font-size: 0.85em; color: #999;">(ID: ${booking.id})</span>${booking.is_deleted ? ' <span style="color: #ff6b6b; font-size: 0.8em;">(Deleted)</span>' : ''}</span>
                </div>
                <div class="status-badge status-${booking.status?.toLowerCase()}">
                    <i class="fas fa-circle"></i>
                    ${booking.status?.charAt(0).toUpperCase() + booking.status?.slice(1).toLowerCase() || 'Pending'}
                </div>
                <div class="booking-actions">
                    <button class="icon-btn edit-booking-btn" title="Edit" data-id="${booking.id}" onclick="openEditModal(${booking.id})" ${booking.is_deleted ? 'disabled style="opacity: 0.5; cursor: not-allowed;"' : ''}>
                        <i class="fas fa-edit"></i>
                    </button>
                    ${isAdmin ? `
                    <button class="icon-btn ${booking.is_deleted ? 'reactivate-booking-btn' : 'delete-booking-btn'}" title="${booking.is_deleted ? 'Reactivate' : 'Delete'}" data-id="${booking.id}" onclick="openDeleteModal(${booking.id})">
                        <i class="fas fa-${booking.is_deleted ? 'undo' : 'trash'}"></i>
                    </button>
                    ` : ''}
                </div>
            </div>
            <div class="booking-card-body">
                <div class="booking-info">
                    <span class="info-label">Guest:</span>
                    <span class="info-value">${booking.guest_name || 'N/A'}</span>
                </div>
                <div class="booking-info">
                    <span class="info-label">Room:</span>
                    <span class="info-value">Room ${booking.room_number || 'N/A'}</span>
                </div>
                <div class="booking-info">
                    <span class="info-label">Room Type:</span>
                    <span class="info-value">${booking.room_type_name || 'N/A'}</span>
                </div>
                <div class="booking-dates">
                    <div class="date-item">
                        <span class="date-label">Check-in:</span>
                        <span class="date-value">${booking.check_in ? new Date(booking.check_in).toLocaleDateString() : 'N/A'}</span>
                    </div>
                    <div class="date-item">
                        <span class="date-label">Check-out:</span>
                        <span class="date-value">${booking.check_out ? new Date(booking.check_out).toLocaleDateString() : 'N/A'}</span>
                    </div>
                </div>
                <div class="booking-info">
                    <span class="info-label">Number of Guests:</span>
                    <span class="info-value">${booking.number_of_guests || 0}</span>
                </div>
                <div class="booking-info">
                    <span class="info-label">Status:</span>
                    <span class="info-value">${booking.status?.charAt(0).toUpperCase() + booking.status?.slice(1).toLowerCase() || 'N/A'}</span>
                </div>
                <div class="booking-info">
                    <span class="info-label">Payment Status:</span>
                    <span class="info-value payment-badge status-${booking.payment_status?.toLowerCase()}">${booking.payment_status?.charAt(0).toUpperCase() + booking.payment_status?.slice(1).toLowerCase() || 'N/A'}</span>
                </div>
                ${booking.special_requests ? `
                <div class="booking-info">
                    <span class="info-label">Special Requests:</span>
                    <span class="info-value">${booking.special_requests}</span>
                </div>
                ` : ''}
                ${booking.cancellation_reason ? `
                <div class="booking-info">
                    <span class="info-label">Cancellation Reason:</span>
                    <span class="info-value">${booking.cancellation_reason}</span>
                </div>
                ` : ''}
                ${booking.cancellation_date ? `
                <div class="booking-info">
                    <span class="info-label">Cancelled:</span>
                    <span class="info-value">${humanizeDate(booking.cancellation_date)}</span>
                </div>
                ` : ''}
                ${booking.created_at ? `
                <div class="booking-info">
                    <span class="info-label">Created:</span>
                    <span class="info-value">${humanizeDate(booking.created_at)}</span>
                </div>
                ` : ''}
            </div>
        </div>
    `).join('');
}

function openCreateModal() {
    currentBookingId = null;
    document.getElementById('modalTitle').textContent = 'Create New Booking';
    document.getElementById('bookingForm').reset();
    document.getElementById('cancellationReasonGroup').style.display = 'none';
    document.getElementById('cancellationReason').required = false;
    
    // Disable booking status and payment status selects
    document.getElementById('bookingStatus').disabled = true;
    document.getElementById('paymentStatus').disabled = true;
    
    // Disable CANCELLED, NO_SHOW, and CHECKED_OUT options for new bookings
    const cancelledOption = document.querySelector('#bookingStatus option[value="CANCELLED"]');
    const noShowOption = document.querySelector('#bookingStatus option[value="NO_SHOW"]');
    const checkedOutOption = document.querySelector('#bookingStatus option[value="CHECKED_OUT"]');
    if (cancelledOption) cancelledOption.disabled = true;
    if (noShowOption) noShowOption.disabled = true;
    if (checkedOutOption) checkedOutOption.disabled = true;
    
    document.getElementById('bookingModal').classList.add('active');
}

function openEditModal(bookingId) {
    const booking = allBookings.find(b => b.id === bookingId);
    if (!booking) return;
    
    currentBookingId = bookingId;
    document.getElementById('modalTitle').textContent = 'Edit Booking';
    document.getElementById('guestSelect').value = booking.guest || '';
    document.getElementById('roomSelect').value = booking.room || '';
    document.getElementById('checkInDate').value = booking.check_in || '';
    document.getElementById('checkOutDate').value = booking.check_out || '';
    document.getElementById('numberOfGuests').value = booking.number_of_guests || 1;
    document.getElementById('bookingStatus').value = booking.status || 'RESERVED';
    document.getElementById('paymentStatus').value = booking.payment_status || 'PENDING';
    document.getElementById('specialRequests').value = booking.special_requests || '';
    document.getElementById('cancellationReason').value = booking.cancellation_reason || '';
    
    // Disable booking status and payment status selects
    document.getElementById('bookingStatus').disabled = true;
    document.getElementById('paymentStatus').disabled = true;
    
    // Show/hide cancellation reason field based on status
    const cancellationGroup = document.getElementById('cancellationReasonGroup');
    if (booking.status === 'CANCELLED') {
        cancellationGroup.style.display = 'block';
    } else {
        cancellationGroup.style.display = 'none';
    }
    
    // Enable CANCELLED, NO_SHOW, and CHECKED_OUT options for existing bookings
    const cancelledOption = document.querySelector('#bookingStatus option[value="CANCELLED"]');
    const noShowOption = document.querySelector('#bookingStatus option[value="NO_SHOW"]');
    const checkedOutOption = document.querySelector('#bookingStatus option[value="CHECKED_OUT"]');
    if (cancelledOption) cancelledOption.disabled = false;
    if (noShowOption) noShowOption.disabled = false;
    if (checkedOutOption) checkedOutOption.disabled = false;
    
    document.getElementById('bookingModal').classList.add('active');
}

function closeBookingModal() {
    document.getElementById('bookingModal').classList.remove('active');
    currentBookingId = null;
}

function openDeleteModal(bookingId) {
    const booking = allBookings.find(b => b.id === bookingId);
    if (!booking) return;
    
    currentBookingId = bookingId;
    if (booking.is_deleted) {
        document.getElementById('deleteMessage').textContent = `Are you sure you want to reactivate booking "${booking.confirmation_code}" for ${booking.guest_name}? It will be available again.`;
        document.getElementById('confirmDeleteBtn').textContent = 'Reactivate';
    } else {
        document.getElementById('deleteMessage').textContent = `Are you sure you want to delete booking "${booking.confirmation_code}" for ${booking.guest_name}? You can reactivate it later.`;
        document.getElementById('confirmDeleteBtn').textContent = 'Delete';
    }
    document.getElementById('deleteBookingModal').classList.add('active');
}

function closeDeleteModal() {
    document.getElementById('deleteBookingModal').classList.remove('active');
    currentBookingId = null;
}

async function saveBooking() {
    const guestId = document.getElementById('guestSelect').value;
    const roomId = document.getElementById('roomSelect').value;
    const checkInDate = document.getElementById('checkInDate').value;
    const checkOutDate = document.getElementById('checkOutDate').value;
    const numberOfGuests = document.getElementById('numberOfGuests').value;
    const status = document.getElementById('bookingStatus').value;
    const paymentStatus = document.getElementById('paymentStatus').value;
    const specialRequests = document.getElementById('specialRequests').value;
    const cancellationReason = document.getElementById('cancellationReason')?.value || '';
    
    if (!guestId || !roomId || !checkInDate || !checkOutDate) {
        showModal('Please fill in all required fields.', 'fail');
        return;
    }
    
    const payload = {
        guest: parseInt(guestId),
        room: parseInt(roomId),
        check_in: checkInDate,
        check_out: checkOutDate,
        number_of_guests: parseInt(numberOfGuests),
        status: status,
        payment_status: paymentStatus,
        special_requests: specialRequests
    };
    
    // Add cancellation fields if status is CANCELLED
    if (status === 'CANCELLED') {
        payload.cancellation_date = new Date().toISOString();
        payload.cancellation_reason = cancellationReason;
    }
    
    try {
        let response;
        if (currentBookingId) {
            // Update existing booking
            response = await APIInterceptor.fetch(`${ADMIN_URL}booking/${currentBookingId}/update/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                },
                body: JSON.stringify(payload)
            });
        } else {
            // Create new booking
            response = await APIInterceptor.fetch(`${ADMIN_URL}booking/create/`, {
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
            showModal(currentBookingId ? 'Booking updated successfully!' : 'Booking created successfully!', 'success');
            closeBookingModal();
            loadBookings();
        } else {
            showModal(data.message || 'Failed to save booking.', 'fail');
        }
    } catch (error) {
        console.error('Error saving booking:', error);
        showModal('Error saving booking. Please try again.', 'fail');
    }
}

async function confirmDelete() {
    if (!currentBookingId) return;
    
    try {
        const response = await APIInterceptor.fetch(`${ADMIN_URL}booking/${currentBookingId}/delete/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success || response.ok) {
            showModal('Booking deleted successfully!', 'success');
            closeDeleteModal();
            loadBookings();
        } else {
            showModal(data.message || 'Failed to delete booking.', 'fail');
        }
    } catch (error) {
        console.error('Error deleting booking:', error);
        showModal('Error deleting booking. Please try again.', 'fail');
    }
}

function searchBookings(e) {
    const searchTerm = e.target.value.toLowerCase();
    
    if (!searchTerm) {
        displayBookingsAsCards(allBookings);
        return;
    }
    
    const filteredBookings = allBookings.filter(booking => 
        booking.confirmation_code?.toLowerCase().includes(searchTerm) ||
        booking.guest_name?.toLowerCase().includes(searchTerm) ||
        booking.room_number?.toLowerCase().includes(searchTerm) ||
        booking.status?.toLowerCase().includes(searchTerm)
    );
    
    displayBookingsAsCards(filteredBookings);
}
