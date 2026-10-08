import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/Checkout.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Load Razorpay Script
if "razorpay-script" not in code:
    code = re.sub(r'(container\.innerHTML = `)', r'    if (!document.getElementById("razorpay-script")) {\n        const script = document.createElement("script");\n        script.id = "razorpay-script";\n        script.src = "https://checkout.razorpay.com/v1/checkout.js";\n        document.body.appendChild(script);\n    }\n\n    \1', code)

# 2. Remove old manual UPI validation
code = re.sub(r'        if \(payment === \'UPI\' && !upiId\) \{\s*msg\.textContent = "Please enter your UPI ID\."; msg\.style\.color = "#d9534f"; return;\s*\}\s*', '', code)

# 3. Hide the manual UPI input field
code = code.replace('document.getElementById(\'upiBox\').style.display = e.target.value === \'UPI\' ? \'block\' : \'none\';', 'document.getElementById(\'upiBox\').style.display = \'none\'; // Handled by Razorpay popup')


# 4. Modify the placeOrderBtn handler
# First find the old fetch to /api/orders and replace it.
old_fetch_regex = r'''        fetch\('http://127\.0\.0\.1:5000/api/orders', \{\s*method: 'POST',\s*headers: \{ 'Content-Type': 'application/json' \},\s*body: JSON\.stringify\(newOrder\)\s*\}\)\s*\.then\(res => res\.json\(\)\)\s*\.then\(data => \{\s*if \(data\.success\) \{\s*Store\.clearCart\(\);\s*const orderDataToSave = \{\s*orderId: newOrder\.order_id,\s*name: fullName,\s*phone: phone,\s*address: address,\s*city: city,\s*paymentMethod: payment,\s*total: total,\s*items: cart\s*\};\s*localStorage\.setItem\("arnaverseOrder", JSON\.stringify\(orderDataToSave\)\);\s*router\.navigate\('/order-confirmation'\);\s*\} else \{\s*msg\.textContent = data\.message \|\| "Failed to place order\.";\s*msg\.style\.color = "#d9534f";\s*\}\s*\}\)\s*\.catch\(err => \{\s*console\.error\(err\);\s*msg\.textContent = "Error placing order\. Try again later\.";\s*msg\.style\.color = "#d9534f";\s*\}\);'''

new_fetch_code = '''        const submitOrder = (orderPayload) => {
            msg.textContent = "Placing order...";
            msg.style.color = "#333";
            fetch('http://127.0.0.1:5000/api/orders', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(orderPayload)
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    Store.clearCart();
                    const orderDataToSave = {
                        orderId: orderPayload.order_id,
                        name: fullName,
                        phone: phone,
                        address: address,
                        city: city,
                        paymentMethod: payment,
                        total: total,
                        items: cart
                    };
                    localStorage.setItem("arnaverseOrder", JSON.stringify(orderDataToSave));
                    router.navigate('/order-confirmation');
                } else {
                    msg.textContent = data.message || "Failed to place order.";
                    msg.style.color = "#d9534f";
                }
            })
            .catch(err => {
                console.error(err);
                msg.textContent = "Error placing order. Try again later.";
                msg.style.color = "#d9534f";
            });
        };

        if (payment === 'UPI') {
            msg.textContent = "Initializing secure payment...";
            msg.style.color = "#333";
            
            fetch('http://127.0.0.1:5000/api/create-razorpay-order', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ amount: total })
            })
            .then(res => res.json())
            .then(data => {
                if (!data.success) throw new Error(data.message || "Failed to create payment");
                
                const options = {
                    "key": data.key_id,
                    "amount": total * 100,
                    "currency": "INR",
                    "name": "Arnaverse",
                    "description": "Bouquet Order",
                    "order_id": data.razorpay_order_id,
                    "prefill": {
                        "name": fullName,
                        "email": user ? user.email : "",
                        "contact": phone
                    },
                    "theme": {
                        "color": "#1a1a1a"
                    },
                    "handler": function (response) {
                        // Payment Successful
                        newOrder.razorpay_payment_id = response.razorpay_payment_id;
                        newOrder.razorpay_order_id = response.razorpay_order_id;
                        newOrder.razorpay_signature = response.razorpay_signature;
                        submitOrder(newOrder);
                    }
                };
                
                const rzp = new window.Razorpay(options);
                rzp.on('payment.failed', function (response){
                    msg.textContent = "Payment failed. Please try again.";
                    msg.style.color = "#d9534f";
                });
                rzp.open();
            })
            .catch(err => {
                console.error(err);
                msg.textContent = "Payment initialization failed.";
                msg.style.color = "#d9534f";
            });
        } else {
            // COD
            submitOrder(newOrder);
        }'''

if "Razorpay(" not in code:
    code = re.sub(old_fetch_regex, new_fetch_code, code)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Regex replace done")
