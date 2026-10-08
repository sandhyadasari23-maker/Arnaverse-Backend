import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/backend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

target = '''                if generated_signature != razorpay_signature:
                    # Invalid signature
                    order_data["payment_status"] = "Failed"
                    # We might not even save the order or we save it as Failed
                    # It's better to reject it
                    return jsonify({"success": False, "message": "Payment verification failed."}), 400
                    
                order_data["payment_status"] = "Successful"
            else:
                # COD or other
                order_data["payment_status"] = "Pending"'''

replacement = '''                if generated_signature != razorpay_signature:
                    # Invalid signature
                    order_data["payment_method"] = "UPI (Failed)"
                    return jsonify({"success": False, "message": "Payment verification failed."}), 400
                    
                order_data["payment_method"] = "UPI (Successful)"
            else:
                # COD or other
                order_data["payment_method"] = order_data.get("payment_method", "COD") + " (Pending)"'''

if "payment_status" in code:
    code = code.replace(target, replacement)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(code)
    print("Updated app.py to bypass payment_status column")
else:
    print("Target not found or already replaced.")
