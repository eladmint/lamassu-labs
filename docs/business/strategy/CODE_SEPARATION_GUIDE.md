# Code Separation Implementation Guide

## Quick Decision Guide

### 🔓 Keep Open Source (trustwrapper-core)

```
✅ Basic TrustWrapper interface
✅ Standard hallucination detection (basic patterns)
✅ Public API endpoints
✅ Leo/Aleo contract interfaces
✅ Basic verification flow
✅ Documentation and examples
✅ Test framework
✅ Basic CLI tools
```

### 🔒 Make Private (trustwrapper-enterprise)

```
❌ Advanced hallucination detection algorithms
❌ Multi-AI consensus engine
❌ Performance optimizations
❌ Caching strategies
❌ Enterprise dashboard
❌ Compliance modules
❌ Analytics and reporting
❌ Customer management code
❌ Industry-specific rules
❌ Advanced ZK optimizations
```

## File-by-File Analysis

### Core Source Files

| File | Current Location | Decision | New Location |
|------|-----------------|----------|--------------|
| `trust_wrapper.py` | `/src/core/` | Split | Basic → Open, Advanced → Private |
| `enhanced_hallucination_detector.py` | `/src/core/` | Private | `/enterprise/core/` |
| `hallucination_detector.py` | `/src/core/` | Split | Basic → Open, Advanced → Private |
| `zk_proof_generator.py` | `/src/core/` | Split | Interface → Open, Optimizations → Private |
| `trust_wrapper_xai.py` | `/src/core/` | Private | `/enterprise/core/` |
| `enhanced_trust_wrapper.py` | `/src/core/` | Private | `/enterprise/core/` |

### API Files

| File | Current Location | Decision | Reason |
|------|-----------------|----------|---------|
| `trustwrapper_api.py` | `/src/api/` | Split | Basic endpoints → Open, Enterprise → Private |
| `auth.py` | `/src/api/` | Private | Customer authentication |
| `monitoring.py` | `/src/api/` | Private | Business metrics |

### Smart Contracts

| File | Current Location | Decision | Reason |
|------|-----------------|----------|---------|
| `*.leo` contracts | `/src/contracts/` | Open | Industry standard benefit |
| Deployment scripts | `/tools/deployment/` | Open | Help adoption |

### Tests

| File | Current Location | Decision | Reason |
|------|-----------------|----------|---------|
| Basic tests | `/tests/` | Open | Encourage contributions |
| Performance tests | `/tests/` | Private | Reveal optimizations |
| Enterprise tests | `/tests/` | Private | Feature exposure |

## Refactoring Plan

### Step 1: Create Interface Abstractions

```python
# trustwrapper-core/src/interfaces/verifier.py (OPEN SOURCE)
from abc import ABC, abstractmethod

class AIVerifier(ABC):
    @abstractmethod
    def verify(self, response: str, context: dict) -> VerificationResult:
        """Basic verification interface"""
        pass

class VerificationResult:
    def __init__(self, trust_score: float, issues: list):
        self.trust_score = trust_score
        self.issues = issues
```

```python
# trustwrapper-enterprise/src/core/advanced_verifier.py (PRIVATE)
from trustwrapper_core.interfaces import AIVerifier

class EnterpriseAIVerifier(AIVerifier):
    def verify(self, response: str, context: dict) -> VerificationResult:
        # Advanced proprietary logic
        # Multi-AI consensus
        # Industry-specific rules
        # Performance optimizations
        pass
```

### Step 2: Extract Proprietary Algorithms

**Move to Private:**
```python
# Current location: src/core/enhanced_hallucination_detector.py
# Move to: enterprise/algorithms/advanced_detection.py

class ProprietaryHallucinationDetector:
    def _advanced_temporal_check(self):
        # This is our secret sauce
        pass
    
    def _multi_model_consensus(self):
        # Proprietary consensus algorithm
        pass
    
    def _industry_specific_rules(self):
        # Paid feature
        pass
```

**Keep Public:**
```python
# Keep in: core/basic_detector.py
class BasicHallucinationDetector:
    def detect_obvious_errors(self):
        # Simple, well-known techniques
        pass
    
    def check_basic_facts(self):
        # Standard fact checking
        pass
```

### Step 3: Separate Features

**Open Source Version:**
```python
# trustwrapper-core/src/wrapper.py
class TrustWrapper:
    def __init__(self, model):
        self.model = model
        self.detector = BasicHallucinationDetector()
    
    def verify(self, query: str) -> dict:
        response = self.model.execute(query)
        result = self.detector.detect(response)
        return {
            "response": response,
            "trust_score": result.trust_score,
            "verified": result.trust_score > 0.7
        }
```

**Enterprise Version:**
```python
# trustwrapper-enterprise/src/enterprise_wrapper.py
class EnterpriseTrustWrapper(TrustWrapper):
    def __init__(self, model, config):
        super().__init__(model)
        self.detector = EnhancedHallucinationDetector(config)
        self.analytics = AnalyticsEngine()
        self.compliance = ComplianceModule()
    
    def verify_with_compliance(self, query: str) -> dict:
        result = super().verify(query)
        
        # Add enterprise features
        result["compliance_report"] = self.compliance.generate_report(result)
        result["analytics"] = self.analytics.track(result)
        result["advanced_consensus"] = self._multi_ai_consensus(query)
        
        return result
```

## Repository Structure

### trustwrapper-core (Public)
```
trustwrapper-core/
├── LICENSE (Apache 2.0)
├── README.md
├── src/
│   ├── core/
│   │   ├── basic_wrapper.py
│   │   ├── basic_detector.py
│   │   └── interfaces.py
│   ├── api/
│   │   └── public_endpoints.py
│   └── contracts/
│       └── *.leo (all contracts)
├── examples/
├── docs/
└── tests/
    └── basic_tests/
```

### trustwrapper-enterprise (Private)
```
trustwrapper-enterprise/
├── LICENSE (Proprietary)
├── README.md
├── src/
│   ├── core/
│   │   ├── enterprise_wrapper.py
│   │   ├── advanced_detector.py
│   │   └── consensus_engine.py
│   ├── algorithms/
│   │   ├── proprietary_detection.py
│   │   └── optimization.py
│   ├── features/
│   │   ├── analytics/
│   │   ├── compliance/
│   │   └── dashboard/
│   └── integrations/
│       └── enterprise_connectors.py
├── tests/
│   └── enterprise_tests/
└── deployment/
    └── kubernetes/
```

## Migration Checklist

### Week 1: Preparation
- [ ] Create private repository
- [ ] Set up CI/CD for both repos
- [ ] Configure dependency management
- [ ] Plan feature split

### Week 2: Code Movement
- [ ] Move enterprise features to private repo
- [ ] Create public interfaces
- [ ] Update import paths
- [ ] Test both versions

### Week 3: Documentation
- [ ] Update public README
- [ ] Create enterprise docs
- [ ] API documentation split
- [ ] Migration guide

### Week 4: Release
- [ ] Version tagging
- [ ] License headers
- [ ] Security audit
- [ ] Announcement

## Licensing Strategy

### Open Source (trustwrapper-core)
```
Apache License 2.0
- Business-friendly
- Allows commercial use
- Requires attribution
- Patent protection
```

### Enterprise (trustwrapper-enterprise)
```
Lamassu Labs Commercial License
- Annual subscription
- Source code access for enterprise customers
- No redistribution rights
- Support included
```

## Communication Plan

### For Open Source Community
"We're committed to keeping TrustWrapper's core verification capabilities open source. The basic SDK, contracts, and APIs remain free. We're adding enterprise features in a separate package for organizations needing advanced capabilities."

### For Enterprise Customers
"Get advanced features including multi-AI consensus, compliance reporting, and premium support with TrustWrapper Enterprise. Full source code access included with enterprise subscriptions."

### For Investors
"Open core model protects IP while driving adoption. Community edition creates pipeline for enterprise sales. Clear upgrade path from free to paid."

---

## Next Steps

1. **Get Legal Review** on license choices
2. **Create Private Repo** with proper access controls
3. **Begin Code Separation** starting with most valuable IP
4. **Update CI/CD** for dual repo structure
5. **Prepare Communications** for community and customers

Remember: The goal is to build both a community AND a business. Open source drives adoption; proprietary features drive revenue.