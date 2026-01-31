# 🤖 AI Being Unified

A comprehensive, modular AI assistant framework that integrates multiple AI capabilities including multi-agent systems, intelligent reasoning, safety enforcement, and advanced task planning.

## 🌟 Features

- **Multi-Agent System**: Specialized agents (Planner, Researcher, Analyst, Executor, Evaluator)
- **Intelligent LLM Routing**: Automatic selection of optimal AI models
- **Advanced Memory Management**: Context-aware conversation history
- **Safety & Policy Enforcement**: Built-in content filtering and safety guards
- **Self-Reflection & Learning**: Continuous performance improvement
- **Task Planning & Orchestration**: Complex workflow management
- **Web Tools**: Search, browsing, and research capabilities
- **RESTful API**: FastAPI-based server with Swagger documentation

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning and version control)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/blackholeinfiverse32/AI-BEING-FINAL.git
cd AI-BEING-FINAL
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy the `.env.example` file to `.env`:

```bash
copy .env.example .env
```

Edit the `.env` file and configure your settings:

```env
# Required: API Key for authentication
API_KEY=ai_being_unified_demo_key_12345

# Optional: Add your LLM provider API keys
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

**Important**: The default API key is `ai_being_unified_demo_key_12345`. You'll need this to authenticate API requests.

### 4. Run the System

#### Option A: Interactive Mode (Recommended for Testing)

```bash
python main.py --mode interactive
```

This starts an interactive chat session where you can directly communicate with the AI.

#### Option B: API Server Mode (Recommended for Production)

```bash
python main.py --mode server
```

The server will start at `http://localhost:8000`

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

#### Option C: Demo Mode

```bash
python main.py --mode demo
```

Runs pre-configured demonstration scenarios.

#### Option D: Live Demo

```bash
python demo_live_system.py
```

Comprehensive live demonstration of all system capabilities.

## 🔑 API Authentication

All API endpoints (except `/health`) require authentication using the API key.

### Using Swagger UI (http://localhost:8000/docs)

1. Click the **"Authorize"** button (lock icon) at the top right
2. Enter the API key: `ai_being_unified_demo_key_12345`
3. Click **"Authorize"**
4. Click **"Close"**

### Using cURL

```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "accept: application/json" \
  -H "X-API-Key: ai_being_unified_demo_key_12345" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, how are you?",
    "user_id": "user123",
    "session_id": "session456"
  }'
```

### Using Python Requests

```python
import requests

url = "http://localhost:8000/api/chat"
headers = {
    "X-API-Key": "ai_being_unified_demo_key_12345",
    "Content-Type": "application/json"
}
data = {
    "message": "What is artificial intelligence?",
    "user_id": "user123",
    "session_id": "session456"
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

## 📡 API Endpoints

### Chat Endpoint
- **POST** `/api/chat` - Main chat interface
  ```json
  {
    "message": "Your question here",
    "user_id": "anonymous",
    "session_id": "default",
    "context": {}
  }
  ```

### Task Management
- **POST** `/api/tasks` - Create a new task
- **GET** `/api/tasks/{task_id}` - Get task status

### Search & Research
- **POST** `/api/search` - Web search
- **POST** `/api/research` - Deep research on a topic

### File Operations
- **POST** `/api/files` - File operations (read, write, delete, list)

### System Information
- **GET** `/api/system/info` - System information
- **GET** `/api/system/stats` - System statistics

### Performance Insights
- **GET** `/api/insights/performance` - Performance metrics and recommendations

### Health Check
- **GET** `/health` - Health check (no authentication required)

## 🏗️ Project Structure

```
ai_being_unified/
├── api/                    # FastAPI server
│   └── server.py
├── core/                   # Core system components
│   ├── agent_manager.py
│   ├── llm_router.py
│   ├── memory_manager.py
│   ├── task_planner.py
│   └── extended_integration.py
├── intelligence_layer/     # Advanced AI capabilities
│   ├── reasoning.py
│   ├── decision_engine.py
│   ├── self_reflection.py
│   └── karma_system.py
├── enforcement/            # Safety and policy
│   ├── policy_engine.py
│   └── safety_guard.py
├── tools/                  # Utility tools
│   ├── web_tools.py
│   └── system_tools.py
├── tests/                  # Test suite
├── memory/                 # Persistent memory storage
├── logs/                   # System logs
├── .env                    # Environment configuration
├── main.py                 # Main entry point
└── requirements.txt        # Python dependencies
```

## 🧪 Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python tests/test_ai_assistant_integration.py

# Run system audit
python audit.py
```

## 🛠️ Configuration Options

Edit `.env` file to customize:

| Variable | Description | Default |
|----------|-------------|---------|
| `API_KEY` | API authentication key | `a
` |
| `ANTHROPIC_API_KEY` | Claude API key | - |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `EMERGENCY_MODE` | Block all interactions | `false` |
| `DEFAULT_SAFETY_LEVEL` | Safety level (safe/caution/danger/critical) | `safe` |
| `MAX_INPUT_LENGTH` | Maximum input length | `2000` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `DEVELOPMENT_MODE` | Enable debugging | `true` |

## 🔒 Security Features

- **API Key Authentication**: Secure endpoint access
- **Safety Guard**: Content filtering and policy enforcement
- **Input Validation**: Automatic sanitization of user inputs
- **Rate Limiting**: Configurable request limits
- **Emergency Mode**: Quick system lockdown capability

## 📊 System Capabilities

### Processing Modes
- **Simple Mode**: Direct LLM responses for straightforward queries
- **Complex Mode**: Multi-agent orchestration for complex tasks

### Agent Types
- **Planner**: Task decomposition and planning
- **Researcher**: Information gathering and analysis
- **Analyst**: Data analysis and insights
- **Executor**: Task execution and implementation
- **Evaluator**: Quality assessment and validation

### Memory System
- **Short-term Memory**: Recent conversation context
- **Long-term Memory**: Persistent user profiles and preferences
- **Interaction Logs**: Complete audit trail

## 🐛 Troubleshooting

### Issue: "Invalid API key" error
**Solution**: Ensure you're using the correct API key: `ai_being_unified_demo_key_12345`

### Issue: Unicode encoding errors on Windows
**Solution**: The system automatically handles this. If issues persist, run:
```bash
chcp 65001
```

### Issue: Module not found errors
**Solution**: Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

### Issue: Port 8000 already in use
**Solution**: Change the port:
```bash
python main.py --mode server --port 8080
```

## 📝 Example Usage

### Interactive Chat
```bash
python main.py --mode interactive

👤 You: What is quantum computing?
🤖 Assistant: [Detailed response about quantum computing]

👤 You: status
📊 System Status: operational
```

### API Request Example
```python
import requests

# Chat request
response = requests.post(
    "http://localhost:8000/api/chat",
    headers={"X-API-Key": "ai_being_unified_demo_key_12345"},
    json={"message": "Explain machine learning"}
)

print(response.json()["response"])
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with FastAPI, Python, and modern AI technologies
- Integrates multiple AI providers (Anthropic, OpenAI, Google, Groq)
- Inspired by advanced AI assistant architectures

## 📞 Support

For issues, questions, or contributions:
- **GitHub Issues**: https://github.com/blackholeinfiverse32/AI-BEING-FINAL/issues
- **Documentation**: http://localhost:8000/docs (when server is running)

## 🚀 Quick Command Reference

```bash
# Start interactive mode
python main.py --mode interactive

# Start API server
python main.py --mode server

# Run demo
python main.py --mode demo

# Run live demo
python demo_live_system.py

# Run tests
python tests/test_ai_assistant_integration.py

# System audit
python audit.py
```

---

**Made with ❤️ by the AI Being Unified Team**
