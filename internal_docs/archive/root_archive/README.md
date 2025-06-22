# Lamassu Labs Archive

Historical files and deprecated components for the TrustWrapper project.

## Directory Structure

- **build/** - Archived build artifacts and compilation outputs
- **contracts/** - Legacy contract files and deprecated versions
- **data/** - Archived data files and development artifacts

## Contents

### Build Artifacts (`build/`)
- Legacy compilation outputs
- Historical build directories
- Development artifacts

### Contracts (`contracts/`)
- `hallucination_verifier.leo` - Original contract version (replaced by modular version)
- `agent_registry.leo` - Legacy agent registry contract
- `trust_verifier.leo` - Original trust verification contract
- Various test contract directories

### Data (`data/`)
- `leo.zip` - Leo compiler archive
- Historical data files
- Development snapshots

## Usage

These files are archived for historical reference. 

**Active development should use:**
- `src/contracts/hallucination_verifier/` - Current working contract
- Current build processes in root directory
- Latest contract versions in `src/contracts/`

## Restoration

To restore archived components:

```bash
# Copy from archive to working directory if needed
cp archive/contracts/[file] src/contracts/

# Note: Archived contracts may require updates for current Leo syntax
```

## Maintenance

- Files moved here during project organization cleanup
- Maintained for historical reference and potential restoration
- Not included in active development or deployments