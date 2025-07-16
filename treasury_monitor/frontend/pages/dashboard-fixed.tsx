/**
 * Treasury Monitor Dashboard Page - Design System Compliant
 * Enterprise dashboard using design system components properly
 */

import React, { useState, useEffect } from 'react'
// Proper design system imports
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  Button,
  Alert,
  AlertDescription,
  Badge,
  Container,
  Grid,
  GridItem,
  Stack,
  VStack,
  HStack,
  Separator,
  Avatar,
  Progress,
  Skeleton,
  LoadingContainer
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
      <Container
        size="full"
        style={{
          minHeight: '100vh',
          background: 'linear-gradient(135deg, var(--primary-50), var(--primary-100))',
          padding: 'var(--space-6)'
        }}
      >
        <Container size="7xl">
          <LoadingContainer>
            <VStack spacing="6">
              <Skeleton style={{ height: 'var(--space-8)', width: '16rem' }} />
              <Grid cols={4} gap="6">
                {Array.from({ length: 4 }).map((_, i) => (
                  <GridItem key={i}>
                    <Skeleton style={{ height: '8rem' }} />
                  </GridItem>
                ))}
              </Grid>
              <Grid cols={2} gap="6">
                <GridItem>
                  <Skeleton style={{ height: '16rem' }} />
                </GridItem>
                <GridItem>
                  <Skeleton style={{ height: '16rem' }} />
                </GridItem>
              </Grid>
            </VStack>
          </LoadingContainer>
        </Container>
      </Container>
    )
  }

  return (
    <Container
      size="full"
      style={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, var(--primary-50), var(--primary-100))'
      }}
    >
      {/* Header */}
      <Container
        style={{
          background: 'var(--background)',
          borderBottom: '1px solid var(--border)',
          boxShadow: 'var(--shadow-sm)'
        }}
      >
        <Container size="7xl" style={{ padding: 'var(--space-6)' }}>
          <HStack justify="between" align="center">
            <HStack spacing="4" align="center">
              <Avatar
                size="md"
                style={{
                  background: 'var(--primary-600)',
                  color: 'var(--primary-foreground)'
                }}
              >
                ₳
              </Avatar>
              <VStack spacing="1">
                <h1 style={{
                  fontSize: 'var(--text-2xl)',
                  fontWeight: '700',
                  color: 'var(--foreground)'
                }}>
                  Treasury Monitor
                </h1>
                <p style={{
                  fontSize: 'var(--text-sm)',
                  color: 'var(--muted-foreground)'
                }}>
                  Welcome back, {user?.first_name || user?.email}
                </p>
              </VStack>
            </HStack>
            <HStack spacing="3">
              <Button variant="outline" size="sm">
                Add Address
              </Button>
              <Button size="sm">
                Start Monitoring
              </Button>
            </HStack>
          </HStack>
        </Container>
      </Container>

      <Container size="7xl" style={{ padding: 'var(--space-6)' }}>
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

        <VStack spacing="8">
          {/* Metrics Grid */}
          <Grid cols={4} gap="6" responsive>
            <GridItem>
              <Card>
                <CardContent style={{ paddingTop: 'var(--space-6)' }}>
                  <HStack justify="between" align="center">
                    <VStack spacing="1">
                      <p style={{
                        fontSize: 'var(--text-sm)',
                        fontWeight: '500',
                        color: 'var(--muted-foreground)'
                      }}>
                        Total Value
                      </p>
                      <p style={{
                        fontSize: 'var(--text-2xl)',
                        fontWeight: '700',
                        color: 'var(--foreground)'
                      }}>
                        {metrics ? formatCurrency(metrics.totalValue) : '$0'}
                      </p>
                    </VStack>
                    <Avatar
                      size="sm"
                      style={{
                        background: 'var(--success-100)',
                        color: 'var(--success-600)'
                      }}
                    >
                      💰
                    </Avatar>
                  </HStack>
                  <p style={{
                    fontSize: 'var(--text-xs)',
                    color: 'var(--muted-foreground)',
                    marginTop: 'var(--space-2)'
                  }}>
                    Across all monitored addresses
                  </p>
                </CardContent>
              </Card>
            </GridItem>

            <GridItem>
              <Card>
                <CardContent style={{ paddingTop: 'var(--space-6)' }}>
                  <HStack justify="between" align="center">
                    <VStack spacing="1">
                      <p style={{
                        fontSize: 'var(--text-sm)',
                        fontWeight: '500',
                        color: 'var(--muted-foreground)'
                      }}>
                        Addresses
                      </p>
                      <p style={{
                        fontSize: 'var(--text-2xl)',
                        fontWeight: '700',
                        color: 'var(--foreground)'
                      }}>
                        {metrics?.addressCount || 0}
                      </p>
                    </VStack>
                    <Avatar
                      size="sm"
                      style={{
                        background: 'var(--primary-100)',
                        color: 'var(--primary-600)'
                      }}
                    >
                      📍
                    </Avatar>
                  </HStack>
                  <p style={{
                    fontSize: 'var(--text-xs)',
                    color: 'var(--muted-foreground)',
                    marginTop: 'var(--space-2)'
                  }}>
                    Currently being monitored
                  </p>
                </CardContent>
              </Card>
            </GridItem>

            <GridItem>
              <Card>
                <CardContent style={{ paddingTop: 'var(--space-6)' }}>
                  <HStack justify="between" align="center">
                    <VStack spacing="1">
                      <p style={{
                        fontSize: 'var(--text-sm)',
                        fontWeight: '500',
                        color: 'var(--muted-foreground)'
                      }}>
                        Active Alerts
                      </p>
                      <p style={{
                        fontSize: 'var(--text-2xl)',
                        fontWeight: '700',
                        color: 'var(--foreground)'
                      }}>
                        {alerts.length}
                      </p>
                    </VStack>
                    <Avatar
                      size="sm"
                      style={{
                        background: 'var(--warning-100)',
                        color: 'var(--warning-600)'
                      }}
                    >
                      🚨
                    </Avatar>
                  </HStack>
                  <p style={{
                    fontSize: 'var(--text-xs)',
                    color: 'var(--muted-foreground)',
                    marginTop: 'var(--space-2)'
                  }}>
                    Requiring attention
                  </p>
                </CardContent>
              </Card>
            </GridItem>

            <GridItem>
              <Card>
                <CardContent style={{ paddingTop: 'var(--space-6)' }}>
                  <HStack justify="between" align="center">
                    <VStack spacing="1">
                      <p style={{
                        fontSize: 'var(--text-sm)',
                        fontWeight: '500',
                        color: 'var(--muted-foreground)'
                      }}>
                        Last Update
                      </p>
                      <p style={{
                        fontSize: 'var(--text-sm)',
                        fontWeight: '700',
                        color: 'var(--foreground)'
                      }}>
                        {metrics?.lastUpdate ? new Date(metrics.lastUpdate).toLocaleTimeString() : 'Never'}
                      </p>
                    </VStack>
                    <Avatar
                      size="sm"
                      style={{
                        background: 'var(--primary-100)',
                        color: 'var(--primary-600)'
                      }}
                    >
                      🔄
                    </Avatar>
                  </HStack>
                  <p style={{
                    fontSize: 'var(--text-xs)',
                    color: 'var(--muted-foreground)',
                    marginTop: 'var(--space-2)'
                  }}>
                    Real-time monitoring
                  </p>
                </CardContent>
              </Card>
            </GridItem>
          </Grid>

          {/* Content Grid */}
          <Grid cols={2} gap="6" responsive>
            {/* Recent Alerts */}
            <GridItem>
              <Card>
                <CardHeader>
                  <HStack justify="between" align="center">
                    <CardTitle>Recent Alerts</CardTitle>
                    <Badge variant="outline">{alerts.length}</Badge>
                  </HStack>
                </CardHeader>
                <CardContent>
                  {alerts.length === 0 ? (
                    <VStack spacing="3" align="center" style={{ padding: 'var(--space-8)' }}>
                      <Avatar
                        size="lg"
                        style={{
                          background: 'var(--success-100)',
                          color: 'var(--success-600)'
                        }}
                      >
                        ✅
                      </Avatar>
                      <VStack spacing="1" align="center">
                        <h3 style={{
                          fontSize: 'var(--text-sm)',
                          fontWeight: '500',
                          color: 'var(--foreground)'
                        }}>
                          All Clear
                        </h3>
                        <p style={{
                          fontSize: 'var(--text-xs)',
                          color: 'var(--muted-foreground)'
                        }}>
                          No alerts detected across your monitored addresses
                        </p>
                      </VStack>
                    </VStack>
                  ) : (
                    <VStack spacing="3">
                      {alerts.slice(0, 5).map((alert) => (
                        <HStack
                          key={alert.id}
                          spacing="3"
                          align="start"
                          style={{
                            padding: 'var(--space-3)',
                            borderRadius: 'var(--radius-lg)',
                            border: '1px solid var(--border)'
                          }}
                        >
                          <Badge variant={getAlertColor(alert.level)}>
                            {alert.level.toUpperCase()}
                          </Badge>
                          <VStack spacing="1" style={{ flex: 1, minWidth: 0 }}>
                            <p style={{
                              fontSize: 'var(--text-sm)',
                              fontWeight: '500',
                              color: 'var(--foreground)'
                            }}>
                              {alert.message}
                            </p>
                            <HStack
                              spacing="2"
                              align="center"
                              style={{
                                fontSize: 'var(--text-xs)',
                                color: 'var(--muted-foreground)'
                              }}
                            >
                              <span>{alert.address.slice(0, 8)}...{alert.address.slice(-6)}</span>
                              <Separator orientation="vertical" style={{ height: 'var(--space-1)' }} />
                              <span>{new Date(alert.timestamp).toLocaleTimeString()}</span>
                            </HStack>
                          </VStack>
                        </HStack>
                      ))}
                      {alerts.length > 5 && (
                        <Button variant="outline" size="sm" style={{ width: '100%' }}>
                          View All Alerts ({alerts.length})
                        </Button>
                      )}
                    </VStack>
                  )}
                </CardContent>
              </Card>
            </GridItem>

            {/* Quick Actions */}
            <GridItem>
              <Card>
                <CardHeader>
                  <CardTitle>Quick Actions</CardTitle>
                </CardHeader>
                <CardContent>
                  <VStack spacing="4">
                    <Button variant="outline" style={{ width: '100%', justifyContent: 'flex-start' }}>
                      <span style={{ marginRight: 'var(--space-3)' }}>📍</span>
                      Add New Address to Monitor
                    </Button>

                    <Button variant="outline" style={{ width: '100%', justifyContent: 'flex-start' }}>
                      <span style={{ marginRight: 'var(--space-3)' }}>📊</span>
                      Generate Portfolio Report
                    </Button>

                    <Button variant="outline" style={{ width: '100%', justifyContent: 'flex-start' }}>
                      <span style={{ marginRight: 'var(--space-3)' }}>🔔</span>
                      Configure Alert Settings
                    </Button>

                    <Button variant="outline" style={{ width: '100%', justifyContent: 'flex-start' }}>
                      <span style={{ marginRight: 'var(--space-3)' }}>📈</span>
                      View Historical Data
                    </Button>

                    <Button variant="outline" style={{ width: '100%', justifyContent: 'flex-start' }}>
                      <span style={{ marginRight: 'var(--space-3)' }}>🔑</span>
                      Manage API Keys
                    </Button>

                    <VStack spacing="3" style={{ paddingTop: 'var(--space-4)', borderTop: '1px solid var(--border)' }}>
                      <h4 style={{
                        fontSize: 'var(--text-sm)',
                        fontWeight: '500',
                        color: 'var(--foreground)'
                      }}>
                        Enterprise Features
                      </h4>
                      <VStack spacing="2">
                        {[
                          'Multi-signature wallet support',
                          'Advanced compliance reporting',
                          '24/7 monitoring with instant alerts',
                          'Dedicated support team'
                        ].map((feature, index) => (
                          <HStack key={index} spacing="2" align="center">
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
                          </HStack>
                        ))}
                      </VStack>
                    </VStack>
                  </VStack>
                </CardContent>
              </Card>
            </GridItem>
          </Grid>

          {/* Security Notice */}
          <Card style={{
            background: 'linear-gradient(135deg, var(--primary-50), var(--accent-50))',
            border: '1px solid var(--primary-200)'
          }}>
            <CardContent style={{ paddingTop: 'var(--space-6)' }}>
              <HStack spacing="4" align="start">
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
                <VStack spacing="2">
                  <h3 style={{
                    fontSize: 'var(--text-sm)',
                    fontWeight: '600',
                    color: 'var(--foreground)'
                  }}>
                    Enterprise Security & Compliance
                  </h3>
                  <Grid cols={3} gap="4" responsive>
                    <GridItem>
                      <VStack spacing="1">
                        <strong style={{ fontSize: 'var(--text-xs)' }}>Data Protection:</strong>
                        <p style={{
                          fontSize: 'var(--text-xs)',
                          color: 'var(--muted-foreground)'
                        }}>
                          Your treasury data is encrypted end-to-end and never shared with third parties.
                        </p>
                      </VStack>
                    </GridItem>
                    <GridItem>
                      <VStack spacing="1">
                        <strong style={{ fontSize: 'var(--text-xs)' }}>Compliance:</strong>
                        <p style={{
                          fontSize: 'var(--text-xs)',
                          color: 'var(--muted-foreground)'
                        }}>
                          SOC 2 Type II certified with regular security audits and penetration testing.
                        </p>
                      </VStack>
                    </GridItem>
                    <GridItem>
                      <VStack spacing="1">
                        <strong style={{ fontSize: 'var(--text-xs)' }}>Monitoring:</strong>
                        <p style={{
                          fontSize: 'var(--text-xs)',
                          color: 'var(--muted-foreground)'
                        }}>
                          24/7 infrastructure monitoring with 99.9% uptime SLA and instant failover.
                        </p>
                      </VStack>
                    </GridItem>
                  </Grid>
                </VStack>
              </HStack>
            </CardContent>
          </Card>
        </VStack>
      </Container>
    </Container>
  )
}

export default DashboardPage
