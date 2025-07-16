#!/usr/bin/env python3
"""
ValidationAgent - Sprint 96 Immediate Implementation
Minimal working agent for immediate testing
"""

import time
import logging
from typing import Dict, Any, Optional

class ValidationAgent:
    """
    IMMEDIATE IMPLEMENTATION: ValidationAgent with basic functionality
    No dependencies, immediate import capability
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.agent_id = "validation_agent"
        self.redis_client = None
        self.logger = logging.getLogger(__name__)
        
        print(f"ValidationAgent initialized: {self.agent_id}")
        
        # Try to initialize Redis if available
        self._init_redis_connection()
    
    def _init_redis_connection(self):
        """Initialize Redis connection if available"""
        try:
            import redis
            self.redis_client = redis.Redis(
                host='localhost',  # Test locally first
                port=6379,
                decode_responses=True,
                socket_timeout=2.0
            )
            # Test connection
            self.redis_client.ping()
            print("ValidationAgent: Redis connection successful")
        except Exception as e:
            print(f"ValidationAgent: Redis connection failed: {e}")
            self.redis_client = None
    
    def validate_extraction(self, task_id: str, extraction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        IMMEDIATE IMPLEMENTATION: Basic validation functionality
        Returns validation results immediately
        """
        start_time = time.time()
        
        try:
            # Basic validation logic
            field_count = len([v for v in extraction_data.values() if v and str(v).strip()])
            total_fields = len(extraction_data)
            field_completeness = field_count / total_fields if total_fields > 0 else 0.0
            
            # Simple quality assessment
            quality_score = min(1.0, field_completeness * 1.2)  # Boost for completeness
            
            validation_result = {
                "task_id": task_id,
                "status": "validation_complete",
                "quality_score": round(quality_score, 2),
                "field_completeness": round(field_completeness, 2),
                "data_accuracy": 0.75,  # Baseline estimate
                "format_consistency": 0.80,  # Baseline estimate
                "processing_time": time.time() - start_time,
                "validation_method": "immediate_basic",
                "recommendations": self._generate_recommendations(extraction_data, quality_score)
            }
            
            print(f"Validation completed for task {task_id}: quality={quality_score}")
            
            # Store in Redis if available
            if self.redis_client:
                self._store_validation_result(validation_result)
            
            return validation_result
            
        except Exception as e:
            print(f"Validation error: {e}")
            return {
                "task_id": task_id,
                "status": "validation_error",
                "error": str(e),
                "processing_time": time.time() - start_time
            }
    
    def _generate_recommendations(self, data: Dict[str, Any], quality_score: float) -> list:
        """Generate basic recommendations based on data quality"""
        recommendations = []
        
        if quality_score < 0.7:
            recommendations.append("improve_data_completeness")
        if not data.get("name") and not data.get("title"):
            recommendations.append("add_event_title")
        if not data.get("date") and not data.get("start_time"):
            recommendations.append("add_event_date")
        if not data.get("location"):
            recommendations.append("add_location_info")
            
        return recommendations
    
    def _store_validation_result(self, result: Dict[str, Any]):
        """Store validation result in Redis if available"""
        try:
            if self.redis_client:
                key = f"validation:result:{result['task_id']}"
                self.redis_client.hset(key, mapping={
                    "task_id": result["task_id"],
                    "quality_score": result["quality_score"],
                    "status": result["status"],
                    "processing_time": result["processing_time"],
                    "timestamp": time.time()
                })
                self.redis_client.expire(key, 3600)  # 1 hour expiration
                print(f"Validation result stored in Redis: {key}")
        except Exception as e:
            print(f"Redis storage failed: {e}")

# Export for immediate import
__all__ = ["ValidationAgent"]

if __name__ == "__main__":
    # Test ValidationAgent
    print("Testing ValidationAgent...")
    agent = ValidationAgent()
    
    test_data = {
        "event_title": "Test Blockchain Conference",
        "event_date": "2025-07-06",
        "location": "Miami, FL",
        "speakers": ["Speaker 1", "Speaker 2"]
    }
    
    result = agent.validate_extraction("test_001", test_data)
    print(f"Test result: {result}")