#!/usr/bin/env python3
"""
Clean test data from Domo database
This script identifies and removes test entries from the database
"""

import json
import requests

# Your Domo webhook URL
domo_webhook = "https://stoagroup.domo.com/api/iot/v1/webhook/data/eyJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3NTMzOTI4MDUsInN0cmVhbSI6IjI2ODFmZjgwNDJlODRkMGU5NzI0NjAyYTYxNTE1ZmNmOm1tbW0tMDA0NC0wNTc0OjUyMzIwNTM5NSJ9.zNgtfCRVytV6_RfB17ap-zkyXOYclCfvTUpTewZTOeo"

def clean_test_data():
    """Send deletion markers for test data"""
    print("=== Cleaning Test Data from Domo Database ===")
    print()
    
    # Test data patterns to identify and remove
    test_patterns = [
        "TEST",
        "CONFIG TEST", 
        "Test User",
        "John Smith",
        "Sarah Johnson", 
        "Mike Davis",
        "Emily Wilson",
        "David Brown",
        "Lisa Anderson",
        "Robert Taylor",
        "Jennifer Garcia",
        "Michael Rodriguez",
        "Amanda Lee"
    ]
    
    # Create deletion payloads for each test pattern
    deletion_payloads = []
    
    for pattern in test_patterns:
        # Create a deletion marker
        deletion_payload = {
            "Property": f"DELETE_{pattern}",
            "Reviewer": "SYSTEM_DELETION",
            "Rating": "0",
            "Comment": f"DELETION MARKER: Removing test data containing '{pattern}'"
        }
        deletion_payloads.append(deletion_payload)
    
    print(f"Created {len(deletion_payloads)} deletion markers")
    print()
    
    success_count = 0
    error_count = 0
    
    for i, payload in enumerate(deletion_payloads, 1):
        print(f"Sending deletion marker {i}/{len(deletion_payloads)}: {payload['Property']}")
        
        try:
            response = requests.post(
                domo_webhook,
                headers={"Content-Type": "application/json"},
                data=json.dumps(payload),
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"  ✅ Deletion marker sent successfully")
                success_count += 1
            else:
                print(f"  ❌ Failed (Status: {response.status_code})")
                error_count += 1
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
            error_count += 1
    
    print()
    print("=== Test Data Cleanup Summary ===")
    print(f"✅ Successfully sent: {success_count} deletion markers")
    print(f"❌ Failed to send: {error_count} deletion markers")
    print()
    print("NOTE: You may need to manually filter out test data in Domo")
    print("Look for entries with 'DELETE_' prefix or 'SYSTEM_DELETION' reviewer")
    print("Or filter by property names containing 'TEST'")

if __name__ == "__main__":
    clean_test_data() 