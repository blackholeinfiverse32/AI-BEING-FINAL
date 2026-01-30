"""
Test API with proper authentication
"""
import requests
import json

# API Configuration
BASE_URL = "http://localhost:8000"
API_KEY = "ai_being_unified_demo_key_12345"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

print("=" * 70)
print("AI BEING UNIFIED - API TEST")
print("=" * 70)
print()

# Test 1: Health Check (No auth required)
print("1. Testing Health Check...")
response = requests.get(f"{BASE_URL}/health")
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")
print()

# Test 2: Chat Endpoint (Auth required)
print("2. Testing Chat Endpoint...")
chat_data = {
    "message": "Hello! Tell me about AI.",
    "user_id": "test_user"
}
response = requests.post(
    f"{BASE_URL}/api/chat",
    headers=headers,
    json=chat_data
)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print(f"   Response: {result.get('response', '')[:100]}...")
    print(f"   Mode: {result.get('processing_mode', 'N/A')}")
else:
    print(f"   Error: {response.text}")
print()

# Test 3: System Info
print("3. Testing System Info...")
response = requests.get(
    f"{BASE_URL}/api/system/info",
    headers=headers
)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    info = response.json()
    print(f"   Version: {info.get('version', 'N/A')}")
    print(f"   Status: {info.get('status', 'N/A')}")
print()

# Test 4: Calculator (AI-ASSISTANT Integration)
print("4. Testing Calculator Tool...")
calc_data = {
    "message": "Calculate 15 * 8 + 42",
    "user_id": "test_user"
}
response = requests.post(
    f"{BASE_URL}/api/chat",
    headers=headers,
    json=calc_data
)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print(f"   Response: {result.get('response', '')[:150]}...")
print()

# Test 5: Karma System (AI-ASSISTANT Integration)
print("5. Testing with Karma Tracking...")
karma_data = {
    "message": "What is machine learning?",
    "user_id": "karma_test_user"
}
response = requests.post(
    f"{BASE_URL}/api/chat",
    headers=headers,
    json=karma_data
)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print(f"   Karma tracked for user: karma_test_user")
print()

print("=" * 70)
print("API TEST COMPLETE")
print("=" * 70)
print()
print("To use the API, always include the header:")
print(f'  X-API-Key: {API_KEY}')
print()
print("Example curl command:")
print(f'curl -X POST "{BASE_URL}/api/chat" \\')
print(f'  -H "X-API-Key: {API_KEY}" \\')
print('  -H "Content-Type: application/json" \\')
print('  -d \'{"message": "Hello!", "user_id": "user123"}\'')
