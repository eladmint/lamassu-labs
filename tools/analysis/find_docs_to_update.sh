#!/bin/bash

# Script to find documentation files that need updates after Aleo deployment
# Note: This script should be run from the project root or will cd to project root

# Change to project root directory
cd "$(dirname "$0")/../.." || exit 1

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}📋 Documentation Files Needing Updates${NC}"
echo -e "${GREEN}======================================${NC}"

# High Priority - Sprint docs
echo -e "\n${RED}HIGH PRIORITY - Sprint Documentation:${NC}"
find internal_docs/memory-bank/current-focus-sprints -name "sprint10*.md" -type f 2>/dev/null | head -5

# Main project files
echo -e "\n${RED}HIGH PRIORITY - Main Project Files:${NC}"
ls -la README.md CHANGELOG.md 2>/dev/null

# Hackathon docs
echo -e "\n${YELLOW}MEDIUM PRIORITY - Hackathon Materials:${NC}"
find docs/hackathon -name "*.md" -type f 2>/dev/null | head -10

# Technical docs
echo -e "\n${YELLOW}MEDIUM PRIORITY - Technical Documentation:${NC}"
find docs/architecture -name "*.md" -type f 2>/dev/null | grep -E "(TECHNICAL|ARCHITECTURE)" | head -5
find docs/technical -name "*.md" -type f 2>/dev/null | head -5

# API docs
echo -e "\n${YELLOW}MEDIUM PRIORITY - API Documentation:${NC}"
find docs/getting-started -name "*API*.md" -type f 2>/dev/null | head -5

# Internal progress docs
echo -e "\n${GREEN}INTERNAL - Progress Tracking:${NC}"
find internal_docs/memory-bank -name "0[2-3]*.md" -type f 2>/dev/null | head -5

# Contract related files
echo -e "\n${GREEN}CODE - Contract Documentation:${NC}"
find src/contracts -name "*.md" -o -name "*.leo" 2>/dev/null | head -10

# Test documentation
echo -e "\n${GREEN}TESTING - Test Reports:${NC}"
find tests/reports -name "*.md" -type f 2>/dev/null | head -5

# Count total markdown files
echo -e "\n${GREEN}📊 Summary:${NC}"
TOTAL_MD=$(find . -name "*.md" -type f 2>/dev/null | wc -l)
echo "Total markdown files in project: $TOTAL_MD"

# Files mentioning Aleo
echo -e "\nFiles already mentioning 'Aleo' or 'Leo':"
grep -r -l -i "aleo\|leo" --include="*.md" . 2>/dev/null | grep -v node_modules | head -10

echo -e "\n${GREEN}✅ Use the checklist at: docs/DOCUMENTATION_UPDATE_CHECKLIST.md${NC}"
