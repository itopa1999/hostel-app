// Ensure main.js is loaded before running
let accessToken = null;
let allFloors = [];
let currentFloorId = null;

if (typeof CookieManager === 'undefined') {
    console.error('CookieManager not found. Make sure main.js is loaded before floors.js');
    window.location.href = "auth.html";
} else {
    accessToken = CookieManager.get("access_token");
    if (!accessToken) {
        window.location.href = "auth.html";
    }
}

document.addEventListener('DOMContentLoaded', function() {
    hidePreloader();
    loadFloors();
    setupEventListeners();
});



function setupEventListeners() {
    // Create button
    document.getElementById('createFloorBtn')?.addEventListener('click', openCreateModal);
    
    // Modal controls
    document.getElementById('closeFloorModal')?.addEventListener('click', closeFloorModal);
    document.getElementById('cancelFloorBtn')?.addEventListener('click', closeFloorModal);
    document.getElementById('saveFloorBtn')?.addEventListener('click', saveFloor);
    
    // Delete modal controls
    document.getElementById('closeDeleteModal')?.addEventListener('click', closeDeleteModal);
    document.getElementById('cancelDeleteBtn')?.addEventListener('click', closeDeleteModal);
    document.getElementById('confirmDeleteBtn')?.addEventListener('click', confirmDelete);
    
    // Search
    document.getElementById('floorSearchInput')?.addEventListener('keyup', searchFloors);
}

async function loadFloors() {
    try {        
        const response = await APIInterceptor.fetch(`${ADMIN_URL}floor/list/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success && data.data) {
            console.log('Floors data:', data.data);
            allFloors = data.data;
            displayFloorsAsCards(data.data);
        } else {
            console.error('Failed to load floors:', data.message);
            showModal('Failed to load floors. Please refresh the page.', 'fail');
        }
    } catch (error) {
        console.error('Error fetching floors:', error);
        showModal('Error loading floors. Please check your connection.', 'fail');
    }
}

function displayFloorsAsCards(floors) {
    const container = document.getElementById('floorsContainer');
    if (!container) return;
    
    if (floors.length === 0) {
        container.style.display = 'flex';
        container.style.alignItems = 'center';
        container.style.justifyContent = 'center';
        container.style.minHeight = '400px';
        container.innerHTML = `
            <div style="text-align: center; color: var(--text-muted); padding: 3rem;">
                <i class="fas fa-building" style="font-size: 3rem; margin-bottom: 1rem; display: block; color: var(--text-muted);"></i>
                <p style="font-size: 1.1rem; margin-bottom: 1rem;">No floors found</p>
                <p style="margin-bottom: 1.5rem; color: var(--text-muted);">Create a new floor to get started.</p>
                <button class="btn btn-primary" onclick="openCreateModal()"><i class="fas fa-plus" style="margin-right: 0.5rem;"></i>Create Floor</button>
            </div>
        `;
        return;
    }
    
    container.innerHTML = floors.map(floor => `
        <div class="floor-card" style="${floor.is_deleted ? 'opacity: 0.6; border: 2px solid #ff6b6b;' : ''}">
            <div class="floor-card-header">
                <div class="floor-number">Floor ${floor.number} ${floor.is_deleted ? '<span style="color: #ff6b6b; font-size: 0.8em; margin-left: 0.5rem;">(Deleted)</span>' : ''}</div>
                <div class="floor-actions">
                    <button class="icon-btn edit-floor-btn" title="Edit" data-id="${floor.id}" onclick="openEditModal(${floor.id})" ${floor.is_deleted ? 'disabled style="opacity: 0.5; cursor: not-allowed;"' : ''}>
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="icon-btn ${floor.is_deleted ? 'reactivate-floor-btn' : 'delete-floor-btn'}" title="${floor.is_deleted ? 'Reactivate' : 'Delete'}" data-id="${floor.id}" onclick="openDeleteModal(${floor.id})">
                        <i class="fas fa-${floor.is_deleted ? 'undo' : 'trash'}"></i>
                    </button>
                </div>
            </div>
            <div class="floor-card-body">
                <div class="floor-info">
                    <span class="info-label">Description:</span>
                    <span class="info-value">${floor.description || 'No description'}</span>
                </div>
                <div class="floor-info">
                    <span class="info-label">Total Rooms:</span>
                    <span class="info-value">${floor.total_rooms || 0}</span>
                </div>
                <div class="floor-info">
                    <span class="info-label">Occupied:</span>
                    <span class="info-value">${floor.occupied_rooms || 0}</span>
                </div>
            </div>
        </div>
    `).join('');
}

function openCreateModal() {
    currentFloorId = null;
    document.getElementById('modalTitle').textContent = 'Create New Floor';
    document.getElementById('floorForm').reset();
    document.getElementById('floorModal').classList.add('active');
}

function openEditModal(floorId) {
    const floor = allFloors.find(f => f.id === floorId);
    if (!floor) return;
    
    currentFloorId = floorId;
    document.getElementById('modalTitle').textContent = 'Edit Floor';
    document.getElementById('floorNumber').value = floor.number;
    document.getElementById('floorDescription').value = floor.description || '';
    document.getElementById('floorModal').classList.add('active');
}

function closeFloorModal() {
    document.getElementById('floorModal').classList.remove('active');
    currentFloorId = null;
}

function openDeleteModal(floorId) {
    const floor = allFloors.find(f => f.id === floorId);
    if (!floor) return;
    
    currentFloorId = floorId;
    if (floor.is_deleted) {
        document.getElementById('deleteMessage').textContent = `Are you sure you want to reactivate Floor ${floor.number}? It will be available again.`;
        document.getElementById('confirmDeleteBtn').textContent = 'Reactivate';
    } else {
        document.getElementById('deleteMessage').textContent = `Are you sure you want to delete Floor ${floor.number}? You can reactivate it later.`;
        document.getElementById('confirmDeleteBtn').textContent = 'Delete';
    }
    document.getElementById('deleteFloorModal').classList.add('active');
}

function closeDeleteModal() {
    document.getElementById('deleteFloorModal').classList.remove('active');
    currentFloorId = null;
}

async function saveFloor() {
    const floorNumber = document.getElementById('floorNumber').value;
    const description = document.getElementById('floorDescription').value;
    
    if (!floorNumber) {
        showModal('Please enter a floor number.', 'fail');
        return;
    }
    
    const payload = {
        number: parseInt(floorNumber),
        description: description
    };
    
    try {
        let response;
        if (currentFloorId) {
            // Update existing floor
            response = await APIInterceptor.fetch(`${ADMIN_URL}floor/${currentFloorId}/update/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                },
                body: JSON.stringify(payload)
            });
        } else {
            // Create new floor
            response = await APIInterceptor.fetch(`${ADMIN_URL}floor/create/`, {
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
            showModal(currentFloorId ? 'Floor updated successfully!' : 'Floor created successfully!', 'success');
            closeFloorModal();
            loadFloors();
        } else {
            showModal(data.message || 'Failed to save floor.', 'fail');
        }
    } catch (error) {
        console.error('Error saving floor:', error);
        showModal('Error saving floor. Please try again.', 'fail');
    }
}

async function confirmDelete() {
    if (!currentFloorId) return;
    
    try {
        const response = await APIInterceptor.fetch(`${ADMIN_URL}floor/${currentFloorId}/delete/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });
        
        const data = await response.json();
        
        if (data.is_success || response.ok) {
            showModal('Floor deleted successfully!', 'success');
            closeDeleteModal();
            loadFloors();
        } else {
            showModal(data.message || 'Failed to delete floor.', 'fail');
        }
    } catch (error) {
        console.error('Error deleting floor:', error);
        showModal('Error deleting floor. Please try again.', 'fail');
    }
}

function searchFloors(e) {
    const searchTerm = e.target.value.toLowerCase();
    
    if (!searchTerm) {
        displayFloorsAsCards(allFloors);
        return;
    }
    
    const filteredFloors = allFloors.filter(floor => 
        floor.number?.toString().includes(searchTerm) ||
        floor.description?.toLowerCase().includes(searchTerm)
    );
    
    displayFloorsAsCards(filteredFloors);
}