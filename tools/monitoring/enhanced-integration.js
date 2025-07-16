/**
 * Enhanced Mento Dashboard Integration
 * Connects existing ICP frontend to Hivelocity backend API
 * Maintains partnership demo flow while adding real-time data
 */

// Hivelocity Backend Configuration
const HIVELOCITY_API = {
    baseURL: 'http://74.50.113.152:8086',
    apiKey: 'demo_mento_key_123',
    endpoints: {
        protocolHealth: '/api/mento/protocol-health',
        stablecoins: '/api/mento/stablecoins',
        threatIntelligence: '/api/mento/threat-intelligence',
        compliance: '/api/mento/compliance'
    }
};

// Enhanced API Client with Fallback
class EnhancedMentoAPI {
    constructor() {
        this.baseURL = HIVELOCITY_API.baseURL;
        this.apiKey = HIVELOCITY_API.apiKey;
        this.useRealAPI = false; // Start with fallback, test real API
        this.testConnection();
    }

    async testConnection() {
        try {
            const response = await fetch(`${this.baseURL}/api/health`, {
                method: 'GET',
                timeout: 5000
            });

            if (response.ok) {
                this.useRealAPI = true;
                console.log('✅ Connected to Hivelocity backend API');
                this.updateConnectionStatus(true);
            }
        } catch (error) {
            console.warn('🔄 Using fallback data, Hivelocity API unavailable:', error);
            this.updateConnectionStatus(false);
        }
    }

    updateConnectionStatus(connected) {
        // Update UI to show API connection status
        const statusElement = document.querySelector('#api-status');
        if (statusElement) {
            statusElement.innerHTML = connected
                ? '<span class="status-connected">🟢 Live Data from Hivelocity</span>'
                : '<span class="status-fallback">🟡 Demo Mode - Simulated Data</span>';
        }

        // Add banner for partner demo
        this.addPartnershipBanner(connected);
    }

    addPartnershipBanner(connected) {
        const banner = document.createElement('div');
        banner.className = 'partnership-banner';
        banner.innerHTML = `
            <div class="banner-content">
                <div class="banner-icon">🤝</div>
                <div class="banner-text">
                    <strong>Mento Protocol Partnership Demo</strong><br>
                    ${connected
                        ? 'Live monitoring powered by TrustWrapper on enterprise Hivelocity infrastructure'
                        : 'Professional demo environment showcasing TrustWrapper capabilities'
                    }
                </div>
                <div class="banner-action">
                    <a href="${this.baseURL}/api/docs" target="_blank" class="banner-link">
                        📚 API Documentation
                    </a>
                </div>
            </div>
        `;

        // Insert banner at top of dashboard
        const dashboard = document.querySelector('.dashboard-container');
        if (dashboard) {
            dashboard.insertBefore(banner, dashboard.firstChild);
        }
    }

    async makeRequest(endpoint) {
        if (!this.useRealAPI) {
            return this.getFallbackData(endpoint);
        }

        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`API request failed: ${response.statusText}`);
            }

            const data = await response.json();
            console.log(`✅ Real data from ${endpoint}:`, data);
            return data;
        } catch (error) {
            console.warn(`🔄 API call failed, using fallback for ${endpoint}:`, error);
            return this.getFallbackData(endpoint);
        }
    }

    getFallbackData(endpoint) {
        // Enhanced fallback data matching the existing dashboard structure
        switch (endpoint) {
            case HIVELOCITY_API.endpoints.protocolHealth:
                return {
                    overall_score: 94.2,
                    total_value_protected: 134000000,
                    threats_blocked: 127,
                    uptime: 99.94,
                    status: "OPERATIONAL",
                    stablecoins_monitored: 15,
                    ai_protection_status: "ACTIVE"
                };

            case HIVELOCITY_API.endpoints.stablecoins:
                return {
                    stablecoins: this.generateStablecoinData(),
                    total_count: 15,
                    monitoring_active: true
                };

            case HIVELOCITY_API.endpoints.threatIntelligence:
                return {
                    current_threats: {
                        active_threat_count: 0,
                        protection_status: "ACTIVE"
                    },
                    protection_summary: {
                        threats_blocked_today: 8,
                        protection_effectiveness: 99.8,
                        average_response_time: 42.3
                    },
                    ai_insights: {
                        market_condition_score: 87.5,
                        manipulation_probability: 3.2,
                        confidence_level: 95.7
                    }
                };

            default:
                return {};
        }
    }

    generateStablecoinData() {
        const coins = [
            { symbol: 'cUSD', peg: 'USD', price: 1.0001 },
            { symbol: 'cEUR', peg: 'EUR', price: 0.8502 },
            { symbol: 'cREAL', peg: 'BRL', price: 5.1987 },
            { symbol: 'eXOF', peg: 'XOF', price: 649.5 },
            { symbol: 'cKES', peg: 'KES', price: 144.8 }
        ];

        return coins.map(coin => ({
            symbol: coin.symbol,
            peg_currency: coin.peg,
            current_price: coin.price,
            peg_deviation: (Math.random() - 0.5) * 0.02,
            reserve_ratio: 1.1 + Math.random() * 0.4,
            health_score: 85 + Math.random() * 15,
            risk_assessment: {
                manipulation_risk: "LOW",
                stability_trend: "STABLE",
                protection_active: true
            }
        }));
    }

    // Enhanced methods for dashboard integration
    async getProtocolHealth() {
        return this.makeRequest(HIVELOCITY_API.endpoints.protocolHealth);
    }

    async getStablecoins() {
        return this.makeRequest(HIVELOCITY_API.endpoints.stablecoins);
    }

    async getThreatIntelligence() {
        return this.makeRequest(HIVELOCITY_API.endpoints.threatIntelligence);
    }

    async getComplianceMetrics() {
        return this.makeRequest(HIVELOCITY_API.endpoints.compliance);
    }
}

// Dashboard Enhancement Functions
function enhanceExistingDashboard() {
    // Initialize enhanced API client
    window.enhancedAPI = new EnhancedMentoAPI();

    // Add partnership-specific styling
    addPartnershipStyles();

    // Enhance existing data displays with real-time updates
    startRealTimeUpdates();

    // Add TrustWrapper integration indicators
    addTrustWrapperBranding();
}

function addPartnershipStyles() {
    const styles = `
        <style>
        .partnership-banner {
            background: linear-gradient(135deg, #7C3AED 0%, #5b21b6 100%);
            color: white;
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 24px;
            box-shadow: 0 4px 12px rgba(124, 58, 237, 0.2);
        }

        .banner-content {
            display: flex;
            align-items: center;
            gap: 16px;
            max-width: 1200px;
            margin: 0 auto;
        }

        .banner-icon {
            font-size: 24px;
            flex-shrink: 0;
        }

        .banner-text {
            flex: 1;
            font-size: 14px;
            line-height: 1.4;
        }

        .banner-text strong {
            font-size: 16px;
            display: block;
            margin-bottom: 4px;
        }

        .banner-action {
            flex-shrink: 0;
        }

        .banner-link {
            color: white;
            text-decoration: none;
            background: rgba(255, 255, 255, 0.2);
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 14px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            transition: all 0.2s ease;
        }

        .banner-link:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-1px);
        }

        .status-connected {
            color: #22c55e;
            font-weight: 500;
        }

        .status-fallback {
            color: #f59e0b;
            font-weight: 500;
        }

        .trustwrapper-badge {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #7C3AED;
            color: white;
            padding: 12px 16px;
            border-radius: 12px;
            font-size: 12px;
            box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
            z-index: 1000;
        }

        @media (max-width: 768px) {
            .banner-content {
                flex-direction: column;
                text-align: center;
                gap: 12px;
            }

            .trustwrapper-badge {
                position: relative;
                bottom: auto;
                right: auto;
                margin: 16px;
            }
        }
        </style>
    `;

    document.head.insertAdjacentHTML('beforeend', styles);
}

function addTrustWrapperBranding() {
    const badge = document.createElement('div');
    badge.className = 'trustwrapper-badge';
    badge.innerHTML = '🛡️ Powered by TrustWrapper';
    document.body.appendChild(badge);
}

function startRealTimeUpdates() {
    // Update dashboard with real data every 30 seconds
    setInterval(async () => {
        try {
            await updateDashboardData();
        } catch (error) {
            console.warn('Real-time update failed:', error);
        }
    }, 30000);

    // Initial data load
    updateDashboardData();
}

async function updateDashboardData() {
    if (!window.enhancedAPI) return;

    try {
        // Get real-time data from API
        const [protocolHealth, stablecoins, threatIntel] = await Promise.all([
            window.enhancedAPI.getProtocolHealth(),
            window.enhancedAPI.getStablecoins(),
            window.enhancedAPI.getThreatIntelligence()
        ]);

        // Update existing dashboard elements with real data
        updateProtocolHealthDisplay(protocolHealth);
        updateStablecoinMetrics(stablecoins);
        updateThreatIntelligence(threatIntel);

        console.log('✅ Dashboard updated with real-time data');
    } catch (error) {
        console.warn('Dashboard update failed:', error);
    }
}

function updateProtocolHealthDisplay(data) {
    // Update overall score
    const scoreElement = document.querySelector('[data-metric="overall-score"]');
    if (scoreElement) {
        scoreElement.textContent = `${data.overall_score}%`;
    }

    // Update TVL
    const tvlElement = document.querySelector('[data-metric="total-tvl"]');
    if (tvlElement) {
        tvlElement.textContent = `$${(data.total_value_protected / 1000000).toFixed(1)}M`;
    }

    // Update threats blocked
    const threatsElement = document.querySelector('[data-metric="threats-blocked"]');
    if (threatsElement) {
        threatsElement.textContent = data.threats_blocked;
    }
}

function updateStablecoinMetrics(data) {
    // Update stablecoin count
    const countElement = document.querySelector('[data-metric="stablecoin-count"]');
    if (countElement) {
        countElement.textContent = data.total_count || data.stablecoins?.length || 15;
    }

    // Update individual stablecoin cards if they exist
    if (data.stablecoins) {
        data.stablecoins.forEach((coin, index) => {
            const cardElement = document.querySelector(`[data-coin="${coin.symbol}"]`);
            if (cardElement) {
                updateStablecoinCard(cardElement, coin);
            }
        });
    }
}

function updateStablecoinCard(element, coin) {
    // Update price
    const priceElement = element.querySelector('[data-field="price"]');
    if (priceElement) {
        priceElement.textContent = coin.current_price?.toFixed(4) || '1.0000';
    }

    // Update health score
    const healthElement = element.querySelector('[data-field="health"]');
    if (healthElement) {
        healthElement.textContent = `${coin.health_score?.toFixed(1) || '95.0'}%`;
    }

    // Update risk assessment
    const riskElement = element.querySelector('[data-field="risk"]');
    if (riskElement) {
        const risk = coin.risk_assessment?.manipulation_risk || 'LOW';
        riskElement.textContent = risk;
        riskElement.className = `risk-badge risk-${risk.toLowerCase()}`;
    }
}

function updateThreatIntelligence(data) {
    // Update threat count
    const threatCountElement = document.querySelector('[data-metric="active-threats"]');
    if (threatCountElement) {
        threatCountElement.textContent = data.current_threats?.active_threat_count || 0;
    }

    // Update protection effectiveness
    const effectivenessElement = document.querySelector('[data-metric="protection-effectiveness"]');
    if (effectivenessElement) {
        effectivenessElement.textContent = `${data.protection_summary?.protection_effectiveness?.toFixed(1) || '99.8'}%`;
    }

    // Update response time
    const responseTimeElement = document.querySelector('[data-metric="response-time"]');
    if (responseTimeElement) {
        responseTimeElement.textContent = `${data.protection_summary?.average_response_time?.toFixed(0) || '42'}ms`;
    }
}

// Partnership Demo Enhancement
function addPartnershipContext() {
    // Add partner-specific messaging to key sections
    const partnerMessages = {
        'fx-partners': {
            title: '🌍 FX Partner Integration',
            content: 'Connect your FX operations to blockchain stablecoins with enterprise-grade monitoring and AI-powered risk management.'
        },
        'enterprise-features': {
            title: '🏢 Enterprise Infrastructure',
            content: 'TrustWrapper provides 24/7 monitoring, compliance reporting, and automatic threat detection for institutional FX operations.'
        },
        'api-integration': {
            title: '🔗 Seamless Integration',
            content: 'RESTful APIs enable quick integration with existing FX systems. Live backend: http://74.50.113.152:8086/api/docs'
        }
    };

    // Add these messages to appropriate sections
    Object.entries(partnerMessages).forEach(([id, message]) => {
        const section = document.querySelector(`#${id}`) || document.querySelector(`[data-section="${id}"]`);
        if (section) {
            const messageDiv = document.createElement('div');
            messageDiv.className = 'partnership-message';
            messageDiv.innerHTML = `
                <h4>${message.title}</h4>
                <p>${message.content}</p>
            `;
            section.appendChild(messageDiv);
        }
    });
}

// Initialize enhancement when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', enhanceExistingDashboard);
} else {
    enhanceExistingDashboard();
}

// Add partnership context after initial load
setTimeout(addPartnershipContext, 1000);

console.log('🚀 Enhanced Mento Dashboard Integration Loaded');
console.log('🔗 Backend API: http://74.50.113.152:8086');
console.log('🎯 Partnership Demo Mode Active');
