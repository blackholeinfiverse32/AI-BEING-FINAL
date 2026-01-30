# API Authentication - Quick Reference

## Why 401 Unauthorized?

The API requires authentication for security. You need to include an API key in your requests.

## Default API Key

```
ai_being_unified_demo_key_12345
```

## How to Use

### PowerShell (curl)
```powershell
curl -X POST "http://localhost:8000/api/chat" `
  -H "X-API-Key: ai_being_unified_demo_key_12345" `
  -H "Content-Type: application/json" `
  -d '{\"message\": \"Hello!\", \"user_id\": \"user123\"}'
```

### Python
```python
import requests

headers = {"X-API-Key": "ai_being_unified_demo_key_12345"}
response = requests.post(
    "http://localhost:8000/api/chat",
    headers=headers,
    json={"message": "Hello!", "user_id": "user123"}
)
print(response.json())
```

### JavaScript (fetch)
```javascript
fetch('http://localhost:8000/api/chat', {
  method: 'POST',
  headers: {
    'X-API-Key': 'ai_being_unified_demo_key_12345',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: 'Hello!',
    user_id: 'user123'
  })
})
.then(res => res.json())
.then(data => console.log(data));
```

### Postman / Insomnia
1. Open Headers tab
2. Add header:
   - Key: `X-API-Key`
   - Value: `ai_being_unified_demo_key_12345`

## Test the API

Run the test script:
```powershell
cd "c:\Users\Microsoft\Desktop\integration endpoints\ai_being_unified"
python test_api.py
```

## Endpoints That Need Authentication

- ✅ `/api/chat` - Requires API key
- ✅ `/api/tasks` - Requires API key
- ✅ `/api/search` - Requires API key
- ✅ `/api/system/info` - Requires API key
- ❌ `/health` - No auth required
- ❌ `/docs` - No auth required

## Change API Key

Edit `.env` file:
```
API_KEY=your_custom_key_here
```

Then restart the server.

## Security Note

The demo key is for testing only. In production:
1. Generate a strong random key
2. Store it securely
3. Use HTTPS
4. Rotate keys regularly
