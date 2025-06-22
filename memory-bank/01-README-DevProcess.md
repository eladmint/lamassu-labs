# Development Process for Lamassu Labs

**Last Updated**: June 21, 2025

## 🚀 Development Workflow

### 1. Explore Phase
- Understand the hackathon requirements
- Research zero-knowledge proofs and Aleo platform
- Review existing Agent Forge capabilities

### 2. Plan Phase
- Design ZK verification architecture
- Plan Leo smart contract structure
- Define marketplace integration points
- **CRITICAL**: Get approval before implementation

### 3. Code Phase
- Implement Leo contracts for agent verification
- Build proof generation SDK
- Create marketplace UI components
- Follow project structure standards

### 4. Commit Phase
- Write clear commit messages
- Update relevant documentation
- Submit to hackathon platform

## 📋 Code Quality Standards

### Before Committing
```bash
# Format code
black .

# Lint code
ruff check . --fix

# Run tests
pytest
```

### File Organization
- Source code: `src/{component}/`
- Tests: `tests/{unit|integration}/`
- Documentation: `docs/{architecture|guides|reports}/`
- Examples: `examples/`
- Tools: `tools/{deployment|testing}/`

## 🧪 Testing Requirements

1. Unit tests for all ZK verification logic
2. Integration tests for marketplace functionality
3. End-to-end tests for complete workflow
4. Performance benchmarks for proof generation

## 📚 Documentation Standards

### Required Documentation
- Architecture decisions in `docs/adrs/`
- Implementation guides in `docs/guides/`
- API documentation in source files
- Sprint updates in `memory-bank/`

### Naming Conventions
- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions: `snake_case`
- Constants: `UPPER_SNAKE_CASE`

## 🔒 Security Considerations

1. Never expose agent implementation details
2. Validate all inputs before proof generation
3. Use secure randomness for ZK proofs
4. Follow Aleo security best practices

## 🎯 Hackathon Timeline

### Day 1 (June 20)
- Morning: Setup and architecture
- Afternoon: Leo contract development
- Evening: Initial integration

### Day 2 (June 21)
- Morning: Marketplace UI
- Afternoon: Demo features
- Evening: Testing and refinement

### Day 3 (June 22)
- Morning: Final polish
- Afternoon: Documentation
- Evening: Submission

## 📝 Memory Bank Updates

Update these files regularly:
- `02-activeContext.md` - Current task focus
- `03-progress.md` - Completed milestones
- Sprint documents - Task status

## 🚨 Important Notes

1. This is a 48-hour hackathon - prioritize core features
2. Target Aleo's specific requirements for maximum points
3. Create compelling demo video
4. Ensure code runs on testnet