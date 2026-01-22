// Ensure main.js is loaded before running
let accessToken = null;
let allRoomTypes = [];
let currentRoomTypeId = null;

if (typeof CookieManager === 'undefined') {
    console.error('CookieManager not found. Make sure main.js is loaded before room-types.js');
    window.location.href = "auth.html";
} else {
    accessToken = CookieManager.get("access_token");
    if (!accessToken) {
        window.location.href = "auth.html";
    }
}

document.addEventListener('DOMContentLoaded', function() {
    hidePreloader();
    loadRoomTypes();
    setupEventListeners();
});



function setupEventListeners() {
    // Create button
    document.getElementById('createRoomTypeBtn')?.addEventListener('click', openCreateModal);
    
    // Modal controls
    document.getElementById('closeRoomTypeModal')?.addEventListener('click', closeRoomTypeModal);
    document.getElementById('cancelRoomTypeBtn')?.addEventListener('click', closeRoomTypeModal);
    document.getElementById('saveRoomTypeBtn')?.addEventListener('click', saveRoomType);
    
    // Delete modal controls
    document.getElementById('closeDeleteModal')?.addEventListener('click', closeDeleteModal);
    document.getElementById('cancelDeleteBtn')?.addEventListener('click', closeDeleteModal);
    document.getElementById('confirmDeleteBtn')?.addEventListener('click', confirmDelete);
    
    // Search
    document.getElementById('roomTypeSearchInput')?.addEventListener('keyup', searchRoomTypes);
}

async function loadRoomTypes() {
    try {        
        const response = await APIInterceptor.fetch(`${ADMIN_URL}room-type/list/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success && data.data) {
            console.log('Room types data:', data.data);
            allRoomTypes = data.data;
            displayRoomTypesAsCards(data.data);
        } else {
            console.error('Failed to load room types:', data.message);
        }
    } catch (error) {
        console.error('Error fetching room types:', error);
    }
}

function displayRoomTypesAsCards(roomTypes) {
    const container = document.getElementById('roomTypesContainer');
    if (!container) return;
    
    if (roomTypes.length === 0) {
        container.style.display = 'flex';
        container.style.alignItems = 'center';
        container.style.justifyContent = 'center';
        container.style.minHeight = '400px';
        container.innerHTML = `
            <div style="text-align: center; color: var(--text-muted); padding: 3rem;">
                <i class="fas fa-door-open" style="font-size: 3rem; margin-bottom: 1rem; display: block; color: var(--text-muted);"></i>
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">No room types found</p>
                <p style="margin-bottom: 1.5rem; color: var(--text-muted);">Create a new room type to get started.</p>
                <button class="btn btn-primary" onclick="openCreateModal()"><i class="fas fa-plus" style="margin-right: 0.5rem;"></i>Create Room Type</button>
            </div>
        `;
        return;
    }
    
    container.innerHTML = roomTypes.map(type => {
        let amenitiesList = [];
        if (Array.isArray(type.amenities)) {
            amenitiesList = type.amenities;
        } else if (typeof type.amenities === 'string' && type.amenities.trim()) {
            amenitiesList = type.amenities.split(',');
        } else {
            amenitiesList = [];
        }
        
        return `
        <div class="room-type-card" style="${type.is_deleted ? 'opacity: 0.6; border: 2px solid #ff6b6b;' : ''}">
            <div class="room-type-card-header">
                <div class="room-type-name">${type.name} ${type.is_deleted ? '<span style="color: #ff6b6b; font-size: 0.8em; margin-left: 0.5rem;">(Deleted)</span>' : ''}</div>
                <div class="room-type-actions">
                    <button class="icon-btn edit-room-type-btn" title="Edit" data-id="${type.id}" onclick="openEditModal(${type.id})" ${type.is_deleted ? 'disabled style="opacity: 0.5; cursor: not-allowed;"' : ''}>
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="icon-btn ${type.is_deleted ? 'reactivate-room-type-btn' : 'delete-room-type-btn'}" title="${type.is_deleted ? 'Reactivate' : 'Delete'}" data-id="${type.id}" onclick="openDeleteModal(${type.id})">
                        <i class="fas fa-${type.is_deleted ? 'undo' : 'trash'}"></i>
                    </button>
                </div>
            </div>
            <div class="room-type-card-body">
                <div class="room-type-price">
                    <span class="price-label">₦</span>
                    <span class="price-value">${type.base_price ? type.base_price.toLocaleString() : '0'}</span>
                    <span class="price-period">/night</span>
                </div>
                <div class="room-type-info">
                    <span class="info-label">Max Occupancy:</span>
                    <span class="info-value">${type.max_occupancy || 0} Guests</span>
                </div>
                ${type.total_rooms ? `
                <div class="room-type-info">
                    <span class="info-label">Total Rooms:</span>
                    <span class="info-value">${type.total_rooms}</span>
                </div>
                ` : ''}
                <div class="room-type-description">
                    ${type.description || 'No description available'}
                </div>
                <div class="room-type-amenities">
                    <span class="amenities-label">Amenities:</span>
                    <div class="amenities-list">
                        ${amenitiesList.map(a => `<span class="amenity-tag">${a.trim()}</span>`).join('')}
                    </div>
                </div>
            </div>
        </div>
    `}).join('');
}

function openCreateModal() {
    currentRoomTypeId = null;
    document.getElementById('modalTitle').textContent = 'Create New Room Type';
    document.getElementById('roomTypeForm').reset();
    document.getElementById('roomTypeModal').classList.add('active');
}

function openEditModal(roomTypeId) {
    const roomType = allRoomTypes.find(r => r.id === roomTypeId);
    if (!roomType) return;
    
    currentRoomTypeId = roomTypeId;
    document.getElementById('modalTitle').textContent = 'Edit Room Type';
    document.getElementById('roomTypeName').value = roomType.name;
    document.getElementById('basePrice').value = roomType.base_price;
    document.getElementById('maxOccupancy').value = roomType.max_occupancy;
    document.getElementById('roomTypeDescription').value = roomType.description || '';
    
    let amenitiesList = '';
    if (Array.isArray(roomType.amenities)) {
        amenitiesList = roomType.amenities.join(', ');
    } else if (typeof roomType.amenities === 'string') {
        amenitiesList = roomType.amenities;
    }
    document.getElementById('amenities').value = amenitiesList;
    
    document.getElementById('roomTypeModal').classList.add('active');
}

function closeRoomTypeModal() {
    document.getElementById('roomTypeModal').classList.remove('active');
    currentRoomTypeId = null;
}

function openDeleteModal(roomTypeId) {
    const roomType = allRoomTypes.find(r => r.id === roomTypeId);
    if (!roomType) return;
    
    currentRoomTypeId = roomTypeId;
    if (roomType.is_deleted) {
        document.getElementById('deleteMessage').textContent = `Are you sure you want to reactivate ${roomType.name}? It will be available again.`;
        document.getElementById('confirmDeleteBtn').textContent = 'Reactivate';
    } else {
        document.getElementById('deleteMessage').textContent = `Are you sure you want to delete ${roomType.name}? You can reactivate it later.`;
        document.getElementById('confirmDeleteBtn').textContent = 'Delete';
    }
    document.getElementById('deleteRoomTypeModal').classList.add('active');
}

function closeDeleteModal() {
    document.getElementById('deleteRoomTypeModal').classList.remove('active');
    currentRoomTypeId = null;
}

async function saveRoomType() {
    const name = document.getElementById('roomTypeName').value;
    const basePrice = document.getElementById('basePrice').value;
    const maxOccupancy = document.getElementById('maxOccupancy').value;
    const description = document.getElementById('roomTypeDescription').value;
    const amenitiesInput = document.getElementById('amenities').value;
    
    if (!name || !basePrice || !maxOccupancy) {
        showModal('Please fill in all required fields.', 'fail');
        return;
    }
    
    const amenities = amenitiesInput 
        ? amenitiesInput.split(',').map(a => a.trim()).filter(a => a)
        : [];
    
    const payload = {
        name: name,
        base_price: parseFloat(basePrice),
        max_occupancy: parseInt(maxOccupancy),
        description: description,
        amenities: amenities
    };
    
    try {
        let response;
        if (currentRoomTypeId) {
            // Update existing room type
            response = await APIInterceptor.fetch(`${ADMIN_URL}room-type/${currentRoomTypeId}/update/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                },
                body: JSON.stringify(payload)
            });
        } else {
            // Create new room type
            response = await APIInterceptor.fetch(`${ADMIN_URL}room-type/create/`, {
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
            showModal(currentRoomTypeId ? 'Room type updated successfully!' : 'Room type created successfully!', 'success');
            closeRoomTypeModal();
            loadRoomTypes();
        } else {
            showModal(data.message || 'Failed to save room type.', 'fail');
        }
    } catch (error) {
        console.error('Error saving room type:', error);
        showModal('Error saving room type. Please try again.', 'fail');
    }
}

async function confirmDelete() {
    if (!currentRoomTypeId) return;
    
    const roomType = allRoomTypes.find(r => r.id === currentRoomTypeId);
    if (!roomType) return;
    
    try {
        const response = await APIInterceptor.fetch(`${ADMIN_URL}room-type/${currentRoomTypeId}/delete/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success || response.ok) {
            showModal('Room type deleted successfully!', 'success');
            closeDeleteModal();
            loadRoomTypes();
        } else {
            showModal(data.message || 'Failed to delete room type.', 'fail');
        }
    } catch (error) {
        console.error('Error deleting room type:', error);
        showModal('Error deleting room type. Please try again.', 'fail');
    }
}

function searchRoomTypes(e) {
    const searchTerm = e.target.value.toLowerCase();
    
    if (!searchTerm) {
        displayRoomTypesAsCards(allRoomTypes);
        return;
    }
    
    const filteredRoomTypes = allRoomTypes.filter(roomType => 
        roomType.name?.toLowerCase().includes(searchTerm) ||
        roomType.description?.toLowerCase().includes(searchTerm)
    );
    
    displayRoomTypesAsCards(filteredRoomTypes);
}
