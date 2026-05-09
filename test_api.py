import requests

BASE_URL = "http://127.0.0.1:8000/api/"

credentials = {
    "email": "Aug1best1@gmail.com", 
    "password": "1A2S3D4F5G"
}

print("--- Testing Authentication ---")
auth_response = requests.post(f"{BASE_URL}token/", json=credentials)

if auth_response.status_code == 200:
    print("✅ Login Successful!")
    access_token = auth_response.json().get('access')
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "content": "I need a vacation next Monday"
    }
    
    print("\n--- Testing the Muayien Bot ---")
    bot_response = requests.post(f"{BASE_URL}message/", json=payload, headers=headers)
    
    if bot_response.status_code in [200, 201]:
        print("✅ Message Processed Successfully!")
        print("\nBot Reply:")
        print(bot_response.json())
    else:
        print(f"❌ Failed to send message. Status: {bot_response.status_code}")
        print(bot_response.text)
        
else:
    print("❌ Login Failed! Check your email and password.")
    print(auth_response.text)