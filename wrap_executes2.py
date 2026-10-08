import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/backend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if ".execute()" in line and "supabase.table" in line and "execute_with_retry" not in line:
        # Find the start of supabase
        start_idx = line.find("supabase.table")
        end_idx = line.find(".execute()")
        
        # Extract the query part
        query = line[start_idx:end_idx]
        
        # Replace
        new_line = line[:start_idx] + f"execute_with_retry({query})" + line[end_idx+10:]
        lines[i] = new_line

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("Manually fixed lines")
