import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from threading import Thread
from datetime import datetime, timedelta

def send_email_async(to_email, subject, html_body):
    sender = os.environ.get('MAIL_DEFAULT_SENDER')
    password = os.environ.get('MAIL_PASSWORD')
    username = os.environ.get('MAIL_USERNAME', sender)
    server = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    port = int(os.environ.get('MAIL_PORT', 587))

    if not sender or not password:
        print('Email credentials missing in .env. Skipping email.')
        return

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = to_email
        
        part = MIMEText(html_body, 'html')
        msg.attach(part)
        
        with smtplib.SMTP(server, port) as server_smtp:
            server_smtp.starttls()
            server_smtp.login(username, password)
            server_smtp.sendmail(sender, to_email, msg.as_string())
        print(f'Email successfully sent to {to_email}')
    except Exception as e:
        print(f'Failed to send email to {to_email}: {e}')

def send_order_email_async(order_data, user_name, is_update=False):
    def email_task():
        try:
            order_id = order_data.get('order_id', 'N/A')
            status = order_data.get('status', 'Order Placed')
            total = order_data.get('total', 0)
            payment = order_data.get('payment_method', 'N/A')
            items = order_data.get('items', [])
            to_email = order_data.get('customer_email')
            
            if not to_email:
                return
                
            delivery_date = (datetime.now() + timedelta(days=3)).strftime('%d %b %Y')

            items_html = ''
            for item in items:
                name = item.get('name', 'Bouquet')
                qty = item.get('quantity', 1)
                price = item.get('price', 0)
                items_html += f'<li>{name} x {qty} - ₹{int(price) * int(qty)}</li>'

            if not items_html:
                items_html = '<li>Order items</li>'
                
            if is_update:
                subject = f'Order Status Update - {order_id}'
                title = 'Your Order Status Has Changed'
                intro = f'The status of your Arnaverse order <strong>{order_id}</strong> is now: <strong style="color:#a8325d;">{status}</strong>'
            else:
                subject = f'Order Confirmation - {order_id}'
                title = 'Thank You For Your Order!'
                intro = f'Your Arnaverse order <strong>{order_id}</strong> has been successfully placed.'

            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; color: #333;">
                    <h2 style="color: #a8325d;">{title}</h2>
                    <p>Hi {user_name},</p>
                    <p>{intro}</p>
                    
                    <h3 style="border-bottom: 1px solid #ccc; padding-bottom: 5px;">Order Details</h3>
                    <ul>{items_html}</ul>
                    
                    <p><strong>Total Amount:</strong> ₹{total}</p>
                    <p><strong>Payment Method:</strong> {payment}</p>
                    <p><strong>Estimated Delivery:</strong> {delivery_date}</p>
                    
                    <p>You can track your order status on your profile.</p>
                    <p>Warm regards,<br><strong>Arnaverse Team</strong></p>
                </body>
            </html>
            """
            send_email_async(to_email, subject, html)
        except Exception as e:
            print(f'Email generation failed: {e}')

    Thread(target=email_task).start()
