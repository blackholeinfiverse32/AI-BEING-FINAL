"""
AI Being Unified - Self Reflection
Continuous learning and improvement system
"""
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from collections import defaultdict

@dataclass
class InteractionLog:
    timestamp: datetime
    user_input: str
    processing_mode: str
    response_quality: float
    user_satisfaction: float
    execution_time: float
    errors: List[str]
    success: bool

@dataclass
class PerformanceMetrics:
    total_interactions: int
    successful_interactions: int
    average_response_time: float
    average_satisfaction: float
    common_errors: Dict[str, int]
    improvement_areas: List[str]

class SelfReflection:
    """System for monitoring performance and identifying improvements"""
    
    def __init__(self, storage_path: str = "memory"):
        self.storage_path = storage_path
        self.interaction_logs = []
        self.performance_history = []
        self.learning_insights = []
        
        self._ensure_storage_exists()
        self._load_historical_data()
    
    def _ensure_storage_exists(self):
        """Create storage directory if it doesn't exist"""
        os.makedirs(self.storage_path, exist_ok=True)
    
    def _load_historical_data(self):
        """Load historical performance data"""
        logs_path = os.path.join(self.storage_path, "interaction_logs.json")
        if os.path.exists(logs_path):
            with open(logs_path, 'r') as f:
                data = json.load(f)
                self.interaction_logs = [
                    InteractionLog(**{**log, 'timestamp': datetime.fromisoformat(log['timestamp'])})
                    for log in data
                ]
    
    def _save_data(self):
        """Save performance data to storage"""
        logs_path = os.path.join(self.storage_path, "interaction_logs.json")
        with open(logs_path, 'w') as f:
            data = [
                {**asdict(log), 'timestamp': log.timestamp.isoformat()}
                for log in self.interaction_logs
            ]
            json.dump(data, f, indent=2)
    
    def log_interaction(self, 
                       user_input: str,
                       processing_mode: str,
                       response_quality: float,
                       user_satisfaction: float,
                       execution_time: float,
                       errors: List[str] = None,
                       success: bool = True):
        """Log an interaction for analysis"""
        
        log_entry = InteractionLog(
            timestamp=datetime.now(),
            user_input=user_input,
            processing_mode=processing_mode,
            response_quality=response_quality,
            user_satisfaction=user_satisfaction,
            execution_time=execution_time,
            errors=errors or [],
            success=success
        )
        
        self.interaction_logs.append(log_entry)
        
        # Keep only recent logs (last 1000 interactions)
        if len(self.interaction_logs) > 1000:
            self.interaction_logs = self.interaction_logs[-1000:]
        
        self._save_data()
    
    def analyze_recent_performance(self, days: int = 7) -> PerformanceMetrics:
        """Analyze performance over recent period"""
        
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_logs = [log for log in self.interaction_logs if log.timestamp > cutoff_date]
        
        if not recent_logs:
            return PerformanceMetrics(
                total_interactions=0,
                successful_interactions=0,
                average_response_time=0.0,
                average_satisfaction=0.0,
                common_errors={},
                improvement_areas=["Insufficient data for analysis"]
            )
        
        # Calculate metrics
        total_interactions = len(recent_logs)
        successful_interactions = sum(1 for log in recent_logs if log.success)
        average_response_time = sum(log.execution_time for log in recent_logs) / total_interactions
        average_satisfaction = sum(log.user_satisfaction for log in recent_logs) / total_interactions
        
        # Analyze errors
        error_counts = defaultdict(int)
        for log in recent_logs:
            for error in log.errors:
                error_counts[error] += 1
        
        # Identify improvement areas
        improvement_areas = []
        
        if successful_interactions / total_interactions < 0.9:
            improvement_areas.append("Increase success rate")
        
        if average_response_time > 5.0:
            improvement_areas.append("Reduce response time")
        
        if average_satisfaction < 0.7:
            improvement_areas.append("Improve response quality")
        
        if error_counts:
            most_common_error = max(error_counts.items(), key=lambda x: x[1])
            if most_common_error[1] > total_interactions * 0.1:
                improvement_areas.append(f"Address frequent error: {most_common_error[0]}")
        
        return PerformanceMetrics(
            total_interactions=total_interactions,
            successful_interactions=successful_interactions,
            average_response_time=average_response_time,
            average_satisfaction=average_satisfaction,
            common_errors=dict(error_counts),
            improvement_areas=improvement_areas
        )
    
    def identify_patterns(self) -> Dict[str, Any]:
        """Identify patterns in user interactions and system performance"""
        
        if len(self.interaction_logs) < 10:
            return {"status": "insufficient_data"}
        
        patterns = {}
        
        # Time-based patterns
        hour_performance = defaultdict(list)
        for log in self.interaction_logs:
            hour = log.timestamp.hour
            hour_performance[hour].append(log.user_satisfaction)
        
        # Find best and worst performing hours
        hour_averages = {
            hour: sum(satisfactions) / len(satisfactions)
            for hour, satisfactions in hour_performance.items()
            if len(satisfactions) > 2
        }
        
        if hour_averages:
            best_hour = max(hour_averages.items(), key=lambda x: x[1])
            worst_hour = min(hour_averages.items(), key=lambda x: x[1])
            patterns["time_patterns"] = {
                "best_performance_hour": best_hour[0],
                "worst_performance_hour": worst_hour[0]
            }
        
        # Processing mode effectiveness
        mode_performance = defaultdict(list)
        for log in self.interaction_logs:
            mode_performance[log.processing_mode].append(log.user_satisfaction)
        
        mode_averages = {
            mode: sum(satisfactions) / len(satisfactions)
            for mode, satisfactions in mode_performance.items()
            if len(satisfactions) > 2
        }
        
        if mode_averages:
            patterns["processing_mode_effectiveness"] = mode_averages
        
        # Response time vs satisfaction correlation
        recent_logs = self.interaction_logs[-100:]  # Last 100 interactions
        if len(recent_logs) > 10:
            fast_responses = [log for log in recent_logs if log.execution_time < 2.0]
            slow_responses = [log for log in recent_logs if log.execution_time > 5.0]
            
            if fast_responses and slow_responses:
                fast_avg_satisfaction = sum(log.user_satisfaction for log in fast_responses) / len(fast_responses)
                slow_avg_satisfaction = sum(log.user_satisfaction for log in slow_responses) / len(slow_responses)
                
                patterns["speed_vs_satisfaction"] = {
                    "fast_response_satisfaction": fast_avg_satisfaction,
                    "slow_response_satisfaction": slow_avg_satisfaction,
                    "correlation": "positive" if fast_avg_satisfaction > slow_avg_satisfaction else "negative"
                }
        
        return patterns
    
    def generate_improvement_recommendations(self) -> List[str]:
        """Generate specific recommendations for system improvement"""
        
        recommendations = []
        
        # Analyze recent performance
        recent_metrics = self.analyze_recent_performance()
        patterns = self.identify_patterns()
        
        # Performance-based recommendations
        if recent_metrics.average_satisfaction < 0.6:
            recommendations.append("Critical: User satisfaction is low. Review response quality and relevance.")
        
        if recent_metrics.average_response_time > 10.0:
            recommendations.append("High: Response times are too slow. Optimize processing pipeline.")
        
        if recent_metrics.successful_interactions / max(recent_metrics.total_interactions, 1) < 0.8:
            recommendations.append("High: Success rate is below acceptable threshold. Review error handling.")
        
        # Pattern-based recommendations
        if "processing_mode_effectiveness" in patterns:
            mode_effectiveness = patterns["processing_mode_effectiveness"]
            best_mode = max(mode_effectiveness.items(), key=lambda x: x[1])
            worst_mode = min(mode_effectiveness.items(), key=lambda x: x[1])
            
            if best_mode[1] - worst_mode[1] > 0.2:
                recommendations.append(f"Medium: Consider using {best_mode[0]} mode more often. It shows {best_mode[1]:.2f} vs {worst_mode[1]:.2f} satisfaction.")
        
        # Error-based recommendations
        if recent_metrics.common_errors:
            most_common_error = max(recent_metrics.common_errors.items(), key=lambda x: x[1])
            if most_common_error[1] > 5:
                recommendations.append(f"Medium: Address recurring error: {most_common_error[0]} (occurred {most_common_error[1]} times)")
        
        # Time-based recommendations
        if "time_patterns" in patterns:
            time_patterns = patterns["time_patterns"]
            recommendations.append(f"Low: Performance varies by time. Best at {time_patterns['best_performance_hour']}:00, worst at {time_patterns['worst_performance_hour']}:00")
        
        return recommendations if recommendations else ["System performance is within acceptable parameters"]
    
    def get_learning_insights(self) -> List[str]:
        """Get insights about system learning and adaptation"""
        
        insights = []
        
        if len(self.interaction_logs) < 50:
            return ["Need more interaction data for meaningful insights"]
        
        # Trend analysis
        recent_logs = self.interaction_logs[-50:]
        older_logs = self.interaction_logs[-100:-50] if len(self.interaction_logs) >= 100 else []
        
        if older_logs:
            recent_avg_satisfaction = sum(log.user_satisfaction for log in recent_logs) / len(recent_logs)
            older_avg_satisfaction = sum(log.user_satisfaction for log in older_logs) / len(older_logs)
            
            if recent_avg_satisfaction > older_avg_satisfaction + 0.1:
                insights.append("Positive trend: User satisfaction is improving over time")
            elif recent_avg_satisfaction < older_avg_satisfaction - 0.1:
                insights.append("Negative trend: User satisfaction is declining")
            else:
                insights.append("Stable performance: User satisfaction remains consistent")
        
        # Adaptation insights
        error_reduction = self._analyze_error_reduction()
        if error_reduction:
            insights.extend(error_reduction)
        
        # Complexity handling
        complex_tasks = [log for log in recent_logs if log.processing_mode == "complex"]
        simple_tasks = [log for log in recent_logs if log.processing_mode == "simple"]
        
        if complex_tasks and simple_tasks:
            complex_satisfaction = sum(log.user_satisfaction for log in complex_tasks) / len(complex_tasks)
            simple_satisfaction = sum(log.user_satisfaction for log in simple_tasks) / len(simple_tasks)
            
            if complex_satisfaction > simple_satisfaction:
                insights.append("System handles complex tasks better than simple ones")
            else:
                insights.append("System performs better on simple tasks")
        
        return insights
    
    def _analyze_error_reduction(self) -> List[str]:
        """Analyze if error rates are improving over time"""
        
        insights = []
        
        if len(self.interaction_logs) < 100:
            return insights
        
        recent_logs = self.interaction_logs[-50:]
        older_logs = self.interaction_logs[-100:-50]
        
        recent_error_rate = sum(1 for log in recent_logs if log.errors) / len(recent_logs)
        older_error_rate = sum(1 for log in older_logs if log.errors) / len(older_logs)
        
        if recent_error_rate < older_error_rate - 0.05:
            insights.append("System is learning: Error rate has decreased over time")
        elif recent_error_rate > older_error_rate + 0.05:
            insights.append("Warning: Error rate has increased recently")
        
        return insights