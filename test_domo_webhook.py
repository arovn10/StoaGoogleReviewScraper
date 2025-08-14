#!/usr/bin/env python3
"""
Test script to verify Domo webhook connection with flattened data structure.
Run this before the main scraper to ensure the webhook is working.
"""

import requests
import json
from datetime import datetime

def test_domo_webhook():
    """Test the Domo webhook with sample flattened review data."""
    
    # Domo webhook URL
    DOMO_WEBHOOK_URL = "https://stoagroup.domo.com/api/iot/v1/webhook/data/eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NTMzOTI4MDUsInN0cmVhbSI6IjI2ODFmZjgwNDJlODRkMGU5NzI0NjAyYTYxNTE1ZmNmOm1tbW0tMDA0NC0wNTc0OjUyMzIwNTM5NSJ9.zNgtfCRVytV6_RfB17ap-zkyXOYclCfvTUpTewZTOeo"
    
    # Test data with flattened structure - one row per review
    test_data = {
        "batch_number": 1,
        "total_batches": 1,
        "batch_size": 3,
        "total_reviews": 3,
        "timestamp": datetime.now().isoformat(),
        "scraper_version": "working_auto_scraper_v1.0",
        "reviews": [
            {
                "timestamp": datetime.now().isoformat(),
                "scraper_version": "working_auto_scraper_v1.0",
                "property_name": "The Waters at Hammond",
                "review_text": "This is a test review for testing the Domo webhook integration. The apartment complex is great and the staff is friendly.",
                "rating": 5,
                "reviewer_name": "Test User 1",
                "review_date": "2025-01-20",
                "review_date_original": "2 days ago",
                "review_year": 2025,
                "review_month": 1,
                "review_month_name": "January",
                "review_day_of_week": "Monday",
                "scraped_at": datetime.now().isoformat(),
                "extraction_method": "test_data",
                "property_url": "https://example.com/test",
                "debug_info": "Test data for webhook verification"
            },
            {
                "timestamp": datetime.now().isoformat(),
                "scraper_version": "working_auto_scraper_v1.0",
                "property_name": "The Waters at Hammond",
                "review_text": "Another test review to verify the flattened data structure works correctly with Domo.",
                "rating": 4,
                "reviewer_name": "Test User 2",
                "review_date": "2025-01-19",
                "review_date_original": "3 days ago",
                "review_year": 2025,
                "review_month": 1,
                "review_month_name": "January",
                "review_day_of_week": "Sunday",
                "scraped_at": datetime.now().isoformat(),
                "extraction_method": "test_data",
                "property_url": "https://example.com/test",
                "debug_info": "Test data for webhook verification"
            },
            {
                "timestamp": datetime.now().isoformat(),
                "scraper_version": "working_auto_scraper_v1.0",
                "property_name": "The Flats at East Bay",
                "review_text": "Third test review from a different property to ensure property_name field works correctly.",
                "rating": 5,
                "reviewer_name": "Test User 3",
                "review_date": "2025-01-18",
                "review_date_original": "4 days ago",
                "review_year": 2025,
                "review_month": 1,
                "review_month_name": "January",
                "review_day_of_week": "Saturday",
                "scraped_at": datetime.now().isoformat(),
                "extraction_method": "test_data",
                "property_url": "https://example.com/test2",
                "debug_info": "Test data for webhook verification"
            }
        ]
    }
    
    print("🧪 Testing Domo Webhook with Flattened Data Structure")
    print("=" * 60)
    print(f"🌐 Webhook URL: {DOMO_WEBHOOK_URL}")
    print(f"📊 Test data: {len(test_data['reviews'])} sample reviews")
    print(f"📦 Batch info: {test_data['batch_number']}/{test_data['total_batches']}")
    print()
    
    try:
        print("🔄 Sending test data to Domo...")
        response = requests.post(
            DOMO_WEBHOOK_URL,
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"📡 Response Status: {response.status_code}")
        print(f"📡 Response Text: {response.text}")
        
        if response.status_code == 200:
            print("✅ SUCCESS: Webhook connection working!")
            print("🎯 Your Domo should now have 3 test review records")
            print("📊 Each review will appear as a separate row in your dataset")
        else:
            print("❌ FAILED: Webhook returned non-200 status")
            print("🔍 Check the response text above for error details")
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR: Could not connect to Domo webhook")
        print("🔍 Check your internet connection and webhook URL")
    except requests.exceptions.Timeout:
        print("❌ TIMEOUT: Request took too long")
        print("🔍 Check your network connection")
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {str(e)}")
        print("🔍 Check the error details above")

if __name__ == "__main__":
    test_domo_webhook() 