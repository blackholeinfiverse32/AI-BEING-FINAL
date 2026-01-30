# AI Being Unified - Quick Start Commands

## PowerShell Commands

### 1. Run Live Demo (Shows All Features)
```powershell
cd "c:\Users\Microsoft\Desktop\integration endpoints\ai_being_unified"
python demo_live_system.py
```

### 2. Run Integration Tests (Verify AI-ASSISTANT Integration)
```powershell
cd "c:\Users\Microsoft\Desktop\integration endpoints\ai_being_unified"
python tests\test_ai_assistant_integration.py
```

### 3. Run Interactive Chat Mode
```powershell
cd "c:\Users\Microsoft\Desktop\integration endpoints\ai_being_unified"
python main.py --mode interactive
```

### 4. Run API Server
```powershell
cd "c:\Users\Microsoft\Desktop\integration endpoints\ai_being_unified"
python main.py --mode server
```
Or:
```powershell
cd "c:\Users\Microsoft\Desktop\integration endpoints\ai_being_unified"
uvicorn api.server:app --reload --host 0.0.0.0 --port 8000
```

### 5. Run Demo Mode
```powershell
cd "c:\Users\Microsoft\Desktop\integration endpoints\ai_being_unified"
python main.py --mode demo
```

### 6. Run System Audit
```powershell
cd "c:\Users\Microsoft\Desktop\integration endpoints\ai_being_unified"
python audit.py
```

### 7. Run Interactive Menu
```powershell
cd "c:\Users\Microsoft\Desktop\integration endpoints\ai_being_unified"
.\run.ps1
```

## One-Line Commands (Copy & Paste)

**Live Demo:**
```powershell
cd "c:\Users\Microsoft\Desktop\integration endpoints\ai_being_unified"; python demo_live_system.py
```

**Integration Tests:**
```powershell
cd "c:\Users\Microsoft\Desktop\integration endpoints\ai_being_unified"; python tests\test_ai_assistant_integration.py
```

**Interactive Mode:**
```powershell
cd "c:\Users\Microsoft\Desktop\integration endpoints\ai_being_unified"; python main.py --mode interactive
```

**API Server:**
```powershell
cd "c:\Users\Microsoft\Desktop\integration endpoints\ai_being_unified"; python main.py --mode server
```

## System Status Check
```powershell
cd "c:\Users\Microsoft\Desktop\integration endpoints\ai_being_unified"
python -c "print('AI Being Unified - System Check'); from core.agents import *; from intelligence_layer.bhiv_integration import *; from intelligence_layer.karma_system import *; from intelligence_layer.insight_engine import *; from tools.calculator_tool import *; print('[OK] All systems operational')"
```

## What Each Command Does

- **demo_live_system.py** - Demonstrates all 6 integrated repositories working together
- **test_ai_assistant_integration.py** - Runs 8 tests to verify AI-ASSISTANT integration
- **main.py --mode interactive** - Start interactive chat with the AI assistant
- **main.py --mode server** - Start FastAPI server on http://localhost:8000
- **main.py --mode demo** - Run demonstration mode with mock responses
- **audit.py** - Run comprehensive system audit (8 component checks)
- **run.ps1** - Interactive menu to choose what to run
