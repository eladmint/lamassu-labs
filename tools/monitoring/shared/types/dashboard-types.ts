// Shared TypeScript types for both user-facing and internal dashboards

export interface UserTier {
  tier: 'free' | 'professional' | 'enterprise'
  features: string[]
  limits: {
    contracts: number
    historicalDays: number
    alertChannels: number
    teamMembers: number
    apiCallsPerMonth: number
  }
}

export interface User {
  id: string
  email: string
  name: string
  tier: UserTier
  subscription: SubscriptionData
  createdAt: string
  lastLogin: string
}

export interface SubscriptionData {
  tier: 'free' | 'professional' | 'enterprise'
  status: 'active' | 'past_due' | 'cancelled' | 'trial'
  currentPeriodStart: string
  currentPeriodEnd: string
  usage: {
    contracts: number
    alerts: number
    apiCalls: number
    historicalDataAccess: number
  }
  limits: {
    contracts: number
    alerts: number
    apiCalls: number
    historicalDays: number
    teamMembers: number
  }
  billingAmount: number
  currency: string
}

export interface ContractData {
  id: string
  name: string
  address: string
  transactions: number
  successRate: number
  gasUsed?: number
  lastActivity?: string
  status: 'healthy' | 'warning' | 'error' | 'inactive'
  alertsEnabled: boolean
  createdAt: string
  owner: string
}

export interface AlertRule {
  id: string
  name: string
  contractId: string
  type: 'threshold' | 'anomaly' | 'performance'
  condition: {
    metric: string
    operator: '>' | '<' | '=' | '!='
    value: number | string
  }
  channels: ('email' | 'slack' | 'webhook' | 'sms')[]
  enabled: boolean
  createdAt: string
  lastTriggered?: string
}

export interface AnalyticsData {
  transactions: Array<{
    timestamp: string
    contract: string
    count: number
    gasUsed: number
    success: boolean
  }>
  performance: {
    successRate: number
    avgResponseTime: number
    uptime: number
    errorRate: number
  }
  trends: {
    daily: Array<{ date: string; value: number }>
    weekly: Array<{ week: string; value: number }>
    monthly: Array<{ month: string; value: number }>
  }
}

export interface BusinessMetrics {
  revenue: {
    mrr: number
    arr: number
    growth: number
  }
  users: {
    total: number
    active: number
    new: number
    churn: number
  }
  conversion: {
    freeToProRate: number
    proToEnterpriseRate: number
    trialConversionRate: number
  }
  engagement: {
    dau: number
    mau: number
    avgSessionTime: number
    featureAdoption: Record<string, number>
  }
}

export interface SystemHealth {
  api: {
    uptime: number
    responseTime: number
    errorRate: number
    requestsPerMinute: number
  }
  database: {
    connectionPool: number
    queryPerformance: number
    storageUsed: number
    backupStatus: 'healthy' | 'warning' | 'error'
  }
  blockchain: {
    connected: boolean
    latestBlock: number
    syncStatus: 'synced' | 'syncing' | 'behind'
    networkHealth: number
  }
}

export interface NavigationItem {
  name: string
  href: string
  icon: React.ComponentType<any>
  current?: boolean
  requiresTier?: UserTier['tier']
  badge?: string | number
}

export interface DashboardProps {
  user?: User
  title: string
  subtitle?: string
  version?: string
  navigation: NavigationItem[]
  userMenu?: {
    user: User
    subscription: SubscriptionData
    onUpgrade?: () => void
    onLogout?: () => void
  }
  children: React.ReactNode
}

// Feature flags for tier-based access
export const FEATURE_FLAGS = {
  BASIC_MONITORING: ['free', 'professional', 'enterprise'],
  HISTORICAL_DATA: ['professional', 'enterprise'],
  CUSTOM_ALERTS: ['professional', 'enterprise'],
  ADVANCED_ANALYTICS: ['professional', 'enterprise'],
  COMPLIANCE_REPORTS: ['enterprise'],
  TEAM_MANAGEMENT: ['enterprise'],
  API_ACCESS: ['professional', 'enterprise'],
  WHITE_LABEL: ['enterprise'],
  PRIORITY_SUPPORT: ['enterprise'],
  DATA_EXPORT: ['professional', 'enterprise'],
  REAL_TIME_COLLABORATION: ['enterprise'],
  CUSTOM_INTEGRATIONS: ['enterprise']
} as const

export type FeatureFlag = keyof typeof FEATURE_FLAGS

// Tier configurations
export const TIER_CONFIGS: Record<UserTier['tier'], UserTier> = {
  free: {
    tier: 'free',
    features: ['BASIC_MONITORING'],
    limits: {
      contracts: 3,
      historicalDays: 7,
      alertChannels: 1,
      teamMembers: 1,
      apiCallsPerMonth: 1000
    }
  },
  professional: {
    tier: 'professional',
    features: [
      'BASIC_MONITORING',
      'HISTORICAL_DATA',
      'CUSTOM_ALERTS',
      'ADVANCED_ANALYTICS',
      'API_ACCESS',
      'DATA_EXPORT'
    ],
    limits: {
      contracts: 25,
      historicalDays: 90,
      alertChannels: 5,
      teamMembers: 5,
      apiCallsPerMonth: 10000
    }
  },
  enterprise: {
    tier: 'enterprise',
    features: [
      'BASIC_MONITORING',
      'HISTORICAL_DATA',
      'CUSTOM_ALERTS',
      'ADVANCED_ANALYTICS',
      'COMPLIANCE_REPORTS',
      'TEAM_MANAGEMENT',
      'API_ACCESS',
      'WHITE_LABEL',
      'PRIORITY_SUPPORT',
      'DATA_EXPORT',
      'REAL_TIME_COLLABORATION',
      'CUSTOM_INTEGRATIONS'
    ],
    limits: {
      contracts: -1, // unlimited
      historicalDays: -1, // unlimited
      alertChannels: -1, // unlimited
      teamMembers: -1, // unlimited
      apiCallsPerMonth: -1 // unlimited
    }
  }
}
