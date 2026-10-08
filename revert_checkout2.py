import os

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/Checkout.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Remove razorpay-script loading block
idx1 = code.find('    // Load Razorpay Script')
if idx1 != -1:
    idx2 = code.find('    container.innerHTML = `', idx1)
    if idx2 != -1:
        code = code[:idx1] + code[idx2:]

# 2. Remove UPI payment option
target_upi = '''                                    <label class="payment-option">
                                        <input type="radio" name="payment" value="UPI">
                                        <div>
                                            <strong>UPI Payment</strong><br>
                                            <span style="font-size:13px; color:var(--text-muted);">Pay using your UPI ID.</span>
                                        </div>
                                    </label>'''
code = code.replace(target_upi, '')

# 3. Replace the entire order submission logic block
start_idx = code.find('        const submitOrder = (orderPayload) => {')
end_idx = code.find('    });\n};\n')

if start_idx != -1 and end_idx != -1:
    replacement = '''        fetch('http://127.0.0.1:5000/api/orders', {
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
        });
'''
    code = code[:start_idx] + replacement + code[end_idx:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Removed UPI from Checkout.js successfully")
