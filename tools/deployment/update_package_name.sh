#!/bin/bash

# Update package name to publish under personal account

cd /Users/eladm/Projects/trustwrapper-eliza-plugin

# Check npm username
echo "🔍 Checking npm username..."
NPM_USER=$(npm whoami)
echo "Your npm username is: $NPM_USER"

# Update package.json to use personal scope or no scope
echo "📝 Updating package.json..."

# Option 1: Use personal scope
cat > update_package.js << 'EOF'
const fs = require('fs');
const pkg = require('./package.json');

// Get npm username from command line
const npmUser = process.argv[2];

// Update package name to use personal scope
pkg.name = `@${npmUser}/trustwrapper-eliza-plugin`;

// Write updated package.json
fs.writeFileSync('./package.json', JSON.stringify(pkg, null, 2));

console.log(`✅ Updated package name to: ${pkg.name}`);
EOF

node update_package.js "$NPM_USER"

# Commit the change
git add package.json
git commit -m "fix: Update package name to use personal npm scope for initial publication"
git push origin main

# Now publish
echo "📦 Publishing package..."
npm publish --access public --ignore-scripts

echo "✅ Package published!"
echo "📦 View at: https://www.npmjs.com/package/@$NPM_USER/trustwrapper-eliza-plugin"

# Instructions for later
echo ""
echo "📋 Next steps:"
echo "1. Create @trustwrapper organization on npm"
echo "2. Transfer package ownership or republish under @trustwrapper"
echo "3. Update all documentation with new package name"
