"""Orchestration Module"""
# AssistantOrchestrator is a function-based module, not a class
# Import the process_message function as the main entry point
from backend.orchestration.assistant_orchestrator import process_message, generate_chat_response

__all__ = ['process_message', 'generate_chat_response']

# For backward compatibility, create a wrapper class
class AssistantOrchestrator:
    """Wrapper class for the assistant orchestrator pipeline"""
    
    @staticmethod
    def process(message: str, session_id=None, metadata=None):
        """Process a message through the assistant pipeline"""
        return process_message(message, session_id, metadata)
    
    @staticmethod
    def generate_response(message: str):
        """Generate a simple chat response"""
        return generate_chat_response(message)
