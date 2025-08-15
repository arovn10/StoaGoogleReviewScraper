#!/usr/bin/env python3
"""
Test script to verify Domo webhook connection with flattened data structure.
Run this before the main scraper to ensure the webhook is working.
"""

import requests
import json
from datetime import datetime

def test_domo_webhook():
    """Test the Domo webhook with sample flattened review data matching CSV format."""
    
    # Domo webhook URL
    DOMO_WEBHOOK_URL = "https://stoagroup.domo.com/api/iot/v1/webhook/data/eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NTMzOTI4MDUsInN0cmVhbSI6IjI2ODFmZjgwNDJlODRkMGU5NzI0NjAyYTYxNTE1ZmNmOm1tbW0tMDA0NC0wNTc0OjUyMzIwNTM5NSJ9.zNgtfCRVytV6_RfB17ap-zkyXOYclCfvTUpTewZTOeo"
    
    # Test data with flattened structure matching CSV format exactly
    # Send the array directly to Domo - each review becomes a separate row
    test_data = [
        {
            'scraped_at': datetime.now().isoformat(),
            'review_text': 'This is a test review for Domo webhook testing.',
            'rating': 5,
            'reviewer_name': 'Test User 1',
            'review_date': '2025-01-20',
            'review_date_original': '2 days ago',
            'review_year': 2025,  # Integer
            'review_month': 1,    # Integer
            'review_month_name': 'January',
            'review_day_of_week': 'Monday',
            'Property': 'The Waters at Hammond',
            'property_url': 'https://example.com/test1',
            'request.ip': '127.0.0.1',
            'request.timestamp': int(datetime.now().timestamp() * 1000),  # Integer timestamp
            'extraction_method': 'test_webhook',
            '_BATCH_ID_': 1.0,  # Float
            '_BATCH_LAST_RUN_': datetime.now().isoformat()  # ISO timestamp string
        },
        {
            'scraped_at': datetime.now().isoformat(),
            'review_text': 'Another test review to verify the webhook is working correctly.',
            'rating': 4,
            'reviewer_name': 'Test User 2',
            'review_date': '2025-01-19',
            'review_date_original': '3 days ago',
            'review_year': 2025,  # Integer
            'review_month': 1,    # Integer
            'review_month_name': 'January',
            'review_day_of_week': 'Sunday',
            'Property': 'The Waters at Hammond',
            'property_url': 'https://example.com/test2',
            'request.ip': '127.0.0.1',
            'request.timestamp': int(datetime.now().timestamp() * 1000),  # Integer timestamp
            'extraction_method': 'test_webhook',
            '_BATCH_ID_': 1.0,  # Float
            '_BATCH_LAST_RUN_': datetime.now().isoformat()  # ISO timestamp string
        }
    ]
    
    print("🧪 Testing Domo Webhook with Flattened Data Structure")
    print("=" * 60)
    print(f"📊 Sending {len(test_data)} test reviews to Domo...")
    print(f"🌐 Webhook URL: {DOMO_WEBHOOK_URL}")
    print()
    
    try:
        # Send the test data directly to Domo
        # This should result in 2 separate rows in Domo
        response = requests.post(
            DOMO_WEBHOOK_URL,
            json=test_data,  # Send array directly, not wrapped
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"📡 Response Status: {response.status_code}")
        print(f"📡 Response Text: {response.text}")
        
        if response.status_code == 200:
            print("✅ SUCCESS: Test data sent to Domo webhook!")
            print(f"📊 Expected result: {len(test_data)} separate rows in Domo")
            print("🔍 Check your Domo dataset to verify the data structure")
        else:
            print("❌ FAILED: Domo webhook returned an error")
            print(f"💡 Status code: {response.status_code}")
            print(f"💡 Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ REQUEST ERROR: {str(e)}")
        print("💡 Check your internet connection and webhook URL")
        
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {str(e)}")
    
    print("\n🎯 Test completed!")
    print("💡 If successful, you should see 2 new rows in your Domo dataset")
    print("💡 Each row should contain one review with all the CSV fields")

if __name__ == "__main__":
    test_domo_webhook() 