import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/Checkout.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# Remove razorpay script loader
script_loader_regex = r'''    // Load Razorpay Script\s*if \(\!document\.getElementById\(\'razorpay-script\'\)\) \{\s*const script = document\.createElement\(\'script\'\);\s*script\.id = \'razorpay-script\';\s*script\.src = \'https://checkout\.razorpay\.com/v1/checkout\.js\';\s*document\.body\.appendChild\(script\);\s*\}\s*'''
code = re.sub(script_loader_regex, '', code)

# Remove UPI radio button HTML
upi_html_regex = r'''\s*<label class="payment-option">\s*<input type="radio" name="payment" value="UPI">\s*<div>\s*<strong>UPI Payment</strong><br>\s*<span style="font-size:13px; color:var\(--text-muted\);">Pay using your UPI ID\.</span>\s*</div>\s*</label>\s*'''
code = re.sub(upi_html_regex, '\n                                    ', code)

# Remove place order Razorpay logic
submit_logic_regex = r'''        const submitOrder = \(orderPayload\) => \{\s*msg\.textContent = "Placing order\.\.\.";\s*msg\.style\.color = "#333";\s*fetch\('http://127\.0\.0\.1:5000/api/orders', \{\s*method: 'POST',\s*headers: \{ 'Content-Type': 'application/json' \},\s*body: JSON\.stringify\(orderPayload\)\s*\}\)\s*\.then\(res => res\.json\(\)\)\s*\.then\(data => \{\s*if \(!data\.success\) \{\s*msg\.textContent = data\.message \|\| "Failed to place order\.";\s*msg\.style\.color = "#d9534f";\s*throw new Error\(data\.message \|\| "Failed to place order"\);\s*\}\s*if \(data\.success\) \{\s*Store\.setCart\(\[\]\);\s*const orderDataToSave = \{\s*orderId: orderPayload\.order_id,\s*name: fullName,\s*phone: phone,\s*address: address,\s*city: city,\s*paymentMethod: payment,\s*total: total,\s*items: cart\s*\};\s*localStorage\.setItem\("arnaverseOrder", JSON\.stringify\(orderDataToSave\)\);\s*router\.navigate\('/order-confirmation'\);\s*\} else \{\s*msg\.textContent = data\.message \|\| "Failed to place order\.";\s*msg\.style\.color = "#d9534f";\s*\}\s*\}\)\s*\.catch\(err => \{\s*console\.error\(err\);\s*msg\.textContent = "Error placing order\. Try again later\.";\s*msg\.style\.color = "#d9534f";\s*\}\);\s*\};\s*if \(payment === 'UPI'\) \{.*?\} else \{\s*// COD\s*submitOrder\(newOrder\);\s*\}'''

replacement_logic = '''        fetch('http://127.0.0.1:5000/api/orders', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newOrder)
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                Store.setCart([]);
                const orderDataToSave = {
                    orderId: newOrder.order_id,
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
        });'''

code = re.sub(submit_logic_regex, replacement_logic, code, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Removed UPI from Checkout.js")
