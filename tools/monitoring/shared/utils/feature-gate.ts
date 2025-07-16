// Feature gating utilities for tier-based access control

import { UserTier, FeatureFlag, FEATURE_FLAGS, TIER_CONFIGS } from '../types/dashboard-types'

/**
 * Check if a user has access to a specific feature based on their tier
 */
export const hasFeatureAccess = (userTier: UserTier['tier'], feature: FeatureFlag): boolean => {
  const allowedTiers = FEATURE_FLAGS[feature]
  return allowedTiers.includes(userTier)
}

/**
 * Get the minimum tier required for a feature
 */
export const getMinimumTierForFeature = (feature: FeatureFlag): UserTier['tier'] => {
  const allowedTiers = FEATURE_FLAGS[feature]
  const tierOrder: UserTier['tier'][] = ['free', 'professional', 'enterprise']

  for (const tier of tierOrder) {
    if (allowedTiers.includes(tier)) {
      return tier
    }
  }

  return 'enterprise' // fallback to highest tier
}

/**
 * Check if a user has reached their usage limit for a specific resource
 */
export const hasReachedLimit = (
  userTier: UserTier,
  resource: keyof UserTier['limits'],
  currentUsage: number
): boolean => {
  const limit = userTier.limits[resource]

  // -1 means unlimited
  if (limit === -1) return false

  return currentUsage >= limit
}

/**
 * Get usage percentage for a specific resource
 */
export const getUsagePercentage = (
  userTier: UserTier,
  resource: keyof UserTier['limits'],
  currentUsage: number
): number => {
  const limit = userTier.limits[resource]

  // -1 means unlimited
  if (limit === -1) return 0

  return Math.min(Math.round((currentUsage / limit) * 100), 100)
}

/**
 * Get suggested upgrade tier based on feature requirements
 */
export const getSuggestedUpgradeTier = (
  currentTier: UserTier['tier'],
  desiredFeature: FeatureFlag
): UserTier['tier'] | null => {
  const minimumTier = getMinimumTierForFeature(desiredFeature)
  const tierOrder: UserTier['tier'][] = ['free', 'professional', 'enterprise']

  const currentTierIndex = tierOrder.indexOf(currentTier)
  const minimumTierIndex = tierOrder.indexOf(minimumTier)

  // If user already has access, no upgrade needed
  if (currentTierIndex >= minimumTierIndex) {
    return null
  }

  return minimumTier
}

/**
 * Generate upgrade prompt message based on feature and current tier
 */
export const getUpgradePromptMessage = (
  currentTier: UserTier['tier'],
  feature: FeatureFlag
): string => {
  const suggestedTier = getSuggestedUpgradeTier(currentTier, feature)

  if (!suggestedTier) {
    return ''
  }

  const featureNames: Record<FeatureFlag, string> = {
    BASIC_MONITORING: 'Basic Monitoring',
    HISTORICAL_DATA: 'Historical Data',
    CUSTOM_ALERTS: 'Custom Alerts',
    ADVANCED_ANALYTICS: 'Advanced Analytics',
    COMPLIANCE_REPORTS: 'Compliance Reports',
    TEAM_MANAGEMENT: 'Team Management',
    API_ACCESS: 'API Access',
    WHITE_LABEL: 'White Label',
    PRIORITY_SUPPORT: 'Priority Support',
    DATA_EXPORT: 'Data Export',
    REAL_TIME_COLLABORATION: 'Real-time Collaboration',
    CUSTOM_INTEGRATIONS: 'Custom Integrations'
  }

  const tierPricing: Record<UserTier['tier'], string> = {
    free: 'Free',
    professional: '$299/month',
    enterprise: 'Contact Sales'
  }

  const featureName = featureNames[feature]
  const tierName = suggestedTier.charAt(0).toUpperCase() + suggestedTier.slice(1)
  const pricing = tierPricing[suggestedTier]

  return `${featureName} is available with ${tierName} plan (${pricing}). Upgrade to unlock this feature.`
}

/**
 * React hook for feature gating (to be used in React components)
 */
export const createFeatureGateHook = () => {
  return (feature: FeatureFlag, userTier?: UserTier['tier']) => {
    if (!userTier) {
      return {
        hasAccess: false,
        canUpgrade: true,
        suggestedTier: getMinimumTierForFeature(feature),
        upgradeMessage: `This feature requires a paid plan. Upgrade to unlock ${feature.toLowerCase().replace('_', ' ')}.`
      }
    }

    const hasAccess = hasFeatureAccess(userTier, feature)
    const suggestedTier = getSuggestedUpgradeTier(userTier, feature)

    return {
      hasAccess,
      canUpgrade: !!suggestedTier,
      suggestedTier,
      upgradeMessage: hasAccess ? '' : getUpgradePromptMessage(userTier, feature)
    }
  }
}

/**
 * Helper function to check multiple features at once
 */
export const checkMultipleFeatures = (
  userTier: UserTier['tier'],
  features: FeatureFlag[]
): Record<FeatureFlag, boolean> => {
  return features.reduce((acc, feature) => {
    acc[feature] = hasFeatureAccess(userTier, feature)
    return acc
  }, {} as Record<FeatureFlag, boolean>)
}

/**
 * Get all available features for a tier
 */
export const getAvailableFeatures = (tier: UserTier['tier']): FeatureFlag[] => {
  const tierConfig = TIER_CONFIGS[tier]
  return tierConfig.features as FeatureFlag[]
}

/**
 * Get all missing features for a tier (useful for upgrade prompts)
 */
export const getMissingFeatures = (currentTier: UserTier['tier']): FeatureFlag[] => {
  const allFeatures = Object.keys(FEATURE_FLAGS) as FeatureFlag[]
  const availableFeatures = getAvailableFeatures(currentTier)

  return allFeatures.filter(feature => !availableFeatures.includes(feature))
}
