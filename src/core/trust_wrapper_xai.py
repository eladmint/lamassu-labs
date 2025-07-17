"""
Enhanced TrustWrapper with Ziggurat XAI Integration
Proves performance AND explains decisions
"""

<<<<<<< HEAD
import hashlib
import json
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .trust_wrapper import ExecutionMetrics, VerifiedResult, ZKTrustWrapper
=======
import time
import hashlib
import json
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime

from .trust_wrapper import ZKTrustWrapper, VerifiedResult, ExecutionMetrics, ZKProof
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752


@dataclass
class ExplainabilityMetrics:
    """Metrics from Ziggurat explanation"""
<<<<<<< HEAD

=======
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    explanation_method: str  # SHAP, LIME, or Counterfactual
    confidence_score: float  # 0-1 confidence in explanation
    top_features: List[Dict[str, float]]  # Top contributing features
    decision_reasoning: str  # Human-readable explanation
    explanation_time_ms: int  # Time to generate explanation
<<<<<<< HEAD

    def to_dict(self) -> Dict[str, Any]:
        return {
            "method": self.explanation_method,
            "confidence": self.confidence_score,
            "top_features": self.top_features,
            "reasoning": self.decision_reasoning,
            "explanation_time": self.explanation_time_ms,
        }


@dataclass
class XAIVerifiedResult(VerifiedResult):
    """Extended result with explainability"""

    explanation: Optional[ExplainabilityMetrics] = None
    trust_score: Optional[float] = None  # Combined trust score

=======
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'method': self.explanation_method,
            'confidence': self.confidence_score,
            'top_features': self.top_features,
            'reasoning': self.decision_reasoning,
            'explanation_time': self.explanation_time_ms
        }


@dataclass 
class XAIVerifiedResult(VerifiedResult):
    """Extended result with explainability"""
    explanation: Optional[ExplainabilityMetrics] = None
    trust_score: Optional[float] = None  # Combined trust score
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def __str__(self) -> str:
        base = super().__str__()
        if self.explanation:
            xai_info = (
                f"\n🧠 Explainability:\n"
                f"Method: {self.explanation.explanation_method}\n"
                f"Confidence: {self.explanation.confidence_score:.2%}\n"
                f"Reasoning: {self.explanation.decision_reasoning}\n"
            )
<<<<<<< HEAD

=======
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            # Add top features
            if self.explanation.top_features:
                xai_info += "Top Factors:\n"
                for feature in self.explanation.top_features[:3]:
                    xai_info += f"  • {feature['name']}: {feature['importance']:.2f}\n"
<<<<<<< HEAD

            # Add trust score
            if self.trust_score:
                xai_info += f"\n🏆 Overall Trust Score: {self.trust_score:.2%}"

=======
            
            # Add trust score
            if self.trust_score:
                xai_info += f"\n🏆 Overall Trust Score: {self.trust_score:.2%}"
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            return base + xai_info
        return base


class MockZigguratExplainer:
    """Mock Ziggurat explainer for demo"""
<<<<<<< HEAD

    def explain(
        self, agent: Any, input_data: Any, output: Any
    ) -> ExplainabilityMetrics:
        """Generate explanation for agent decision"""
        start_time = time.time()

        # Simulate explanation generation
        time.sleep(0.1)  # Simulate computation

        # Generate mock explanation based on agent type
        agent_name = getattr(agent, "name", agent.__class__.__name__)

        if "event" in agent_name.lower():
            top_features = [
                {"name": "url_structure", "importance": 0.82},
                {"name": "page_content", "importance": 0.65},
                {"name": "calendar_markers", "importance": 0.54},
            ]
            reasoning = "High confidence due to structured URL and calendar markers"
        elif "scraper" in agent_name.lower():
            top_features = [
                {"name": "html_structure", "importance": 0.78},
                {"name": "javascript_required", "importance": 0.71},
                {"name": "anti_bot_score", "importance": 0.45},
            ]
            reasoning = (
                "Successfully bypassed anti-bot measures using advanced techniques"
            )
=======
    
    def explain(self, agent: Any, input_data: Any, output: Any) -> ExplainabilityMetrics:
        """Generate explanation for agent decision"""
        start_time = time.time()
        
        # Simulate explanation generation
        time.sleep(0.1)  # Simulate computation
        
        # Generate mock explanation based on agent type
        agent_name = getattr(agent, 'name', agent.__class__.__name__)
        
        if 'event' in agent_name.lower():
            top_features = [
                {"name": "url_structure", "importance": 0.82},
                {"name": "page_content", "importance": 0.65},
                {"name": "calendar_markers", "importance": 0.54}
            ]
            reasoning = "High confidence due to structured URL and calendar markers"
        elif 'scraper' in agent_name.lower():
            top_features = [
                {"name": "html_structure", "importance": 0.78},
                {"name": "javascript_required", "importance": 0.71},
                {"name": "anti_bot_score", "importance": 0.45}
            ]
            reasoning = "Successfully bypassed anti-bot measures using advanced techniques"
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        else:
            top_features = [
                {"name": "input_complexity", "importance": 0.70},
                {"name": "processing_pattern", "importance": 0.60},
<<<<<<< HEAD
                {"name": "output_consistency", "importance": 0.55},
            ]
            reasoning = "Standard processing pattern detected with consistent output"

        explanation_time = int((time.time() - start_time) * 1000)

=======
                {"name": "output_consistency", "importance": 0.55}
            ]
            reasoning = "Standard processing pattern detected with consistent output"
        
        explanation_time = int((time.time() - start_time) * 1000)
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        return ExplainabilityMetrics(
            explanation_method="SHAP",
            confidence_score=0.85 + (hash(str(input_data)) % 15) / 100,
            top_features=top_features,
            decision_reasoning=reasoning,
<<<<<<< HEAD
            explanation_time_ms=explanation_time,
=======
            explanation_time_ms=explanation_time
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        )


class ZKTrustWrapperXAI(ZKTrustWrapper):
    """Enhanced TrustWrapper with explainable AI"""
<<<<<<< HEAD

    def __init__(
        self, base_agent: Any, agent_name: Optional[str] = None, enable_xai: bool = True
    ):
=======
    
    def __init__(self, base_agent: Any, agent_name: Optional[str] = None, 
                 enable_xai: bool = True):
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        """Initialize with XAI capabilities"""
        super().__init__(base_agent, agent_name)
        self.enable_xai = enable_xai
        self.explainer = MockZigguratExplainer() if enable_xai else None
<<<<<<< HEAD

    def _calculate_trust_score(
        self, metrics: ExecutionMetrics, explanation: Optional[ExplainabilityMetrics]
    ) -> float:
        """Calculate overall trust score combining performance and explainability"""
        # Base score from performance
        perf_score = 0.5 if metrics.success else 0.0

=======
    
    def _calculate_trust_score(self, metrics: ExecutionMetrics, 
                             explanation: Optional[ExplainabilityMetrics]) -> float:
        """Calculate overall trust score combining performance and explainability"""
        # Base score from performance
        perf_score = 0.5 if metrics.success else 0.0
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Speed bonus (faster is better)
        if metrics.execution_time_ms < 100:
            perf_score += 0.2
        elif metrics.execution_time_ms < 1000:
            perf_score += 0.1
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Explainability bonus
        xai_score = 0.0
        if explanation:
            xai_score = explanation.confidence_score * 0.3
<<<<<<< HEAD

        return min(perf_score + xai_score, 1.0)

=======
        
        return min(perf_score + xai_score, 1.0)
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    def verified_execute(self, *args, **kwargs) -> XAIVerifiedResult:
        """Execute with performance metrics AND explanation"""
        # Get basic performance metrics
        basic_result = super().verified_execute(*args, **kwargs)
<<<<<<< HEAD

=======
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Generate explanation if XAI is enabled
        explanation = None
        if self.enable_xai and basic_result.metrics.success:
            try:
                explanation = self.explainer.explain(
<<<<<<< HEAD
                    self.base_agent, {"args": args, "kwargs": kwargs}, basic_result.data
=======
                    self.base_agent,
                    {'args': args, 'kwargs': kwargs},
                    basic_result.data
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
                )
            except Exception as e:
                # XAI failure doesn't invalidate performance proof
                print(f"XAI generation failed: {e}")
<<<<<<< HEAD

        # Calculate combined trust score
        trust_score = self._calculate_trust_score(basic_result.metrics, explanation)

=======
        
        # Calculate combined trust score
        trust_score = self._calculate_trust_score(basic_result.metrics, explanation)
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        # Create enhanced proof that includes XAI
        if explanation:
            # Add XAI hash to proof
            xai_data = json.dumps(explanation.to_dict(), sort_keys=True)
            xai_hash = hashlib.sha256(xai_data.encode()).hexdigest()
<<<<<<< HEAD

=======
            
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
            # In production: This would be included in the Leo proof
            enhanced_proof_data = {
                "performance_proof": basic_result.proof.proof_hash,
                "xai_hash": xai_hash,
<<<<<<< HEAD
                "trust_score": int(trust_score * 100),  # As percentage
            }

=======
                "trust_score": int(trust_score * 100)  # As percentage
            }
        
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        return XAIVerifiedResult(
            data=basic_result.data,
            metrics=basic_result.metrics,
            proof=basic_result.proof,
            verified=basic_result.verified,
            explanation=explanation,
<<<<<<< HEAD
            trust_score=trust_score,
=======
            trust_score=trust_score
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        )


# Convenience function
def create_xai_wrapper(agent: Any, name: Optional[str] = None) -> ZKTrustWrapperXAI:
    """Create an XAI-enabled trust wrapper"""
<<<<<<< HEAD
    return ZKTrustWrapperXAI(agent, name, enable_xai=True)
=======
    return ZKTrustWrapperXAI(agent, name, enable_xai=True)
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
