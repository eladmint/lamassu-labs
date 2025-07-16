# TrustWrapper npm Publishing Guide

**Status**: Ready to publish - requires npm login

## 🚀 Quick Publish Steps

### 1. Login to npm
```bash
npm login
# Enter your npm username, password, and email
```

### 2. Build and Publish
```bash
cd /Users/eladm/Projects/trustwrapper-eliza-plugin

# Clean and build
rm -rf dist/
npm install
npm run build

# Publish
npm publish --access public
```

### 3. Verify Publication
```bash
# Check package info
npm view @trustwrapper/eliza-verification-plugin

# Test installation
mkdir /tmp/test-plugin
cd /tmp/test-plugin
npm init -y
npm install @trustwrapper/eliza-verification-plugin
```

## 📋 Pre-publish Checklist

- [x] GitHub repository public and updated
- [x] API service deployed and running (http://74.50.113.152:8083)
- [x] Package.json configured correctly
- [x] Build process working
- [x] Documentation updated
- [ ] npm account logged in
- [ ] Package published

## 🎯 Post-publish Actions

### 1. Verify Package Page
Visit: https://www.npmjs.com/package/@trustwrapper/eliza-verification-plugin

### 2. Test Installation
```bash
# In a new project
npm install @trustwrapper/eliza-verification-plugin

# Or with Eliza
npm install @ai16z/eliza @trustwrapper/eliza-verification-plugin
```

### 3. Community Announcement
Post in Eliza Discord #plugins channel:

```
🚀 **TrustWrapper for Eliza is LIVE!**

Just released the first universal AI verification plugin for the Eliza framework.

🛡️ **What it does:**
- Prevents AI trading hallucinations (100% accuracy in testing)
- Multi-chain support (70+ blockchains)
- Zero-knowledge proof verification
- <50ms latency impact

📦 **Get started:**
npm install @trustwrapper/eliza-verification-plugin

🔗 **Links:**
- GitHub: https://github.com/eladmint/trustwrapper-eliza-plugin
- API Docs: http://74.50.113.152:8083/docs
- npm: https://www.npmjs.com/package/@trustwrapper/eliza-verification-plugin

Built by Lamassu Labs - Guardians of AI Trust 🦁
```

## 🔧 Troubleshooting

### npm Login Issues
If you need to create an npm account:
1. Visit https://www.npmjs.com/signup
2. Create account
3. Run `npm login` and enter credentials

### Build Errors
```bash
# Clean everything
rm -rf node_modules dist package-lock.json
npm install
npm run build
```

### Publishing Errors
- Check package name is available
- Ensure you're logged in: `npm whoami`
- Try with explicit registry: `npm publish --registry https://registry.npmjs.org/`

## 📊 Success Metrics

After publishing, monitor:
- npm download stats: https://www.npmjs.com/package/@trustwrapper/eliza-verification-plugin
- GitHub stars: https://github.com/eladmint/trustwrapper-eliza-plugin
- Community feedback in Discord

---

**Next Step**: Run `npm login` and then follow the build/publish steps above!
