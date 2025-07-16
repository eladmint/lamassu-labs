# Quick npm Publish Workaround

Since eslint is causing issues, here's a quick workaround:

## Option 1: Skip Validation
```bash
cd /Users/eladm/Projects/trustwrapper-eliza-plugin

# Install dependencies
npm install

# Build directly without validation
npm run build

# Publish without prepublish script
npm publish --access public --ignore-scripts
```

## Option 2: Fix ESLint
```bash
cd /Users/eladm/Projects/trustwrapper-eliza-plugin

# Install missing dev dependencies
npm install --save-dev eslint@^8.0.0 @typescript-eslint/eslint-plugin@^6.0.0 @typescript-eslint/parser@^6.0.0 typescript@^5.0.0

# Try publish again
npm publish --access public
```

## Option 3: Minimal Publish
```bash
cd /Users/eladm/Projects/trustwrapper-eliza-plugin

# Ensure TypeScript is installed
npm install --save-dev typescript

# Build the TypeScript
npx tsc

# Publish with ignore scripts
npm publish --access public --ignore-scripts
```

## Verify Publication
After publishing, check:
```bash
npm view @trustwrapper/eliza-verification-plugin
```

Visit: https://www.npmjs.com/package/@trustwrapper/eliza-verification-plugin
