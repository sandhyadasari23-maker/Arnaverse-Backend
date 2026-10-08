import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/backend/app.py'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Add Razorpay imports
if "import razorpay" not in code:
    code = code.replace("from flask_cors import CORS", "from flask_cors import CORS\nimport razorpay\nimport hmac\nimport hashlib")

# 2. Add /api/create-razorpay-order endpoint
razorpay_endpoint = '''
@app.route("/api/create-razorpay-order", methods=["POST"])
def create_razorpay_order():
    try:
        data = request.get_json()
        amount = data.get("amount") # in INR (Rs)
        if not amount:
            return jsonify({"success": False, "message": "Amount is required"}), 400
            
        key_id = os.environ.get("RAZORPAY_KEY_ID")
        key_secret = os.environ.get("RAZORPAY_KEY_SECRET")
        
        if not key_id or not key_secret:
            return jsonify({"success": False, "message": "Razorpay keys not configured"}), 500
            
        client = razorpay.Client(auth=(key_id, key_secret))
        
        # Razorpay expects amount in paise (1 INR = 100 paise)
        order_amount = int(amount * 100)
        order_currency = "INR"
        
        razorpay_order = client.order.create(dict(amount=order_amount, currency=order_currency, payment_capture=1))
        
        return jsonify({
            "success": True, 
            "razorpay_order_id": razorpay_order["id"],
            "key_id": key_id # Safe to send public key to frontend
        }), 200
    except Exception as error:
        import traceback
        return jsonify({"success": False, "error": str(error), "traceback": traceback.format_exc()}), 500

@app.route("/api/orders", methods=["POST", "GET", "PUT"])
'''

code = re.sub(r'@app\.route\("/api/orders", methods=\["POST", "GET", "PUT"\]\)\s*\n', razorpay_endpoint, code)

# 3. Update handle_orders to verify signature
new_handle_orders_post = '''        if request.method == "POST":
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
                    order_data["payment_status"] = "Failed"
                    # We might not even save the order or we save it as Failed
                    # It's better to reject it
                    return jsonify({"success": False, "message": "Payment verification failed."}), 400
                    
                order_data["payment_status"] = "Successful"
            else:
                # COD or other
                order_data["payment_status"] = "Pending"
                
            response = supabase.table("orders").insert(order_data).execute()'''

code = re.sub(r'        if request\.method == "POST":\n            order_data = request\.get_json\(\)\n            response = supabase\.table\("orders"\)\.insert\(order_data\)\.execute\(\)', new_handle_orders_post, code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated app.py with Razorpay logic")
