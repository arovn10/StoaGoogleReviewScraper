#!/usr/bin/env python3
"""
Push data directly to Domo without wrapper - each review as separate call.
"""

import json
import requests
import time

def push_domo_direct():
    """Push each review directly to Domo webhook."""
    try:
        print("🚀 Pushing reviews directly to Domo webhook...")
        
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
        
        # Domo webhook URL
        domo_webhook_url = "https://stoagroup.domo.com/api/iot/v1/webhook/data/eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NTMzOTI4MDUsInN0cmVhbSI6IjI2ODFmZjgwNDJlODRkMGU5NzI0NjAyYTYxNTE1ZmNmOm1tbW0tMDA0NC0wNTc0OjUyMzIwNTM5NSJ9.zNgtfCRVytV6_RfB17ap-zkyXOYclCfvTUpTewZTOeo"
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        # Try sending without the "data" wrapper
        print(f"\n📤 Sending data without wrapper...")
        
        # Method 1: Send as direct array
        response = requests.post(
            domo_webhook_url,
            json=flattened_data,
            headers=headers,
            timeout=60
        )
        
        print(f"📊 Direct Array Response Status: {response.status_code}")
        print(f"📊 Direct Array Response Text: {response.text}")
        
        if response.status_code == 200:
            print(f"✅ Successfully pushed {len(flattened_data)} reviews to Domo!")
            return True
        else:
            print(f"❌ Direct array failed. Trying batch approach...")
            
            # Method 2: Send in smaller batches
            batch_size = 50
            total_sent = 0
            
            for i in range(0, len(flattened_data), batch_size):
                batch = flattened_data[i:i + batch_size]
                batch_num = (i // batch_size) + 1
                total_batches = (len(flattened_data) + batch_size - 1) // batch_size
                
                print(f"📦 Sending batch {batch_num}/{total_batches} ({len(batch)} reviews)...")
                
                response = requests.post(
                    domo_webhook_url,
                    json=batch,
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    total_sent += len(batch)
                    print(f"✅ Batch {batch_num} successful! Total sent: {total_sent}")
                else:
                    print(f"❌ Batch {batch_num} failed. Status: {response.status_code}")
                    print(f"Response: {response.text}")
                
                # Small delay between batches
                time.sleep(1)
            
            print(f"\n📊 Batch push complete. Total sent: {total_sent}/{len(flattened_data)}")
            return total_sent == len(flattened_data)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    push_domo_direct() 