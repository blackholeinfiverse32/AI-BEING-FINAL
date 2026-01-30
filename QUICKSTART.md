# 🚀 Quick Start Guide - AI Being Unified

## Step-by-Step Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/blackholeinfiverse32/AI-BEING-FINAL.git
cd AI-BEING-FINAL
```

### 2️⃣ Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Environment
```bash
# Copy the example environment file
copy .env.example .env

# Edit .env file (already configured with default values)
# The API key is already set to: ai_being_unified_demo_key_12345
```

### 4️⃣ Start the System

#### Option A: API Server (Recommended)
```bash
python main.py --mode server
```
- Server runs at: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

#### Option B: Interactive Chat
```bash
python main.py --mode interactive
```

#### Option C: Demo Mode
```bash
python main.py --mode demo
```

### 5️⃣ Test the API

#### Using Swagger UI (Easiest)
1. Open http://localhost:8000/docs
2. Click "Authorize" button (🔒 icon)
3. Enter API Key: `ai_being_unified_demo_key_12345`
4. Click "Authorize" then "Close"
5. Try the `/api/chat` endpoint with:
   ```json
   {
     "message": "Hello, how are you?",
     "user_id": "test_user",
     "session_id": "test_session"
   }
   ```

#### Using cURL
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "X-API-Key: ai_being_unified_demo_key_12345" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"What is AI?\", \"user_id\": \"user1\"}"
```

#### Using Python
```python
import requests

response = requests.post(
    "http://localhost:8000/api/chat",
    headers={"X-API-Key": "ai_being_unified_demo_key_12345"},
    json={"message": "Explain quantum computing"}
)
print(response.json()["response"])
```

## 🔑 Important Information

### API Authentication
- **Header Name**: `X-API-Key`
- **API Key Value**: `ai_being_unified_demo_key_12345`
- **Required for**: All endpoints except `/health`

### Default Configuration
All settings in `.env` are pre-configured with working defaults:
- ✅ API Key: `ai_being_unified_demo_key_12345`
- ✅ Safety Level: `safe`
- ✅ Development Mode: `true`
- ✅ CORS: Enabled for all origins

### Optional: Add LLM Provider Keys
To use actual AI models, add your API keys to `.env`:
```env
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx
GROQ_API_KEY=gsk_xxxxx
GOOGLE_API_KEY=xxxxx
```

## 📡 Available Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/health` | GET | Health check | ❌ No |
| `/api/chat` | POST | Chat with AI | ✅ Yes |
| `/api/tasks` | POST | Create task | ✅ Yes |
| `/api/tasks/{id}` | GET | Get task status | ✅ Yes |
| `/api/search` | POST | Web search | ✅ Yes |
| `/api/research` | POST | Deep research | ✅ Yes |
| `/api/files` | POST | File operations | ✅ Yes |
| `/api/system/info` | GET | System info | ✅ Yes |
| `/api/system/stats` | GET | System stats | ✅ Yes |
| `/api/insights/performance` | GET | Performance metrics | ✅ Yes |

## 🎯 Example Requests

### Chat Request
```json
POST /api/chat
{
  "message": "What is machine learning?",
  "user_id": "user123",
  "session_id": "session456",
  "context": {}
}
```

### Search Request
```json
POST /api/search
{
  "query": "artificial intelligence trends",
  "max_results": 5
}
```

### Task Creation
```json
POST /api/tasks
{
  "name": "Research Task",
  "description": "Research quantum computing",
  "agents": ["researcher", "analyst"],
  "input_data": {"topic": "quantum computing"},
  "priority": "high"
}
```

## 🐛 Common Issues

### Issue: "Invalid API key"
✅ **Solution**: Use `ai_being_unified_demo_key_12345`

### Issue: Port 8000 in use
✅ **Solution**: `python main.py --mode server --port 8080`

### Issue: Module not found
✅ **Solution**: `pip install -r requirements.txt`

### Issue: Unicode errors (Windows)
✅ **Solution**: Already fixed in code, or run `chcp 65001`

## 📚 Additional Resources

- **Full Documentation**: See README.md
- **API Documentation**: http://localhost:8000/docs (when running)
- **GitHub Repository**: https://github.com/blackholeinfiverse32/AI-BEING-FINAL
- **Test Suite**: Run `python tests/test_ai_assistant_integration.py`

## 🎉 You're Ready!

The system is now fully operational. Start with the API server mode and explore the Swagger documentation at http://localhost:8000/docs

**Happy coding! 🚀**
