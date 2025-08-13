#!/usr/bin/env python3
"""
Fix the data structure so Domo can properly display each field as a column.
"""

import json
import requests

def fix_domo_structure():
    """Restructure data for proper Domo column display."""
    try:
        print("🔧 Fixing data structure for Domo...")
        
        # Load the fixed JSON file
        json_file = "fixed_multi_property_reviews.json"
        
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 Loaded data from: {json_file}")
        
        # Restructure: flatten each review into individual fields
        flattened_reviews = []
        for property_name, reviews in data.items():
            for review in reviews:
                # Create a flat structure with each field as a top-level key
                flat_review = {
                    'Property': property_name,
                    'Review_Text': review.get('review_text', ''),
                    'Rating': review.get('rating', ''),
                    'Reviewer_Name': review.get('reviewer_name', ''),
                    'Review_Date': review.get('review_date', ''),
                    'Review_Date_Original': review.get('review_date_original', ''),
                    'Review_Year': review.get('review_year', ''),
                    'Review_Month': review.get('review_month', ''),
                    'Review_Month_Name': review.get('review_month_name', ''),
                    'Review_Day_of_Week': review.get('review_day_of_week', ''),
                    'Scraped_At': review.get('scraped_at', ''),
                    'Property_URL': review.get('property_url', '')
                }
                flattened_reviews.append(flat_review)
        
        print(f"📋 Total reviews to push: {len(flattened_reviews)}")
        
        # Show sample of new structure
        print(f"\n📝 Sample of new structure:")
        print(f"First review: {json.dumps(flattened_reviews[0], indent=2)}")
        
        # Save the restructured data
        output_file = "domo_ready_reviews.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(flattened_reviews, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Restructured data saved to: {output_file}")
        
        # Now push to Domo
        print(f"\n🚀 Pushing restructured data to Domo...")
        
        domo_webhook_url = "https://stoagroup.domo.com/api/iot/v1/webhook/data/eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NTMzOTI4MDUsInN0cmVhbSI6IjI2ODFmZjgwNDJlODRkMGU5NzI0NjAyYTYxNTE1ZmNmOm1tbW0tMDA0NC0wNTc0OjUyMzIwNTM5NSJ9.zNgtfCRVytV6_RfB17ap-zkyXOYclCfvTUpTewZTOeo"
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        # Send the restructured data
        response = requests.post(
            domo_webhook_url,
            json=flattened_reviews,
            headers=headers,
            timeout=60
        )
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📊 Response Text: {response.text}")
        
        if response.status_code == 200:
            print(f"✅ Successfully pushed {len(flattened_reviews)} reviews to Domo!")
            print(f"🎯 Each review field should now appear as a separate column!")
            return True
        else:
            print(f"❌ Failed to push to Domo. Status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    fix_domo_structure() 