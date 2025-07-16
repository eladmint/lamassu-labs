#!/bin/bash

# Verify Dual Deployment of Mento Protocol Dashboard
# Tests both Hivelocity VPS and ICP Juno deployments

echo "🔍 Verifying Dual Deployment of Mento Protocol Dashboard..."
echo ""

# URLs
HIVELOCITY_URL="http://74.50.113.152:8090"
JUNO_URL="https://cmhvu-6iaaa-aaaal-asg5q-cai.icp0.io"

echo "🌐 Testing Hivelocity VPS Deployment:"
echo "   URL: $HIVELOCITY_URL"

# Test Hivelocity
HIVE_STATUS=$(curl -s -w "%{http_code}" --connect-timeout 10 "$HIVELOCITY_URL" -o /dev/null 2>/dev/null)
if [[ "$HIVE_STATUS" == "200" ]]; then
    echo "   ✅ Status: Operational (HTTP $HIVE_STATUS)"

    # Check for updated content
    if curl -s "$HIVELOCITY_URL" | grep -q "Mento Protocol Partnership Demo - UPDATED"; then
        echo "   ✅ Content: Updated banner detected"
    else
        echo "   ⚠️  Content: Banner may not be updated"
    fi

    if curl -s "$HIVELOCITY_URL" | grep -q "Enhanced monitoring with real blockchain data integration"; then
        echo "   ✅ Features: Enhanced description detected"
    else
        echo "   ⚠️  Features: Enhanced description not found"
    fi

    # Test health endpoint
    HEALTH_STATUS=$(curl -s "$HIVELOCITY_URL/health" | jq -r '.status' 2>/dev/null)
    if [[ "$HEALTH_STATUS" == "healthy" ]]; then
        echo "   ✅ Health: $HEALTH_STATUS"
    else
        echo "   ⚠️  Health: Unknown"
    fi

else
    echo "   ❌ Status: Failed (HTTP $HIVE_STATUS)"
fi

echo ""
echo "🛰️  Testing ICP Juno Deployment:"
echo "   URL: $JUNO_URL"

# Test Juno
JUNO_STATUS=$(curl -s -w "%{http_code}" --connect-timeout 30 "$JUNO_URL" -o /dev/null 2>/dev/null)
if [[ "$JUNO_STATUS" == "200" ]]; then
    echo "   ✅ Status: Operational (HTTP $JUNO_STATUS)"

    # Check for updated content
    if curl -s "$JUNO_URL" | grep -q "Mento Protocol Partnership Demo - UPDATED"; then
        echo "   ✅ Content: Updated banner detected"
    else
        echo "   ⚠️  Content: Banner may not be updated yet"
    fi

elif [[ "$JUNO_STATUS" == "503" ]]; then
    echo "   ⏳ Status: Warming up (HTTP $JUNO_STATUS)"
    echo "   📝 Note: ICP canisters need time to warm up after deployment"
else
    echo "   ❌ Status: Failed (HTTP $JUNO_STATUS)"
fi

echo ""
echo "📊 Deployment Summary:"
echo ""
echo "🌐 **Hivelocity VPS**:"
echo "   • URL: $HIVELOCITY_URL"
echo "   • Infrastructure: Nginx on Staten Island VPS"
echo "   • Benefits: Instant access, fast loading, enterprise hosting"
echo "   • Cost: Included in $14/month VPS"
echo ""
echo "🛰️  **ICP Juno Canister**:"
echo "   • URL: $JUNO_URL"
echo "   • Infrastructure: Decentralized ICP blockchain"
echo "   • Benefits: Censorship-resistant, Web3 native, global CDN"
echo "   • Cost: ~$0.10/month (extremely low)"
echo ""
echo "🎯 **Dual Deployment Benefits**:"
echo "   • Redundancy: Multiple access points for users"
echo "   • Performance: Hivelocity for speed, ICP for decentralization"
echo "   • Reliability: Service continues if one platform has issues"
echo "   • Flexibility: Different access patterns for different users"
echo ""
echo "📈 **Partnership Value**:"
echo "   • Demonstrates technical capability across platforms"
echo "   • Shows enterprise and Web3 readiness"
echo "   • Provides both traditional and blockchain hosting"
echo "   • Enables different business models"
