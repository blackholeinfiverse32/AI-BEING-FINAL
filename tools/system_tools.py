"""
AI Being Unified - System Tools
File operations, system interactions, and automation tools
"""
import os
import json
import csv
import shutil
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from pathlib import Path
import subprocess
import tempfile
from datetime import datetime

@dataclass
class FileInfo:
    path: str
    name: str
    size: int
    modified: datetime
    is_directory: bool
    permissions: str

@dataclass
class SystemInfo:
    platform: str
    python_version: str
    working_directory: str
    available_space: int
    memory_usage: Dict[str, Any]

class FileOperationsTool:
    """Safe file operations with security constraints"""
    
    def __init__(self, allowed_directories: List[str] = None):
        # Define safe directories for file operations
        self.allowed_directories = allowed_directories or [
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Downloads"),
            tempfile.gettempdir(),
            "./workspace",  # Relative to current directory
            "./data",
            "./output"
        ]
        
        # Ensure workspace directories exist
        for directory in ["./workspace", "./data", "./output"]:
            os.makedirs(directory, exist_ok=True)
    
    def _is_path_allowed(self, path: str) -> bool:
        """Check if path is within allowed directories"""
        
        try:
            abs_path = os.path.abspath(path)
            
            for allowed_dir in self.allowed_directories:
                allowed_abs = os.path.abspath(allowed_dir)
                if abs_path.startswith(allowed_abs):
                    return True
            
            return False
        except Exception:
            return False
    
    def read_file(self, file_path: str, encoding: str = "utf-8") -> Dict[str, Any]:
        """Read file content safely"""
        
        result = {
            "success": False,
            "content": None,
            "error": None,
            "file_info": None
        }
        
        try:
            if not self._is_path_allowed(file_path):
                result["error"] = "File path not allowed for security reasons"
                return result
            
            if not os.path.exists(file_path):
                result["error"] = "File does not exist"
                return result
            
            if os.path.isdir(file_path):
                result["error"] = "Path is a directory, not a file"
                return result
            
            # Check file size (limit to 10MB for safety)
            file_size = os.path.getsize(file_path)
            if file_size > 10 * 1024 * 1024:
                result["error"] = "File too large (>10MB)"
                return result
            
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            
            result["success"] = True
            result["content"] = content
            result["file_info"] = self._get_file_info(file_path)
            
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def write_file(self, file_path: str, content: str, encoding: str = "utf-8", append: bool = False) -> Dict[str, Any]:
        """Write content to file safely"""
        
        result = {
            "success": False,
            "bytes_written": 0,
            "error": None
        }
        
        try:
            if not self._is_path_allowed(file_path):
                result["error"] = "File path not allowed for security reasons"
                return result
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            mode = 'a' if append else 'w'
            with open(file_path, mode, encoding=encoding) as f:
                f.write(content)
            
            result["success"] = True
            result["bytes_written"] = len(content.encode(encoding))
            
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def list_directory(self, directory_path: str) -> Dict[str, Any]:
        """List directory contents safely"""
        
        result = {
            "success": False,
            "files": [],
            "directories": [],
            "error": None
        }
        
        try:
            if not self._is_path_allowed(directory_path):
                result["error"] = "Directory path not allowed for security reasons"
                return result
            
            if not os.path.exists(directory_path):
                result["error"] = "Directory does not exist"
                return result
            
            if not os.path.isdir(directory_path):
                result["error"] = "Path is not a directory"
                return result
            
            for item in os.listdir(directory_path):
                item_path = os.path.join(directory_path, item)
                file_info = self._get_file_info(item_path)
                
                if file_info.is_directory:
                    result["directories"].append(file_info)
                else:
                    result["files"].append(file_info)
            
            result["success"] = True
            
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def _get_file_info(self, path: str) -> FileInfo:
        """Get file information"""
        
        stat = os.stat(path)
        
        return FileInfo(
            path=path,
            name=os.path.basename(path),
            size=stat.st_size,
            modified=datetime.fromtimestamp(stat.st_mtime),
            is_directory=os.path.isdir(path),
            permissions=oct(stat.st_mode)[-3:]
        )
    
    def create_directory(self, directory_path: str) -> Dict[str, Any]:
        """Create directory safely"""
        
        result = {
            "success": False,
            "error": None
        }
        
        try:
            if not self._is_path_allowed(directory_path):
                result["error"] = "Directory path not allowed for security reasons"
                return result
            
            os.makedirs(directory_path, exist_ok=True)
            result["success"] = True
            
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def delete_file(self, file_path: str) -> Dict[str, Any]:
        """Delete file safely"""
        
        result = {
            "success": False,
            "error": None
        }
        
        try:
            if not self._is_path_allowed(file_path):
                result["error"] = "File path not allowed for security reasons"
                return result
            
            if not os.path.exists(file_path):
                result["error"] = "File does not exist"
                return result
            
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)
            
            result["success"] = True
            
        except Exception as e:
            result["error"] = str(e)
        
        return result

class DataProcessingTool:
    """Tools for processing structured data"""
    
    def __init__(self):
        self.file_ops = FileOperationsTool()
    
    def read_json(self, file_path: str) -> Dict[str, Any]:
        """Read and parse JSON file"""
        
        result = self.file_ops.read_file(file_path)
        
        if result["success"]:
            try:
                result["data"] = json.loads(result["content"])
                del result["content"]  # Remove raw content
            except json.JSONDecodeError as e:
                result["success"] = False
                result["error"] = f"Invalid JSON: {str(e)}"
                result["data"] = None
        
        return result
    
    def write_json(self, file_path: str, data: Any, indent: int = 2) -> Dict[str, Any]:
        """Write data to JSON file"""
        
        try:
            json_content = json.dumps(data, indent=indent, default=str)
            return self.file_ops.write_file(file_path, json_content)
        except Exception as e:
            return {
                "success": False,
                "error": f"JSON serialization error: {str(e)}",
                "bytes_written": 0
            }
    
    def read_csv(self, file_path: str, delimiter: str = ",") -> Dict[str, Any]:
        """Read CSV file"""
        
        result = self.file_ops.read_file(file_path)
        
        if result["success"]:
            try:
                import io
                csv_reader = csv.DictReader(io.StringIO(result["content"]), delimiter=delimiter)
                result["data"] = list(csv_reader)
                result["columns"] = csv_reader.fieldnames
                del result["content"]  # Remove raw content
            except Exception as e:
                result["success"] = False
                result["error"] = f"CSV parsing error: {str(e)}"
                result["data"] = None
        
        return result
    
    def write_csv(self, file_path: str, data: List[Dict[str, Any]], delimiter: str = ",") -> Dict[str, Any]:
        """Write data to CSV file"""
        
        try:
            if not data:
                return {
                    "success": False,
                    "error": "No data to write",
                    "bytes_written": 0
                }
            
            import io
            output = io.StringIO()
            fieldnames = data[0].keys()
            writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter=delimiter)
            
            writer.writeheader()
            writer.writerows(data)
            
            csv_content = output.getvalue()
            return self.file_ops.write_file(file_path, csv_content)
            
        except Exception as e:
            return {
                "success": False,
                "error": f"CSV writing error: {str(e)}",
                "bytes_written": 0
            }

class SystemInfoTool:
    """System information and monitoring"""
    
    def get_system_info(self) -> SystemInfo:
        """Get basic system information"""
        
        import platform
        import sys
        import psutil
        
        try:
            # Get available disk space
            disk_usage = shutil.disk_usage(".")
            available_space = disk_usage.free
            
            # Get memory usage
            memory = psutil.virtual_memory()
            memory_usage = {
                "total": memory.total,
                "available": memory.available,
                "percent": memory.percent,
                "used": memory.used
            }
            
        except Exception:
            available_space = 0
            memory_usage = {"error": "Unable to get memory info"}
        
        return SystemInfo(
            platform=platform.system(),
            python_version=sys.version,
            working_directory=os.getcwd(),
            available_space=available_space,
            memory_usage=memory_usage
        )
    
    def run_command(self, command: List[str], timeout: int = 30) -> Dict[str, Any]:
        """Run system command safely (restricted)"""
        
        # Whitelist of allowed commands for security
        allowed_commands = [
            "echo", "date", "pwd", "ls", "dir", "whoami",
            "python", "pip", "git"
        ]
        
        result = {
            "success": False,
            "stdout": "",
            "stderr": "",
            "return_code": -1,
            "error": None
        }
        
        try:
            if not command or command[0] not in allowed_commands:
                result["error"] = f"Command not allowed: {command[0] if command else 'empty'}"
                return result
            
            # Run command with timeout
            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=os.getcwd()
            )
            
            result["success"] = process.returncode == 0
            result["stdout"] = process.stdout
            result["stderr"] = process.stderr
            result["return_code"] = process.returncode
            
        except subprocess.TimeoutExpired:
            result["error"] = f"Command timed out after {timeout} seconds"
        except Exception as e:
            result["error"] = str(e)
        
        return result

class AutomationTool:
    """Simple automation and task scheduling"""
    
    def __init__(self):
        self.file_ops = FileOperationsTool()
        self.data_tool = DataProcessingTool()
        self.scheduled_tasks = []
    
    def create_backup(self, source_path: str, backup_name: str = None) -> Dict[str, Any]:
        """Create backup of file or directory"""
        
        result = {
            "success": False,
            "backup_path": None,
            "error": None
        }
        
        try:
            if not self.file_ops._is_path_allowed(source_path):
                result["error"] = "Source path not allowed"
                return result
            
            if not os.path.exists(source_path):
                result["error"] = "Source path does not exist"
                return result
            
            # Generate backup name
            if not backup_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                base_name = os.path.basename(source_path)
                backup_name = f"{base_name}_backup_{timestamp}"
            
            backup_path = os.path.join("./workspace", backup_name)
            
            # Create backup
            if os.path.isdir(source_path):
                shutil.copytree(source_path, backup_path)
            else:
                shutil.copy2(source_path, backup_path)
            
            result["success"] = True
            result["backup_path"] = backup_path
            
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def batch_process_files(self, directory: str, operation: str, pattern: str = "*") -> Dict[str, Any]:
        """Batch process files in directory"""
        
        result = {
            "success": False,
            "processed_files": [],
            "failed_files": [],
            "error": None
        }
        
        try:
            if not self.file_ops._is_path_allowed(directory):
                result["error"] = "Directory path not allowed"
                return result
            
            if not os.path.exists(directory):
                result["error"] = "Directory does not exist"
                return result
            
            import glob
            files = glob.glob(os.path.join(directory, pattern))
            
            for file_path in files:
                try:
                    if operation == "list_info":
                        file_info = self.file_ops._get_file_info(file_path)
                        result["processed_files"].append({
                            "path": file_path,
                            "info": file_info
                        })
                    elif operation == "count_lines":
                        if not os.path.isdir(file_path):
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                line_count = sum(1 for _ in f)
                            result["processed_files"].append({
                                "path": file_path,
                                "line_count": line_count
                            })
                    # Add more operations as needed
                    
                except Exception as e:
                    result["failed_files"].append({
                        "path": file_path,
                        "error": str(e)
                    })
            
            result["success"] = True
            
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def generate_report(self, data: List[Dict[str, Any]], report_type: str = "summary") -> Dict[str, Any]:
        """Generate reports from data"""
        
        result = {
            "success": False,
            "report": None,
            "error": None
        }
        
        try:
            if not data:
                result["error"] = "No data provided"
                return result
            
            if report_type == "summary":
                report = {
                    "total_records": len(data),
                    "fields": list(data[0].keys()) if data else [],
                    "sample_record": data[0] if data else None,
                    "generated_at": datetime.now().isoformat()
                }
            elif report_type == "statistics":
                # Basic statistics for numeric fields
                numeric_fields = []
                for key, value in data[0].items():
                    if isinstance(value, (int, float)):
                        numeric_fields.append(key)
                
                stats = {}
                for field in numeric_fields:
                    values = [record.get(field, 0) for record in data if isinstance(record.get(field), (int, float))]
                    if values:
                        stats[field] = {
                            "min": min(values),
                            "max": max(values),
                            "avg": sum(values) / len(values),
                            "count": len(values)
                        }
                
                report = {
                    "total_records": len(data),
                    "numeric_fields": numeric_fields,
                    "statistics": stats,
                    "generated_at": datetime.now().isoformat()
                }
            else:
                result["error"] = f"Unknown report type: {report_type}"
                return result
            
            result["success"] = True
            result["report"] = report
            
        except Exception as e:
            result["error"] = str(e)
        
        return result