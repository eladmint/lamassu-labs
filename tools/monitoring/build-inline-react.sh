#!/bin/bash

# Build React app with inline CSS for Juno
echo "🛠️  Building React app with inline CSS for Juno deployment..."

# First build the React app
npm run build

# Now inline the CSS into the HTML
if [ -f "dist/index.html" ]; then
    # Find the CSS file
    CSS_FILE=$(find dist/assets -name "*.css" -type f | head -1)

    if [ -f "$CSS_FILE" ]; then
        echo "📄 Found CSS file: $CSS_FILE"

        # Create a backup
        cp dist/index.html dist/index.html.bak

        # Extract CSS content
        CSS_CONTENT=$(cat "$CSS_FILE")

        # Create new index.html with inline CSS
        cat > dist/index.html << EOF
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="./shield.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="TrustWrapper Dashboard - Universal AI Trust Infrastructure Monitoring" />
    <meta name="keywords" content="AI, trust, verification, blockchain, monitoring, dashboard" />
    <title>TrustWrapper Dashboard v4.0</title>
    <style>
${CSS_CONTENT}
    </style>
    <script type="module" crossorigin src="./assets/index-DWbAh4eY.js"></script>
    <link rel="modulepreload" crossorigin href="./assets/vendor-DJG_os-6.js">
    <link rel="modulepreload" crossorigin href="./assets/charts-LzuhKkTR.js">
    <link rel="modulepreload" crossorigin href="./assets/ui-DU-WIhZE.js">
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
EOF

        echo "✅ Created index.html with inline CSS"

        # Remove the CSS file link from the HTML since it's now inline
        # Keep the JS files as they are

        echo "🎉 Build complete! React app ready with inline CSS"
    else
        echo "❌ No CSS file found in dist/assets"
    fi
else
    echo "❌ dist/index.html not found. Run npm run build first"
fi
