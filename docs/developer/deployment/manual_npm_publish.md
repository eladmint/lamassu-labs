# Manual npm Publish Steps

The package is trying to publish but needs your OTP. Here's what to do:

## Step 1: Update package.json manually

Edit `/Users/eladm/Projects/trustwrapper-eliza-plugin/package.json` and change:
```json
"name": "@trustwrapper/eliza-verification-plugin"
```
to:
```json
"name": "trustwrapper-eliza-plugin"
```

## Step 2: Commit the change
```bash
cd /Users/eladm/Projects/trustwrapper-eliza-plugin
git add package.json
git commit -m "fix: Remove npm scope for publication"
git push origin main
```

## Step 3: Publish with OTP
```bash
npm publish --access public --ignore-scripts --otp=YOUR_OTP_CODE
```

Replace `YOUR_OTP_CODE` with the 6-digit code from your authenticator app.

## Alternative: Interactive publish
```bash
npm publish --access public --ignore-scripts
```

When prompted, enter your OTP code.

## After Publishing

The package will be available at:
- npm: https://www.npmjs.com/package/trustwrapper-eliza-plugin
- Install: `npm install trustwrapper-eliza-plugin`

## Update Documentation

After publishing, we'll need to update all references from:
- `@trustwrapper/eliza-verification-plugin`
- to `trustwrapper-eliza-plugin`
