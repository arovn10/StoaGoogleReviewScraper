#!/usr/bin/env python3
"""
Debug script to see exactly what we're sending to Domo.
"""

import json
import requests

def debug_domo_push():
    """Debug the Domo webhook push."""
    try:
        print("🔍 Debugging Domo webhook push...")
        
        # Load the fixed JSON file
        json_file = "fixed_multi_property_reviews.json"
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 Loaded data from: {json_file}")
        
        # Convert to list format for Domo (flatten the data)
        flattened_data = []
        for property_name, reviews in data.items():
            for review in reviews:
                # Ensure Property column is set
                review['Property'] = property_name
                flattened_data.append(review)
        
        print(f"📋 Total reviews to push: {len(flattened_data)}")
        
        # Show sample of what we're sending
        print(f"\n📝 Sample data being sent:")
        print(f"First review: {json.dumps(flattened_data[0], indent=2)}")
        
        # Domo webhook URL
        domo_webhook_url = "https://stoagroup.domo.com/api/iot/v1/webhook/data/eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NTMzOTI4MDUsInN0cmVhbSI6IjI2ODFmZjgwNDJlODRkMGU5NzI0NjAyYTYxNTE1ZmNmOm1tbW0tMDA0NC0wNTc0OjUyMzIwNTM5NSJ9.zNgtfCRVytV6_RfB17ap-zkyXOYclCfvTUpTewZTOeo"
        
        # Try different payload formats
        print(f"\n🧪 Testing different payload formats...")
        
        # Format 1: Current format
        payload1 = {
            "data": flattened_data
        }
        
        # Format 2: Direct array
        payload2 = flattened_data
        
        # Format 3: With metadata
        payload3 = {
            "reviews": flattened_data,
            "total_count": len(flattened_data),
            "properties": list(set(review['Property'] for review in flattened_data))
        }
        
        print(f"\n📤 Testing Format 1 (current):")
        print(f"Payload structure: {type(payload1)}")
        print(f"Payload keys: {list(payload1.keys())}")
        print(f"Data type: {type(payload1['data'])}")
        print(f"Data length: {len(payload1['data'])}")
        
        # Test the webhook with a small sample first
        test_data = flattened_data[:3]  # Just 3 reviews for testing
        test_payload = {"data": test_data}
        
        print(f"\n🧪 Testing with 3 reviews first...")
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            domo_webhook_url,
            json=test_payload,
            headers=headers,
            timeout=30
        )
        
        print(f"📊 Test Response Status: {response.status_code}")
        print(f"📊 Test Response Text: {response.text}")
        
        if response.status_code == 200:
            print(f"✅ Test successful! Now sending full data...")
            
            # Send full data
            response = requests.post(
                domo_webhook_url,
                json=payload1,
                headers=headers,
                timeout=60
            )
            
            print(f"📊 Full Response Status: {response.status_code}")
            print(f"📊 Full Response Text: {response.text}")
            
            if response.status_code == 200:
                print(f"✅ Successfully pushed {len(flattened_data)} reviews to Domo!")
                return True
            else:
                print(f"❌ Failed to push full data. Status code: {response.status_code}")
                return False
        else:
            print(f"❌ Test failed. Status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    debug_domo_push() 