#!/usr/bin/env python3
"""
Quick test to send reviews after webhook configuration changes
"""

import json
import requests

domo_webhook = "https://stoagroup.domo.com/api/iot/v1/webhook/data/eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NTMzOTI4MDUsInN0cmVhbSI6IjI2ODFmZjgwNDJlODRkMGU5NzI0NjAyYTYxNTE1ZmNmOm1tbW0tMDA0NC0wNTc0OjUyMzIwNTM5NSJ9.zNgtfCRVytV6_RfB17ap-zkyXOYclCfvTUpTewZTOeo"

# Test review
test_review = {
    "Property": "CONFIG TEST - The Waters at Bluebonnet",
    "Reviewer": "Test User",
    "Rating": "5", 
    "Comment": "Testing webhook configuration changes. This should appear in Domo now."
}

print("Sending test review after webhook configuration changes...")
print(json.dumps(test_review, indent=2))

try:
    response = requests.post(
        domo_webhook,
        headers={"Content-Type": "application/json"},
        data=json.dumps(test_review),
        timeout=30
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Test review sent successfully!")
        print("Now check the Data Preview section in your Domo webhook configuration.")
    else:
        print(f"❌ Failed: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}") 