# AI Being Unified - PowerShell Run Script
# Quick commands to run the integrated system

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "AI BEING UNIFIED - RUN COMMANDS" -ForegroundColor Cyan
Write-Host "All 6 Repositories Integrated" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to project directory
Set-Location "c:\Users\Microsoft\Desktop\integration endpoints\ai_being_unified"

Write-Host "Available Commands:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Run Live Demo (Recommended)" -ForegroundColor Green
Write-Host "   python demo_live_system.py" -ForegroundColor White
Write-Host ""
Write-Host "2. Run Integration Tests" -ForegroundColor Green
Write-Host "   python tests\test_ai_assistant_integration.py" -ForegroundColor White
Write-Host ""
Write-Host "3. Run Interactive Mode" -ForegroundColor Green
Write-Host "   python main.py --mode interactive" -ForegroundColor White
Write-Host ""
Write-Host "4. Run API Server" -ForegroundColor Green
Write-Host "   python main.py --mode server" -ForegroundColor White
Write-Host "   # OR" -ForegroundColor Gray
Write-Host "   uvicorn api.server:app --reload" -ForegroundColor White
Write-Host ""
Write-Host "5. Run Demo Mode" -ForegroundColor Green
Write-Host "   python main.py --mode demo" -ForegroundColor White
Write-Host ""
Write-Host "6. Run System Audit" -ForegroundColor Green
Write-Host "   python audit.py" -ForegroundColor White
Write-Host ""

# Ask user what to run
Write-Host "What would you like to run? (1-6): " -ForegroundColor Yellow -NoNewline
$choice = Read-Host

switch ($choice) {
    "1" {
        Write-Host "`nRunning Live Demo..." -ForegroundColor Cyan
        python demo_live_system.py
    }
    "2" {
        Write-Host "`nRunning Integration Tests..." -ForegroundColor Cyan
        python tests\test_ai_assistant_integration.py
    }
    "3" {
        Write-Host "`nStarting Interactive Mode..." -ForegroundColor Cyan
        python main.py --mode interactive
    }
    "4" {
        Write-Host "`nStarting API Server..." -ForegroundColor Cyan
        python main.py --mode server
    }
    "5" {
        Write-Host "`nRunning Demo Mode..." -ForegroundColor Cyan
        python main.py --mode demo
    }
    "6" {
        Write-Host "`nRunning System Audit..." -ForegroundColor Cyan
        python audit.py
    }
    default {
        Write-Host "`nInvalid choice. Running Live Demo by default..." -ForegroundColor Yellow
        python demo_live_system.py
    }
}
