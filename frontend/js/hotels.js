// Ensure main.js is loaded before running
let accessToken = null;
let hotelData = null;

if (typeof CookieManager === 'undefined') {
    console.error('CookieManager not found. Make sure main.js is loaded before hotels.js');
    window.location.href = "auth.html";
} else {
    accessToken = CookieManager.get("access_token");
    if (!accessToken) {
        window.location.href = "auth.html";
    }
}

document.addEventListener('DOMContentLoaded', function() {
    hidePreloader();
    loadHotel();
    setupEventListeners();
});

function setupEventListeners() {
    const updateBtn = document.getElementById('updateBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const hotelForm = document.getElementById('hotelForm');
    
    if (updateBtn) {
        updateBtn.addEventListener('click', toggleEditMode);
    }
    
    if (cancelBtn) {
        cancelBtn.addEventListener('click', toggleEditMode);
    }
    
    if (hotelForm) {
        hotelForm.addEventListener('submit', saveHotelData);
    }
}

async function loadHotel() {
    try {        
        const response = await APIInterceptor.fetch(`${ADMIN_URL}hotel/details/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success && data.data) {
            console.log('Hotel data:', data.data);
            hotelData = data.data;
            displayHotelData(data.data);
        } else {
            console.error('Failed to load hotel:', data.message);
            showModal('Failed to load hotel data. Please refresh the page.', 'fail');
        }
    } catch (error) {
        console.error('Error fetching hotel:', error);
        showModal('Error loading hotel data. Please check your connection.', 'fail');
    }
}

function displayHotelData(hotel) {
    // Display mode
    document.getElementById('hotelName').textContent = hotel.name || '-';
    document.getElementById('idNumber').textContent = hotel.id_number || '-';
    document.getElementById('phone').textContent = hotel.phone || '-';
    document.getElementById('email').textContent = hotel.email || '-';
    document.getElementById('address').textContent = hotel.address || '-';
    document.getElementById('city').textContent = hotel.city || '-';
    document.getElementById('country').textContent = hotel.country || '-';
    document.getElementById('postalCode').textContent = hotel.postal_code || '-';
    document.getElementById('checkInTime').textContent = formatTime(hotel.check_in_time) || '-';
    document.getElementById('checkOutTime').textContent = formatTime(hotel.check_out_time) || '-';
    
    // Form mode
    document.getElementById('hotelNameInput').value = hotel.name || '';
    document.getElementById('idNumberInput').value = hotel.id_number || '';
    document.getElementById('phoneInput').value = hotel.phone || '';
    document.getElementById('emailInput').value = hotel.email || '';
    document.getElementById('addressInput').value = hotel.address || '';
    document.getElementById('cityInput').value = hotel.city || '';
    document.getElementById('countryInput').value = hotel.country || '';
    document.getElementById('postalCodeInput').value = hotel.postal_code || '';
    document.getElementById('checkInTimeInput').value = hotel.check_in_time || '14:00';
    document.getElementById('checkOutTimeInput').value = hotel.check_out_time || '12:00';
}

function formatTime(time) {
    if (!time) return '-';
    return time.substring(0, 5); // Format HH:MM
}

function toggleEditMode() {
    const viewMode = document.getElementById('viewMode');
    const editMode = document.getElementById('editMode');
    const updateBtn = document.getElementById('updateBtn');
    const updateBtnIcon = updateBtn.querySelector('i');
    const updateBtnText = updateBtn.querySelector('span');
    
    viewMode.style.display = viewMode.style.display === 'none' ? 'block' : 'none';
    editMode.style.display = editMode.style.display === 'none' ? 'block' : 'none';
    
    // Toggle button text and icon
    if (viewMode.style.display === 'none') {
        // Edit mode is now visible
        updateBtnIcon.className = 'fas fa-eye';
        updateBtnText.textContent = 'View Details';
    } else {
        // View mode is now visible
        updateBtnIcon.className = 'fas fa-edit';
        updateBtnText.textContent = 'Update';
    }
}

function cancelEdit() {
    // Reload data and switch back to view mode
    displayHotelData(hotelData);
    const viewMode = document.getElementById('viewMode');
    const editMode = document.getElementById('editMode');
    const updateBtn = document.getElementById('updateBtn');
    const updateBtnIcon = updateBtn.querySelector('i');
    const updateBtnText = updateBtn.querySelector('span');
    
    // Ensure view mode is visible
    viewMode.style.display = 'block';
    editMode.style.display = 'none';
    
    // Reset button to "Update"
    updateBtnIcon.className = 'fas fa-edit';
    updateBtnText.textContent = 'Update';
}

async function saveHotelData(e) {
    e.preventDefault();
    
    const updatedData = {
        name: document.getElementById('hotelNameInput').value,
        id_number: document.getElementById('idNumberInput').value || null,
        phone: document.getElementById('phoneInput').value || null,
        email: document.getElementById('emailInput').value || null,
        address: document.getElementById('addressInput').value,
        city: document.getElementById('cityInput').value || null,
        country: document.getElementById('countryInput').value || null,
        postal_code: document.getElementById('postalCodeInput').value || null,
        check_in_time: document.getElementById('checkInTimeInput').value,
        check_out_time: document.getElementById('checkOutTimeInput').value
    };
    
    try {
        const response = await APIInterceptor.fetch(`${ADMIN_URL}hotel/update/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            },
            body: JSON.stringify(updatedData)
        });
        
        const data = await response.json();
        
        if (data.is_success) {
            showModal('Hotel information updated successfully!', 'success');
            hotelData = data.data;
            displayHotelData(data.data);
            toggleEditMode();
            
            // Reset button to "Update" after successful save
            const updateBtn = document.getElementById('updateBtn');
            const updateBtnIcon = updateBtn.querySelector('i');
            const updateBtnText = updateBtn.querySelector('span');
            updateBtnIcon.className = 'fas fa-edit';
            updateBtnText.textContent = 'Update';
        } else {
            showModal('Failed to update hotel information.', 'fail');
        }
    } catch (error) {
        console.error('Error updating hotel:', error);
        showModal('Error updating hotel information. Please try again.', 'fail');
    }
}
