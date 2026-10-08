import urllib.request
import json

data = json.dumps({'email': 'admin@arnaverse.com', 'password': 'admin123'}).encode('utf-8')
req = urllib.request.Request('http://127.0.0.1:5000/api/login', data=data, method='POST')
req.add_header('Content-Type', 'application/json')
with urllib.request.urlopen(req) as res:
    token = json.loads(res.read())['token']

# Test POST to /api/bouquets
data = json.dumps({'id': 'B999', 'name': 'Test', 'price': 100, 'stock': 10, 'category': 'Test'}).encode('utf-8')
req = urllib.request.Request('http://127.0.0.1:5000/api/bouquets', data=data, method='POST')
req.add_header('Content-Type', 'application/json')
req.add_header('Authorization', 'Bearer ' + token)
try:
    with urllib.request.urlopen(req) as response:
        print('SUCCESS BOUQUETS:', response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print('ERROR BOUQUETS:', e.code, e.read().decode('utf-8'))

# Test POST to /api/upload
boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
body = f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="test.txt"\r\nContent-Type: text/plain\r\n\r\nTest content\r\n--{boundary}--\r\n'
req = urllib.request.Request('http://127.0.0.1:5000/api/upload', data=body.encode('utf-8'), method='POST')
req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
req.add_header('Authorization', 'Bearer ' + token)
try:
    with urllib.request.urlopen(req) as response:
        print('SUCCESS UPLOAD:', response.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print('ERROR UPLOAD:', e.code, e.read().decode('utf-8'))
