import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/backend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = '''        supabase = get_db()
        # Upload to Supabase 'bouquets' bucket
        res = supabase.storage.from_("bouquets").upload(
            file_name, 
            file_bytes, 
            {"content-type": file.content_type}
        )
        
        public_url = supabase.storage.from_("bouquets").get_public_url(file_name)
        
        return jsonify({"success": True, "url": public_url}), 200'''

replacement = '''        # Save locally to frontend/assets/images/bouquets instead of Supabase
        import os
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        target_dir = os.path.join(base_dir, "frontend", "assets", "images", "bouquets")
        os.makedirs(target_dir, exist_ok=True)
        
        save_path = os.path.join(target_dir, file_name)
        with open(save_path, "wb") as f:
            f.write(file_bytes)
            
        public_url = f"assets/images/bouquets/{file_name}"
        return jsonify({"success": True, "url": public_url}), 200'''

code = code.replace(target, replacement)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Fixed app.py upload logic")
