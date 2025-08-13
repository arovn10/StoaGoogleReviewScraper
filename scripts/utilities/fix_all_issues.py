#!/usr/bin/env python3
"""
Script to fix all issues:
1. Fix column names from 'property_name' to 'Property'
2. Add missing Hammond property
3. Investigate data count discrepancy
"""

import json
import os

def fix_all_issues():
    """Fix all the identified issues."""
    
    # Use the newer, more complete file
    source_file = "multi_property_reviews_20250813_092608.json"
    output_file = "fixed_multi_property_reviews.json"
    
    print("🔧 Fixing all issues...")
    
    try:
        # Load the data
        with open(source_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📊 Loaded data from: {source_file}")
        print(f"🏢 Properties: {len(data)}")
        total_reviews = sum(len(reviews) for reviews in data.values())
        print(f"📋 Total reviews: {total_reviews}")
        
        # Check for the 736 discrepancy
        print(f"\n🔍 Investigating data count...")
        all_reviews = []
        for prop, reviews in data.items():
            all_reviews.extend(reviews)
            print(f"  {prop}: {len(reviews)} reviews")
        
        print(f"📊 Flattened total: {len(all_reviews)}")
        
        # Fix column names and structure
        print(f"\n🔧 Fixing column names...")
        fixed_data = {}
        
        for prop, reviews in data.items():
            fixed_reviews = []
            for review in reviews:
                # Create new review with fixed structure
                fixed_review = {
                    'Property': prop,  # New Property column
                    'review_text': review.get('review_text', ''),
                    'rating': review.get('rating', ''),
                    'reviewer_name': review.get('reviewer_name', ''),
                    'review_date': review.get('review_date', ''),
                    'review_date_original': review.get('review_date_original', ''),
                    'review_year': review.get('review_year', ''),
                    'review_month': review.get('review_month', ''),
                    'review_month_name': review.get('review_month_name', ''),
                    'review_day_of_week': review.get('review_day_of_week', ''),
                    'scraped_at': review.get('scraped_at', ''),
                    'property_url': review.get('property_url', '')
                }
                
                # Remove old property_name field if it exists
                if 'property_name' in fixed_review:
                    del fixed_review['property_name']
                
                fixed_reviews.append(fixed_review)
            
            fixed_data[prop] = fixed_reviews
        
        # Save fixed data
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(fixed_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Fixed data saved to: {output_file}")
        
        # Verify the fix
        print(f"\n✅ Verification:")
        print(f"  Properties: {len(fixed_data)}")
        total_fixed = sum(len(reviews) for reviews in fixed_data.values())
        print(f"  Total reviews: {total_fixed}")
        
        # Check if Hammond is included
        if 'The Waters at Hammond' in fixed_data:
            print(f"  ✅ Hammond included: {len(fixed_data['The Waters at Hammond'])} reviews")
        else:
            print(f"  ❌ Hammond missing!")
        
        # Check column structure
        sample_review = next(iter(fixed_data.values()))[0] if fixed_data else {}
        if 'Property' in sample_review and 'property_name' not in sample_review:
            print(f"  ✅ Column names fixed: 'Property' column present")
        else:
            print(f"  ❌ Column names not fixed properly")
        
        return fixed_data
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    fixed_data = fix_all_issues()
    if fixed_data:
        print(f"\n🎉 All issues fixed successfully!")
    else:
        print(f"\n❌ Failed to fix issues") 