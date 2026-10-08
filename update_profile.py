import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/Profile.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = '''            } else {
                msg.textContent = data.message || "Failed to update profile.";
                msg.style.color = "red";
            }'''

replacement = '''            } else {
                msg.textContent = data.message || "Failed to update profile.";
                msg.style.color = "red";
                if (data.message && data.message.includes("User not found")) {
                    setTimeout(() => Store.logoutUser(), 2000);
                }
            }'''

if target in code:
    code = code.replace(target, replacement)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print("Updated Profile.js auto-logout")
else:
    print("Could not find target in Profile.js")
