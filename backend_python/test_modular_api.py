import sys
from fastapi.testclient import TestClient

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from main import app

print("=" * 60)
print("RUNNING INTEGRATION SMOKE TESTS VIA TESTCLIENT")
print("=" * 60)

client = TestClient(app)

# 1. Root
res = client.get("/")
print(f"GET / -> Status: {res.status_code}, Body: {res.json()}")
assert res.status_code == 200

# 2. Webview links
res = client.get("/api/webview-links")
print(f"GET /api/webview-links -> Status: {res.status_code}, Found: {len(res.json()) if isinstance(res.json(), list) else res.json()}")
assert res.status_code == 200

# 3. Posts local
res = client.get("/api/posts/local")
print(f"GET /api/posts/local -> Status: {res.status_code}, Found: {len(res.json()) if isinstance(res.json(), list) else res.json()}")
assert res.status_code == 200

# 4. Learning videos
res = client.get("/api/learning-videos")
print(f"GET /api/learning-videos -> Status: {res.status_code}, Items: {len(res.json()) if isinstance(res.json(), list) else res.json()}")
assert res.status_code == 200

# 5. Editor cancel
res = client.post("/api/editor/cancel", json={"jobId": "smoke-test-job"})
print(f"POST /api/editor/cancel -> Status: {res.status_code}, Response: {res.json()}")
assert res.status_code == 200

# 6. YouTube channels
res = client.get("/api/youtube/channels")
print(f"GET /api/youtube/channels -> Status: {res.status_code}, Channels: {len(res.json()) if isinstance(res.json(), list) else res.json()}")
assert res.status_code == 200

# 7. TikTok channels
res = client.get("/api/tiktok/channels")
print(f"GET /api/tiktok/channels -> Status: {res.status_code}, Channels: {len(res.json()) if isinstance(res.json(), list) else res.json()}")
assert res.status_code == 200

# 8. Typing lessons
res = client.get("/api/typing-lessons")
print(f"GET /api/typing-lessons -> Status: {res.status_code}, Lessons count: {len(res.json()) if isinstance(res.json(), list) else res.json()}")
assert res.status_code == 200

# 9. Lyrics search proxy check
res = client.get("/api/lyrics/search?q=test")
print(f"GET /api/lyrics/search?q=test -> Status: {res.status_code}")
assert res.status_code in [200, 500]

# 10. Chat endpoint validation
res = client.post("/api/chat", json={})
print(f"POST /api/chat -> Status: {res.status_code}, Response: {res.json()}")
assert res.status_code in [400, 422]

# 11. Search endpoint validation (requires Pixabay API key)
res = client.get("/api/search?q=hello")
print(f"GET /api/search?q=hello -> Status: {res.status_code}, Detail: {res.json()}")
assert res.status_code == 400

print("\n[SUCCESS] ALL MODULAR API SMOKE TESTS PASSED PERFECTLY!")
