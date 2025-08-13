#!/usr/bin/env python3
import json

def check_data():
    try:
        with open('multi_property_reviews_20250813_091752.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"Properties: {len(data)}")
        total_reviews = sum(len(reviews) for reviews in data.values())
        print(f"Total reviews: {total_reviews}")
        print("\nProperty breakdown:")
        
        for prop, reviews in data.items():
            print(f"  {prop}: {len(reviews)} reviews")
            
        # Check for duplicates
        print(f"\nChecking for duplicates...")
        all_reviews = []
        for prop, reviews in data.items():
            for review in reviews:
                review['Property'] = prop
                all_reviews.append(review)
        
        # Check for duplicate review text
        review_texts = [review.get('review_text', '') for review in all_reviews]
        unique_texts = set(review_texts)
        print(f"Unique review texts: {len(unique_texts)}")
        print(f"Total reviews: {len(all_reviews)}")
        print(f"Potential duplicates: {len(all_reviews) - len(unique_texts)}")
        
        # Check for exact duplicates
        seen = set()
        duplicates = 0
        for review in all_reviews:
            review_key = f"{review.get('review_text', '')}_{review.get('reviewer_name', '')}_{review.get('rating', '')}"
            if review_key in seen:
                duplicates += 1
            else:
                seen.add(review_key)
        
        print(f"Exact duplicates: {duplicates}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_data() 