import { useState, useEffect } from 'react'
import { DashboardLayout, MetricsDashboard } from './design-system-adapter'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Shield, Wifi, WifiOff, RefreshCw, ExternalLink, Activity, TrendingUp } from 'lucide-react'

interface ContractData {
  id: string
  name: string
  address: string
  transactions: number
  successRate: number
  gasUsed?: number
  lastActivity?: string
  status: 'healthy' | 'warning' | 'error'
}

interface SubscriptionData {
  tier: 'free' | 'starter' | 'professional' | 'enterprise'
  usage: {
    addresses: number
    alerts: number
    apiCalls: number
  }
  limits: {
    addresses: number
    alerts: number
    apiCalls: number
  }
}

// Mock subscription data - will be connected to billing system
const mockSubscription: SubscriptionData = {
  tier: 'professional',
  usage: {
    addresses: 3,
    alerts: 5,
    apiCalls: 1250
  },
  limits: {
    addresses: 25,
    alerts: 50,
    apiCalls: 10000
  }
}

export function TrustWrapperDashboard() {
  const [contracts, setContracts] = useState<ContractData[]>([
    {
      id: '1',
      name: 'Hallucination Verifier',
      address: 'hallucination_verifier.aleo',
      transactions: 5,
      successRate: 100,
      gasUsed: 6250,
      lastActivity: '2 min ago',
      status: 'healthy'
    },
    {
      id: '2',
      name: 'Agent Registry V2',
      address: 'agent_registry_v2.aleo',
      transactions: 3,
      successRate: 100,
      gasUsed: 2940,
      lastActivity: '5 min ago',
      status: 'healthy'
    },
    {
      id: '3',
      name: 'Trust Verifier V2',
      address: 'trust_verifier_v2.aleo',
      transactions: 4,
      successRate: 100,
      gasUsed: 4400,
      lastActivity: '8 min ago',
      status: 'healthy'
    }
  ])

  const [isConnected, setIsConnected] = useState(false)
  const [lastUpdate, setLastUpdate] = useState<string>()

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
      // Simulate data update
      setContracts(prev => prev.map(contract => ({
        ...contract,
        transactions: contract.transactions + Math.floor(Math.random() * 2),
        lastActivity: 'Just now'
      })))
    }, 1500)
  }

  const handleUpgrade = () => {
    // Will connect to billing system
    console.log('Upgrade to Enterprise tier')
  }

  const totalTransactions = contracts.reduce((sum, c) => sum + c.transactions, 0)
  const totalGasUsed = contracts.reduce((sum, c) => sum + (c.gasUsed || 0), 0)

  // Prepare data for MetricsDashboard
  const metricsData = {
    transactions: contracts.map(c => ({
      timestamp: new Date().toISOString(),
      contract: c.name,
      count: c.transactions
    })),
    performance: {
      successRate: 100,
      avgResponseTime: 1.2,
      uptime: 99.9
    }
  }

  return (
    <DashboardLayout
      title="TrustWrapper Dashboard"
      subtitle="Universal AI Trust Infrastructure Monitoring"
      version="v4.0"
      userMenu={{
        user: { name: 'Demo User', email: 'demo@trustwrapper.ai' },
        subscription: mockSubscription,
        onUpgrade: handleUpgrade
      }}
      navigation={[
        { name: 'Dashboard', href: '/', icon: Activity, current: true },
        { name: 'Contracts', href: '/contracts', icon: Shield },
        { name: 'Analytics', href: '/analytics', icon: TrendingUp },
        { name: 'Alerts', href: '/alerts', icon: Activity },
        { name: 'Settings', href: '/settings', icon: Activity }
      ]}
    >
      <div className="space-y-6">
        {/* Connection Status Alert */}
        <Alert variant={isConnected ? "success" : "warning"}>
          <div className="flex items-center gap-2">
            {isConnected ? (
              <Wifi className="h-4 w-4" />
            ) : (
              <WifiOff className="h-4 w-4" />
            )}
            <Badge
              variant={isConnected ? "success" : "warning"}
              className="animate-pulse"
            >
              {isConnected ? "Connected" : "Connecting..."}
            </Badge>
          </div>
          <AlertDescription className="mt-2">
            {isConnected ? (
              <span>
                Connected to Aleo blockchain. Real-time data active.
                {lastUpdate && (
                  <span className="ml-2 text-xs">
                    Last update: {lastUpdate}
                  </span>
                )}
              </span>
            ) : (
              <span>
                Establishing connection to Aleo blockchain.
                Dashboard will show cached data until connection is restored.
              </span>
            )}
          </AlertDescription>
        </Alert>

        {/* Quick Actions */}
        <div className="flex gap-3">
          <Button onClick={handleRefresh} variant="outline" size="sm">
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh Data
          </Button>
          <Button variant="default" size="sm" asChild>
            <a href="https://trustwrapper.ai" target="_blank" rel="noopener noreferrer">
              <ExternalLink className="h-4 w-4 mr-2" />
              Visit Site
            </a>
          </Button>
        </div>

        {/* Contract Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {contracts.map((contract) => (
            <Card key={contract.id} className="hover:shadow-lg transition-shadow">
              <CardHeader className="pb-3">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-lg font-semibold">
                    {contract.name}
                  </CardTitle>
                  <Badge
                    variant={contract.status === 'healthy' ? 'success' : 'warning'}
                    className="flex items-center gap-1"
                  >
                    <span className="h-2 w-2 rounded-full bg-current animate-pulse" />
                    {contract.status.toUpperCase()}
                  </Badge>
                </div>
                <p className="text-sm text-muted-foreground font-mono">
                  {contract.address}
                </p>
              </CardHeader>

              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="rounded-lg p-3 bg-primary/10">
                    <div className="flex items-center gap-2">
                      <Activity className="h-4 w-4 text-primary" />
                      <span className="text-sm font-medium">Transactions</span>
                    </div>
                    <p className="text-2xl font-bold mt-1 text-primary">
                      {contract.transactions}
                    </p>
                  </div>

                  <div className="rounded-lg p-3 bg-blue-500/10">
                    <div className="flex items-center gap-2">
                      <TrendingUp className="h-4 w-4 text-blue-500" />
                      <span className="text-sm font-medium">Success Rate</span>
                    </div>
                    <p className="text-2xl font-bold mt-1 text-blue-500">
                      {contract.successRate}%
                    </p>
                  </div>
                </div>

                {(contract.gasUsed || contract.lastActivity) && (
                  <div className="space-y-2 pt-2 border-t">
                    {contract.gasUsed && (
                      <div className="flex justify-between text-sm">
                        <span className="text-muted-foreground">Total Gas Used:</span>
                        <span className="font-medium">{contract.gasUsed.toLocaleString()}</span>
                      </div>
                    )}
                    {contract.lastActivity && (
                      <div className="flex justify-between text-sm">
                        <span className="text-muted-foreground">Last Activity:</span>
                        <span className="font-medium">{contract.lastActivity}</span>
                      </div>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Metrics Dashboard */}
        <MetricsDashboard
          data={metricsData}
          title="Real-Time Analytics"
          showExport={mockSubscription.tier !== 'free'}
          className="mt-8"
        />

        {/* Footer Stats */}
        <div className="text-center py-8 border-t border-border/50">
          <p className="text-sm text-muted-foreground">
            <strong>TrustWrapper Dashboard v4.0</strong> •
            {totalTransactions} total transactions •
            {(totalGasUsed / 1000).toFixed(1)}K gas used
          </p>
          <p className="text-xs text-muted-foreground mt-1">
            Powered by Lamassu Labs • Built with Unified Design System
          </p>
        </div>
      </div>
    </DashboardLayout>
  )
}
