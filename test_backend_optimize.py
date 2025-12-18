#!/usr/bin/env python3
"""
Quick test script to test the optimize endpoint locally.
Run this to see if the backend is working correctly.
"""

import requests
import json

# Test data
test_data = {
    'num_stocks': 10,
    'target_beta': 1.0,
    'target_return': None,
    'strategy': 'diversified'
}

print("Testing /api/optimize endpoint...")
print(f"Request data: {json.dumps(test_data, indent=2)}")
print()

try:
    response = requests.post('http://localhost:5000/api/optimize', json=test_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("\n✅ SUCCESS! Backend is working correctly.")
    else:
        print(f"\n❌ ERROR: Status {response.status_code}")
        print("Check the backend terminal for detailed error logs.")
except requests.exceptions.ConnectionError:
    print("❌ ERROR: Cannot connect to backend.")
    print("Make sure the backend is running on http://localhost:5000")
except Exception as e:
    print(f"❌ ERROR: {str(e)}")

