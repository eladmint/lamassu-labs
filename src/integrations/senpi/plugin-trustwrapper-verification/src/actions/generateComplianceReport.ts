/**
 * Generate Compliance Report Action for Senpi Integration
 *
 * Creates comprehensive compliance monitoring reports for institutional
 * requirements, regulatory adherence, and audit trail documentation.
 */

import { Action, IAgentRuntime, Memory, State } from "@ai16z/eliza";
import { trustWrapperService } from "../services/trustWrapperService.js";
import {
    ComplianceMonitoringRequest,
    ComplianceMonitoringResult,
    SenpiVerificationContext
} from "../types/index.js";

export const generateComplianceReportAction: Action = {
    name: "GENERATE_COMPLIANCE_REPORT",
    similes: [
        "COMPLIANCE_REPORT",
        "AUDIT_REPORT",
        "REGULATORY_REPORT",
        "GENERATE_AUDIT",
        "COMPLIANCE_CHECK",
        "REGULATORY_COMPLIANCE",
        "INSTITUTIONAL_REPORT"
    ],
    description: "Generate comprehensive compliance monitoring reports for institutional requirements and regulatory adherence",

    validate: async (runtime: IAgentRuntime, message: Memory) => {
        // Check if message contains compliance monitoring request
        const text = message.content.text?.toLowerCase() || "";

        const complianceKeywords = [
            "compliance", "audit", "regulatory", "report",
            "institutional", "requirements", "violations"
        ];

        const hasComplianceKeyword = complianceKeywords.some(keyword =>
            text.includes(keyword)
        );

        // Must have compliance keyword and either specific request or account context
        return hasComplianceKeyword && (
            text.includes("generate") ||
            text.includes("create") ||
            text.includes("report") ||
            message.content.accountId ||
            message.content.institutionalLevel
        );
    },

    handler: async (runtime: IAgentRuntime, message: Memory, state: State, options: any, callback: any) => {
        try {
            console.log("🏛️ Generating compliance report via TrustWrapper...");

            // Extract compliance monitoring parameters from message
            const request = extractComplianceRequest(message);

            // Get additional context from Senpi
            const context: SenpiVerificationContext = {
                agentId: runtime.agentId || "senpi_agent",
                sessionId: state?.sessionId || `session_${Date.now()}`,
                userWallet: message.content.userWallet,
                tradingContext: message.content.tradingContext
            };

            // Call TrustWrapper compliance monitoring service
            const complianceResult = await trustWrapperService.monitorCompliance(request);

            // Generate formatted response
            const responseText = formatComplianceResponse(complianceResult, request, context);

            console.log("✅ Compliance report generated successfully");

            callback({
                text: responseText,
                action: "COMPLIANCE_REPORT_GENERATED",
                metadata: {
                    complianceId: complianceResult.complianceId,
                    status: complianceResult.status,
                    score: complianceResult.score,
                    violations: complianceResult.violations.length,
                    requirements: complianceResult.requirements.length
                }
            });

        } catch (error) {
            console.error("❌ Failed to generate compliance report:", error);

            // Generate fallback compliance report
            const fallbackReport = generateFallbackComplianceReport(message);

            callback({
                text: fallbackReport,
                action: "COMPLIANCE_REPORT_ERROR",
                metadata: {
                    error: "TrustWrapper service unavailable",
                    fallback: true
                }
            });
        }
    }
};

/**
 * Extract compliance monitoring request from message
 */
function extractComplianceRequest(message: Memory): ComplianceMonitoringRequest {
    const content = message.content;

    // Extract parameters from message content or use defaults
    const accountId = content.accountId || content.userId || `account_${Date.now()}`;
    const institutionalLevel = content.institutionalLevel || "retail";
    const jurisdiction = content.jurisdiction || "US";

    // Extract trading activity parameters
    const volume = content.volume || content.tradingVolume || 100000;
    const frequency = content.frequency || content.tradingFrequency || 10;
    const riskLevel = content.riskLevel || 0.3;

    // Extract timeframe (default to last 30 days)
    const endTime = Date.now();
    const startTime = content.startTime || (endTime - (30 * 24 * 60 * 60 * 1000));

    return {
        accountId,
        institutionalLevel: institutionalLevel as "retail" | "professional" | "institutional",
        jurisdiction,
        tradingActivity: {
            volume,
            frequency,
            riskLevel
        },
        timeframe: {
            start: startTime,
            end: endTime
        }
    };
}

/**
 * Format compliance monitoring result into readable response
 */
function formatComplianceResponse(
    result: ComplianceMonitoringResult,
    request: ComplianceMonitoringRequest,
    context: SenpiVerificationContext
): string {
    const statusEmoji = getComplianceStatusEmoji(result.status);
    const scorePercentage = Math.round(result.score * 100);

    let response = `${statusEmoji} **COMPLIANCE REPORT GENERATED**\n\n`;

    // Overall status and score
    response += `📊 **Compliance Status**: ${result.status.toUpperCase()}\n`;
    response += `🎯 **Compliance Score**: ${scorePercentage}%\n`;
    response += `🏛️ **Institution Level**: ${request.institutionalLevel.toUpperCase()}\n`;
    response += `🌍 **Jurisdiction**: ${request.jurisdiction}\n\n`;

    // Requirements summary
    if (result.requirements.length > 0) {
        response += `📋 **COMPLIANCE REQUIREMENTS**\n`;

        const metRequirements = result.requirements.filter(req => req.status === "met");
        const pendingRequirements = result.requirements.filter(req => req.status === "pending");
        const failedRequirements = result.requirements.filter(req => req.status === "failed");

        response += `✅ Met: ${metRequirements.length}\n`;
        response += `⏳ Pending: ${pendingRequirements.length}\n`;
        response += `❌ Failed: ${failedRequirements.length}\n\n`;

        // Show critical failed requirements
        const criticalFailed = failedRequirements.filter(req => req.severity === "critical");
        if (criticalFailed.length > 0) {
            response += `🚨 **CRITICAL ISSUES**:\n`;
            criticalFailed.forEach(req => {
                response += `   • ${req.name}: ${req.description}\n`;
            });
            response += `\n`;
        }
    }

    // Violations summary
    if (result.violations.length > 0) {
        response += `⚠️ **COMPLIANCE VIOLATIONS** (${result.violations.length})\n`;

        const criticalViolations = result.violations.filter(v => v.severity === "critical");
        const highViolations = result.violations.filter(v => v.severity === "high");

        if (criticalViolations.length > 0) {
            response += `🔴 Critical: ${criticalViolations.length}\n`;
        }
        if (highViolations.length > 0) {
            response += `🟠 High: ${highViolations.length}\n`;
        }

        // Show recent violations
        const recentViolations = result.violations
            .filter(v => v.status === "open")
            .slice(0, 3);

        if (recentViolations.length > 0) {
            response += `\n**Recent Open Violations**:\n`;
            recentViolations.forEach(violation => {
                const severityEmoji = violation.severity === "critical" ? "🔴" :
                                     violation.severity === "high" ? "🟠" : "🟡";
                response += `   ${severityEmoji} ${violation.type}: ${violation.description}\n`;
            });
        }
        response += `\n`;
    }

    // Reporting data summary
    if (result.reportingData) {
        const report = result.reportingData;
        response += `📈 **TRADING ACTIVITY SUMMARY**\n`;
        response += `💰 Total Volume: $${report.details.tradingVolume.toLocaleString()}\n`;
        response += `📊 Total Transactions: ${report.summary.totalTransactions}\n`;
        response += `💸 Avg Transaction: $${report.details.averageTransactionSize.toLocaleString()}\n`;
        response += `⚡ Risk Score: ${Math.round(report.summary.riskScore * 100)}%\n\n`;
    }

    // Recommendations
    if (result.recommendations.length > 0) {
        response += `💡 **RECOMMENDATIONS**\n`;
        result.recommendations.slice(0, 5).forEach(rec => {
            response += `   • ${rec}\n`;
        });
        response += `\n`;
    }

    // Report metadata
    response += `📄 **Report Details**\n`;
    response += `🆔 Compliance ID: \`${result.complianceId}\`\n`;
    response += `📅 Generated: ${new Date().toLocaleString()}\n`;
    response += `🔗 Agent: ${context.agentId}\n`;

    // Audit trail info
    if (result.auditTrail.length > 0) {
        response += `📝 Audit Events: ${result.auditTrail.length}\n`;
    }

    return response;
}

/**
 * Get emoji for compliance status
 */
function getComplianceStatusEmoji(status: string): string {
    switch (status) {
        case "compliant": return "✅";
        case "warning": return "⚠️";
        case "violation": return "🚨";
        default: return "📊";
    }
}

/**
 * Generate fallback compliance report when TrustWrapper is unavailable
 */
function generateFallbackComplianceReport(message: Memory): string {
    const accountId = message.content.accountId || "demo_account";
    const timestamp = new Date().toLocaleString();

    return `⚠️ **COMPLIANCE REPORT - DEMO MODE**

🔧 **System Status**: TrustWrapper service temporarily unavailable
📊 **Account**: ${accountId}
📅 **Generated**: ${timestamp}

📋 **SIMULATED COMPLIANCE CHECK**
✅ **Status**: Compliant (Demo)
🎯 **Score**: 87% (Simulated)
🏛️ **Level**: Retail Investor

📈 **DEMO METRICS**
💰 Trading Volume: $25,000 (30 days)
📊 Transactions: 15
💸 Avg Transaction: $1,667
⚡ Risk Score: 23%

✅ **REQUIREMENTS MET** (4/5)
   • Know Your Customer (KYC): ✅
   • Anti-Money Laundering (AML): ✅
   • Risk Assessment: ✅
   • Transaction Monitoring: ✅
   • Advanced Reporting: ⏳ Pending

💡 **RECOMMENDATIONS**
   • Complete advanced reporting setup
   • Consider professional investor upgrade
   • Enable real-time monitoring alerts

🔗 **Real Integration**: Contact support for TrustWrapper API access
📧 **Support**: enterprise@trustwrapper.io`;
}
