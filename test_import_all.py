"""
PHASE 1: File & Module Import Verification
Tests every Python file for importability
"""
import sys
import os
import importlib.util
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "errors": []
}

def test_import(file_path):
    """Test if a Python file can be imported"""
    results["total"] += 1
    
    try:
        # Convert file path to module name
        rel_path = file_path.relative_to(project_root)
        module_name = str(rel_path).replace(os.sep, '.').replace('.py', '')
        
        # Try to import
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)
            results["passed"] += 1
            return True, None
        else:
            results["failed"] += 1
            error = f"Could not create spec for {file_path}"
            results["errors"].append({"file": str(file_path), "error": error})
            return False, error
            
    except Exception as e:
        results["failed"] += 1
        error = str(e)
        results["errors"].append({"file": str(file_path), "error": error})
        return False, error

# Find all Python files
python_files = []
exclude_dirs = {'.git', '__pycache__', 'venv', 'env', '.venv', 'node_modules', 'frontend'}

for root, dirs, files in os.walk(project_root):
    # Remove excluded directories
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    
    for file in files:
        if file.endswith('.py') and not file.startswith('test_import'):
            python_files.append(Path(root) / file)

print(f"Found {len(python_files)} Python files to test\n")
print("=" * 80)

# Test each file
for py_file in sorted(python_files):
    success, error = test_import(py_file)
    status = "PASS" if success else "FAIL"
    print(f"[{status}] {py_file.relative_to(project_root)}")
    if error:
        print(f"        Error: {error[:100]}")

print("=" * 80)
print(f"\nRESULTS:")
print(f"Total Files: {results['total']}")
print(f"Passed: {results['passed']}")
print(f"Failed: {results['failed']}")
print(f"Success Rate: {(results['passed']/results['total']*100):.1f}%")

if results['failed'] > 0:
    print(f"\n[CRITICAL] {results['failed']} files failed to import")
    print("\nFailed Files:")
    for err in results['errors']:
        print(f"  - {err['file']}")
        print(f"    {err['error'][:200]}")
    sys.exit(1)
else:
    print("\n[SUCCESS] ALL FILES IMPORTABLE")
    sys.exit(0)
