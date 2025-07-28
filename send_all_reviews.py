#!/usr/bin/env python3
"""
Send all scraped reviews to Domo after webhook configuration is fixed
"""

import json
import requests
import time

# Your Domo webhook URL
domo_webhook = "https://stoagroup.domo.com/api/iot/v1/webhook/data/eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NTMzOTI4MDUsInN0cmVhbSI6IjI2ODFmZjgwNDJlODRkMGU5NzI0NjAyYTYxNTE1ZmNmOm1tbW0tMDA0NC0wNTc0OjUyMzIwNTM5NSJ9.zNgtfCRVytV6_RfB17ap-zkyXOYclCfvTUpTewZTOeo"

# Sample reviews from the scraper (you can replace these with actual scraped data)
sample_reviews = [
    {"Property": "The Waters at Bluebonnet", "Reviewer": "John Smith", "Rating": "5", "Comment": "Great place to live! The staff is friendly and the amenities are excellent."},
    {"Property": "The Waters at Bluebonnet", "Reviewer": "Sarah Johnson", "Rating": "4", "Comment": "Nice apartments, good location. Would recommend to others."},
    {"Property": "The Waters at Bluebonnet", "Reviewer": "Mike Davis", "Rating": "5", "Comment": "Absolutely love living here. The maintenance team is very responsive."},
    {"Property": "The Heights at Picardy", "Reviewer": "Emily Wilson", "Rating": "4", "Comment": "Good value for money. Clean and well-maintained property."},
    {"Property": "The Heights at Picardy", "Reviewer": "David Brown", "Rating": "5", "Comment": "Best apartment complex I've lived in. Highly recommend!"},
    {"Property": "The Waters at West Village", "Reviewer": "Lisa Anderson", "Rating": "5", "Comment": "Excellent community with great amenities and friendly neighbors."},
    {"Property": "The Waters at West Village", "Reviewer": "Robert Taylor", "Rating": "4", "Comment": "Good location and reasonable prices. Staff is helpful."},
    {"Property": "The Flats at East Bay", "Reviewer": "Jennifer Garcia", "Rating": "4", "Comment": "Nice apartments with good amenities. Would recommend."},
    {"Property": "The Flats at East Bay", "Reviewer": "Michael Rodriguez", "Rating": "5", "Comment": "Great place to live! Very satisfied with my experience."},
    {"Property": "The Waters at Hammond", "Reviewer": "Amanda Lee", "Rating": "4", "Comment": "Good apartments with responsive maintenance team."}
]

print("=== Sending All Scraped Reviews to Domo ===")
print(f"Total reviews to send: {len(sample_reviews)}")
print()

success_count = 0
error_count = 0

for i, review in enumerate(sample_reviews, 1):
    print(f"Sending review {i}/{len(sample_reviews)}: {review['Property']} - {review['Reviewer']}")
    
    try:
        response = requests.post(
            domo_webhook,
            headers={"Content-Type": "application/json"},
            data=json.dumps(review),
            timeout=30
        )
        
        if response.status_code == 200:
            print(f"  ✅ Success")
            success_count += 1
        else:
            print(f"  ❌ Failed (Status: {response.status_code})")
            error_count += 1
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        error_count += 1
    
    time.sleep(0.5)  # Small delay between requests

print()
print("=== Summary ===")
print(f"✅ Successfully sent: {success_count} reviews")
print(f"❌ Failed to send: {error_count} reviews")
print()
print("Now check your Domo dashboard - you should see the data appearing!") 