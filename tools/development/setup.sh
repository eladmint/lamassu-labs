#!/bin/bash
# TrustWrapper Development Environment Setup
# Automated setup script for developers

set -e

echo "🚀 Setting up TrustWrapper development environment..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
echo "🔧 Installing pre-commit hooks..."
pre-commit install

# Install package in development mode
echo "📦 Installing TrustWrapper in development mode..."
pip install -e .

# Run initial quality checks
echo "🧪 Running initial quality checks..."
echo "  - Black formatting check..."
black --check . || echo "⚠️  Some files need formatting. Run 'black .' to fix."

echo "  - Import sorting check..."
isort --check-only . || echo "⚠️  Some imports need sorting. Run 'isort .' to fix."

echo "  - Ruff linting..."
ruff check . || echo "⚠️  Linting issues found. Run 'ruff check . --fix' to fix."

echo "  - Type checking..."
mypy src/ || echo "⚠️  Type checking issues found."

# Test the installation
echo "🧪 Testing installation..."
python -c "import sys; print('Python executable:', sys.executable)"
python -c "try: import trustwrapper; print('✅ TrustWrapper module imported successfully') except ImportError as e: print('⚠️  TrustWrapper import failed:', e)"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env template..."
    cat > .env << EOF
# TrustWrapper Environment Variables
TRUSTWRAPPER_ENV=development
PYTHONPATH=/workspace

# API Keys (replace with your actual keys)
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_google_key_here

# Database (for development)
DATABASE_URL=postgresql://trustwrapper:development@localhost:5432/trustwrapper_dev

# Redis (for caching)
REDIS_URL=redis://localhost:6379/0
EOF
    echo "⚠️  Please update .env with your actual API keys"
fi

echo ""
echo "✅ Development environment setup complete!"
echo ""
echo "🎯 Next steps:"
echo "  1. Activate the virtual environment: source .venv/bin/activate"
echo "  2. Update .env with your API keys"
echo "  3. Run tests: pytest"
echo "  4. Start coding! 🚀"
echo ""
echo "💡 Available commands:"
echo "  - pytest                    # Run tests"
echo "  - black .                   # Format code"
echo "  - ruff check . --fix        # Lint and fix issues"
echo "  - pre-commit run --all-files # Run all quality checks"
echo "  - mypy src/                 # Type check"
echo ""