#!/usr/bin/env python
"""
End-to-end API Test Script
Tests all backend endpoints to ensure they work correctly
"""

import requests
import sys

BASE_URL = "http://localhost:8000/api"

def test_endpoint(name, url, expected_status=200):
    """Test an API endpoint"""
    try:
        response = requests.get(url, timeout=10)
        status = "✅ PASS" if response.status_code == expected_status else f"❌ FAIL (status: {response.status_code})"
        print(f"{status} - {name}")
        
        if response.status_code != expected_status:
            print(f"  Response: {response.text[:200]}")
            return False
            
        # Check response structure
        data = response.json()
        if 'data' not in data or 'error' not in data or 'isSuccess' not in data:
            print(f"  ❌ Invalid response structure")
            return False
            
        return True
    except Exception as e:
        print(f"❌ ERROR - {name}: {str(e)}")
        return False

def main():
    print("\n🔍 Testing CivicView MGNREGA API Endpoints\n")
    print("=" * 60)
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Health Check
    tests_total += 1
    if test_endpoint("Health Check", f"{BASE_URL}/health/"):
        tests_passed += 1
    
    # Test 2: List Districts
    tests_total += 1
    if test_endpoint("List Districts", f"{BASE_URL}/districts/"):
        tests_passed += 1
    
    # Test 3: Get District Detail
    tests_total += 1
    if test_endpoint("Get District #1", f"{BASE_URL}/districts/1/"):
        tests_passed += 1
    
    # Test 4: District Summary
    tests_total += 1
    if test_endpoint("District Summary", f"{BASE_URL}/districts/1/summary/"):
        tests_passed += 1
    
    # Test 5: Historical Data
    tests_total += 1
    if test_endpoint("Historical Data (6 months)", 
                     f"{BASE_URL}/districts/1/history/?from=2025-05&to=2025-10"):
        tests_passed += 1
    
    # Test 6: Comparison
    tests_total += 1
    if test_endpoint("Compare Districts", 
                     f"{BASE_URL}/compare/?districts=1,2,3&metric=person_days&period=2025-10"):
        tests_passed += 1
    
    print("=" * 60)
    print(f"\n📊 Results: {tests_passed}/{tests_total} tests passed")
    
    if tests_passed == tests_total:
        print("✅ All tests passed! API is working correctly.\n")
        return 0
    else:
        print(f"❌ {tests_total - tests_passed} test(s) failed.\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
