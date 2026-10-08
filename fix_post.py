import os
file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/backend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = '''        if request.method == "POST":
            data = request.get_json()
            response = supabase.table("bouquets").insert(data).execute()
            return jsonify({"success": True, "message": "Bouquet added!"}), 201'''

replacement = '''        if request.method == "POST":
            data = request.get_json()
            # Check if ID already exists
            bouquet_id = data.get("id")
            if bouquet_id:
                existing = supabase.table("bouquets").select("id").eq("id", bouquet_id).execute()
                if len(existing.data) > 0:
                    return jsonify({"success": False, "message": f"Bouquet ID '{bouquet_id}' already exists! Please use a unique ID."}), 400
            
            response = supabase.table("bouquets").insert(data).execute()
            return jsonify({"success": True, "message": "Bouquet added!"}), 201'''

code = code.replace(target, replacement)
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print('Updated app.py')
