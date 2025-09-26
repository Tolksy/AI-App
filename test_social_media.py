#!/usr/bin/env python3
import requests
import json

# Test the social media endpoint
url = "http://localhost:8000/api/v1/social-media/create"
payload = {
    "topic": "AI for entrepreneurs",
    "platform": "linkedin",
    "tone": "professional",
    "content_type": "post",
    "length": "medium",
    "include_hashtags": True
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("✅ Social Media API Working!")
        print(f"Generated Content: {result['content'][:100]}...")
        print(f"Hashtags: {result['hashtags']}")
        print(f"Optimal Time: {result['optimal_time']}")
    else:
        print(f"❌ Error: {response.text}")
except Exception as e:
    print(f"❌ Connection Error: {e}")
    print("Make sure the backend is running on localhost:8000")
