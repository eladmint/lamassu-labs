# Architecture Decision Records (ADRs)

This directory contains the Architecture Decision Records for the Lamassu Labs TrustWrapper project. ADRs document significant architectural decisions made during the project, including the context, decision, rationale, and consequences.

## What is an ADR?

An Architecture Decision Record captures an important architectural decision made along with its context and consequences. ADRs help:
- Document why decisions were made
- Provide context for future developers
- Track the evolution of the architecture
- Enable informed changes to past decisions

## ADR Index

| ADR | Title | Status | Date |
|-----|-------|--------|------|
| [ADR-001](ADR-001-aleo-blockchain-selection.md) | Selection of Aleo Blockchain for Zero-Knowledge AI Verification | Accepted | 2025-06-21 |
| [ADR-002](ADR-002-contract-security-architecture.md) | Smart Contract Security Architecture | Accepted | 2025-06-21 |
| [ADR-003](ADR-003-trustwrapper-integration-pattern.md) | TrustWrapper Integration Pattern | Accepted | 2025-06-21 |

## ADR Status

- **Draft**: Under discussion
- **Proposed**: Ready for review
- **Accepted**: Approved and implemented
- **Deprecated**: No longer relevant
- **Superseded**: Replaced by another ADR

## ADR Template

When creating a new ADR, use this template:

```markdown
# ADR-XXX: [Title]

**Date**: [YYYY-MM-DD]  
**Status**: [Draft|Proposed|Accepted|Deprecated|Superseded]  
**Author**: [Name]  
**Deciders**: [List of decision makers]

## Context
[What is the issue we're seeing that is motivating this decision?]

## Decision
[What is the change we're proposing/doing?]

## Rationale
[Why is this the right decision? What are the trade-offs?]

## Consequences
### Positive
[What good things will happen?]

### Negative
[What bad things will happen?]

### Neutral
[What things will change that are neither good nor bad?]

## References
[Links to related documents, discussions, or resources]

## Review Triggers
[When should this decision be reviewed?]
```

## Creating a New ADR

1. Copy the template above
2. Create a new file: `ADR-XXX-brief-description.md`
3. Fill in all sections
4. Submit for review
5. Update this index

## Reviewing ADRs

ADRs should be reviewed:
- When assumptions change
- When better solutions emerge
- At regular architecture reviews
- When problems arise from the decision

## Related Documentation

- [Technical Architecture](../../TECHNICAL_DEEP_DIVE.md)
- [API Reference](../../API_QUICK_REFERENCE.md)
- [Security Audit](../../ALEO_SECURITY_AUDIT.md)
- [Deployment Guide](../../ALEO_DEPLOYMENT_GUIDE.md)