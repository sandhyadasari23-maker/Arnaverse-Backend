import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/backend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = '''        supabase = get_db()
        response = supabase.table("users").update(update_data).eq("email", email.strip().lower()).execute()
        
        if not response.data or len(response.data) == 0:
            return jsonify({"success": False, "message": "User not found."}), 404'''

replacement = '''        supabase = get_db()
        response = execute_with_retry(supabase.table("users").update(update_data).eq("email", email.strip().lower()))
        
        if not response.data or len(response.data) == 0:
            # Return 200 with success: False so the browser doesn't log a scary 404 NOT FOUND network error
            return jsonify({"success": False, "message": "User not found in database. Please log in again."}), 200'''

code = code.replace(target, replacement)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Fixed update_profile 404 error")
