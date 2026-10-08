import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/login.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Replace the entire handleLogin function
start_idx = code.find('    const handleLogin = () => {')
end_idx = code.find('    document.getElementById("loginBtn").addEventListener', start_idx)

replacement = '''    const handleLogin = () => {
        const email = document.getElementById("email").value.trim().toLowerCase();
        const passwordValue = password.value;
        const loginType = document.querySelector('input[name="loginType"]:checked').value;
        const message = document.getElementById("loginMessage");

        if (!email || !passwordValue) {
            message.textContent = "Please enter email and password.";
            message.style.color = "#c62828";
            return;
        }

        // Connect to Python Backend
        message.textContent = "Logging in...";
        message.style.color = "#333";
        
        fetch('http://127.0.0.1:5000/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: passwordValue })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (loginType === "admin") {
                    if (data.user.is_admin) {
                        localStorage.setItem("arnaverseToken", data.token);
                        localStorage.setItem("arnaverseAdminLoggedIn", "true");
                        localStorage.setItem("arnaverseAdmin", JSON.stringify(data.user));
                        
                        // Also set user login so normal app works if they navigate there
                        localStorage.setItem("arnaverseLoggedIn", "true");
                        localStorage.setItem("arnaverseUser", JSON.stringify(data.user));
                        localStorage.setItem("arnaverseCurrentUser", JSON.stringify(data.user));
                        
                        message.textContent = "Admin login successful!";
                        message.style.color = "#198754";
                        setTimeout(() => window.location.hash = "#/admin-dashboard", 600);
                    } else {
                        message.textContent = "Unauthorized. You are not an admin.";
                        message.style.color = "#c62828";
                    }
                } else {
                    // User Login
                    if (data.token) localStorage.setItem("arnaverseToken", data.token);
                    localStorage.setItem("arnaverseLoggedIn", "true");
                    localStorage.setItem("arnaverseCurrentUser", JSON.stringify(data.user));
                    localStorage.setItem("arnaverseUser", JSON.stringify(data.user));
                    
                    message.textContent = "Login successful!";
                    message.style.color = "#198754";
                    setTimeout(() => window.location.hash = "#/", 600);
                }
            } else {
                message.textContent = data.message || "Invalid email or password.";
                message.style.color = "#c62828";
            }
        })
        .catch(err => {
            message.textContent = "Server error. Please try again later.";
            message.style.color = "#c62828";
            console.error(err);
        });
    };

'''

code = code[:start_idx] + replacement + code[end_idx:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated Login.js logic")
