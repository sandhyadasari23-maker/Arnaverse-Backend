import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/backend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Remove razorpay endpoint
razorpay_endpoint_regex = r'@app\.route\("/api/create-razorpay-order", methods=\["POST"\]\).*?def create_razorpay_order\(\):.*?return jsonify\(\{"success": False, "error": str\(error\), "traceback": traceback\.format_exc\(\)\}\), 500'
code = re.sub(razorpay_endpoint_regex, '', code, flags=re.DOTALL)

# Revert /api/orders to simple insert
target_orders = '''        if request.method == "POST":
            order_data = request.get_json()
            
            # Verify Razorpay signature if payment is UPI
            if order_data.get("payment_method") == "UPI":
                razorpay_payment_id = order_data.pop("razorpay_payment_id", None)
                razorpay_order_id = order_data.pop("razorpay_order_id", None)
                razorpay_signature = order_data.pop("razorpay_signature", None)
                
                key_secret = os.environ.get("RAZORPAY_KEY_SECRET")
                if not key_secret or not razorpay_payment_id or not razorpay_order_id or not razorpay_signature:
                    return jsonify({"success": False, "message": "Invalid payment verification details."}), 400
                    
                # Verify signature
                generated_signature = hmac.new(
                    key_secret.encode('utf-8'),
                    f"{razorpay_order_id}|{razorpay_payment_id}".encode('utf-8'),
                    hashlib.sha256
                ).hexdigest()
                
                if generated_signature != razorpay_signature:
                    # Invalid signature
                    order_data["payment_method"] = "UPI (Failed)"
                    return jsonify({"success": False, "message": "Payment verification failed."}), 400
                    
                order_data["payment_method"] = "UPI (Successful)"
            else:
                # COD or other
                order_data["payment_method"] = order_data.get("payment_method", "COD") + " (Pending)"
                
            response = supabase.table("orders").insert(order_data).execute()'''

replacement_orders = '''        if request.method == "POST":
            order_data = request.get_json()
            response = supabase.table("orders").insert(order_data).execute()'''

if "razorpay_payment_id = order_data.pop" in code:
    code = code.replace(target_orders, replacement_orders)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Reverted app.py successfully")
