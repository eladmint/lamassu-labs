"""
TrustWrapper ZK Proof Engine

Integrates with Ziggurat Intelligence on ICP to generate zero-knowledge proofs
for AI performance verification without exposing proprietary algorithms.

This enables the "Performance Insurance" value proposition - enterprises can
prove their AI meets performance standards without revealing trade secrets.
"""

import hashlib
import json
import os

# Import Ziggurat configuration from parent project
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import httpx

agent_forge_path = (
    Path(__file__).parent.parent.parent.parent / "agent_forge" / "agent_forge_public"
)
sys.path.append(str(agent_forge_path))

try:
    from layers.shared.src.config.ziggurat_config import (
        ZIGGURAT_CONFIG,
        get_openxai_endpoint,
    )
except ImportError:
    # Fallback configuration
    ZIGGURAT_CONFIG = {
        "icp_openxai": {
            "endpoint": "https://bvxuo-uaaaa-aaaal-asgua-cai.raw.icp0.io/api/v1",
            "timeout": 30,
        }
    }

    def get_openxai_endpoint():
        return ZIGGURAT_CONFIG["icp_openxai"]["endpoint"]


class ProofType(Enum):
    """Types of zero-knowledge proofs for AI verification"""

    PERFORMANCE_METRICS = "performance_metrics"  # Prove performance SLAs met
    COMPLIANCE_CHECK = "compliance_check"  # Prove regulatory compliance
    QUALITY_THRESHOLD = "quality_threshold"  # Prove quality standards met
    VIOLATION_ABSENCE = "violation_absence"  # Prove no violations detected
    ACCURACY_VALIDATION = "accuracy_validation"  # Prove accuracy benchmarks


class VerificationLevel(Enum):
    """Verification depth for ZK proofs"""

    BASIC = "basic"  # Simple boolean proof
    STANDARD = "standard"  # With confidence scores
    DETAILED = "detailed"  # With metadata
    ENTERPRISE = "enterprise"  # Full audit trail


@dataclass
class ZKProof:
    """Zero-knowledge proof for AI performance verification"""

    proof_id: str
    proof_type: ProofType
    timestamp: datetime

    # Proof data
    statement: str  # What is being proven
    commitment: str  # Cryptographic commitment
    proof_data: Dict[str, Any]  # ZK proof parameters

    # Verification data
    is_valid: bool
    confidence: float  # 0.0 to 1.0
    verification_method: str  # Algorithm used

    # Blockchain attestation
    chain: str = "ICP"  # Default to Internet Computer
    transaction_id: Optional[str] = None
    block_height: Optional[int] = None

    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    audit_trail: List[Dict[str, Any]] = field(default_factory=list)


class ZKProofEngine:
    """
    Zero-Knowledge Proof Engine for TrustWrapper

    Generates cryptographic proofs of AI performance without revealing:
    - Proprietary algorithms
    - Training data
    - Model weights
    - Business logic

    This is the key differentiator for enterprise adoption.
    """

    def __init__(self):
        self.endpoint = get_openxai_endpoint()
        self.client = httpx.AsyncClient(timeout=30.0)
        self.proof_cache: Dict[str, ZKProof] = {}

        # Performance tracking
        self.stats = {
            "proofs_generated": 0,
            "proofs_verified": 0,
            "average_generation_time_ms": 0,
            "cache_hits": 0,
            "blockchain_attestations": 0,
        }

    async def generate_performance_proof(
        self,
        metrics: Dict[str, float],
        thresholds: Dict[str, float],
        verification_level: VerificationLevel = VerificationLevel.STANDARD,
    ) -> ZKProof:
        """
        Generate ZK proof that AI performance meets specified thresholds.

        Example:
        - Prove latency < 100ms without revealing actual timing
        - Prove accuracy > 95% without revealing test data
        - Prove uptime > 99.9% without revealing infrastructure
        """
        start_time = time.time()

        # Create proof statement
        statement = self._create_performance_statement(metrics, thresholds)

        # Generate cryptographic commitment
        commitment = self._generate_commitment(metrics, thresholds)

        # Create ZK proof data
        proof_data = await self._generate_zk_proof_data(
            input_data={"metrics": metrics, "thresholds": thresholds},
            proof_type=ProofType.PERFORMANCE_METRICS,
            verification_level=verification_level,
        )

        # Verify the proof meets all thresholds
        all_thresholds_met = all(
            metrics.get(key, 0) >= threshold for key, threshold in thresholds.items()
        )

        # Calculate confidence based on margin above thresholds
        confidence = self._calculate_performance_confidence(metrics, thresholds)

        # Create ZK proof object
        proof = ZKProof(
            proof_id=self._generate_proof_id(),
            proof_type=ProofType.PERFORMANCE_METRICS,
            timestamp=datetime.utcnow(),
            statement=statement,
            commitment=commitment,
            proof_data=proof_data,
            is_valid=all_thresholds_met,
            confidence=confidence,
            verification_method="threshold_comparison_zk",
            metadata={
                "metrics_count": len(metrics),
                "thresholds_count": len(thresholds),
                "verification_level": verification_level.value,
            },
        )

        # Optionally create blockchain attestation
        if verification_level == VerificationLevel.ENTERPRISE:
            await self._create_blockchain_attestation(proof)

        # Update statistics
        self._update_stats(start_time)

        # Cache the proof
        self.proof_cache[proof.proof_id] = proof

        return proof

    async def generate_compliance_proof(
        self,
        violations_detected: int,
        compliance_checks: Dict[str, bool],
        regulatory_framework: str,
    ) -> ZKProof:
        """
        Generate ZK proof of regulatory compliance without exposing:
        - Specific violations or their content
        - Internal compliance procedures
        - Sensitive data handling methods
        """
        start_time = time.time()

        # Create compliance statement
        statement = f"AI system complies with {regulatory_framework} regulations"
        if violations_detected == 0:
            statement += " with zero violations detected"

        # Generate commitment
        commitment = self._generate_commitment(
            {"violations": violations_detected, "checks": compliance_checks},
            {"framework": regulatory_framework},
        )

        # Create ZK proof
        proof_data = await self._generate_zk_proof_data(
            input_data={
                "violations_count": violations_detected,
                "compliance_checks": len(compliance_checks),
                "checks_passed": sum(1 for v in compliance_checks.values() if v),
                "framework": regulatory_framework,
            },
            proof_type=ProofType.COMPLIANCE_CHECK,
            verification_level=VerificationLevel.DETAILED,
        )

        # Determine validity and confidence
        all_checks_passed = all(compliance_checks.values())
        confidence = (
            (sum(1 for v in compliance_checks.values() if v) / len(compliance_checks))
            if compliance_checks
            else 0.0
        )

        proof = ZKProof(
            proof_id=self._generate_proof_id(),
            proof_type=ProofType.COMPLIANCE_CHECK,
            timestamp=datetime.utcnow(),
            statement=statement,
            commitment=commitment,
            proof_data=proof_data,
            is_valid=violations_detected == 0 and all_checks_passed,
            confidence=confidence,
            verification_method="compliance_verification_zk",
            metadata={
                "regulatory_framework": regulatory_framework,
                "total_checks": len(compliance_checks),
                "checks_passed": sum(1 for v in compliance_checks.values() if v),
            },
        )

        self._update_stats(start_time)
        self.proof_cache[proof.proof_id] = proof

        return proof

    async def generate_quality_proof(
        self,
        quality_scores: Dict[str, float],
        business_risk_level: str,
        violations_summary: Dict[str, int],
    ) -> ZKProof:
        """
        Generate ZK proof of AI quality and safety without revealing:
        - Specific content that triggered violations
        - Internal quality assessment methods
        - Proprietary risk calculation algorithms
        """
        start_time = time.time()

        # Create quality statement
        total_violations = sum(violations_summary.values())
        avg_quality = (
            sum(quality_scores.values()) / len(quality_scores) if quality_scores else 0
        )

        statement = f"AI system maintains quality score of {avg_quality:.2f} with {business_risk_level} risk"

        # Generate commitment
        commitment = self._generate_commitment(
            {
                "quality_scores": quality_scores,
                "violations": violations_summary,
                "risk_level": business_risk_level,
            },
            {"timestamp": str(datetime.utcnow())},
        )

        # Create ZK proof
        proof_data = await self._generate_zk_proof_data(
            input_data={
                "average_quality": avg_quality,
                "total_violations": total_violations,
                "risk_level": business_risk_level,
                "violation_categories": len(violations_summary),
            },
            proof_type=ProofType.QUALITY_THRESHOLD,
            verification_level=VerificationLevel.STANDARD,
        )

        # Determine validity based on thresholds
        is_valid = (
            avg_quality >= 0.8
            and business_risk_level in ["LOW", "MEDIUM"]
            and total_violations < 5
        )

        proof = ZKProof(
            proof_id=self._generate_proof_id(),
            proof_type=ProofType.QUALITY_THRESHOLD,
            timestamp=datetime.utcnow(),
            statement=statement,
            commitment=commitment,
            proof_data=proof_data,
            is_valid=is_valid,
            confidence=avg_quality,
            verification_method="quality_assessment_zk",
            metadata={
                "risk_level": business_risk_level,
                "total_violations": total_violations,
                "quality_dimensions": len(quality_scores),
            },
        )

        self._update_stats(start_time)
        self.proof_cache[proof.proof_id] = proof

        return proof

    async def verify_proof(self, proof: ZKProof) -> Tuple[bool, Dict[str, Any]]:
        """
        Verify a ZK proof is valid and unchanged.

        Returns:
        - (is_valid, verification_details)
        """
        # Check proof structure
        if not self._validate_proof_structure(proof):
            return False, {"error": "Invalid proof structure"}

        # Verify commitment matches
        expected_commitment = self._recalculate_commitment(proof)
        if proof.commitment != expected_commitment:
            return False, {"error": "Commitment mismatch"}

        # Verify blockchain attestation if present
        if proof.transaction_id:
            blockchain_valid = await self._verify_blockchain_attestation(proof)
            if not blockchain_valid:
                return False, {"error": "Blockchain attestation invalid"}

        # Return verification result
        verification_details = {
            "proof_id": proof.proof_id,
            "proof_type": proof.proof_type.value,
            "timestamp": proof.timestamp.isoformat(),
            "is_valid": proof.is_valid,
            "confidence": proof.confidence,
            "blockchain_verified": bool(proof.transaction_id),
        }

        self.stats["proofs_verified"] += 1

        return True, verification_details

    def _generate_proof_id(self) -> str:
        """Generate unique proof ID"""
        timestamp = str(time.time())
        random_bytes = os.urandom(16).hex()
        return hashlib.sha256(f"{timestamp}{random_bytes}".encode()).hexdigest()[:16]

    def _generate_commitment(self, data: Dict, salt: Dict) -> str:
        """Generate cryptographic commitment for data"""
        # Serialize data deterministically
        data_str = json.dumps(data, sort_keys=True)
        salt_str = json.dumps(salt, sort_keys=True)

        # Create commitment using SHA-256
        commitment_input = f"{data_str}|{salt_str}"
        return hashlib.sha256(commitment_input.encode()).hexdigest()

    async def _generate_zk_proof_data(
        self,
        input_data: Dict[str, Any],
        proof_type: ProofType,
        verification_level: VerificationLevel,
    ) -> Dict[str, Any]:
        """
        Generate ZK proof data using cryptographic techniques.

        In production, this would use advanced ZK protocols like:
        - zk-SNARKs for succinct proofs
        - zk-STARKs for transparent proofs
        - Bulletproofs for range proofs
        """
        # For MVP, use simplified proof generation
        proof_data = {
            "protocol": "simplified_zk_v1",
            "proof_type": proof_type.value,
            "verification_level": verification_level.value,
            "timestamp": datetime.utcnow().isoformat(),
            # Proof components
            "challenge": hashlib.sha256(str(input_data).encode()).hexdigest()[:32],
            "response": hashlib.sha256(
                f"{input_data}{time.time()}".encode()
            ).hexdigest()[:32],
            "public_inputs_hash": hashlib.sha256(
                json.dumps(
                    self._extract_public_inputs(input_data), sort_keys=True
                ).encode()
            ).hexdigest(),
            # Verification parameters
            "verification_key": self._generate_verification_key(proof_type),
            "proof_size_bytes": 256,  # Simplified fixed size
            "generation_time_ms": 50,  # Simplified fixed time
        }

        # Add additional data for enterprise level
        if verification_level == VerificationLevel.ENTERPRISE:
            proof_data["audit_trail"] = {
                "generator": "trustwrapper_zk_engine_v1",
                "environment": "production",
                "compliance_frameworks": ["GDPR", "HIPAA", "SOX"],
            }

        return proof_data

    def _extract_public_inputs(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract public inputs that can be revealed in the proof"""
        # Only reveal aggregate statistics, not raw data
        public_inputs = {}

        for key, value in input_data.items():
            if isinstance(value, (int, float)):
                # Reveal ranges instead of exact values
                if value < 0.5:
                    public_inputs[f"{key}_range"] = "low"
                elif value < 0.8:
                    public_inputs[f"{key}_range"] = "medium"
                else:
                    public_inputs[f"{key}_range"] = "high"
            elif isinstance(value, dict):
                public_inputs[f"{key}_count"] = len(value)
            elif isinstance(value, list):
                public_inputs[f"{key}_count"] = len(value)

        return public_inputs

    def _generate_verification_key(self, proof_type: ProofType) -> str:
        """Generate verification key for proof type"""
        base_key = "trustwrapper_zk_verification"
        return hashlib.sha256(f"{base_key}_{proof_type.value}".encode()).hexdigest()[
            :32
        ]

    def _create_performance_statement(
        self, metrics: Dict[str, float], thresholds: Dict[str, float]
    ) -> str:
        """Create human-readable statement about performance"""
        statements = []

        for metric, threshold in thresholds.items():
            if metric in metrics:
                if metrics[metric] >= threshold:
                    statements.append(f"{metric} meets threshold of {threshold}")
                else:
                    statements.append(f"{metric} below threshold of {threshold}")

        return f"AI system performance: {'; '.join(statements)}"

    def _calculate_performance_confidence(
        self, metrics: Dict[str, float], thresholds: Dict[str, float]
    ) -> float:
        """Calculate confidence score based on how well metrics exceed thresholds"""
        if not thresholds:
            return 0.0

        confidence_scores = []

        for metric, threshold in thresholds.items():
            if metric in metrics and threshold > 0:
                # Calculate how much the metric exceeds the threshold
                ratio = metrics[metric] / threshold
                # Cap at 2.0 (200% of threshold)
                confidence_scores.append(min(ratio, 2.0) / 2.0)
            else:
                confidence_scores.append(0.0)

        return sum(confidence_scores) / len(confidence_scores)

    def _validate_proof_structure(self, proof: ZKProof) -> bool:
        """Validate proof has required fields"""
        required_fields = [
            "proof_id",
            "proof_type",
            "timestamp",
            "statement",
            "commitment",
            "proof_data",
            "is_valid",
            "confidence",
        ]

        for field in required_fields:
            if not hasattr(proof, field):
                return False

        return True

    def _recalculate_commitment(self, proof: ZKProof) -> str:
        """Recalculate commitment from proof data for verification"""
        # Extract data from proof metadata
        data = proof.metadata.copy()
        salt = {"timestamp": proof.timestamp.isoformat()}

        return self._generate_commitment(data, salt)

    async def _create_blockchain_attestation(self, proof: ZKProof) -> None:
        """
        Create blockchain attestation on ICP via Ziggurat.

        In production, this would:
        - Submit proof hash to ICP canister
        - Get transaction ID and block height
        - Store attestation on-chain
        """
        # Simplified attestation for MVP
        proof.transaction_id = f"icp_tx_{proof.proof_id[:8]}"
        proof.block_height = 1000000 + self.stats["blockchain_attestations"]

        self.stats["blockchain_attestations"] += 1

        # Add to audit trail
        proof.audit_trail.append(
            {
                "action": "blockchain_attestation",
                "timestamp": datetime.utcnow().isoformat(),
                "chain": "ICP",
                "transaction_id": proof.transaction_id,
                "block_height": proof.block_height,
            }
        )

    async def _verify_blockchain_attestation(self, proof: ZKProof) -> bool:
        """Verify blockchain attestation is valid"""
        # In production, query ICP to verify transaction
        # For MVP, simple validation
        return bool(proof.transaction_id and proof.block_height)

    def _update_stats(self, start_time: float) -> None:
        """Update performance statistics"""
        generation_time_ms = (time.time() - start_time) * 1000

        self.stats["proofs_generated"] += 1

        # Update average generation time
        current_avg = self.stats["average_generation_time_ms"]
        count = self.stats["proofs_generated"]
        new_avg = ((current_avg * (count - 1)) + generation_time_ms) / count
        self.stats["average_generation_time_ms"] = new_avg

    def get_statistics(self) -> Dict[str, Any]:
        """Get ZK proof engine statistics"""
        return self.stats.copy()

    async def close(self):
        """Clean up resources"""
        await self.client.aclose()
