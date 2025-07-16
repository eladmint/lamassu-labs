/**
 * Treasury Monitor Dashboard Page - VERIFIED Design System Compliant
 * Uses only confirmed existing components from the design system
 */

import React, { useState, useEffect } from 'react'
// Only import components that definitely exist
import { DashboardLayout } from '../../../design-system/components/layouts/dashboard-layout'
import { MetricCard } from '../../../design-system/components/composite/metrics-dashboard'
import type { MetricData } from '../../../design-system/components/composite/metrics-dashboard'
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  Button,
  Alert,
  AlertDescription,
  Badge
} from '../../../design-system/components/ui'
import { useAuth } from '../hooks/useAuth'

interface TreasuryMetrics {
  totalValue: number
  addressCount: number
  alertsCount: number
  lastUpdate: string
}

interface TreasuryAlert {
  id: string
  level: 'low' | 'medium' | 'high' | 'critical'
  message: string
  timestamp: string
  address: string
}

const DashboardPage: React.FC = () => {
  const { user, token } = useAuth()
  const [metrics, setMetrics] = useState<TreasuryMetrics | null>(null)
  const [alerts, setAlerts] = useState<TreasuryAlert[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true)
        setError(null)

        // Fetch metrics
        const metricsResponse = await fetch('/api/metrics', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        })

        if (!metricsResponse.ok) {
          throw new Error('Failed to fetch metrics')
        }

        const metricsData = await metricsResponse.json()
        setMetrics(metricsData)

        // Fetch alerts
        const alertsResponse = await fetch('/api/alerts', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        })

        if (!alertsResponse.ok) {
          throw new Error('Failed to fetch alerts')
        }

        const alertsData = await alertsResponse.json()
        setAlerts(alertsData.alerts || [])

      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load dashboard')
      } finally {
        setLoading(false)
      }
    }

    if (token) {
      fetchDashboardData()
    }
  }, [token])

  const getAlertColor = (level: string) => {
    switch (level) {
      case 'critical': return 'destructive'
      case 'high': return 'destructive'
      case 'medium': return 'default'
      case 'low': return 'secondary'
      default: return 'secondary'
    }
  }

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value)
  }

  // Prepare metrics data using the correct MetricData interface
  const metricsData: MetricData[] = metrics ? [
    {
      id: 'total-value',
      label: 'Total Value',
      value: formatCurrency(metrics.totalValue),
      icon: '💰',
      color: 'success',
      description: 'Across all monitored addresses'
    },
    {
      id: 'addresses',
      label: 'Addresses',
      value: metrics.addressCount,
      icon: '📍',
      color: 'primary',
      description: 'Currently being monitored'
    },
    {
      id: 'alerts',
      label: 'Active Alerts',
      value: alerts.length,
      icon: '🚨',
      color: alerts.length > 0 ? 'warning' : 'success',
      description: 'Requiring attention'
    },
    {
      id: 'last-update',
      label: 'Last Update',
      value: metrics.lastUpdate ? new Date(metrics.lastUpdate).toLocaleTimeString() : 'Never',
      icon: '🔄',
      color: 'neutral',
      description: 'Real-time monitoring'
    }
  ] : []

  if (loading) {
    return (
      <DashboardLayout variant="topnav">
        <div className="p-6">
          <div className="animate-pulse">
            <div className="h-8 bg-muted rounded w-64 mb-6"></div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              {Array.from({ length: 4 }).map((_, i) => (
                <div key={i} className="h-32 bg-muted rounded-lg"></div>
              ))}
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="h-64 bg-muted rounded-lg"></div>
              <div className="h-64 bg-muted rounded-lg"></div>
            </div>
          </div>
        </div>
      </DashboardLayout>
    )
  }

  return (
    <DashboardLayout variant="topnav">
      {/* Header */}
      <div className="bg-background border-b shadow-sm">
        <div className="container mx-auto px-6 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center text-primary-foreground text-lg font-bold">
                ₳
              </div>
              <div>
                <h1 className="text-2xl font-bold text-foreground">
                  Treasury Monitor
                </h1>
                <p className="text-muted-foreground">
                  Welcome back, {user?.first_name || user?.email}
                </p>
              </div>
            </div>
            <div className="flex gap-3">
              <Button variant="outline" size="sm">
                Add Address
              </Button>
              <Button size="sm">
                Start Monitoring
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto p-6">
        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertDescription>
              {error}
            </AlertDescription>
          </Alert>
        )}

        {/* Metrics Grid - Using individual MetricCard components */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {metricsData.map((metric) => (
            <MetricCard
              key={metric.id}
              metric={metric}
              variant={metric.color}
            />
          ))}
        </div>

        {/* Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Recent Alerts */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle>Recent Alerts</CardTitle>
                <Badge variant="outline">{alerts.length}</Badge>
              </div>
            </CardHeader>
            <CardContent>
              {alerts.length === 0 ? (
                <div className="text-center py-8">
                  <div className="w-12 h-12 bg-success/10 text-success rounded-full flex items-center justify-center mx-auto mb-3 text-xl">
                    ✅
                  </div>
                  <h3 className="text-sm font-medium text-foreground mb-1">
                    All Clear
                  </h3>
                  <p className="text-xs text-muted-foreground">
                    No alerts detected across your monitored addresses
                  </p>
                </div>
              ) : (
                <div className="space-y-3">
                  {alerts.slice(0, 5).map((alert) => (
                    <div
                      key={alert.id}
                      className="flex items-start gap-3 p-3 rounded-lg border"
                    >
                      <Badge variant={getAlertColor(alert.level)}>
                        {alert.level.toUpperCase()}
                      </Badge>
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-foreground">
                          {alert.message}
                        </p>
                        <div className="flex items-center text-xs text-muted-foreground mt-1 gap-2">
                          <span>{alert.address.slice(0, 8)}...{alert.address.slice(-6)}</span>
                          <span>•</span>
                          <span>{new Date(alert.timestamp).toLocaleTimeString()}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                  {alerts.length > 5 && (
                    <Button variant="outline" size="sm" className="w-full">
                      View All Alerts ({alerts.length})
                    </Button>
                  )}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {[
                  { icon: '📍', label: 'Add New Address to Monitor' },
                  { icon: '📊', label: 'Generate Portfolio Report' },
                  { icon: '🔔', label: 'Configure Alert Settings' },
                  { icon: '📈', label: 'View Historical Data' },
                  { icon: '🔑', label: 'Manage API Keys' }
                ].map((action, index) => (
                  <Button
                    key={index}
                    variant="outline"
                    className="w-full justify-start gap-3"
                  >
                    <span>{action.icon}</span>
                    {action.label}
                  </Button>
                ))}

                <div className="pt-4 border-t">
                  <h4 className="text-sm font-medium text-foreground mb-3">
                    Enterprise Features
                  </h4>
                  <div className="space-y-2">
                    {[
                      'Multi-signature wallet support',
                      'Advanced compliance reporting',
                      '24/7 monitoring with instant alerts',
                      'Dedicated support team'
                    ].map((feature, index) => (
                      <div key={index} className="flex items-center gap-2">
                        <div className="w-2 h-2 bg-success rounded-full" />
                        <span className="text-xs text-muted-foreground">
                          {feature}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Security Notice */}
        <Card className="mt-6 bg-gradient-to-r from-primary/5 to-accent/5 border-primary/20">
          <CardContent className="pt-6">
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 bg-primary/10 text-primary rounded-lg flex items-center justify-center text-lg shrink-0">
                🔒
              </div>
              <div>
                <h3 className="text-sm font-semibold text-foreground mb-2">
                  Enterprise Security & Compliance
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {[
                    {
                      title: 'Data Protection',
                      description: 'Your treasury data is encrypted end-to-end and never shared with third parties.'
                    },
                    {
                      title: 'Compliance',
                      description: 'SOC 2 Type II certified with regular security audits and penetration testing.'
                    },
                    {
                      title: 'Monitoring',
                      description: '24/7 infrastructure monitoring with 99.9% uptime SLA and instant failover.'
                    }
                  ].map((item, index) => (
                    <div key={index}>
                      <strong className="text-xs">{item.title}:</strong>
                      <p className="text-xs text-muted-foreground mt-1">
                        {item.description}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}

export default DashboardPage
