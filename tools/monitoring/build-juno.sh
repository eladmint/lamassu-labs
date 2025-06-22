#!/bin/bash

# Build script for deploying to Juno satellite on ICP

echo "🚀 Building Lamassu Labs monitoring dashboard for Juno deployment..."

# Create dist directory
rm -rf dist
mkdir -p dist

# Copy the Juno-adapted dashboard as index.html
cp dashboard-juno.html dist/index.html

# Create a simple package.json for Juno SDK
cat > dist/package.json << EOF
{
  "name": "lamassu-monitoring",
  "version": "1.0.0",
  "type": "module",
  "dependencies": {
    "@junobuild/core": "^0.0.26"
  }
}
EOF

# Create a simple import map for browser ES modules
cat > dist/import-map.json << EOF
{
  "imports": {
    "@junobuild/core": "https://unpkg.com/@junobuild/core@0.0.26/dist/index.js"
  }
}
EOF

# Update the HTML to use import maps
sed -i '' '/<script type="module">/a\
    <script type="importmap">\
      {\
        "imports": {\
          "@junobuild/core": "https://unpkg.com/@junobuild/core@0.0.26/dist/index.js"\
        }\
      }\
    </script>' dist/index.html

echo "✅ Build complete! Files ready in ./dist directory"
echo ""
echo "Next steps:"
echo "1. Install Juno CLI: npm install -g @junobuild/cli"
echo "2. Deploy to Juno: juno deploy"
echo "3. Access your dashboard at: https://bvxuo-uaaaa-aaaal-asgua-cai.icp0.io"