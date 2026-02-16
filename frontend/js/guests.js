// Ensure main.js is loaded before running
let accessToken = null;
let allGuests = [];
let currentGuestId = null;

if (typeof CookieManager === 'undefined') {
    console.error('CookieManager not found. Make sure main.js is loaded before guests.js');
    window.location.href = "auth.html";
} else {
    accessToken = CookieManager.get("access_token");
    if (!accessToken) {
        window.location.href = "auth.html";
    }
}

document.addEventListener('DOMContentLoaded', function() {
    hidePreloader();
    loadGuests();
    setupEventListeners();
    
    // Check if modal should be opened from dashboard quick action
    if (sessionStorage.getItem('openNewGuestModal') === 'true') {
        sessionStorage.removeItem('openNewGuestModal');
        setTimeout(() => openCreateModal(), 500);
    }
});


function setupEventListeners() {
    // Create button
    document.getElementById('createGuestBtn')?.addEventListener('click', openCreateModal);
    
    // Modal controls
    document.getElementById('closeGuestModal')?.addEventListener('click', closeGuestModal);
    document.getElementById('cancelGuestBtn')?.addEventListener('click', closeGuestModal);
    document.getElementById('saveGuestBtn')?.addEventListener('click', saveGuest);
    
    // Delete modal controls
    document.getElementById('closeDeleteModal')?.addEventListener('click', closeDeleteModal);
    document.getElementById('cancelDeleteBtn')?.addEventListener('click', closeDeleteModal);
    document.getElementById('confirmDeleteBtn')?.addEventListener('click', confirmDelete);
    
    // Details modal controls
    document.getElementById('closeDetailsModal')?.addEventListener('click', closeDetailsModal);
    
    // Search
    document.getElementById('guestSearchInput')?.addEventListener('keyup', searchGuests);
}

async function loadGuests() {
    try {        
        const response = await APIInterceptor.fetch(`${ADMIN_URL}guest/list/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success && data.data) {
            console.log('Guests data:', data.data);
            allGuests = data.data;
            displayGuestsAsCards(data.data);
        } else {
            console.error('Failed to load guests:', data.message);
        }
    } catch (error) {
        console.error('Error fetching guests:', error);
    }
}

function displayGuestsAsCards(guests) {
    const container = document.getElementById('guestsContainer');
    if (!container) return;
    
    if (guests.length === 0) {
        container.style.display = 'flex';
        container.style.alignItems = 'center';
        container.style.justifyContent = 'center';
        container.style.minHeight = '400px';
        container.innerHTML = `
            <div style="text-align: center; color: var(--text-muted); padding: 3rem;">
                <i class="fas fa-users" style="font-size: 3rem; margin-bottom: 1rem; display: block; color: var(--text-muted);"></i>
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">No guests found</p>
                <p style="margin-bottom: 1.5rem; color: var(--text-muted);">Create a new guest to get started.</p>
                <button class="btn btn-primary" onclick="openCreateModal()"><i class="fas fa-plus" style="margin-right: 0.5rem;"></i>Create Guest</button>
            </div>
        `;
        return;
    }
    
    container.innerHTML = guests.map(guest => `
        <div class="guest-card" style="${guest.is_deleted ? 'opacity: 0.6; border: 2px solid #ff6b6b;' : ''}">
            <div class="guest-card-header">
                <div class="guest-name">${guest.name || 'N/A'} ${guest.is_deleted ? '<span style="color: #ff6b6b; font-size: 0.8em; margin-left: 0.5rem;">(Deleted)</span>' : ''}</div>
                <div class="guest-status-badge">
                    <i class="fas fa-user-circle"></i> Guest
                </div>
                <div class="guest-actions" style="display: flex; gap: 0.5rem; margin-left: auto;">
                    <button class="icon-btn" title="View Details" onclick="openDetailsModal(${guest.id})" style="color: var(--primary-color);">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="icon-btn edit-guest-btn" title="Edit" data-id="${guest.id}" onclick="openEditModal(${guest.id})" ${guest.is_deleted ? 'disabled style="opacity: 0.5; cursor: not-allowed;"' : ''}>
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="icon-btn ${guest.is_deleted ? 'reactivate-guest-btn' : 'delete-guest-btn'}" title="${guest.is_deleted ? 'Reactivate' : 'Delete'}" data-id="${guest.id}" onclick="openDeleteModal(${guest.id})">
                        <i class="fas fa-${guest.is_deleted ? 'undo' : 'trash'}"></i>
                    </button>
                </div>
            </div>
            <div class="guest-card-body">
                <div class="guest-info">
                    <span class="info-label">Email:</span>
                    <span class="info-value">${guest.email || 'N/A'}</span>
                </div>
                <div class="guest-info">
                    <span class="info-label">Phone:</span>
                    <span class="info-value">${guest.phone || 'N/A'}</span>
                </div>
                <div class="guest-info">
                    <span class="info-label">City:</span>
                    <span class="info-value">${guest.city || 'N/A'}</span>
                </div>
                ${guest.total_stays !== undefined ? `
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 0.75rem; padding-top: 0.75rem; border-top: 1px solid var(--border-color);">
                    <div style="text-align: center;">
                        <div style="font-size: 1.2rem; font-weight: 600; color: var(--primary-color);">${guest.total_stays}</div>
                        <div style="font-size: 0.8rem; color: var(--text-muted);">Total Stays</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 1rem; font-weight: 500;">${guest.first_visit_date ? humanizeDate(guest.first_visit_date) : 'Not booked'}</div>
                        <div style="font-size: 0.8rem; color: var(--text-muted);">First Visit</div>
                    </div>
                </div>
                ` : ''}
            </div>
        </div>
    `).join('');
}

function openCreateModal() {
    currentGuestId = null;
    document.getElementById('guestForm').reset();
    document.getElementById('guestModal').classList.add('active');
}

function closeGuestModal() {
    document.getElementById('guestModal').classList.remove('active');
    currentGuestId = null;
}

function openDeleteModal(guestId) {
    const guest = allGuests.find(g => g.id === guestId);
    if (!guest) return;
    
    currentGuestId = guestId;
    if (guest.is_deleted) {
        document.getElementById('deleteMessage').textContent = `Are you sure you want to reactivate ${guest.name}? They will be available again.`;
        document.getElementById('confirmDeleteBtn').textContent = 'Reactivate';
    } else {
        document.getElementById('deleteMessage').textContent = `Are you sure you want to delete ${guest.name}? You can reactivate them later.`;
        document.getElementById('confirmDeleteBtn').textContent = 'Delete';
    }
    document.getElementById('deleteGuestModal').classList.add('active');
}

function closeDeleteModal() {
    document.getElementById('deleteGuestModal').classList.remove('active');
    currentGuestId = null;
}

function openDetailsModal(guestId) {
    const guest = allGuests.find(g => g.id === guestId);
    if (!guest) return;
    
    const modal = document.getElementById('detailsGuestModal');
    if (!modal) return;
    
    // Populate basic info
    document.getElementById('detailsGuestName').textContent = guest.name || 'N/A';
    document.getElementById('detailsGuestEmail').textContent = guest.email || 'N/A';
    document.getElementById('detailsGuestPhone').textContent = guest.phone || 'N/A';
    document.getElementById('detailsGuestNationality').textContent = guest.nationality || 'N/A';
    
    // Populate address info
    document.getElementById('detailsGuestAddress').textContent = guest.address || 'Not provided';
    document.getElementById('detailsGuestCity').textContent = guest.city || 'Not provided';
    document.getElementById('detailsGuestCountry').textContent = guest.country || 'Not provided';
    document.getElementById('detailsGuestPostalCode').textContent = guest.postal_code || 'Not provided';
    
    // Populate stats
    document.getElementById('detailsGuestTotalStays').textContent = guest.total_stays || 0;
    document.getElementById('detailsGuestFirstVisit').textContent = guest.first_visit_date ? humanizeDate(guest.first_visit_date) : 'Not booked yet';
    document.getElementById('detailsGuestRegistered').textContent = guest.created_at ? humanizeDate(guest.created_at) : 'N/A';
    
    // Populate notes
    const notesSection = document.getElementById('detailsGuestNotes');
    if (guest.notes) {
        notesSection.innerHTML = `
            <div style="background-color: var(--input-bg); padding: 1rem; border-radius: 0.5rem; border-left: 4px solid var(--primary-color);">
                ${guest.notes}
            </div>
        `;
    } else {
        notesSection.innerHTML = `
            <div style="color: var(--text-muted); font-style: italic;">
                No notes added
            </div>
        `;
    }
    
    modal.classList.add('active');
}

function closeDetailsModal() {
    const modal = document.getElementById('detailsGuestModal');
    if (modal) {
        modal.classList.remove('active');
    }
}

function openEditModal(guestId) {
    const guest = allGuests.find(g => g.id === guestId);
    if (!guest) {
        return;
    }
    
    currentGuestId = guestId;
    document.getElementById('guestName').value = guest.name || '';
    document.getElementById('guestEmail').value = guest.email || '';
    document.getElementById('guestPhone').value = guest.phone || '';
    document.getElementById('guestAddress').value = guest.address || '';
    document.getElementById('guestCity').value = guest.city || '';
    document.getElementById('guestCountry').value = guest.country || '';
    document.getElementById('guestPostalCode').value = guest.postal_code || '';
    document.getElementById('guestNationality').value = guest.nationality || '';
    document.getElementById('guestNotes').value = guest.notes || '';
    
    document.getElementById('guestModal').classList.add('active');
}

async function saveGuest() {
    const name = document.getElementById('guestName').value;
    const email = document.getElementById('guestEmail').value;
    const phone = document.getElementById('guestPhone').value;
    const address = document.getElementById('guestAddress').value;
    const city = document.getElementById('guestCity').value;
    const country = document.getElementById('guestCountry').value;
    const postalCode = document.getElementById('guestPostalCode').value;
    const nationality = document.getElementById('guestNationality').value;
    const notes = document.getElementById('guestNotes').value;
    
    if (!name) {
        showModal('Please enter guest name.', 'fail');
        return;
    }
    
    const payload = {
        name: name,
        email: email,
        phone: phone,
        address: address,
        city: city,
        country: country,
        postal_code: postalCode,
        nationality: nationality,
        notes: notes
    };
    
    try {
        let response;
        if (currentGuestId) {
            // Update existing guest
            response = await APIInterceptor.fetch(`${ADMIN_URL}guest/${currentGuestId}/update/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                },
                body: JSON.stringify(payload)
            });
        } else {
            // Create new guest
            response = await APIInterceptor.fetch(`${ADMIN_URL}guest/create/`, {
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
            showModal(currentGuestId ? 'Guest updated successfully!' : 'Guest added successfully!', 'success');
            closeGuestModal();
            loadGuests();
        } else {
            showModal(data.message || 'Failed to save guest.', 'fail');
        }
    } catch (error) {
        console.error('Error saving guest:', error);
        showModal('Error saving guest. Please try again.', 'fail');
    }
}

async function confirmDelete() {
    if (!currentGuestId) return;
    
    const guest = allGuests.find(g => g.id === currentGuestId);
    if (!guest) return;
    
    try {
        const response = await APIInterceptor.fetch(`${ADMIN_URL}guest/${currentGuestId}/delete/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success || response.ok) {
            showModal('Guest deleted successfully!', 'success');
            closeDeleteModal();
            loadGuests();
        } else {
            showModal(data.message || 'Failed to delete guest.', 'fail');
        }
    } catch (error) {
        console.error('Error deleting guest:', error);
        showModal('Error deleting guest. Please try again.', 'fail');
    }
}

function searchGuests(e) {
    const searchTerm = e.target.value.toLowerCase();
    
    if (!searchTerm) {
        displayGuestsAsCards(allGuests);
        return;
    }
    
    const filteredGuests = allGuests.filter(guest => 
        guest.name?.toLowerCase().includes(searchTerm) ||
        guest.email?.toLowerCase().includes(searchTerm) ||
        guest.phone?.toLowerCase().includes(searchTerm) ||
        guest.city?.toLowerCase().includes(searchTerm) ||
        guest.country?.toLowerCase().includes(searchTerm) ||
        guest.nationality?.toLowerCase().includes(searchTerm)
    );
    
    displayGuestsAsCards(filteredGuests);
}
