import React, { useState, useEffect } from 'react'
import {
  Shield,
  Wifi,
  WifiOff,
  RefreshCw,
  ExternalLink,
  Activity,
  TrendingUp,
  AlertTriangle,
  Crown,
  Users,
  FileText,
  Settings,
  BarChart3,
  Zap,
  Lock,
  ArrowUp
} from 'lucide-react'

// Import types and utilities
import {
  User,
  ContractData,
  SubscriptionData,
  FeatureFlag,
  NavigationItem,
  TIER_CONFIGS
} from '../../shared/types/dashboard-types'
import {
  hasFeatureAccess,
  getUsagePercentage,
  hasReachedLimit,
  getSuggestedUpgradeTier,
  getUpgradePromptMessage
} from '../../shared/utils/feature-gate'

// Mock user data - will be replaced with real authentication
const mockUsers: Record<string, User> = {
  free: {
    id: '1',
    email: 'developer@startup.com',
    name: 'Alex Developer',
    tier: TIER_CONFIGS.free,
    subscription: {
      tier: 'free',
      status: 'active',
      currentPeriodStart: '2025-06-01',
      currentPeriodEnd: '2025-07-01',
      usage: {
        contracts: 2,
        alerts: 1,
        apiCalls: 650,
        historicalDataAccess: 3
      },
      limits: TIER_CONFIGS.free.limits,
      billingAmount: 0,
      currency: 'USD'
    },
    createdAt: '2025-05-15',
    lastLogin: '2025-06-23'
  },
  professional: {
    id: '2',
    email: 'pm@growingcompany.com',
    name: 'Sarah Product Manager',
    tier: TIER_CONFIGS.professional,
    subscription: {
      tier: 'professional',
      status: 'active',
      currentPeriodStart: '2025-06-01',
      currentPeriodEnd: '2025-07-01',
      usage: {
        contracts: 12,
        alerts: 8,
        apiCalls: 4200,
        historicalDataAccess: 45
      },
      limits: TIER_CONFIGS.professional.limits,
      billingAmount: 299,
      currency: 'USD'
    },
    createdAt: '2025-03-10',
    lastLogin: '2025-06-23'
  },
  enterprise: {
    id: '3',
    email: 'cto@enterprise.com',
    name: 'Michael CTO',
    tier: TIER_CONFIGS.enterprise,
    subscription: {
      tier: 'enterprise',
      status: 'active',
      currentPeriodStart: '2025-06-01',
      currentPeriodEnd: '2025-07-01',
      usage: {
        contracts: 156,
        alerts: 45,
        apiCalls: 89000,
        historicalDataAccess: 365
      },
      limits: TIER_CONFIGS.enterprise.limits,
      billingAmount: 2999,
      currency: 'USD'
    },
    createdAt: '2024-11-20',
    lastLogin: '2025-06-23'
  }
}

interface TieredDashboardProps {
  userType?: 'free' | 'professional' | 'enterprise'
}

export function TieredTrustWrapperDashboard({ userType = 'free' }: TieredDashboardProps) {
  const [currentUser, setCurrentUser] = useState<User>(mockUsers[userType])
  const [contracts, setContracts] = useState<ContractData[]>([
    {
      id: '1',
      name: 'Hallucination Verifier',
      address: 'hallucination_verifier.aleo',
      transactions: 5,
      successRate: 100,
      gasUsed: 6250,
      lastActivity: '2 min ago',
      status: 'healthy',
      alertsEnabled: true,
      createdAt: '2025-06-20',
      owner: currentUser.id
    },
    {
      id: '2',
      name: 'Agent Registry V2',
      address: 'agent_registry_v2.aleo',
      transactions: 3,
      successRate: 100,
      gasUsed: 2940,
      lastActivity: '5 min ago',
      status: 'healthy',
      alertsEnabled: false,
      createdAt: '2025-06-21',
      owner: currentUser.id
    },
    {
      id: '3',
      name: 'Trust Verifier V2',
      address: 'trust_verifier_v2.aleo',
      transactions: 4,
      successRate: 100,
      gasUsed: 4400,
      lastActivity: '8 min ago',
      status: 'healthy',
      alertsEnabled: true,
      createdAt: '2025-06-22',
      owner: currentUser.id
    }
  ])

  const [isConnected, setIsConnected] = useState(false)
  const [lastUpdate, setLastUpdate] = useState<string>()
  const [activeNav, setActiveNav] = useState('dashboard')

  // Feature access checks
  const canAccessHistoricalData = hasFeatureAccess(currentUser.tier.tier, 'HISTORICAL_DATA')
  const canCreateCustomAlerts = hasFeatureAccess(currentUser.tier.tier, 'CUSTOM_ALERTS')
  const canAccessAdvancedAnalytics = hasFeatureAccess(currentUser.tier.tier, 'ADVANCED_ANALYTICS')
  const canAccessComplianceReports = hasFeatureAccess(currentUser.tier.tier, 'COMPLIANCE_REPORTS')
  const canManageTeam = hasFeatureAccess(currentUser.tier.tier, 'TEAM_MANAGEMENT')

  // Usage calculations
  const contractUsagePercentage = getUsagePercentage(currentUser.tier, 'contracts', contracts.length)
  const apiUsagePercentage = getUsagePercentage(currentUser.tier, 'apiCallsPerMonth', currentUser.subscription.usage.apiCalls)
  const isNearContractLimit = contractUsagePercentage > 80
  const isNearApiLimit = apiUsagePercentage > 80

  // Navigation based on tier
  const navigation: NavigationItem[] = [
    { name: 'Dashboard', href: '/dashboard', icon: Activity, current: activeNav === 'dashboard' },
    { name: 'Contracts', href: '/contracts', icon: Shield, current: activeNav === 'contracts' },
    {
      name: 'Analytics',
      href: '/analytics',
      icon: BarChart3,
      current: activeNav === 'analytics',
      requiresTier: canAccessAdvancedAnalytics ? undefined : 'professional'
    },
    {
      name: 'Alerts',
      href: '/alerts',
      icon: AlertTriangle,
      current: activeNav === 'alerts',
      requiresTier: canCreateCustomAlerts ? undefined : 'professional'
    },
    {
      name: 'Compliance',
      href: '/compliance',
      icon: FileText,
      current: activeNav === 'compliance',
      requiresTier: canAccessComplianceReports ? undefined : 'enterprise'
    },
    {
      name: 'Team',
      href: '/team',
      icon: Users,
      current: activeNav === 'team',
      requiresTier: canManageTeam ? undefined : 'enterprise'
    },
    { name: 'Settings', href: '/settings', icon: Settings, current: activeNav === 'settings' }
  ]

  // Simulate connection
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsConnected(true)
      setLastUpdate(new Date().toLocaleTimeString())
    }, 2000)
    return () => clearTimeout(timer)
  }, [])

  const handleRefresh = () => {
    setIsConnected(false)
    setTimeout(() => {
      setIsConnected(true)
      setLastUpdate(new Date().toLocaleTimeString())
      setContracts(prev => prev.map(contract => ({
        ...contract,
        transactions: contract.transactions + Math.floor(Math.random() * 2),
        lastActivity: 'Just now'
      })))
    }, 1500)
  }

  const handleUpgrade = (targetTier: 'professional' | 'enterprise') => {
    console.log(`Upgrade to ${targetTier} tier`)
    // Will integrate with billing system
  }

  const handleNavigation = (item: NavigationItem) => {
    if (item.requiresTier && item.requiresTier !== currentUser.tier.tier) {
      // Show upgrade prompt
      const upgradeMessage = getUpgradePromptMessage(currentUser.tier.tier, 'ADVANCED_ANALYTICS')
      alert(`${upgradeMessage} Click here to upgrade.`)
      return
    }
    setActiveNav(item.href.replace('/', ''))
  }

  const totalTransactions = contracts.reduce((sum, c) => sum + c.transactions, 0)
  const totalGasUsed = contracts.reduce((sum, c) => sum + (c.gasUsed || 0), 0)

  // Tier display
  const tierColors = {
    free: 'bg-gray-100 text-gray-800',
    professional: 'bg-blue-100 text-blue-800',
    enterprise: 'bg-purple-100 text-purple-800'
  }

  const tierIcons = {
    free: Activity,
    professional: TrendingUp,
    enterprise: Crown
  }

  const TierIcon = tierIcons[currentUser.tier.tier]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo and Title */}
            <div className="flex items-center">
              <Shield className="h-8 w-8 text-blue-600 mr-3" />
              <div>
                <h1 className="text-xl font-semibold text-gray-900">TrustWrapper Dashboard</h1>
                <p className="text-sm text-gray-500">Universal AI Trust Infrastructure</p>
              </div>
            </div>

            {/* User Menu */}
            <div className="flex items-center space-x-4">
              {/* Tier Badge */}
              <div className={`px-3 py-1 rounded-full text-sm font-medium flex items-center gap-2 ${tierColors[currentUser.tier.tier]}`}>
                <TierIcon className="h-4 w-4" />
                {currentUser.tier.tier.toUpperCase()}
              </div>

              {/* User Info */}
              <div className="text-right">
                <p className="text-sm font-medium text-gray-900">{currentUser.name}</p>
                <p className="text-xs text-gray-500">{currentUser.email}</p>
              </div>

              {/* Upgrade Button (if not enterprise) */}
              {currentUser.tier.tier !== 'enterprise' && (
                <button
                  onClick={() => handleUpgrade(currentUser.tier.tier === 'free' ? 'professional' : 'enterprise')}
                  className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 flex items-center gap-2"
                >
                  <Crown className="h-4 w-4" />
                  Upgrade
                </button>
              )}
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Navigation Tabs */}
        <div className="border-b border-gray-200 mb-8">
          <nav className="-mb-px flex space-x-8">
            {navigation.map((item) => {
              const isLocked = item.requiresTier && item.requiresTier !== currentUser.tier.tier
              const Icon = item.icon

              return (
                <button
                  key={item.name}
                  onClick={() => handleNavigation(item)}
                  className={`
                    whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm flex items-center gap-2
                    ${item.current
                      ? 'border-blue-500 text-blue-600'
                      : isLocked
                      ? 'border-transparent text-gray-400 cursor-not-allowed'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }
                  `}
                  disabled={isLocked}
                >
                  <Icon className="h-4 w-4" />
                  {item.name}
                  {isLocked && <Lock className="h-3 w-3" />}
                  {item.requiresTier && (
                    <span className="ml-1 px-1.5 py-0.5 text-xs font-medium bg-yellow-100 text-yellow-800 rounded">
                      {item.requiresTier}
                    </span>
                  )}
                </button>
              )
            })}
          </nav>
        </div>

        {/* Usage Alerts */}
        {(isNearContractLimit || isNearApiLimit) && (
          <div className="mb-6 bg-yellow-50 border border-yellow-200 rounded-md p-4">
            <div className="flex">
              <AlertTriangle className="h-5 w-5 text-yellow-400" />
              <div className="ml-3">
                <h3 className="text-sm font-medium text-yellow-800">Approaching Usage Limits</h3>
                <div className="mt-2 text-sm text-yellow-700">
                  <ul className="list-disc list-inside space-y-1">
                    {isNearContractLimit && (
                      <li>Contract monitoring: {contracts.length}/{currentUser.tier.limits.contracts} ({contractUsagePercentage}%)</li>
                    )}
                    {isNearApiLimit && (
                      <li>API calls: {currentUser.subscription.usage.apiCalls.toLocaleString()}/{currentUser.tier.limits.apiCallsPerMonth.toLocaleString()} ({apiUsagePercentage}%)</li>
                    )}
                  </ul>
                  <p className="mt-2">
                    <button
                      onClick={() => handleUpgrade(currentUser.tier.tier === 'free' ? 'professional' : 'enterprise')}
                      className="font-medium text-yellow-800 underline hover:text-yellow-900"
                    >
                      Upgrade to increase limits →
                    </button>
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Connection Status */}
        <div className="mb-6 bg-white rounded-lg shadow p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              {isConnected ? (
                <Wifi className="h-5 w-5 text-green-500" />
              ) : (
                <WifiOff className="h-5 w-5 text-yellow-500" />
              )}
              <div>
                <p className="font-medium text-gray-900">
                  {isConnected ? 'Connected' : 'Connecting...'}
                </p>
                <p className="text-sm text-gray-500">
                  {isConnected
                    ? `Real-time data active${lastUpdate ? ` • Last update: ${lastUpdate}` : ''}`
                    : 'Establishing connection to Aleo blockchain'
                  }
                </p>
              </div>
            </div>
            <button
              onClick={handleRefresh}
              className="flex items-center gap-2 px-3 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
            >
              <RefreshCw className="h-4 w-4" />
              Refresh
            </button>
          </div>
        </div>

        {/* Main Content - Dashboard View */}
        {activeNav === 'dashboard' && (
          <>
            {/* Usage Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Contracts</p>
                    <p className="text-2xl font-bold text-gray-900">{contracts.length}</p>
                    {currentUser.tier.limits.contracts > 0 && (
                      <p className="text-sm text-gray-500">of {currentUser.tier.limits.contracts}</p>
                    )}
                  </div>
                  <Shield className="h-8 w-8 text-blue-500" />
                </div>
                {contractUsagePercentage > 0 && (
                  <div className="mt-3">
                    <div className="flex justify-between text-sm">
                      <span>Usage</span>
                      <span>{contractUsagePercentage}%</span>
                    </div>
                    <div className="mt-1 bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${contractUsagePercentage > 80 ? 'bg-red-500' : contractUsagePercentage > 60 ? 'bg-yellow-500' : 'bg-green-500'}`}
                        style={{ width: `${contractUsagePercentage}%` }}
                      />
                    </div>
                  </div>
                )}
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">API Calls</p>
                    <p className="text-2xl font-bold text-gray-900">{currentUser.subscription.usage.apiCalls.toLocaleString()}</p>
                    {currentUser.tier.limits.apiCallsPerMonth > 0 && (
                      <p className="text-sm text-gray-500">of {currentUser.tier.limits.apiCallsPerMonth.toLocaleString()}/mo</p>
                    )}
                  </div>
                  <Zap className="h-8 w-8 text-yellow-500" />
                </div>
                {apiUsagePercentage > 0 && (
                  <div className="mt-3">
                    <div className="flex justify-between text-sm">
                      <span>Usage</span>
                      <span>{apiUsagePercentage}%</span>
                    </div>
                    <div className="mt-1 bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${apiUsagePercentage > 80 ? 'bg-red-500' : apiUsagePercentage > 60 ? 'bg-yellow-500' : 'bg-green-500'}`}
                        style={{ width: `${apiUsagePercentage}%` }}
                      />
                    </div>
                  </div>
                )}
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Success Rate</p>
                    <p className="text-2xl font-bold text-green-600">100%</p>
                    <p className="text-sm text-gray-500">All contracts healthy</p>
                  </div>
                  <TrendingUp className="h-8 w-8 text-green-500" />
                </div>
              </div>

              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">Total Transactions</p>
                    <p className="text-2xl font-bold text-gray-900">{totalTransactions}</p>
                    <p className="text-sm text-gray-500">{(totalGasUsed / 1000).toFixed(1)}K gas used</p>
                  </div>
                  <Activity className="h-8 w-8 text-purple-500" />
                </div>
              </div>
            </div>

            {/* Contract Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {contracts.map((contract) => (
                <div key={contract.id} className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow">
                  <div className="p-6">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-lg font-semibold text-gray-900">{contract.name}</h3>
                      <div className={`
                        px-2 py-1 rounded-full text-xs font-medium flex items-center gap-1
                        ${contract.status === 'healthy' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}
                      `}>
                        <span className="h-2 w-2 rounded-full bg-current animate-pulse" />
                        {contract.status.toUpperCase()}
                      </div>
                    </div>

                    <p className="text-sm text-gray-600 font-mono mb-4">{contract.address}</p>

                    <div className="grid grid-cols-2 gap-4 mb-4">
                      <div className="bg-blue-50 rounded-lg p-3">
                        <div className="flex items-center gap-2 mb-1">
                          <Activity className="h-4 w-4 text-blue-600" />
                          <span className="text-sm font-medium text-blue-900">Transactions</span>
                        </div>
                        <p className="text-xl font-bold text-blue-600">{contract.transactions}</p>
                      </div>

                      <div className="bg-green-50 rounded-lg p-3">
                        <div className="flex items-center gap-2 mb-1">
                          <TrendingUp className="h-4 w-4 text-green-600" />
                          <span className="text-sm font-medium text-green-900">Success Rate</span>
                        </div>
                        <p className="text-xl font-bold text-green-600">{contract.successRate}%</p>
                      </div>
                    </div>

                    {(contract.gasUsed || contract.lastActivity) && (
                      <div className="space-y-2 pt-4 border-t border-gray-200">
                        {contract.gasUsed && (
                          <div className="flex justify-between text-sm">
                            <span className="text-gray-600">Gas Used:</span>
                            <span className="font-medium">{contract.gasUsed.toLocaleString()}</span>
                          </div>
                        )}
                        {contract.lastActivity && (
                          <div className="flex justify-between text-sm">
                            <span className="text-gray-600">Last Activity:</span>
                            <span className="font-medium">{contract.lastActivity}</span>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {/* Add Contract Card (if under limit) */}
              {!hasReachedLimit(currentUser.tier, 'contracts', contracts.length) && (
                <div className="bg-white border-2 border-dashed border-gray-300 rounded-lg hover:border-gray-400 transition-colors">
                  <div className="p-6 text-center">
                    <Shield className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Add New Contract</h3>
                    <p className="text-sm text-gray-600 mb-4">
                      Monitor additional AI contracts with TrustWrapper verification
                    </p>
                    <button className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700">
                      Add Contract
                    </button>
                  </div>
                </div>
              )}

              {/* Upgrade Prompt Card (if at limit) */}
              {hasReachedLimit(currentUser.tier, 'contracts', contracts.length) && (
                <div className="bg-gradient-to-br from-blue-50 to-indigo-100 border border-blue-200 rounded-lg">
                  <div className="p-6 text-center">
                    <Crown className="h-12 w-12 text-blue-600 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Upgrade to Add More</h3>
                    <p className="text-sm text-gray-600 mb-4">
                      You've reached your contract limit. Upgrade to monitor more AI contracts.
                    </p>
                    <button
                      onClick={() => handleUpgrade(currentUser.tier.tier === 'free' ? 'professional' : 'enterprise')}
                      className="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 flex items-center gap-2 mx-auto"
                    >
                      <ArrowUp className="h-4 w-4" />
                      Upgrade Now
                    </button>
                  </div>
                </div>
              )}
            </div>
          </>
        )}

        {/* Footer */}
        <div className="mt-12 text-center py-8 border-t border-gray-200">
          <p className="text-sm text-gray-500">
            <strong>TrustWrapper Dashboard v4.0</strong> •
            {totalTransactions} total transactions •
            {(totalGasUsed / 1000).toFixed(1)}K gas used
          </p>
          <p className="text-xs text-gray-400 mt-1">
            Powered by Lamassu Labs • {currentUser.tier.tier.toUpperCase()} Tier
          </p>
        </div>
      </div>
    </div>
  )
}
