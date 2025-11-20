#!/usr/bin/env python3
"""
Quick test to verify the backend works
"""
import requests
import json

def test_backend():
    try:
        # Test health endpoint
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure it's running on http://localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Error testing backend: {e}")
        return False

if __name__ == "__main__":
    test_backend()

