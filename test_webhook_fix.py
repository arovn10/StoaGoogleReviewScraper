import requests
import json

domo_webhook = "https://stoagroup.domo.com/api/iot/v1/webhook/data/eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NTMzOTI4MDUsInN0cmVhbSI6IjI2ODFmZjgwNDJlODRkMGU5NzI0NjAyYTYxNTE1ZmNmOm1tbW0tMDA0NC0wNTc0OjUyMzIwNTM5NSJ9.zNgtfCRVytV6_RfB17ap-zkyXOYclCfvTUpTewZTOeo"

# Test payload with the new ReviewDate field
test_payload = {
    "Property": "TEST - The Waters at Settlers Trace",
    "Reviewer": "Test User",
    "Rating": "5",
    "Comment": "This is a test review to verify the webhook is working with the corrected URL and new ReviewDate field.",
    "ReviewDate": "2 weeks ago"
}

try:
    response = requests.post(
        domo_webhook, 
        headers={"Content-Type": "application/json"}, 
        data=json.dumps(test_payload),
        timeout=30
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        print("✅ Webhook test successful! The corrected URL is working.")
    else:
        print(f"❌ Webhook test failed with status {response.status_code}")
        
except Exception as e:
    print(f"❌ Error testing webhook: {e}") 