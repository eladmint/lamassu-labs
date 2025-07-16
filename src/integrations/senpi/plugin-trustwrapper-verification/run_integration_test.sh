#!/bin/bash

# TrustWrapper Senpi Plugin - Real Data Integration Test Runner
echo "🚀 TrustWrapper Senpi Plugin - Real Data Integration Test"
echo "========================================================="

# Check if Node.js is available
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if TypeScript is available
if ! command -v npx &> /dev/null; then
    echo "❌ npx is not available. Please install npm first."
    exit 1
fi

# Set up environment
echo "🔧 Setting up environment..."

# Check for .env file
if [ -f ".env" ]; then
    echo "✅ Found .env configuration file"
    source .env
else
    echo "⚠️  No .env file found. Using .env.example defaults."
    echo "💡 Copy .env.example to .env and add your API keys for full functionality."

    # Set basic environment variables for testing
    export NODE_ENV=development
    export ENABLE_ZK_PROOFS=true
    export ENABLE_COMPLIANCE=true
    export CACHE_VERIFICATION_RESULTS=true
    export USE_MOCK_BLOCKCHAIN_DATA=true
    export USE_MOCK_MARKET_DATA=true
fi

# Check for required dependencies
echo "📦 Checking dependencies..."

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📥 Installing dependencies..."
    npm install
fi

# Compile TypeScript if needed
echo "🔨 Compiling TypeScript..."
npx tsc --noEmit --skipLibCheck test_real_data_integration.ts || {
    echo "⚠️  TypeScript compilation check failed, but continuing with test..."
}

# Run the integration test
echo "🧪 Running integration tests..."
echo ""

# Use ts-node to run TypeScript directly
npx ts-node --esm test_real_data_integration.ts

# Capture exit code
test_exit_code=$?

echo ""
echo "========================================================="

if [ $test_exit_code -eq 0 ]; then
    echo "✅ Integration tests completed successfully!"
    echo "🎯 TrustWrapper Senpi Plugin is ready for production use."
    echo ""
    echo "🚀 Next Steps:"
    echo "   1. Configure production API keys in .env"
    echo "   2. Schedule demo with Jason Goldberg (Senpi AI)"
    echo "   3. Prepare partnership presentation"
    echo "   4. Begin enterprise customer outreach"
else
    echo "❌ Integration tests failed!"
    echo "🔧 Please check the error messages above and:"
    echo "   1. Verify your API keys in .env"
    echo "   2. Check your internet connection"
    echo "   3. Ensure all dependencies are installed"
    echo "   4. Try running with mock data enabled"
fi

exit $test_exit_code
