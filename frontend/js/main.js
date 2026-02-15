const themeToggle = document.getElementById('themeToggle');
if (themeToggle) {
    const themeIcon = themeToggle.querySelector('i');

    // Check for saved theme preference or default to light
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);

    if (currentTheme === 'dark') {
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
    }

    themeToggle.addEventListener('click', function() {
        let theme = document.documentElement.getAttribute('data-theme');
        
        if (theme === 'light') {
            document.documentElement.setAttribute('data-theme', 'dark');
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
            themeIcon.classList.remove('fa-sun');
            themeIcon.classList.add('fa-moon');
            localStorage.setItem('theme', 'light');
        }
    });
}

/* ============================================
   SIDEBAR NAVIGATION - Available on all pages
   ============================================ */

// Navigation items structure
const navItems = [
    { href: 'dashboard.html', icon: 'fa-home', label: 'Dashboard' },
    { href: 'hotels.html', icon: 'fa-building', label: 'Hotels' },
    { href: 'floors.html', icon: 'fa-layer-group', label: 'Floors' },
    { href: 'room-types.html', icon: 'fa-door-open', label: 'Room Types' },
    { href: 'rooms.html', icon: 'fa-key', label: 'Rooms' },
    { href: 'guests.html', icon: 'fa-users', label: 'Guests' },
    { href: 'bookings.html', icon: 'fa-calendar-check', label: 'Bookings' },
    { href: 'invoices.html', icon: 'fa-file-invoice', label: 'Invoices' },
    { href: 'payments.html', icon: 'fa-credit-card', label: 'Payments' },
    { href: 'reports.html', icon: 'fa-chart-bar', label: 'Reports' },
    { href: 'staff.html', icon: 'fa-user-tie', label: 'Staff' },
    { href: 'audit.html', icon: 'fa-clipboard-list', label: 'Audit Logs', adminOnly: true },
    { href: 'backups.html', icon: 'fa-database', label: 'Backups', adminOnly: true },
    { href: 'settings.html', icon: 'fa-cogs', label: 'Settings' }
];

// Get filtered nav items based on user group
function getFilteredNavItems() {
    const userGroup = CookieManager.get('user_group');
    
    // If no user group or admin, show all items
    if (!userGroup || userGroup === 'Admin') {
        return navItems;
    }
    
    // For staff, exclude hotels, staff, settings, and admin-only items
    if (userGroup === 'Staff') {
        return navItems.filter(item => 
            item.href !== 'hotels.html' && 
            item.href !== 'staff.html' &&
            !item.adminOnly
        );
    }
    
    // For other roles, filter out admin-only items
    return navItems.filter(item => !item.adminOnly);
}

// Get current page filename
function getCurrentPage() {
    const href = window.location.href;
    const filename = href.substring(href.lastIndexOf('/') + 1) || 'dashboard.html';
    return filename;
}

// Initialize sidebar navigation
function initSidebarNav() {
    const sidebarNav = document.querySelector('.sidebar-nav');
    if (!sidebarNav) return;
    
    const currentPage = getCurrentPage();
    const filteredItems = getFilteredNavItems();
    
    // Generate navigation HTML
    let navHTML = '';
    filteredItems.forEach(item => {
        const isActive = item.href === currentPage ? ' active' : '';
        navHTML += `
            <a href="${item.href}" class="nav-item${isActive}">
                <i class="fas ${item.icon}"></i>
                <span>${item.label}</span>
            </a>
        `;
    });
    
    // Clear existing nav items and insert new ones
    sidebarNav.innerHTML = navHTML;
}

function initSidebar() {
    // Initialize sidebar navigation
    initSidebarNav();
    
    // Initialize sidebar collapse functionality
    const desktopSidebarToggle = document.getElementById('desktopSidebarToggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (desktopSidebarToggle && sidebar) {
        desktopSidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
            // Save state to localStorage
            const isCollapsed = sidebar.classList.contains('collapsed');
            localStorage.setItem('sidebarCollapsed', isCollapsed);
        });

        // Restore sidebar state from localStorage
        const sidebarCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
        if (sidebarCollapsed) {
            sidebar.classList.add('collapsed');
        }
    }
}

// Initialize sidebar when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initSidebar();
    
    // Particles animation on auth pages
    const particlesContainer = document.getElementById('particles');
    if (particlesContainer) {
        const particleCount = 50;

        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            
            // Random properties
            const size = Math.random() * 5 + 2;
            const posX = Math.random() * 100;
            const posY = Math.random() * 100;
            const delay = Math.random() * 15;
            const duration = Math.random() * 10 + 15;
            
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            particle.style.left = `${posX}%`;
            particle.style.top = `${posY}%`;
            particle.style.animationDelay = `${delay}s`;
            particle.style.animationDuration = `${duration}s`;
            
            particlesContainer.appendChild(particle);
        }
    }
});


function showPreloader() {
    const preload = document.getElementById('preloader');
    preload.style.opacity = '1';
    preload.style.visibility = 'visible';
}

function hidePreloader() {
    const preload = document.getElementById('preloader');
    preload.style.opacity = '0';
    preload.style.visibility = 'hidden';
}


// Cookie Management Utilities
const CookieManager = {
    set: function(name, value, days = 7) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        const expires = "expires=" + date.toUTCString();
        document.cookie = `${name}=${value};${expires};path=/;SameSite=Lax`;
    },
    
    get: function(name) {
        const nameEQ = name + "=";
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i];
            while (cookie.charAt(0) === ' ') cookie = cookie.substring(1);
            if (cookie.indexOf(nameEQ) === 0) {
                return cookie.substring(nameEQ.length, cookie.length);
            }
        }
        return null;
    },
    
    delete: function(name) {
        document.cookie = `${name}=;expires=Thu, 01 Jan 1970 00:00:00 UTC;path=/;`;
    },
    
    clearAuth: function() {
        this.delete('access_token');
        this.delete('refresh_token');
        this.delete('admin_username');
        this.delete('admin_email');
        this.delete('admin_first_name');
        this.delete('admin_last_name');
    },
    
    clearUserSession: function() {
        this.delete('access_token');
        this.delete('refresh_token');
        this.delete('username');
        this.delete('email');
        this.delete('user_name');
        this.delete('id_number');
        this.delete('is_staff');
        this.delete('is_superuser');
        this.delete('user_group');
        this.delete('group_id');
        this.delete('csrftoken');
        this.delete('group');
        this.delete('name');
        this.delete('refresh');
    }
};

// Error display function
function showError(message, formElement) {
    // Use provided formElement or try to find loginForm
    const targetForm = formElement || document.getElementById('loginForm');
    if (!targetForm) {
        console.error('Form element not found for error display');
        return;
    }
    
    // Remove any existing error
    const existingError = targetForm.parentElement.querySelector('.form-error');
    if (existingError) {
        existingError.remove();
    }
    
    // Create error element
    const errorElement = document.createElement('div');
    errorElement.className = 'form-error';
    errorElement.innerHTML = `
        <i class="fas fa-exclamation-circle"></i>
        <span>${message}</span>
    `;
    errorElement.style.cssText = `
        background: rgba(255, 0, 0, 0.1);
        border: 1px solid rgba(255, 0, 0, 0.2);
        color: #ff2e63;
        padding: 0.8rem 1rem;
        border-radius: 8px;
        margin-top: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.9rem;
    `;
    
    // Insert after the form
    targetForm.appendChild(errorElement);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        if (errorElement.parentNode) {
            errorElement.remove();
        }
    }, 3000);
}

// Modal function - handles success, fail, and info
function showModal(message, type = 'info', redirectUrl = null, duration = 3000) {
    // Define modal configurations based on type
    const configs = {
        success: {
            icon: 'fa-check-circle',
            color: '#4CAF50',
            title: 'Success!',
            bgColor: 'rgba(76, 175, 80, 0.1)'
        },
        fail: {
            icon: 'fa-exclamation-circle',
            color: '#ff2e63',
            title: 'Error!',
            bgColor: 'rgba(255, 46, 99, 0.1)'
        },
        info: {
            icon: 'fa-info-circle',
            color: '#2196F3',
            title: 'Information',
            bgColor: 'rgba(33, 150, 243, 0.1)'
        }
    };
    
    const config = configs[type] || configs.info;
    
    // Create modal overlay
    const modalOverlay = document.createElement('div');
    modalOverlay.className = 'modal-overlay';
    modalOverlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.6);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
        animation: fadeIn 0.3s ease;
    `;
    
    // Create modal content
    const modalContent = document.createElement('div');
    modalContent.className = 'modal-content';
    modalContent.style.cssText = `
        background: var(--card-bg);
        border-radius: 16px;
        padding: 2rem;
        max-width: 400px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        animation: slideUp 0.3s ease;
        border-left: 4px solid ${config.color};
        position: relative;
    `;
    
    // Modal HTML
    modalContent.innerHTML = `
        <button class="modal-close-btn" style="position: absolute; top: 1rem; right: 1rem; background: none; border: none; font-size: 1.5rem; color: var(--text-muted); cursor: pointer; padding: 0.5rem; display: flex; align-items: center; justify-content: center;">
            <i class="fas fa-times"></i>
        </button>
        <div style="margin-bottom: 1.5rem; background: ${config.bgColor}; padding: 1rem; border-radius: 50%; display: inline-block; width: 80px; height: 80px; display: flex; align-items: center; justify-content: center;">
            <i class="fas ${config.icon}" style="font-size: 2.5rem; color: ${config.color};"></i>
        </div>
        <h2 style="color: var(--text); margin: 1.5rem 0 1rem; font-size: 1.5rem;">${config.title}</h2>
        <p style="color: var(--text-muted); margin-bottom: 1.5rem; line-height: 1.6;">${message}</p>
        ${redirectUrl ? '<div style="color: var(--text-muted); font-size: 0.9rem;"><i class="fas fa-spinner fa-spin"></i> Redirecting in ' + (duration / 1000) + ' seconds...</div>' : ''}
    `;
    
    modalOverlay.appendChild(modalContent);
    document.body.appendChild(modalOverlay);
    
    // Add close button functionality
    const closeBtn = modalContent.querySelector('.modal-close-btn');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            if (modalOverlay.parentNode) {
                modalOverlay.remove();
            }
        });
    }
    
    // Close modal when clicking on overlay background
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) {
            if (modalOverlay.parentNode) {
                modalOverlay.remove();
            }
        }
    });
    if (!document.querySelector('style[data-modal-animation]')) {
        const style = document.createElement('style');
        style.setAttribute('data-modal-animation', 'true');
        style.textContent = `
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @keyframes slideUp {
                from { transform: translateY(30px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Auto redirect after specified duration if URL provided
    if (redirectUrl) {
        setTimeout(() => {
            if (modalOverlay.parentNode) {
                modalOverlay.remove();
            }
            window.location.href = redirectUrl;
        }, duration);
    }
    
    return modalOverlay;
}


const username = CookieManager.get('admin_username')
const userGroup = CookieManager.get('user_group')
const userSpan = document.querySelector('profile-name');
const userRoleSpan = document.querySelector('.profile-role');

if (username && userSpan) {
    userSpan.innerHTML = username;
}

if (userGroup && userRoleSpan) {
    userRoleSpan.innerHTML = userGroup;
}

const USER_URL = "http://127.0.0.1:8000/auth/api/user/";
const HOSTEL_URL = "http://127.0.0.1:8000/hotel/api/hotel/";
const ADMIN_URL = "http://127.0.0.1:8000/admin/api/";

// Humanize date function - Convert date to relative time (e.g., "2 days ago")
function humanizeDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = now - date;
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) {
        return 'Today';
    } else if (diffDays === 1) {
        return 'Yesterday';
    } else if (diffDays < 7) {
        return `${diffDays} days ago`;
    } else if (diffDays < 30) {
        const weeks = Math.floor(diffDays / 7);
        return `${weeks} week${weeks > 1 ? 's' : ''} ago`;
    } else if (diffDays < 365) {
        const months = Math.floor(diffDays / 30);
        return `${months} month${months > 1 ? 's' : ''} ago`;
    } else {
        const years = Math.floor(diffDays / 365);
        return `${years} year${years > 1 ? 's' : ''} ago`;
    }
}
// Global API Fetch Wrapper - Handles 40x errors and redirects to login
const APIInterceptor = {
    isAuthPage: function() {
        const currentPage = window.location.href;
        return currentPage.includes('auth.html') || currentPage.includes('/auth');
    },
    
    storeReturnUrl: function() {
        const currentPage = window.location.href;
        if (!this.isAuthPage()) {
            sessionStorage.setItem('returnUrl', currentPage);
        }
    },
    
    getReturnUrl: function() {
        return sessionStorage.getItem('returnUrl') || 'dashboard.html';
    },
    
    clearReturnUrl: function() {
        sessionStorage.removeItem('returnUrl');
    },
    
    handleUnauthorized: function() {
        // Don't redirect if already on auth page
        if (this.isAuthPage()) {
            return;
        }
        
        // Store current page before redirecting
        this.storeReturnUrl();
        
        // Clear user session
        CookieManager.clearUserSession();
        
        // Redirect to login page
        window.location.href = 'auth.html';
    },
    
    fetch: async function(url, options = {}) {
        try {
            const response = await fetch(url, options);
            
            // Check for authentication-related errors (401 Unauthorized, 403 Forbidden)
            if (response.status === 401 || response.status === 403) {
                // Call the unauthorized handler
                this.handleUnauthorized();
                // Return a rejected promise to prevent further processing
                throw new Error(`HTTP Error ${response.status}`);
            }
            
            return response;
        } catch (error) {
            console.error('API Fetch Error:', error);
            throw error;
        }
    }
};

// Store return URL when page loads (except on auth page)
document.addEventListener('DOMContentLoaded', function() {
    APIInterceptor.storeReturnUrl();
    
    // Setup logout button functionality
    setupLogoutButton();
});

// Logout Function - Clear session and redirect to login
function performLogout() {
    // Clear user session cookies
    CookieManager.clearUserSession();
    
    // Show logout modal
    showModal('You have been logged out successfully. Redirecting to login page...', 'success', 'auth.html', 2000);
}

// Setup logout button click handler
function setupLogoutButton() {
    const logoutBtn = document.querySelector('.logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            performLogout();
        });
    }
}