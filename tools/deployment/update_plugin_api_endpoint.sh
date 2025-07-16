#!/bin/bash

# Update TrustWrapper plugin to use deployed API endpoint

PLUGIN_DIR="/Users/eladm/Projects/trustwrapper-eliza-plugin"
API_ENDPOINT="http://74.50.113.152:8083"

echo "🔧 Updating plugin to use deployed API endpoint..."

# Update the service file to use production API
cat > "$PLUGIN_DIR/src/services/trustWrapperService.ts" << 'EOF'
import axios from 'axios';
import { TradingDecision, VerificationResult, PerformanceData, ComplianceRequest } from '../types';

const API_BASE_URL = process.env.TRUSTWRAPPER_API_URL || 'http://74.50.113.152:8083';

export class TrustWrapperService {
    private apiKey?: string;

    constructor(apiKey?: string) {
        this.apiKey = apiKey;
    }

    async verifyTradingDecision(decision: TradingDecision): Promise<VerificationResult> {
        try {
            const response = await axios.post(`${API_BASE_URL}/verify/trading`, decision, {
                headers: this.getHeaders(),
                timeout: 5000
            });

            return response.data;
        } catch (error) {
            console.error('TrustWrapper API error:', error);
            // Return safe default if API is unavailable
            return {
                verified: false,
                trust_score: 0,
                risk_level: 'HIGH',
                warnings: ['TrustWrapper API unavailable - defaulting to safe mode'],
                recommendation: 'REVIEW',
                details: { error: error.message },
                timestamp: new Date().toISOString()
            };
        }
    }

    async verifyPerformance(performanceData: PerformanceData): Promise<any> {
        // Placeholder for future implementation
        return {
            status: 'not_implemented',
            message: 'Performance verification coming in v1.1'
        };
    }

    async generateComplianceReport(request: ComplianceRequest): Promise<any> {
        // Placeholder for future implementation
        return {
            status: 'not_implemented',
            message: 'Compliance reporting coming in v1.1'
        };
    }

    private getHeaders() {
        const headers: any = {
            'Content-Type': 'application/json'
        };

        if (this.apiKey) {
            headers['X-API-Key'] = this.apiKey;
        }

        return headers;
    }
}

// Export singleton instance for convenience
export const trustWrapperService = new TrustWrapperService();
EOF

# Add environment variable documentation
cat >> "$PLUGIN_DIR/README.md" << 'EOF'

## Configuration

### API Endpoint

By default, the plugin connects to the public TrustWrapper API at `http://74.50.113.152:8083`. You can override this by setting the environment variable:

```bash
export TRUSTWRAPPER_API_URL=https://your-custom-api.com
```

### API Documentation

View the full API documentation at: http://74.50.113.152:8083/docs
EOF

# Commit and push changes
cd "$PLUGIN_DIR"
git add src/services/trustWrapperService.ts README.md
git commit -m "feat: Update to use production TrustWrapper API endpoint

- API endpoint: http://74.50.113.152:8083
- Added environment variable support for custom endpoints
- Added API documentation link to README"
git push origin main

echo "✅ Plugin updated to use production API!"
