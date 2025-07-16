#!/bin/bash

# Publish without scope

cd /Users/eladm/Projects/trustwrapper-eliza-plugin

# Update package.json to remove scope
echo "📝 Removing scope from package name..."

cat > update_package_no_scope.js << 'EOF'
const fs = require('fs');
const pkg = require('./package.json');

// Remove scope, just use plain name
pkg.name = 'trustwrapper-eliza-plugin';

// Write updated package.json
fs.writeFileSync('./package.json', JSON.stringify(pkg, null, 2));

console.log(`✅ Updated package name to: ${pkg.name}`);
EOF

node update_package_no_scope.js

# Commit the change
git add package.json
git commit -m "fix: Remove npm scope for initial publication"
git push origin main

# Now publish
echo "📦 Publishing package..."
npm publish --access public --ignore-scripts

echo "✅ Package published!"
echo "📦 View at: https://www.npmjs.com/package/trustwrapper-eliza-plugin"
