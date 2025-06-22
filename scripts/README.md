# Lamassu Labs Scripts

Shell scripts for TrustWrapper development and deployment automation.

## Available Scripts

### Test Scripts
- `run_hallucination_tests.sh` - Execute comprehensive hallucination detection tests
- `test_local.sh` - Local environment testing

### Setup Scripts
- `setup_environment.sh` - Environment configuration and dependency setup

### Contract Scripts
Located in `scripts/` subdirectory from root:
- `compile_leo.sh` - Compile Leo/Aleo smart contracts
- `deploy_contracts.sh` - Deploy contracts to Aleo testnet
- `test_contracts.sh` - Test contract functionality
- `test_deployed_contracts.sh` - Validate deployed contracts

### Development Scripts
- `install_leo_aleo.sh` - Install Leo compiler and Aleo CLI
- `install_leo_manual.sh` - Manual Leo installation
- `organize_files.sh` - Project file organization
- `find_docs_to_update.sh` - Documentation maintenance

## Usage

Run scripts from the Lamassu Labs root directory:

```bash
# Setup environment
./scripts/setup_environment.sh

# Run tests
./scripts/run_hallucination_tests.sh

# Compile contracts
./scripts/compile_leo.sh

# Deploy to testnet
./scripts/deploy_contracts.sh
```

## Prerequisites

- Leo compiler installed
- Aleo CLI configured
- Environment variables set in `.env`
- Python virtual environment activated

## Security Note

Deployment scripts use testnet by default. Production deployments require additional configuration.