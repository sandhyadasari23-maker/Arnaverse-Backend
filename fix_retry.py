import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/backend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace(
    'response = supabase.table("orders").insert(order_data).execute()', 
    'response = execute_with_retry(supabase.table("orders").insert(order_data))'
)

code = code.replace(
    'user_res = supabase.table("users").select("name").eq("email", email).execute()', 
    'user_res = execute_with_retry(supabase.table("users").select("name").eq("email", email))'
)

code = code.replace(
    'response = supabase.table("orders").select("*").eq("customer_email", email).order("created_at", desc=True).execute()', 
    'response = execute_with_retry(supabase.table("orders").select("*").eq("customer_email", email).order("created_at", desc=True))'
)

code = code.replace(
    'response = supabase.table("orders").update({"status": new_status}).eq("order_id", order_id).execute()', 
    'response = execute_with_retry(supabase.table("orders").update({"status": new_status}).eq("order_id", order_id))'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Fixed execute calls")
