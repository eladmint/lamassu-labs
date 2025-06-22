# Lamassu Labs Tools

Development tools for TrustWrapper development, testing, and deployment automation.

## Directory Structure

### `/analysis/` - Code and Documentation Analysis
- `find_docs_to_update.sh` - Documentation maintenance
- `identify_proprietary_code.py` - Code classification analysis
- `organize_files.sh` - Project file organization

### `/deployment/` - Deployment Tools
- `contracts/` - Contract deployment scripts
  - `01_deploy_agent_registry.sh` - Deploy agent registry contract
  - `01_deploy_hallucination_verifier.sh` - Deploy hallucination verifier
  - `01_deploy_trust_verifier.sh` - Deploy trust verifier
  - `02_deploy_hallucination_verifier_fallback.sh` - Fallback deployment
  - `03_test_hallucination_verifier.sh` - Contract testing
- `deploy_contracts.sh` - Deploy all contracts to Aleo testnet
- `test_contracts.sh` - Test contract functionality
- `test_deployed_contracts.sh` - Validate deployed contracts

### `/development/` - Development Setup
- `compile_leo.sh` - Compile Leo/Aleo smart contracts
- `install_leo_aleo.sh` - Install Leo compiler and Aleo CLI
- `install_leo_manual.sh` - Manual Leo installation
- `setup_environment.sh` - Environment configuration
- `setup_vscode.py` - VS Code configuration

### `/examples/` - Project Examples
- `quick_demo.py` - Basic TrustWrapper demonstration
- `ultimate_defi_presentation.py` - DeFi integration example

### `/monitoring/` - Production Monitoring
- Contract monitoring and dashboard tools
- Deployment success tracking
- Live monitoring interfaces

### `/testing/` - Testing Infrastructure
- Unit, integration, and performance tests
- Manual testing tools and validation scripts
- Test reports and results

## Usage

Run tools from the Lamassu Labs root directory:

```bash
# Setup environment
./tools/development/setup_environment.sh

# Compile contracts
./tools/development/compile_leo.sh

# Deploy to testnet
./tools/deployment/deploy_contracts.sh

# Run example
python tools/examples/quick_demo.py
```

## Prerequisites

- Leo compiler installed
- Aleo CLI configured
- Environment variables set in `.env`
- Python virtual environment activated

## Security Note

Deployment scripts use testnet by default. Production deployments require additional configuration.