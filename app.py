from dotenv import load_dotenv
load_dotenv()
import os
import jwt
import datetime
from functools import wraps
from flask import Flask, jsonify, request
from flask_cors import CORS
import razorpay
import hmac
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db
from mailer import send_order_email_async

SECRET_KEY = os.environ.get('SECRET_KEY', 'super-secret-key-arnaverse')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'success': False, 'message': 'Unauthorized'}), 401
        try:
            token = token.replace('Bearer ', '')
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            if not data.get('is_admin'):
                return jsonify({'success': False, 'message': 'Forbidden: Admins only'}), 403
        except Exception as e:
            return jsonify({'success': False, 'message': 'Invalid or expired token'}), 401
        return f(*args, **kwargs)
    return decorated_function

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Arnaverse Backend is Running with Supabase!"

@app.route("/api/test-db")
def test_database():
    try:
        supabase = get_db()
        # Test connection by selecting from users table (limit 1)
        # If it doesn't exist, this will throw an error
        response = execute_with_retry(supabase.table("users").select("*").limit(1))
        return jsonify({
            "success": True,
            "message": "Connected to Supabase successfully!",
            "data": response.data
        })
    except Exception as error:
        return jsonify({
            "success": False,
            "message": "Server Error: " + str(error), "error": str(error)
        }), 500

@app.route("/api/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        
        name = data.get("name", "").strip()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "").strip()
        phone = data.get("phone", "").strip()
        address = data.get("address", "").strip()
        city = data.get("city", "").strip()

        if not name or not email or not password:
            return jsonify({
                "success": False,
                "message": "Name, email and password are required."
            }), 400

        supabase = get_db()
        
        # Check if user exists
        existing_user = execute_with_retry(supabase.table("users").select("id").eq("email", email))
        
        if existing_user.data and len(existing_user.data) > 0:
            return jsonify({
                "success": False,
                "message": "User with this email already exists."
            }), 409

        hashed_password = generate_password_hash(password)

        new_user = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "phone": phone,
            "address": address,
            "city": city
        }
        
        response = execute_with_retry(supabase.table("users").insert(new_user))

        return jsonify({
            "success": True,
            "message": "Registration successful!",
            "user_id": response.data[0]["id"] if response.data else None
        }), 201

    except Exception as error:
        return jsonify({
            "success": False,
            "message": "Registration failed.",
            "message": "Server Error: " + str(error), "error": str(error)
        }), 500

@app.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "").strip()

        supabase = get_db()
        response = execute_with_retry(supabase.table("users").select("*").eq("email", email))
        
        if not response.data or len(response.data) == 0:
            return jsonify({"success": False, "message": "Invalid email or password."}), 401
            
        user = response.data[0]
        
        if not check_password_hash(user["password"], password):
            return jsonify({"success": False, "message": "Invalid email or password."}), 401
            
        # Don't send password hash back to frontend
        del user["password"]
        
        # Check if admin
        admin_emails = [e.strip().lower() for e in os.environ.get("ADMIN_EMAILS", "admin@arnaverse.com").split(",")]
        is_admin = user["email"].lower() in admin_emails
        user["is_admin"] = is_admin
        
        token = jwt.encode({
            "email": user["email"],
            "is_admin": is_admin,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }, SECRET_KEY, algorithm="HS256")
        
        return jsonify({
            "success": True,
            "message": "Login successful!",
            "user": user,
            "token": token
        }), 200

    except Exception as error:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": "Server Error: " + str(error), "error": str(error), "traceback": traceback.format_exc()}), 500




@app.route("/api/orders", methods=["POST", "GET", "PUT"])
def handle_orders():
    try:
        supabase = get_db()
        
        if request.method == "POST":
            order_data = request.get_json()
            print("=== INCOMING POST /api/orders ===", flush=True)
            print("Payload:", order_data, flush=True)
            try:
                response = execute_with_retry(supabase.table("orders").insert(order_data))
                print("Supabase Insert Response:", getattr(response, 'data', 'No data attribute'), flush=True)
            except Exception as e:
                print("Supabase Insert Error:", str(e), flush=True)
                raise e
            
            if response.data:
                new_order = response.data[0]
                email = new_order.get("customer_email")
                # Attempt to get user name for the email
                user_res = execute_with_retry(supabase.table("users").select("name").eq("email", email))
                user_name = user_res.data[0]["name"] if user_res.data and "name" in user_res.data[0] else "Customer"
                
                send_order_email_async(new_order, user_name, is_update=False)

            return jsonify({"success": True, "message": "Order placed!", "order": response.data[0]}), 201
            
        elif request.method == "GET":
            email = request.args.get("email")
            if email:
                response = execute_with_retry(supabase.table("orders").select("*").eq("customer_email", email).order("created_at", desc=True))
            else:
                response = execute_with_retry(supabase.table("orders").select("*").order("created_at", desc=True))
            return jsonify({"success": True, "orders": response.data}), 200
            
        elif request.method == "PUT":
            data = request.get_json()
            order_id = data.get("order_id")
            new_status = data.get("status")
            if not order_id or not new_status:
                return jsonify({"success": False, "message": "Missing order_id or status."}), 400
                
            # If status is anything other than Cancelled, require admin
            if new_status.lower() != "cancelled":
                token = request.headers.get("Authorization")
                if not token:
                    return jsonify({"success": False, "message": "Unauthorized"}), 401
                try:
                    token = token.replace("Bearer ", "")
                    data_jwt = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                    if not data_jwt.get("is_admin"):
                        return jsonify({"success": False, "message": "Forbidden"}), 403
                except:
                    return jsonify({"success": False, "message": "Invalid token"}), 401
            
            response = execute_with_retry(supabase.table("orders").update({"status": new_status}).eq("order_id", order_id))
            
            if response.data:
                updated_order = response.data[0]
                email = updated_order.get("customer_email")
                user_res = execute_with_retry(supabase.table("users").select("name").eq("email", email))
                user_name = user_res.data[0]["name"] if user_res.data and "name" in user_res.data[0] else "Customer"
                
                send_order_email_async(updated_order, user_name, is_update=True)

            return jsonify({"success": True, "message": "Order updated successfully!"}), 200

    except Exception as error:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": "Server Error: " + str(error), "error": str(error), "traceback": traceback.format_exc()}), 500

@app.route("/api/profile", methods=["PUT"])
def update_profile():
    try:
        data = request.get_json()
        email = data.get("email")
        
        if not email:
            return jsonify({"success": False, "message": "Email is required to update profile."}), 400
            
        update_data = {
            "name": data.get("name", "").strip(),
            "phone": data.get("phone", "").strip(),
            "city": data.get("city", "").strip(),
            "address": data.get("address", "").strip()
        }
        
        supabase = get_db()
        response = execute_with_retry(supabase.table("users").update(update_data).eq("email", email.strip().lower()))
        
        if not response.data or len(response.data) == 0:
            # Return 200 with success: False so the browser doesn't log a scary 404 NOT FOUND network error
            return jsonify({"success": False, "message": "User not found in database. Please log in again."}), 200
            
        updated_user = response.data[0]
        del updated_user["password"] # Don't return password
        
        return jsonify({
            "success": True, 
            "message": "Profile updated successfully!",
            "user": updated_user
        }), 200

    except Exception as error:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": "Server Error: " + str(error), "error": str(error), "traceback": traceback.format_exc()}), 500

@app.route("/api/users", methods=["GET"])
@admin_required
def get_users():
    try:
        supabase = get_db()
        response = execute_with_retry(supabase.table("users").select("id, name, email, phone, city, created_at"))
        return jsonify({"success": True, "users": response.data}), 200
    except Exception as error:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": "Server Error: " + str(error), "error": str(error), "traceback": traceback.format_exc()}), 500

@app.route("/api/admin/orders", methods=["GET"])
@admin_required
def get_all_orders():
    try:
        supabase = get_db()
        response = execute_with_retry(supabase.table("orders").select("*").order("created_at", desc=True))
        orders = response.data or []
        
        # Join with users table to get correct customer profile names
        users_res = execute_with_retry(supabase.table("users").select("email, name"))
        user_map = {u["email"].lower(): u["name"] for u in (users_res.data or []) if u.get("email")}
        
        for order in orders:
            email = order.get("customer_email", "").strip().lower()
            order["customer_name"] = user_map.get(email, "Unknown")
            
        return jsonify({"success": True, "orders": orders}), 200
    except Exception as error:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": "Server Error: " + str(error), "error": str(error), "traceback": traceback.format_exc()}), 500

@app.route("/api/bouquets", methods=["GET", "POST", "PUT", "DELETE"])
def handle_bouquets():
    try:
        supabase = get_db()
        if request.method == "GET":
            response = execute_with_retry(supabase.table("bouquets").select("*").order("id"))
            return jsonify({"success": True, "bouquets": response.data}), 200
            
        # Admin required for POST, PUT, DELETE
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"success": False, "message": "Unauthorized"}), 401
        try:
            token = token.replace("Bearer ", "")
            data_jwt = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if not data_jwt.get("is_admin"):
                return jsonify({"success": False, "message": "Forbidden"}), 403
        except:
            return jsonify({"success": False, "message": "Invalid token"}), 401

        if request.method == "POST":
            data = request.get_json()
            # Check if ID already exists
            bouquet_id = data.get("id")
            if bouquet_id:
                existing = execute_with_retry(supabase.table("bouquets").select("id").eq("id", bouquet_id))
                if len(existing.data) > 0:
                    return jsonify({"success": False, "message": f"Bouquet ID '{bouquet_id}' already exists! Please use a unique ID."}), 400
            
            response = execute_with_retry(supabase.table("bouquets").insert(data))
            return jsonify({"success": True, "message": "Bouquet added!"}), 201
            
        elif request.method == "PUT":
            data = request.get_json()
            bouquet_id = data.get("id")
            response = execute_with_retry(supabase.table("bouquets").update(data).eq("id", bouquet_id))
            return jsonify({"success": True, "message": "Bouquet updated!"}), 200
            
        elif request.method == "DELETE":
            bouquet_id = request.args.get("id")
            response = execute_with_retry(supabase.table("bouquets").delete().eq("id", bouquet_id))
            return jsonify({"success": True, "message": "Bouquet deleted!"}), 200

    except Exception as error:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": "Server Error: " + str(error), "error": str(error), "traceback": traceback.format_exc()}), 500

import time

def execute_with_retry(query_builder, max_retries=3, delay=1):
    last_err = None
    for _ in range(max_retries):
        try:
            return query_builder.execute()
        except Exception as e:
            last_err = e
            time.sleep(delay)
    raise last_err

import uuid

@app.route("/api/upload", methods=["POST"])
@admin_required
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "message": "No file uploaded"}), 400
            
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "message": "No selected file"}), 400
            
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'jpg'
        file_name = f"{uuid.uuid4()}.{file_ext}"
        file_bytes = file.read()
        
        # Save locally to frontend/assets/images/bouquets instead of Supabase
        import os
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        target_dir = os.path.join(base_dir, "frontend", "assets", "images", "bouquets")
        os.makedirs(target_dir, exist_ok=True)
        
        save_path = os.path.join(target_dir, file_name)
        with open(save_path, "wb") as f:
            f.write(file_bytes)
            
        public_url = f"assets/images/bouquets/{file_name}"
        return jsonify({"success": True, "url": public_url}), 200
        
    except Exception as error:
        return jsonify({"success": False, "message": str(error)}), 200

@app.route("/api/ai-picks", methods=["POST"])
def ai_picks():
    import os
    try:
        data = request.json
        occasion = data.get("occasion", "")
        budget = data.get("budget", "")
        flower = data.get("flower", "")
        color = data.get("color", "")
        custom_prompt = data.get("prompt", "")

        # Fetch all bouquets from db
        supabase = get_db()
        res = execute_with_retry(supabase.table("bouquets").select("*"))
        inventory = res.data

        prompt = f"""
        You are an expert florist assistant for Arnaverse. 
        A customer is looking for a bouquet.
        Their preferences:
        Occasion: {occasion}
        Budget: {budget}
        Preferred Flower: {flower}
        Preferred Color: {color}
        Custom request: "{custom_prompt}"

        Here is our current inventory:
        {inventory}

        Task 1: Select up to 3 of the BEST matching bouquets from the inventory based on their request. 
        Task 2: Write a personalized 2-sentence greeting card message they can use for this occasion.
        
        Respond EXACTLY in this JSON format:
        {{
            "recommended_ids": ["id1", "id2"],
            "greeting_message": "Your custom message here"
        }}
        """

        def fallback_logic():
            filtered = inventory
            if budget and budget != "any":
                filtered = [b for b in filtered if b.get("price", 0) <= int(budget)]
            if flower:
                filtered = [b for b in filtered if flower.lower() in str(b.get("flower", "")).lower() or flower.lower() in str(b.get("name", "")).lower()]
            if color:
                filtered = [b for b in filtered if color.lower() in str(b.get("color", "")).lower()]
            if not filtered:
                filtered = [b for b in inventory if not budget or budget == "any" or b.get("price", 0) <= int(budget)]
            import random
            random.shuffle(filtered)
            recommended_ids = [b["id"] for b in filtered[:3]]
            msg_occasion = occasion if occasion else "celebration"
            return {
                "success": True,
                "recommended_ids": recommended_ids,
                "greeting_message": f"Wishing you a wonderful {msg_occasion}! Enjoy these beautiful flowers."
            }

        gemini_key = os.getenv("GEMINI_API_KEY")
        if not gemini_key:
            return jsonify(fallback_logic()), 200

        import google.generativeai as genai
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        try:
            response = model.generate_content(prompt)
            import json
            import re
            
            text = response.text
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group(1))
            else:
                result = json.loads(text)
            
            return jsonify({
                "success": True,
                "recommended_ids": result.get("recommended_ids", []),
                "greeting_message": result.get("greeting_message", "")
            }), 200
        except Exception as e:
            # If Gemini API returns 500 Backend Error or fails to parse, use fallback
            print(f"Gemini API Error: {e}")
            return jsonify(fallback_logic()), 200

    except Exception as error:
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": "Server Error: " + str(error), "error": str(error), "traceback": traceback.format_exc()}), 500

if __name__ == "__main__":
     app.run(debug=False, port=5000, use_reloader=False)




