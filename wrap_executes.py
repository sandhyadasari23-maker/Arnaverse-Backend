import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/backend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Lines with .execute()
def replacer(match):
    # The match captures everything before .execute()
    # e.g., 'supabase.table("users").select("*").limit(1)'
    expression = match.group(1)
    
    # Do not wrap if it's already inside execute_with_retry
    # or if it's the actual execution inside execute_with_retry itself.
    if "execute_with_retry" in expression or "query_builder" in expression:
        return match.group(0)
    
    # Strip any trailing whitespace/newlines from expression
    return f"execute_with_retry({expression})"

# Regex to match variable assignment or bare supabase call
# matches `supabase.something().something().execute()`
# and replaces it with `execute_with_retry(supabase.something().something())`
code = re.sub(r'(supabase\.table\([^\)]+\)[^;]+?)\.execute\(\)', replacer, code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Wrapped all unhandled executes")
