document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const errorMsg = document.getElementById('error-msg');
    
    loginForm.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevent default form submission
        
        const usernameInput = document.getElementById('username').value.trim();
        const passwordInput = document.getElementById('password').value.trim();
        
        // Check if the entered credentials match any user in the users array
        const user = users.find(user => 
            user.username === usernameInput && 
            user.password === passwordInput
        );
        
        if (user) {
            // Successful login
            errorMsg.textContent = ''; // Clear any previous error messages
            
            // Store username in session storage for use on other pages
            sessionStorage.setItem('currentUser', user.username);
            
            // Redirect to home page first (changed from dashboard.html)
            window.location.href = 'home.html';
        } else {
            // Failed login
            errorMsg.textContent = 'Invalid username or password. Please try again.';
            errorMsg.style.color = '#863a29';
            errorMsg.style.fontWeight = 'bold';
        }
    });
});