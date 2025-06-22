#!/bin/bash
# Run hallucination detection tests to prove TrustWrapper's value

echo "🚀 TrustWrapper Hallucination Detection Test Suite"
echo "=================================================="
echo ""

# Check if we're in the right directory
if [ ! -f "test_hallucination_detection.py" ]; then
    echo "❌ Error: Please run this script from the lamassu-labs directory"
    exit 1
fi

# Create a simple menu
echo "Choose a test to run:"
echo "1) Quick Proof of Value (recommended)"
echo "2) Full Demo with Examples"
echo "3) Unit Tests"
echo "4) Integration Tests"
echo "5) Performance Benchmark"
echo "6) Run All Tests"
echo ""
read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        echo ""
        echo "🧪 Running Quick Proof of Value Test..."
        echo ""
        python test_hallucination_detection.py
        ;;
    2)
        echo ""
        echo "🎭 Running Full Demo..."
        echo ""
        python demos/hallucination_testing_demo.py
        ;;
    3)
        echo ""
        echo "🔬 Running Unit Tests..."
        echo ""
        python -m pytest tests/unit/test_hallucination_detection.py -v
        ;;
    4)
        echo ""
        echo "🔗 Running Integration Tests..."
        echo ""
        python -m pytest tests/integration/test_hallucination_system.py -v
        ;;
    5)
        echo ""
        echo "⚡ Running Performance Benchmark..."
        echo ""
        python -c "
import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path('.')))
from test_hallucination_detection import test_performance_impact
asyncio.run(test_performance_impact())
"
        ;;
    6)
        echo ""
        echo "🏃 Running All Tests..."
        echo ""
        echo "Step 1: Quick Proof of Value"
        python test_hallucination_detection.py
        echo ""
        echo "Step 2: Unit Tests"
        python -m pytest tests/unit/test_hallucination_detection.py -v --tb=short
        echo ""
        echo "Step 3: Integration Tests"
        python -m pytest tests/integration/test_hallucination_system.py -v --tb=short
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again and choose 1-6."
        exit 1
        ;;
esac

echo ""
echo "✅ Test completed!"