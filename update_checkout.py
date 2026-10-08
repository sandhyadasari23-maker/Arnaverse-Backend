import os
import re

file_path = 'C:/Users/Archana/OneDrive/Desktop/ARNAVERSE/frontend/js/views/Checkout.js'
with open(file_path, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Load Razorpay script dynamically in init()
init_target = '''    container.innerHTML = `'''
init_replacement = '''    // Load Razorpay Script
    if (!document.getElementById("razorpay-script")) {
        const script = document.createElement("script");
        script.id = "razorpay-script";
        script.src = "https://checkout.razorpay.com/v1/checkout.js";
        document.body.appendChild(script);
    }

    container.innerHTML = `'''

code = code.replace(init_target, init_replacement)

# 2. Modify the click handler for placeOrderBtn
place_order_target = '''        const newOrder = {
            order_id: "ARN" + Date.now(),
            customer_email: user ? user.email : "",
            total: total,
            status: "Order Placed",
            payment_method: payment,
            items: cart
        };
        
        msg.textContent = "Updating profile & placing order...";
        msg.style.color = "#333";
        
        // Update user profile with latest checkout details
        if (user && user.email) {
            fetch('http://127.0.0.1:5000/api/profile', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: user.email,
                    name: fullName,
                    phone: phone,
                    address: address,
                    city: city
                })
            }).catch(e => console.error("Profile update failed:", e));
        }

        fetch('http://127.0.0.1:5000/api/orders', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newOrder)
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                Store.clearCart();
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
    });
};'''

place_order_replacement = '''        const newOrder = {
            order_id: "ARN" + Date.now(),
            customer_email: user ? user.email : "",
            total: total,
            status: "Order Placed",
            payment_method: payment,
            items: cart
        };
        
        // Update user profile with latest checkout details
        if (user && user.email) {
            fetch('http://127.0.0.1:5000/api/profile', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: user.email,
                    name: fullName,
                    phone: phone,
                    address: address,
                    city: city
                })
            }).catch(e => console.error("Profile update failed:", e));
        }

        const submitOrder = (orderPayload) => {
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
        }
    });
};'''

code = code.replace(place_order_target, place_order_replacement)

# 3. Clean up the manual upiId check since Razorpay popup handles it
code = code.replace('''        if (payment === 'UPI' && !upiId) {
            msg.textContent = "Please enter your UPI ID."; msg.style.color = "#d9534f"; return;
        }''', '')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated Checkout.js with Razorpay popup")
