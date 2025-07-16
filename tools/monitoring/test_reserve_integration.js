/**
 * Test script for Reserve section integration
 * Verifies that the reserves section displays real Mento data correctly
 *
 * Run this in browser console after loading the dashboard
 */

async function testReserveIntegration() {
    console.log('🧪 Testing Reserve Integration...');

    // Check if Mento API is loaded
    if (!window.mentoAPI) {
        console.error('❌ MentoAPI not loaded');
        return false;
    }

    console.log('✅ MentoAPI loaded');

    try {
        // Test fetching reserve holdings
        console.log('📊 Fetching reserve holdings...');
        const reserves = await window.mentoAPI.getReserveHoldings();

        console.log('Reserve Data:', reserves);

        // Verify required fields
        const requiredFields = ['totalValue', 'holdings', 'collateralRatio', 'lastUpdated'];
        const missingFields = requiredFields.filter(field => !(field in reserves));

        if (missingFields.length > 0) {
            console.error('❌ Missing required fields:', missingFields);
            return false;
        }

        console.log('✅ Reserve data structure valid');

        // Test asset data
        const holdings = reserves.holdings;
        if (!holdings || Object.keys(holdings).length === 0) {
            console.error('❌ No holdings data found');
            return false;
        }

        console.log('✅ Holdings data found:', Object.keys(holdings));

        // Verify each holding has required fields
        for (const [asset, data] of Object.entries(holdings)) {
            if (!data.amount || !data.valueUSD) {
                console.error(`❌ Invalid data for ${asset}:`, data);
                return false;
            }
        }

        console.log('✅ All asset holdings have valid data');

        // Test UI elements exist
        const requiredElements = [
            'reserve-total-value',
            'reserve-health-status',
            'reserve-collateral-ratio',
            'reserve-asset-count',
            'reserve-last-update',
            'reserve-assets-table',
            'reserveCompositionCanvas',
            'reserve-risk-assessment'
        ];

        const missingElements = requiredElements.filter(id => !document.getElementById(id));

        if (missingElements.length > 0) {
            console.error('❌ Missing UI elements:', missingElements);
            return false;
        }

        console.log('✅ All required UI elements found');

        // Test updateReservesSection function exists
        if (typeof updateReservesSection !== 'function') {
            console.error('❌ updateReservesSection function not found');
            return false;
        }

        console.log('✅ updateReservesSection function available');

        // Test navigation to reserves section
        const reservesNav = document.querySelector('[data-section="reserves"]');
        if (!reservesNav) {
            console.error('❌ Reserves navigation not found');
            return false;
        }

        console.log('✅ Reserves navigation found');

        // Test updating reserves section
        console.log('🔄 Testing reserves section update...');
        await updateReservesSection();

        // Verify data was populated
        const totalValueElement = document.getElementById('reserve-total-value');
        if (totalValueElement && totalValueElement.textContent === 'Loading...') {
            console.error('❌ Total value not updated');
            return false;
        }

        console.log('✅ Reserves section updated successfully');

        // Test collateral ratio coloring
        const healthStatus = document.getElementById('reserve-health-status');
        if (healthStatus) {
            const hasHealthClass = healthStatus.className.includes('status-healthy') ||
                                 healthStatus.className.includes('status-warning') ||
                                 healthStatus.className.includes('status-error');

            if (!hasHealthClass) {
                console.error('❌ Health status not properly colored');
                return false;
            }

            console.log('✅ Health status properly colored:', healthStatus.className);
        }

        // Test chart elements
        const canvas = document.getElementById('reserveCompositionCanvas');
        if (canvas) {
            const ctx = canvas.getContext('2d');
            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            const hasDrawing = imageData.data.some(channel => channel !== 0);

            if (!hasDrawing) {
                console.warn('⚠️ Composition chart appears empty');
            } else {
                console.log('✅ Composition chart has been drawn');
            }
        }

        console.log('🎉 Reserve integration test PASSED');
        console.log('📊 Summary:');
        console.log(`   Total Reserve Value: ${window.mentoAPI.formatCurrency(reserves.totalValue)}`);
        console.log(`   Collateral Ratio: ${reserves.collateralRatio.toFixed(1)}%`);
        console.log(`   Asset Count: ${Object.keys(holdings).length}`);
        console.log(`   Assets: ${Object.keys(holdings).join(', ')}`);

        return true;

    } catch (error) {
        console.error('❌ Reserve integration test FAILED:', error);
        return false;
    }
}

// Auto-run test when mentoAPI is ready
if (window.mentoAPI) {
    testReserveIntegration();
} else {
    window.addEventListener('mentoAPIReady', testReserveIntegration);
}

// Also expose test function globally for manual testing
window.testReserveIntegration = testReserveIntegration;

console.log('🔧 Reserve integration test script loaded');
console.log('Run: testReserveIntegration() to test manually');
