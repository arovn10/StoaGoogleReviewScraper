#!/usr/bin/env python3
"""
Test script to verify Domo webhook connection.
Run this before the main scraper to ensure the webhook is working.
"""

import requests
import json
from datetime import datetime

def test_domo_webhook():
    """Test the Domo webhook with sample data."""
    
    # Domo webhook URL
    DOMO_WEBHOOK_URL = "https://stoagroup.domo.com/api/iot/v1/webhook/data/eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NTMzOTI4MDUsInN0cmVhbSI6IjI2ODFmZjgwNDJlODRkMGU5NzI0NjAyYTYxNTE1ZmNmOm1tbW0tMDA0NC0wNTc0OjUyMzIwNTM5NSJ9.zNgtfCRVytV6_RfB17ap-zkyXOYclCfvTUpTewZTOeo"
    
    # Test data
    test_data = {
        "timestamp": datetime.now().isoformat(),
        "test_type": "webhook_connection_test",
        "scraper_version": "working_auto_scraper_v1.0",
        "message": "This is a test message to verify Domo webhook connectivity",
        "sample_data": {
            "test_property": "Test Property",
            "test_reviews": 5,
            "status": "connection_test"
        }
    }
    
    print("🧪 Testing Domo webhook connection...")
    print(f"🔗 Webhook URL: {DOMO_WEBHOOK_URL}")
    print(f"📦 Test data: {json.dumps(test_data, indent=2)}")
    print()
    
    try:
        # Send test request
        print("🔄 Sending test request to Domo...")
        response = requests.post(
            DOMO_WEBHOOK_URL,
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📊 Response Headers: {dict(response.headers)}")
        print(f"📊 Response Body: {response.text}")
        
        if response.status_code == 200:
            print("✅ SUCCESS: Domo webhook is working correctly!")
            print("🚀 You can now run the main scraper with Domo integration enabled.")
        else:
            print(f"⚠️ WARNING: Domo webhook returned status {response.status_code}")
            print("💡 Check the response body for more details.")
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ ERROR: Connection failed - {str(e)}")
        print("💡 Check your internet connection and the webhook URL.")
    except requests.exceptions.Timeout as e:
        print(f"❌ ERROR: Request timed out - {str(e)}")
        print("💡 The webhook might be slow to respond.")
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: Request failed - {str(e)}")
        print("💡 There was an issue with the HTTP request.")
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {str(e)}")
        print("💡 Something unexpected went wrong.")

if __name__ == "__main__":
    test_domo_webhook() 