#!/usr/bin/env python3
"""
Test script to verify the data structure matches CSV format exactly.
This helps ensure all required fields are present before running the scraper.
"""

import json
from datetime import datetime
import time

def test_data_structure():
    """Test that the data structure matches the CSV format exactly."""
    
    print("🧪 Testing Data Structure for CSV Format Compatibility")
    print("=" * 60)
    
    # Simulate the data structure that would be created by the scraper
    sample_reviews = [
        {
            'scraped_at': datetime.now().isoformat(),
            'review_text': 'This is a test review for testing the data structure.',
            'rating': 5,
            'reviewer_name': 'Test User 1',
            'review_date': '2025-01-20',
            'review_date_original': '2 days ago',
            'review_year': '2025',
            'review_month': '1',
            'review_month_name': 'January',
            'review_day_of_week': 'Monday',
            'Property': 'The Waters at Hammond',  # Added this field
            'property_url': 'https://example.com/test',
            'request.ip': '127.0.0.1',
            'request.timestamp': str(int(time.time() * 1000)),
            'extraction_method': 'test_data',
            '_BATCH_ID_': 'test_batch_1',
            '_BATCH_LAST_RUN_': datetime.now().isoformat()
        },
        {
            'scraped_at': datetime.now().isoformat(),
            'review_text': 'Another test review to verify all fields are present.',
            'rating': 4,
            'reviewer_name': 'Test User 2',
            'review_date': '2025-01-19',
            'review_date_original': '3 days ago',
            'review_year': '2025',
            'review_month': '1',
            'review_month_name': 'January',
            'review_day_of_week': 'Sunday',
            'Property': 'The Waters at Hammond',  # Added this field
            'property_url': 'https://example.com/test',
            'request.ip': '127.0.0.1',
            'request.timestamp': str(int(time.time() * 1000)),
            'extraction_method': 'test_data',
            '_BATCH_ID_': 'test_batch_1',
            '_BATCH_LAST_RUN_': datetime.now().isoformat()
        }
    ]
    
    # Expected CSV columns from the data (1).csv file
    expected_columns = [
        'scraped_at',
        'review_text', 
        'rating',
        'reviewer_name',
        'review_date',
        'review_date_original',
        'review_year',
        'review_month',
        'review_month_name',
        'review_day_of_week',
        'Property',
        'property_url',
        'request.ip',
        'request.timestamp',
        'extraction_method',
        '_BATCH_ID_',
        '_BATCH_LAST_RUN_'
    ]
    
    print("📋 Expected CSV Columns:")
    for i, col in enumerate(expected_columns, 1):
        print(f"   {i:2d}. {col}")
    
    print("\n🔍 Checking Sample Review Data:")
    
    # Check each review
    for i, review in enumerate(sample_reviews, 1):
        print(f"\n📝 Review {i}:")
        missing_fields = []
        
        for col in expected_columns:
            if col in review:
                value = review[col]
                if value is not None and value != '':
                    print(f"   ✅ {col}: {str(value)[:50]}{'...' if len(str(value)) > 50 else ''}")
                else:
                    print(f"   ⚠️  {col}: (empty)")
                    missing_fields.append(col)
            else:
                print(f"   ❌ {col}: MISSING")
                missing_fields.append(col)
        
        if missing_fields:
            print(f"   ⚠️  Review {i} has {len(missing_fields)} missing/empty fields: {missing_fields}")
        else:
            print(f"   ✅ Review {i} has all required fields")
    
    # Test the flattened structure for Domo
    print("\n🔗 Testing Domo Webhook Structure:")
    
    # Simulate the flattened structure that would be sent to Domo
    domo_payload = {
        'batch_number': 1,
        'total_batches': 1,
        'batch_size': len(sample_reviews),
        'total_reviews': len(sample_reviews),
        'timestamp': datetime.now().isoformat(),
        'scraper_version': 'working_auto_scraper_v1.0',
        'reviews': sample_reviews
    }
    
    print(f"📊 Domo payload structure:")
    print(f"   - batch_number: {domo_payload['batch_number']}")
    print(f"   - total_batches: {domo_payload['total_batches']}")
    print(f"   - batch_size: {domo_payload['batch_size']}")
    print(f"   - total_reviews: {domo_payload['total_reviews']}")
    print(f"   - reviews array length: {len(domo_payload['reviews'])}")
    
    # Verify that each review in the Domo payload has all required fields
    print(f"\n🔍 Verifying Domo payload reviews:")
    for i, review in enumerate(domo_payload['reviews'], 1):
        missing_in_domo = [col for col in expected_columns if col not in review or review[col] is None or review[col] == '']
        if missing_in_domo:
            print(f"   ⚠️  Domo review {i} missing: {missing_in_domo}")
        else:
            print(f"   ✅ Domo review {i} complete")
    
    print("\n🎯 Summary:")
    print(f"   - Expected columns: {len(expected_columns)}")
    print(f"   - Sample reviews: {len(sample_reviews)}")
    print(f"   - CSV format compatibility: {'✅ PASS' if all(all(col in review for col in expected_columns) for review in sample_reviews) else '❌ FAIL'}")
    print(f"   - Domo webhook compatibility: {'✅ PASS' if all(all(col in review for col in expected_columns) for review in domo_payload['reviews']) else '❌ FAIL'}")
    
    # Save sample data to JSON for inspection
    output_file = "test_data_structure_output.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'expected_columns': expected_columns,
            'sample_reviews': sample_reviews,
            'domo_payload': domo_payload
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Sample data saved to: {output_file}")
    print("🔍 You can inspect this file to verify the data structure")

if __name__ == "__main__":
    test_data_structure() 