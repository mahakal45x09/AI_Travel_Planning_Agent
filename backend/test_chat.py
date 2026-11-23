"""Quick test for the chat API endpoint."""
import urllib.request
import json

url = "http://localhost:8000/api/chat/"
data = json.dumps({"message": "Show me Rajasthan destinations"}).encode()
headers = {"Content-Type": "application/json"}

req = urllib.request.Request(url, data=data, headers=headers)
try:
    resp = urllib.request.urlopen(req, timeout=30)
    result = json.loads(resp.read().decode())
    print("✅ Chat API working!")
    print(f"Session: {result.get('session_id', 'N/A')}")
    reply = result.get("reply", "")
    print(f"Reply ({len(reply)} chars):")
    print(reply[:800])
except Exception as e:
    print(f"❌ Error: {e}")
