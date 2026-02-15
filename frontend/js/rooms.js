// Ensure main.js is loaded before running
let accessToken = null;
let allRooms = [];
let allFloors = [];
let allRoomTypes = [];
let currentRoomId = null;
let userRole = null;
let isAdmin = false;

if (typeof CookieManager === 'undefined') {
    console.error('CookieManager not found. Make sure main.js is loaded before rooms.js');
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
    loadFloorsAndTypes();
    loadRooms();
    setupEventListeners();
    setupRoleBasedAccess();
});



function setupRoleBasedAccess() {
    const createRoomBtn = document.getElementById('createRoomBtn');
    
    // Hide add room button for non-admin users
    if (!isAdmin && createRoomBtn) {
        createRoomBtn.style.display = 'none';
    }
}

function setupEventListeners() {
    // Create button
    document.getElementById('createRoomBtn')?.addEventListener('click', openCreateModal);
    
    // Modal controls
    document.getElementById('closeRoomModal')?.addEventListener('click', closeRoomModal);
    document.getElementById('cancelRoomBtn')?.addEventListener('click', closeRoomModal);
    document.getElementById('saveRoomBtn')?.addEventListener('click', saveRoom);
    
    // Delete modal controls
    document.getElementById('closeDeleteModal')?.addEventListener('click', closeDeleteModal);
    document.getElementById('cancelDeleteBtn')?.addEventListener('click', closeDeleteModal);
    document.getElementById('confirmDeleteBtn')?.addEventListener('click', confirmDelete);
    
    // Search
    document.getElementById('roomSearchInput')?.addEventListener('keyup', searchRooms);
}

async function loadFloorsAndTypes() {
    try {
        // Load floors
        const floorsResponse = await APIInterceptor.fetch(`${ADMIN_URL}floor/list/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        const floorsData = await floorsResponse.json();
        if (floorsData.is_success && floorsData.data) {
            allFloors = floorsData.data;
            populateFloorSelect();
        }

        // Load room types
        const typesResponse = await APIInterceptor.fetch(`${ADMIN_URL}room-type/list/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        const typesData = await typesResponse.json();
        if (typesData.is_success && typesData.data) {
            allRoomTypes = typesData.data;
            populateRoomTypeSelect();
        }
    } catch (error) {
        console.error('Error loading floors and types:', error);
    }
}

function populateFloorSelect() {
    const select = document.getElementById('floorSelect');
    if (!select) {
        return;
    }
    
    const options = allFloors.map(floor => {
        const isDeleted = floor.is_deleted ? 'disabled' : '';
        const deletedLabel = floor.is_deleted ? ' (Deleted)' : '';
        return `<option value="${floor.id}" ${isDeleted}>Floor ${floor.number}${deletedLabel}${floor.description ? ' - ' + floor.description : ''}</option>`;
    }).join('');
    
    select.innerHTML = '<option value="">Select a floor</option>' + options;
}

function populateRoomTypeSelect() {
    const select = document.getElementById('roomTypeSelect');
    if (!select) return;
    
    const options = allRoomTypes.map(type => {
        const isDeleted = type.is_deleted ? 'disabled' : '';
        const deletedLabel = type.is_deleted ? ' (Deleted)' : '';
        return `<option value="${type.id}" ${isDeleted}>${type.name}${deletedLabel} (₦${type.base_price?.toLocaleString() || '0'})</option>`;
    }).join('');
    
    select.innerHTML = '<option value="">Select room type</option>' + options;
}

async function loadRooms() {
    try {        
        const response = await APIInterceptor.fetch(`${ADMIN_URL}room/list/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success && data.data) {
            allRooms = data.data;
            displayRoomsAsCards(data.data);
        } else {
            console.error('Failed to load rooms:', data.message);
        }
    } catch (error) {
        console.error('Error fetching rooms:', error);
    }
}

function displayRoomsAsCards(rooms) {
    const container = document.getElementById('roomsContainer');
    if (!container) return;
    
    if (rooms.length === 0) {
        container.style.display = 'flex';
        container.style.alignItems = 'center';
        container.style.justifyContent = 'center';
        container.style.minHeight = '400px';
        container.innerHTML = `
            <div style="text-align: center; color: var(--text-muted); padding: 3rem;">
                <i class="fas fa-door-open" style="font-size: 3rem; margin-bottom: 1rem; display: block; color: var(--text-muted);"></i>
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">No rooms found</p>
                <p style="margin-bottom: 1.5rem; color: var(--text-muted);">Create a new room to get started.</p>
                <button class="btn btn-primary" onclick="openCreateModal()"><i class="fas fa-plus" style="margin-right: 0.5rem;"></i>Create Room</button>
            </div>
        `;
        return;
    }
    
    container.innerHTML = rooms.map(room => `
        <div class="room-card" style="${room.is_deleted ? 'opacity: 0.6; border: 2px solid #ff6b6b;' : ''}">
            <div class="room-card-header">
                <div class="room-number">Room ${room.number} ${room.is_deleted ? '<span style="color: #ff6b6b; font-size: 0.8em; margin-left: 0.5rem;">(Deleted)</span>' : ''}</div>
                <div class="status-badge status-${room.status?.toLowerCase()}">
                    <i class="fas fa-circle"></i>
                    ${room.status?.charAt(0).toUpperCase() + room.status?.slice(1).toLowerCase() || 'Available'}
                </div>
                <div class="room-actions">
                    <button class="icon-btn edit-room-btn" title="Edit" data-id="${room.id}" onclick="openEditModal(${room.id})" ${room.is_deleted ? 'disabled style="opacity: 0.5; cursor: not-allowed;"' : ''}>
                        <i class="fas fa-edit"></i>
                    </button>
                    ${isAdmin ? `
                    <button class="icon-btn ${room.is_deleted ? 'reactivate-room-btn' : 'delete-room-btn'}" title="${room.is_deleted ? 'Reactivate' : 'Delete'}" data-id="${room.id}" onclick="openDeleteModal(${room.id})">
                        <i class="fas fa-${room.is_deleted ? 'undo' : 'trash'}"></i>
                    </button>
                    ` : ''}
                </div>
            </div>
            <div class="room-card-body">
                <div class="room-info">
                    <span class="info-label">Floor:</span>
                    <span class="info-value">Floor ${room.floor_number || 'N/A'}</span>
                </div>
                <div class="room-info">
                    <span class="info-label">Type:</span>
                    <span class="info-value">${room.room_type_name || 'N/A'}</span>
                </div>
                <div class="room-info">
                    <span class="info-label">Capacity:</span>
                    <span class="info-value">${room.max_occupancy || 0} Guests</span>
                </div>
                <div class="room-price">
                    ${room.price_override ? `
                        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                            <div style="display: flex; align-items: baseline; gap: 0.25rem;">
                                <span class="price-label">₦</span>
                                <span class="price-value">${room.price_override.toLocaleString()}</span>
                                <span class="price-override-badge">Override</span>
                            </div>
                            <div style="display: flex; align-items: baseline; gap: 0.25rem; opacity: 0.6; text-decoration: line-through;">
                                <span class="price-label">₦</span>
                                <span style="font-size: 0.85rem;">${(room.base_price || 0).toLocaleString()}</span>
                            </div>
                        </div>
                    ` : `
                        <div style="display: flex; align-items: baseline; gap: 0.25rem;">
                            <span class="price-label">₦</span>
                            <span class="price-value">${(room.base_price || 0).toLocaleString()}</span>
                        </div>
                    `}
                </div>
                ${room.notes ? `
                <div class="room-notes">
                    <span class="notes-label">Notes:</span>
                    <span class="notes-value">${room.notes}</span>
                </div>
                ` : ''}
            </div>
        </div>
    `).join('');
}

function openCreateModal() {
    currentRoomId = null;
    document.getElementById('modalTitle').textContent = 'Create New Room';
    document.getElementById('roomForm').reset();
    
    // Disable OCCUPIED option when creating new room
    const statusSelect = document.getElementById('statusSelect');
    if (statusSelect) {
        const occupiedOption = Array.from(statusSelect.options).find(opt => opt.value === 'OCCUPIED');
        if (occupiedOption) {
            occupiedOption.disabled = true;
        }
    }
    
    document.getElementById('roomModal').classList.add('active');
}

function openEditModal(roomId) {
    const room = allRooms.find(r => r.id === roomId);
    if (!room) {
        return;
    }
    
    currentRoomId = roomId;
    document.getElementById('modalTitle').textContent = 'Edit Room';
    document.getElementById('roomNumber').value = room.number;
    
    const floorSelect = document.getElementById('floorSelect');
    
    if (!floorSelect) {
        return;
    }
    
    let found = false;
    for (let i = 0; i < floorSelect.options.length; i++) {
        if (parseInt(floorSelect.options[i].value) === room.floor) {
            floorSelect.selectedIndex = i;
            found = true;
            break;
        }
    }
    
    if (!found) {
        const floorExists = allFloors.find(f => f.id === room.floor);
        if (floorExists) {
            const newOption = document.createElement('option');
            newOption.value = floorExists.id;
            newOption.text = `Floor ${floorExists.number}${floorExists.description ? ' - ' + floorExists.description : ''}`;
            floorSelect.appendChild(newOption);
            floorSelect.value = floorExists.id;
        } else {
            const newOption = document.createElement('option');
            newOption.value = room.floor;
            newOption.text = `Floor ${room.floor_number} (Current)`;
            newOption.selected = true;
            floorSelect.appendChild(newOption);
        }
    }
    
    document.getElementById('roomTypeSelect').value = room.room_type || '';
    
    const statusSelect = document.getElementById('statusSelect');
    if (statusSelect) {
        // Disable OCCUPIED option unless it's the current room's status
        const occupiedOption = Array.from(statusSelect.options).find(opt => opt.value === 'OCCUPIED');
        if (occupiedOption) {
            occupiedOption.disabled = room.status !== 'OCCUPIED';
        }
        if (room.status) {
            statusSelect.value = room.status;
        }
    }
    
    document.getElementById('priceOverride').value = room.price_override || '';
    document.getElementById('roomNotes').value = room.notes || '';
    
    document.getElementById('roomModal').classList.add('active');
}

function closeRoomModal() {
    document.getElementById('roomModal').classList.remove('active');
    currentRoomId = null;
}

function openDeleteModal(roomId) {
    const room = allRooms.find(r => r.id === roomId);
    if (!room) return;
    
    currentRoomId = roomId;
    if (room.is_deleted) {
        document.getElementById('deleteMessage').textContent = `Are you sure you want to reactivate Room ${room.number}? It will be available again.`;
        document.getElementById('confirmDeleteBtn').textContent = 'Reactivate';
    } else {
        document.getElementById('deleteMessage').textContent = `Are you sure you want to delete Room ${room.number}? You can reactivate it later.`;
        document.getElementById('confirmDeleteBtn').textContent = 'Delete';
    }
    document.getElementById('deleteRoomModal').classList.add('active');
}

function closeDeleteModal() {
    document.getElementById('deleteRoomModal').classList.remove('active');
    currentRoomId = null;
}

async function saveRoom() {
    const roomNumber = document.getElementById('roomNumber').value;
    const floor = document.getElementById('floorSelect').value;
    const roomType = document.getElementById('roomTypeSelect').value;
    const status = document.getElementById('statusSelect').value;
    const priceOverride = document.getElementById('priceOverride').value;
    const notes = document.getElementById('roomNotes').value;
    
    if (!roomNumber || !floor || !roomType) {
        showModal('Please fill in all required fields.', 'fail');
        return;
    }
    
    const payload = {
        number: roomNumber,
        floor: parseInt(floor),
        room_type: parseInt(roomType),
        status: status,
        price_override: priceOverride ? parseFloat(priceOverride) : null,
        notes: notes
    };
    
    try {
        let response;
        if (currentRoomId) {
            // Update existing room
            response = await APIInterceptor.fetch(`${ADMIN_URL}room/${currentRoomId}/update/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                },
                body: JSON.stringify(payload)
            });
        } else {
            // Create new room
            response = await APIInterceptor.fetch(`${ADMIN_URL}room/create/`, {
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
            showModal(currentRoomId ? 'Room updated successfully!' : 'Room created successfully!', 'success');
            closeRoomModal();
            loadRooms();
        } else {
            showModal(data.message || 'Failed to save room.', 'fail');
        }
    } catch (error) {
        console.error('Error saving room:', error);
        showModal('Error saving room. Please try again.', 'fail');
    }
}

async function confirmDelete() {
    if (!currentRoomId) return;
    
    const room = allRooms.find(r => r.id === currentRoomId);
    if (!room) return;
    
    try {
        const response = await APIInterceptor.fetch(`${ADMIN_URL}room/${currentRoomId}/delete/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success || response.ok) {
            showModal('Room deleted successfully!', 'success');
            closeDeleteModal();
            loadRooms();
        } else {
            showModal(data.message || 'Failed to delete room.', 'fail');
        }
    } catch (error) {
        console.error('Error deleting room:', error);
        showModal('Error deleting room. Please try again.', 'fail');
    }
}

function searchRooms(e) {
    const searchTerm = e.target.value.toLowerCase();
    
    if (!searchTerm) {
        displayRoomsAsCards(allRooms);
        return;
    }
    
    const filteredRooms = allRooms.filter(room => 
        room.number?.toLowerCase().includes(searchTerm) ||
        room.room_type_name?.toLowerCase().includes(searchTerm) ||
        room.floor_name?.toLowerCase().includes(searchTerm) ||
        room.status?.toLowerCase().includes(searchTerm)
    );
    
    displayRoomsAsCards(filteredRooms);
}
