import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/backend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

replacement = '''    except Exception as error:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "error": str(error), "traceback": traceback.format_exc()}), 500'''

code = re.sub(r'    except Exception as error:\n\s*return jsonify\(\{"success": False, "error": str\(error\)\}\), 500', replacement, code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Added tracebacks")
