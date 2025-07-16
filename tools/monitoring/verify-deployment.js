#!/usr/bin/env node

/**
 * Verify Juno deployment is working correctly
 */

const https = require('https');

const URL = 'https://cmhvu-6iaaa-aaaal-asg5q-cai.icp0.io';

console.log('🔍 Verifying deployment at:', URL);

// Check index.html
https.get(URL, (res) => {
  let data = '';
  res.on('data', (chunk) => {
    data += chunk;
  });

  res.on('end', () => {
    console.log('\n✅ Index page loaded successfully');
    console.log('📋 Status:', res.statusCode);

    // Check for CSS link
    const cssMatch = data.match(/href="\.\/assets\/index-[^"]+\.css"/);
    if (cssMatch) {
      console.log('✅ CSS link found:', cssMatch[0]);

      // Now verify CSS loads
      const cssPath = cssMatch[0].match(/\.\/assets\/index-[^"]+\.css/)[0];
      const cssUrl = `${URL}/${cssPath.substring(2)}`;

      console.log('\n🔍 Checking CSS at:', cssUrl);
      https.get(cssUrl, (cssRes) => {
        console.log('📋 CSS Status:', cssRes.statusCode);
        console.log('📋 Content-Type:', cssRes.headers['content-type']);

        if (cssRes.statusCode === 200) {
          console.log('✅ CSS file loads successfully!');
        } else {
          console.log('❌ CSS file failed to load');
        }
      });
    } else {
      console.log('❌ No CSS link found in HTML');
    }

    // Check for JS link
    const jsMatch = data.match(/src="\.\/assets\/index-[^"]+\.js"/);
    if (jsMatch) {
      console.log('✅ JS link found:', jsMatch[0]);
    }
  });
}).on('error', (err) => {
  console.error('❌ Error:', err);
});
