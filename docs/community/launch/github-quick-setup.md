# TrustWrapper GitHub Repository Quick Setup Guide

## 🚀 5-Minute Setup Process

### Step 1: Create GitHub Organization (if needed)
1. Go to: https://github.com/organizations/new
2. Organization name: `lamassu-labs`
3. Contact email: `hello@trustwrapper.io`
4. Type: Free (Open Source)

### Step 2: Create Repository
1. Go to: https://github.com/new
2. **Owner**: lamassu-labs
3. **Repository name**: trustwrapper-eliza-plugin
4. **Description**: Universal AI verification plugin for Eliza framework - Build trustworthy AI agents with zero-knowledge proofs
5. **Public** repository
6. **DO NOT** initialize with README, .gitignore, or license

### Step 3: Local Repository Setup
```bash
# Navigate to plugin directory
cd /Users/eladm/Projects/trustwrapper-eliza-plugin

# Add remote origin
git remote add origin https://github.com/lamassu-labs/trustwrapper-eliza-plugin.git

# Push to GitHub
git push -u origin main
```

### Step 4: Configure Repository Settings
```bash
# Using GitHub CLI (install with: brew install gh)
gh auth login

# Set repository topics
gh repo edit lamassu-labs/trustwrapper-eliza-plugin \
  --add-topic eliza-plugin \
  --add-topic ai-agents \
  --add-topic verification \
  --add-topic zero-knowledge-proof \
  --add-topic trustwrapper \
  --add-topic typescript \
  --add-topic blockchain

# Set homepage
gh repo edit lamassu-labs/trustwrapper-eliza-plugin \
  --homepage "https://trustwrapper.io"
```

### Step 5: npm Account Setup
1. Create account: https://www.npmjs.com/signup
2. Verify email
3. Generate token: https://www.npmjs.com/settings/YOUR_USERNAME/tokens
   - Type: Automation
   - Expiration: No expiration
   - Copy token immediately

### Step 6: Add GitHub Secrets
1. Go to: https://github.com/lamassu-labs/trustwrapper-eliza-plugin/settings/secrets/actions
2. Click "New repository secret"
3. Name: `NPM_TOKEN`
4. Value: [paste your npm token]
5. Click "Add secret"

### Step 7: Initial npm Publish
```bash
# From plugin directory
cd /Users/eladm/Projects/trustwrapper-eliza-plugin

# Login to npm
npm login
# Username: [your username]
# Password: [your password]
# Email: [your email]

# Publish package
npm publish --access public
```

### Step 8: Verify Success
- GitHub: https://github.com/lamassu-labs/trustwrapper-eliza-plugin
- npm: https://www.npmjs.com/package/@trustwrapper/eliza-verification-plugin
- CI/CD: Check GitHub Actions tab for green checkmarks

## 🎉 Launch Announcement

Once published, announce in:
1. Eliza Discord: https://discord.gg/eliza (#plugins channel)
2. Twitter/X: Tag @elizaos @ai16z
3. Dev.to: Write launch article
4. Reddit: r/MachineLearning, r/ethereum

## 📊 Monitor Success
- GitHub stars and forks
- npm download statistics
- Community engagement (issues, PRs)
- Integration requests

---

**Time Estimate**: 15-20 minutes for complete setup
**Result**: Public open source plugin available for immediate use
