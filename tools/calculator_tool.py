"""
Calculator Tool - Mathematical operations
Integrated from AI-ASSISTANT repository
"""
import re
from typing import Dict, Any

class CalculatorTool:
    """Safe calculator for mathematical operations"""
    
    def __init__(self):
        self.allowed_chars = set('0123456789+-*/().% ')
    
    async def run(self, query: str) -> str:
        """Execute calculation safely"""
        try:
            # Clean and validate input
            query = query.strip()
            
            # Check for allowed characters only
            if not all(c in self.allowed_chars for c in query):
                return "Invalid calculation: contains forbidden characters"
            
            # Prevent dangerous operations
            if any(keyword in query.lower() for keyword in ['import', 'exec', 'eval', '__']):
                return "Invalid calculation: forbidden operation"
            
            # Safe evaluation using limited scope
            result = eval(query, {"__builtins__": {}}, {})
            return f"Result: {result}"
        except ZeroDivisionError:
            return "Error: Division by zero"
        except SyntaxError:
            return "Error: Invalid syntax"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def calculate(self, expression: str) -> Dict[str, Any]:
        """Synchronous calculation wrapper"""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        result = loop.run_until_complete(self.run(expression))
        return {"success": True, "result": result}

# Global calculator instance
calculator_tool = CalculatorTool()
