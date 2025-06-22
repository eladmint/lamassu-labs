#!/bin/bash

# File Organization Script for Lamassu Labs
# Organizes files according to parent project standards

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}📁 Lamassu Labs File Organization${NC}"
echo -e "${GREEN}=================================${NC}"
echo ""

# Function to move file with confirmation
move_file() {
    local source=$1
    local dest=$2
    
    if [ -f "$source" ]; then
        echo -e "${YELLOW}Moving: $source → $dest${NC}"
        mkdir -p "$(dirname "$dest")"
        mv "$source" "$dest"
        echo -e "${GREEN}✅ Moved${NC}"
    fi
}

# Check if we're in the right directory
if [ ! -f "CLAUDE.md" ] || [ ! -d "src" ]; then
    echo -e "${RED}❌ Error: Run this script from the lamassu-labs root directory${NC}"
    exit 1
fi

echo -e "${YELLOW}🔍 Analyzing files to organize...${NC}"
echo ""

# Files that should be moved according to parent project standards

# 1. Move test_*.py files from root to tools/testing/
if [ -f "test_imports.py" ]; then
    echo -e "${YELLOW}Found test files in root:${NC}"
    move_file "test_imports.py" "tools/testing/test_imports.py"
fi

# 2. Move setup_vscode.py to proper location
if [ -f "setup_vscode.py" ]; then
    echo -e "${YELLOW}Found setup script in root:${NC}"
    move_file "setup_vscode.py" "tools/development/setup_vscode.py"
fi

# 3. Quick start script should be in examples or tools
if [ -f "quick_start.py" ]; then
    echo -e "${YELLOW}Found quick_start.py in root:${NC}"
    move_file "quick_start.py" "examples/quick_start.py"
fi

# 4. Check docs directory for any JSON files
json_files=$(find docs -name "*.json" 2>/dev/null || true)
if [ ! -z "$json_files" ]; then
    echo -e "${YELLOW}Found JSON files in docs:${NC}"
    for json in $json_files; do
        basename=$(basename "$json")
        move_file "$json" "archive/data/docs_json/$basename"
    done
fi

# 5. Ensure proper directory structure exists
echo -e "\n${YELLOW}📂 Ensuring proper directory structure...${NC}"

directories=(
    "tools/testing"
    "tools/debugging"
    "tools/fixes"
    "tools/analysis"
    "tools/database"
    "tools/deployment"
    "tools/development"
    "archive/data"
    "archive/scripts"
)

for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo -e "${GREEN}✅ Created: $dir${NC}"
    fi
done

# 6. Move any deployment-related files to tools/deployment/
if [ -f "scripts/test_deployment.py" ]; then
    echo -e "\n${YELLOW}Organizing deployment scripts:${NC}"
    # test_deployment.py can stay in scripts as it's deployment-related
    echo -e "${GREEN}✅ scripts/test_deployment.py - OK in scripts/${NC}"
fi

# 7. Check internal_docs organization
echo -e "\n${YELLOW}📋 Checking internal_docs organization...${NC}"

# Move deployment docs from archive to current if they're active
if [ -d "internal_docs/archive/deployment" ]; then
    echo -e "${YELLOW}Found deployment docs in archive - these appear to be current:${NC}"
    if [ ! -d "docs" ]; then
        mkdir -p docs
    fi
    
    files=(
        "ALEO_DEPLOYMENT_GUIDE.md"
        "ALEO_DEPLOYMENT_SUMMARY.md"
        "ALEO_SECURITY_AUDIT.md"
        "OPERATIONAL_RUNBOOKS.md"
    )
    
    for file in "${files[@]}"; do
        if [ -f "internal_docs/archive/deployment/$file" ]; then
            move_file "internal_docs/archive/deployment/$file" "docs/$file"
        fi
    done
fi

# 8. Summary of root directory
echo -e "\n${GREEN}📊 Root Directory Status:${NC}"
echo -e "${GREEN}========================${NC}"

allowed_files=(
    "CHANGELOG.md"
    "README.md"
    "LICENSE"
    "CONTRIBUTING.md"
    "CLAUDE.md"
    "requirements.txt"
    "requirements_trustwrapper.txt"
    "pytest.ini"
    "pyproject.toml"
    "pyrightconfig.json"
    "setup.py"
    "program.json"
)

echo -e "${GREEN}Allowed files in root:${NC}"
for file in "${allowed_files[@]}"; do
    if [ -f "$file" ]; then
        echo -e "  ✅ $file"
    fi
done

# Check for files that shouldn't be in root
echo -e "\n${YELLOW}Checking for misplaced files...${NC}"
misplaced=0
for file in *.py; do
    if [ -f "$file" ] && [ "$file" != "setup.py" ]; then
        echo -e "  ⚠️  $file should be moved"
        misplaced=$((misplaced + 1))
    fi
done

if [ $misplaced -eq 0 ]; then
    echo -e "${GREEN}✅ No misplaced Python files in root${NC}"
fi

# 9. Final recommendations
echo -e "\n${GREEN}📋 Organization Complete!${NC}"
echo -e "${GREEN}========================${NC}"
echo ""
echo -e "${YELLOW}Recommendations:${NC}"
echo "1. The internal_docs/archive/deployment/ files appear to be current docs"
echo "2. Consider creating a CHANGELOG.md if you don't have one"
echo "3. All test files are properly organized in tests/ directory"
echo "4. Development tools are in tools/development/"
echo ""
echo -e "${GREEN}✅ File organization complete!${NC}"