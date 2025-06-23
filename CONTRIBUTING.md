# Contributing to Lamassu Labs

Thank you for your interest in contributing to Lamassu Labs!

## 🚀 Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/lamassu-labs.git`
3. Install dependencies: `pip install -e .[dev]`
4. Install Playwright browsers: `playwright install`

## 📋 Development Process

### 1. Create a Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes
- Follow the project structure in `CLAUDE.md`
- Write tests for new functionality
- Update documentation as needed

### 3. Code Quality
```bash
# Format code
black .

# Lint code
ruff check . --fix

# Run tests
pytest
```

### 4. Commit Changes
Follow conventional commits:
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `test:` Test additions/changes
- `refactor:` Code refactoring

### 5. Submit Pull Request
- Ensure all tests pass
- Update relevant documentation
- Provide clear PR description

## 🏗️ Project Structure

See `CLAUDE.md` for detailed project structure and standards.

## 🧪 Testing

- Unit tests: `tests/unit/`
- Integration tests: `tests/integration/`
- Run all tests: `pytest`

## 📚 Documentation

- Architecture docs: `docs/architecture/`
- Guides: `docs/guides/`
- ADRs: `docs/adrs/`
- **Public reports**: Only technical guides in `docs/` (if needed)
- **Internal reports**: Use `internal_docs/reports/` (not tracked in git)

## 🤝 Code of Conduct

Be respectful, inclusive, and constructive in all interactions.

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.