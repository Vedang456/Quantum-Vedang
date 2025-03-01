from typing import Dict, Any
from datetime import datetime

class QuantumMonitor:
    def __init__(self, config: Dict[str, Any]):
        """Initialize monitoring system with configuration"""
        self.config = config
        self.errors = []
        self.requests = []
        self.start_time = datetime.now()

    def log_error(self, error: Exception, additional_info: Dict[str, Any]) -> Dict[str, Any]:
        """Log error details"""
        error_data = {
            "timestamp": datetime.now().isoformat(),
            "error": str(error),
            "info": additional_info
        }
        self.errors.append(error_data)
        return error_data
    
    def log_request(self, request_type: str, duration: float, status: str) -> Dict[str, Any]:
        """Log request details"""
        request_data = {
            "timestamp": datetime.now().isoformat(),
            "type": request_type,
            "duration": duration,
            "status": status
        }
        self.requests.append(request_data)
        return request_data
    
    def get_metrics(self) -> Dict[str, Any]:
        """Compute and return system metrics"""
        total_requests = len(self.requests)
        successful_requests = len([r for r in self.requests if r["status"] == "success"])
        avg_duration = (sum(r["duration"] for r in self.requests) / total_requests) if total_requests > 0 else 0
        
        metrics = {
            "total_errors": len(self.errors),
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "error_rate": len(self.errors) / total_requests if total_requests > 0 else 0,
            "avg_request_duration": avg_duration,
            "uptime_seconds": (datetime.now() - self.start_time).total_seconds()
        }
        return metrics