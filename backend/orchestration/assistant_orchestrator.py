"""Assistant Orchestrator - Coordinates all system components"""
from typing import Dict, Any, List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class AssistantOrchestrator:
    def __init__(self):
        self.components = {}
        self.workflow_history = []
    
    def initialize_components(self, components: Dict[str, Any]):
        self.components = components
    
    def orchestrate(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        workflow = []
        
        # Step 1: Safety check
        workflow.append({'step': 'safety_check', 'status': 'pending'})
        safety_result = self._run_safety_check(user_input, context)
        workflow[-1]['status'] = 'complete'
        workflow[-1]['result'] = safety_result
        
        if not safety_result.get('is_safe', True):
            return {
                'success': False,
                'reason': 'safety_violation',
                'workflow': workflow,
                'response': 'Request blocked by safety policy'
            }
        
        # Step 2: Intelligence analysis
        workflow.append({'step': 'intelligence_analysis', 'status': 'pending'})
        intelligence_result = self._run_intelligence_analysis(user_input, context)
        workflow[-1]['status'] = 'complete'
        workflow[-1]['result'] = intelligence_result
        
        # Step 3: Determine processing strategy
        workflow.append({'step': 'strategy_determination', 'status': 'pending'})
        strategy = self._determine_strategy(intelligence_result)
        workflow[-1]['status'] = 'complete'
        workflow[-1]['result'] = strategy
        
        # Step 4: Execute strategy
        workflow.append({'step': 'execution', 'status': 'pending'})
        execution_result = self._execute_strategy(strategy, user_input, context)
        workflow[-1]['status'] = 'complete'
        workflow[-1]['result'] = execution_result
        
        # Step 5: Enforcement check
        workflow.append({'step': 'enforcement_check', 'status': 'pending'})
        enforcement_result = self._run_enforcement_check(execution_result)
        workflow[-1]['status'] = 'complete'
        workflow[-1]['result'] = enforcement_result
        
        self.workflow_history.append(workflow)
        
        return {
            'success': True,
            'workflow': workflow,
            'response': execution_result.get('response', 'Processing complete'),
            'metadata': {
                'safety_score': safety_result.get('score', 1.0),
                'intelligence_confidence': intelligence_result.get('confidence', 0.8),
                'strategy': strategy.get('type', 'standard')
            }
        }
    
    def _run_safety_check(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        if 'safety' in self.components:
            return self.components['safety'].comprehensive_check(user_input, context)
        return {'is_safe': True, 'score': 1.0}
    
    def _run_intelligence_analysis(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        if 'intelligence' in self.components:
            return self.components['intelligence'].process(user_input, 'analytical', context)
        return {'confidence': 0.8, 'complexity': 'moderate'}
    
    def _determine_strategy(self, intelligence_result: Dict[str, Any]) -> Dict[str, Any]:
        complexity = intelligence_result.get('complexity', 'moderate')
        
        if complexity == 'simple':
            return {'type': 'direct', 'agents': []}
        elif complexity == 'moderate':
            return {'type': 'standard', 'agents': ['planner']}
        else:
            return {'type': 'complex', 'agents': ['planner', 'researcher', 'analyst']}
    
    def _execute_strategy(self, strategy: Dict[str, Any], user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        strategy_type = strategy.get('type', 'standard')
        
        if strategy_type == 'direct':
            return {'response': f"Direct response to: {user_input[:50]}..."}
        elif strategy_type == 'standard':
            return {'response': f"Standard processing of: {user_input[:50]}..."}
        else:
            return {'response': f"Complex multi-agent processing of: {user_input[:50]}..."}
    
    def _run_enforcement_check(self, execution_result: Dict[str, Any]) -> Dict[str, Any]:
        if 'enforcement' in self.components:
            return self.components['enforcement'].check_request('system', execution_result)
        return {'allowed': True, 'action': 'allow'}
    
    def get_orchestration_stats(self) -> Dict[str, Any]:
        return {
            'total_workflows': len(self.workflow_history),
            'recent_workflows': self.workflow_history[-5:],
            'components_active': len(self.components)
        }
