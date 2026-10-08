import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/login.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = '''                        // Also set user login so normal app works if they navigate there
                        localStorage.setItem("arnaverseLoggedIn", "true");
                        localStorage.setItem("arnaverseUser", JSON.stringify(data.user));
                        localStorage.setItem("arnaverseCurrentUser", JSON.stringify(data.user));'''

replacement = '''                        // Also set user login so normal app works if they navigate there
                        localStorage.setItem("arnaverseLoggedIn", "true");
                        localStorage.setItem("arnaverseUser", JSON.stringify(data.user));
                        localStorage.setItem("arnaverseCurrentUser", JSON.stringify(data.user));
'''

target2 = '''                } else {
                    // User Login
                    if (data.token) localStorage.setItem("arnaverseToken", data.token);
                    localStorage.setItem("arnaverseLoggedIn", "true");'''

replacement2 = '''                } else {
                    // User Login
                    if (data.token) localStorage.setItem("arnaverseToken", data.token);
                    localStorage.setItem("arnaverseLoggedIn", "true");
                    // Clear admin state so they don't have conflicting roles
                    localStorage.removeItem("arnaverseAdminLoggedIn");
                    localStorage.removeItem("arnaverseAdmin");'''

code = code.replace(target2, replacement2)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated Login.js auth clearing")
