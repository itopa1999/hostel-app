document.addEventListener('DOMContentLoaded', function() {
    // Form submission handling
    const authForm = document.getElementById('loginForm');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const roleInput = document.getElementById('role');
    
    // Store fetched groups for later use
    let fetchedGroups = [];
    
    fetchUserGroups();
    
    function fetchUserGroups() {
        APIInterceptor.fetch(`${USER_URL}groups/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.is_success && data.data.groups) {
                    const groups = data.data.groups;
                    fetchedGroups = groups; // Store groups for redirect determination
                    // Clear default options and populate with fetched groups
                    roleInput.innerHTML = '<option value="" disabled selected>Select your role</option>';
                    groups.forEach(group => {
                        const option = document.createElement('option');
                        option.value = group.name.toLowerCase();
                        option.textContent = group.name;
                        option.dataset.groupId = group.id;
                        option.dataset.groupName = group.name.toLowerCase();
                        roleInput.appendChild(option);
                    });
                }
            })
            .catch(error => {
                console.error('Error fetching groups:', error);
            });
    }
    
    authForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const username = usernameInput.value.trim();
        const password = passwordInput.value;
        const role = roleInput.value;
        
        // Clear previous errors
        document.getElementById('username-error').style.display = 'none';
        document.getElementById('password-error').style.display = 'none';
        document.getElementById('role-error').style.display = 'none';
        
        if (!username) {
            document.getElementById('username-error').style.display = 'flex';
            return;
        }
        
        // if (password.length < 6) {
        //     document.getElementById('password-error').style.display = 'flex';
        //     return;
        // }
        
        if (!role) {
            document.getElementById('role-error').style.display = 'flex';
            return;
        }
        
        const submitButton = authForm.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;
        submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Logging in...</span>';
        submitButton.disabled = true;
        
        loginUser(username, password, role, submitButton, originalText);
    });
    
    [usernameInput, passwordInput, roleInput].forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });
    });
    
    function loginUser(username, password, role, submitButton, originalText) {
        const roleOption = roleInput.querySelector(`option[value="${role}"]`);
        const selectedGroupId = roleOption ? parseInt(roleOption.dataset.groupId) : 2;
        
        const loginPayload = {
            username: username,
            password: password,
            group_id: selectedGroupId
        };

        
        APIInterceptor.fetch(`${USER_URL}login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(loginPayload)
        })
        .then(response => response.json())
        .then(data => {
            if (data.is_success && data.data) {
                // Check if user has the selected group
                let userGroup = null;
                if (data.data.groups && data.data.groups.length > 0) {
                    // Find the selected group in user's groups
                    userGroup = data.data.groups.find(g => g.id === selectedGroupId);
                    
                    // If selected group not found in user's groups, check if any group exists
                    if (!userGroup) {
                        CookieManager.clearUserSession();
                        showError('You do not have access to this group. Please select an authorized role.', authForm);
                        submitButton.innerHTML = originalText;
                        submitButton.disabled = false;
                        return;
                    }
                } else {
                    // No groups found
                    CookieManager.clearUserSession();
                    showError('No groups assigned. Please contact administrator.', authForm);
                    submitButton.innerHTML = originalText;
                    submitButton.disabled = false;
                    return;
                }
                
                // Save tokens and user data to cookies (5-day expiration)
                CookieManager.set('access_token', data.data.access, 5);
                CookieManager.set('refresh_token', data.data.refresh, 5);
                CookieManager.set('username', data.data.username, 5);
                CookieManager.set('email', data.data.email, 5);
                CookieManager.set('user_name', data.data.name, 5);
                CookieManager.set('id_number', data.data.id_number, 5);
                CookieManager.set('is_staff', data.data.is_staff.toString(), 5);
                CookieManager.set('is_superuser', data.data.is_superuser.toString(), 5);
                CookieManager.set('user_group', userGroup.name, 5);
                CookieManager.set('group_id', selectedGroupId.toString(), 5);
                
                // Clear the return URL from previous session
                APIInterceptor.clearReturnUrl();
                
                // Determine redirect page based on selected group ID
                // Check if there's a stored return URL from previous page
                let returnUrl = sessionStorage.getItem('returnUrl');
                if (returnUrl && !returnUrl.includes('auth.html')) {
                    // User came from a page - redirect back there
                    sessionStorage.removeItem('returnUrl');
                    showModal(`Welcome, ${data.data.name}. Redirecting back...`, 'success', returnUrl, 5000);
                } else {
                    // Determine default dashboard based on selected group from dropdown
                    const selectedOption = roleInput.querySelector(`option[value="${role}"]`);
                    const selectedGroupName = selectedOption ? selectedOption.dataset.groupName : '';
                    let redirectUrl = null;
                    
                    if (selectedGroupName === 'admin') {
                        redirectUrl = 'admin_dashboard.html';
                    } else if (selectedGroupName === 'staff') {
                        redirectUrl = 'staff_dashboard.html';
                    } else {
                        // Unknown group
                        CookieManager.clearUserSession();
                        showError('Unauthorized group: ' + selectedGroupName + '. Please contact administrator.', authForm);
                        submitButton.innerHTML = originalText;
                        submitButton.disabled = false;
                        return;
                    }
                    
                    // Success - redirect to appropriate dashboard
                    showModal(`Welcome, ${data.data.name}. Redirecting to your dashboard...`, 'success', redirectUrl, 5000);
                }

            } else {
                showError(data.message || 'Login failed. Please try again.', authForm);
                submitButton.innerHTML = originalText;
                submitButton.disabled = false;
            }
        })
        .catch(error => {
            console.error('Login error:', error);
            showError('Login error. Please check your credentials and try again.', authForm);
            submitButton.innerHTML = originalText;
            submitButton.disabled = false;
        });
    }
    
    //createParticles();

    hidePreloader();
});

