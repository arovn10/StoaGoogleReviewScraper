#!/usr/bin/env python3
"""
Quick script to push existing JSON data to Domo webhook.
"""

import json
import requests

def push_to_domo():
    """Push the existing JSON file to Domo webhook."""
    try:
        print("🚀 Pushing existing data to Domo webhook...")
        
        # Load the existing JSON file
        json_file = "multi_property_reviews_20250813_091752.json"
        
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
        
        # Domo webhook URL
        domo_webhook_url = "https://stoagroup.domo.com/api/iot/v1/webhook/data/eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NTMzOTI4MDUsInN0cmVhbSI6IjI2ODFmZjgwNDJlODRkMGU5NzI0NjAyYTYxNTE1ZmNmOm1tbW0tMDA0NC0wNTc0OjUyMzIwNTM5NSJ9.zNgtfCRVytV6_RfB17ap-zkyXOYclCfvTUpTewZTOeo"
        
        # Prepare the payload
        payload = {
            "data": flattened_data
        }
        
        # Send POST request to Domo
        headers = {
            'Content-Type': 'application/json'
        }
        
        print("📤 Sending data to Domo...")
        response = requests.post(
            domo_webhook_url,
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            print(f"✅ Successfully pushed {len(flattened_data)} reviews to Domo!")
            print(f"📊 Response: {response.text}")
            return True
        else:
            print(f"❌ Failed to push to Domo. Status code: {response.status_code}")
            print(f"📊 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error pushing to Domo: {str(e)}")
        return False

if __name__ == "__main__":
    push_to_domo() 