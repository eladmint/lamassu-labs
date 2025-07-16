/**
 * Treasury Monitor Dashboard Page - Design System Compliant
 * Enterprise dashboard using design system components properly
 */

import React, { useState, useEffect } from 'react'
// Proper design system imports using composite components
import { DashboardLayout } from '../../../design-system/components/layouts/dashboard-layout'
import { MetricCard, MetricsGrid, AlertsPanel } from '../../../design-system/components/composite/metrics-dashboard'
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

    // Alert color mapping for design system badges
  const getAlertColor = (level: string) => {
    switch (level) {
      case 'critical': return 'destructive'
      case 'high': return 'destructive'
      case 'medium': return 'warning'
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

  if (loading) {
    return (
      <DashboardLayout variant="topnav">
        <LoadingContainer>
          <div style={{ padding: 'var(--space-6)' }}>
            <Skeleton style={{ height: 'var(--space-8)', width: '16rem', marginBottom: 'var(--space-6)' }} />
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
              gap: 'var(--space-6)',
              marginBottom: 'var(--space-8)'
            }}>
              {Array.from({ length: 4 }).map((_, i) => (
                <Skeleton key={i} style={{ height: '8rem' }} />
              ))}
            </div>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
              gap: 'var(--space-6)'
            }}>
              <Skeleton style={{ height: '16rem' }} />
              <Skeleton style={{ height: '16rem' }} />
            </div>
          </div>
        </LoadingContainer>
      </DashboardLayout>
    )
  }

  // Prepare metrics data for MetricDashboard component
  const metricsData = metrics ? [
    {
      id: 'total-value',
      label: 'Total Value',
      value: formatCurrency(metrics.totalValue),
      icon: '💰',
      color: 'success' as const,
      description: 'Across all monitored addresses'
    },
    {
      id: 'addresses',
      label: 'Addresses',
      value: metrics.addressCount,
      icon: '📍',
      color: 'primary' as const,
      description: 'Currently being monitored'
    },
    {
      id: 'alerts',
      label: 'Active Alerts',
      value: alerts.length,
      icon: '🚨',
      color: alerts.length > 0 ? 'warning' as const : 'success' as const,
      description: 'Requiring attention'
    },
    {
      id: 'last-update',
      label: 'Last Update',
      value: metrics.lastUpdate ? new Date(metrics.lastUpdate).toLocaleTimeString() : 'Never',
      icon: '🔄',
      color: 'neutral' as const,
      description: 'Real-time monitoring'
    }
  ] : []

  // Prepare alerts data for AlertPanel component
  const alertsData = alerts.map(alert => ({
    id: alert.id,
    title: alert.message,
    description: `${alert.address.slice(0, 8)}...${alert.address.slice(-6)} • ${new Date(alert.timestamp).toLocaleTimeString()}`,
    severity: alert.level,
    timestamp: new Date(alert.timestamp),
    status: 'active' as const
  }))

  return (
    <DashboardLayout
      variant="topnav"
      style={{
        background: 'linear-gradient(135deg, var(--primary-50), var(--primary-100))'
      }}
    >
      {/* Header */}
      <div style={{
        background: 'var(--background)',
        borderBottom: '1px solid var(--border)',
        boxShadow: 'var(--shadow-sm)',
        padding: 'var(--space-6)'
      }}>
        <div style={{
          maxWidth: '1280px',
          margin: '0 auto',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: 'var(--space-4)'
          }}>
            <Avatar
              size="md"
              style={{
                background: 'var(--primary-600)',
                color: 'var(--primary-foreground)'
              }}
            >
              ₳
            </Avatar>
            <div>
              <h1 style={{
                fontSize: 'var(--text-2xl)',
                fontWeight: '700',
                color: 'var(--foreground)',
                margin: 0
              }}>
                Treasury Monitor
              </h1>
              <p style={{
                fontSize: 'var(--text-sm)',
                color: 'var(--muted-foreground)',
                margin: 0
              }}>
                Welcome back, {user?.first_name || user?.email}
              </p>
            </div>
          </div>
          <div style={{ display: 'flex', gap: 'var(--space-3)' }}>
            <Button variant="outline" size="sm">
              Add Address
            </Button>
            <Button size="sm">
              Start Monitoring
            </Button>
          </div>
        </div>
      </div>

      <div style={{
        maxWidth: '1280px',
        margin: '0 auto',
        padding: 'var(--space-6)'
      }}>
        {error && (
          <Alert
            variant="destructive"
            style={{ marginBottom: 'var(--space-6)' }}
          >
            <AlertDescription>
              {error}
            </AlertDescription>
          </Alert>
        )}

        {/* Metrics Grid - Using design system composite component */}
        <div style={{ marginBottom: 'var(--space-8)' }}>
          <MetricsGrid
            metrics={metricsData}
            columns={4}
            responsive
          />
        </div>

        {/* Content Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))',
          gap: 'var(--space-6)'
        }}>
          {/* Recent Alerts - Using design system AlertsPanel component */}
          <AlertsPanel
            alerts={alertsData}
            title="Recent Alerts"
            maxVisible={5}
            showViewAll={alerts.length > 5}
            onViewAll={() => console.log('View all alerts')}
            emptyState={{
              icon: '✅',
              title: 'All Clear',
              description: 'No alerts detected across your monitored addresses'
            }}
          />

          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <CardTitle>Quick Actions</CardTitle>
            </CardHeader>
            <CardContent>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-4)' }}>
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
                    style={{
                      width: '100%',
                      justifyContent: 'flex-start',
                      gap: 'var(--space-3)'
                    }}
                  >
                    <span>{action.icon}</span>
                    {action.label}
                  </Button>
                ))}

                <div style={{
                  paddingTop: 'var(--space-4)',
                  borderTop: '1px solid var(--border)'
                }}>
                  <h4 style={{
                    fontSize: 'var(--text-sm)',
                    fontWeight: '500',
                    color: 'var(--foreground)',
                    marginBottom: 'var(--space-3)'
                  }}>
                    Enterprise Features
                  </h4>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-2)' }}>
                    {[
                      'Multi-signature wallet support',
                      'Advanced compliance reporting',
                      '24/7 monitoring with instant alerts',
                      'Dedicated support team'
                    ].map((feature, index) => (
                      <div key={index} style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: 'var(--space-2)'
                      }}>
                        <div style={{
                          width: 'var(--space-2)',
                          height: 'var(--space-2)',
                          background: 'var(--success-500)',
                          borderRadius: '50%'
                        }} />
                        <span style={{
                          fontSize: 'var(--text-xs)',
                          color: 'var(--muted-foreground)'
                        }}>
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
        <Card style={{
          marginTop: 'var(--space-6)',
          background: 'linear-gradient(135deg, var(--primary-50), var(--accent-50))',
          border: '1px solid var(--primary-200)'
        }}>
          <CardContent style={{ paddingTop: 'var(--space-6)' }}>
            <div style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: 'var(--space-4)'
            }}>
              <Avatar
                size="md"
                style={{
                  background: 'var(--primary-100)',
                  color: 'var(--primary-600)',
                  flexShrink: 0
                }}
              >
                🔒
              </Avatar>
              <div>
                <h3 style={{
                  fontSize: 'var(--text-sm)',
                  fontWeight: '600',
                  color: 'var(--foreground)',
                  marginBottom: 'var(--space-2)'
                }}>
                  Enterprise Security & Compliance
                </h3>
                <div style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                  gap: 'var(--space-4)'
                }}>
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
                      <strong style={{ fontSize: 'var(--text-xs)' }}>{item.title}:</strong>
                      <p style={{
                        fontSize: 'var(--text-xs)',
                        color: 'var(--muted-foreground)',
                        marginTop: 'var(--space-1)'
                      }}>
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
