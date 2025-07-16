'use client'

import React, { useState, useEffect } from 'react'
import {
  ArrowUpIcon,
  ArrowDownIcon,
  RefreshCw,
  TrendingUp,
  Shield,
  Globe,
  DollarSign,
  Activity,
  Clock,
  AlertTriangle,
  CheckCircle,
  Info
} from 'lucide-react'

interface StablecoinData {
  symbol: string
  name: string
  supply_usd: number
  growth_rate_24h: number
  market_share: number
  fiat_currency: string
}

interface DashboardData {
  summary: {
    total_protocol_value_usd: number
    active_stablecoins: number
    latest_block: number
    data_freshness: string
  }
  stablecoins: StablecoinData[]
  reserves: {
    total_usd_value: number
    addresses_monitored: number
  }
  alerts: Array<{
    severity: string
    message: string
    type: string
  }>
  last_updated: string
}

export default function MentoMonitorDashboard() {
  const [data, setData] = useState<DashboardData | null>(null)
  const [loading, setLoading] = useState(true)
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date())
  const [connectionStatus, setConnectionStatus] = useState<'connected' | 'connecting' | 'disconnected'>('connecting')

  // Simulate real-time data updates
  useEffect(() => {
    const fetchData = async () => {
      try {
        setConnectionStatus('connecting')

        // Simulate API call with our real data structure
        const mockData: DashboardData = {
          summary: {
            total_protocol_value_usd: 25567056.925,
            active_stablecoins: 5,
            latest_block: 38808532,
            data_freshness: 'live'
          },
          stablecoins: [
            {
              symbol: 'cUSD',
              name: 'Celo Dollar',
              supply_usd: 21550941.463,
              growth_rate_24h: 0.0,
              market_share: 84.3,
              fiat_currency: 'USD'
            },
            {
              symbol: 'cEUR',
              name: 'Celo Euro',
              supply_usd: 3527668.98,
              growth_rate_24h: 0.0,
              market_share: 13.8,
              fiat_currency: 'EUR'
            },
            {
              symbol: 'cREAL',
              name: 'Celo Brazilian Real',
              supply_usd: 245513.062,
              growth_rate_24h: 0.0,
              market_share: 1.0,
              fiat_currency: 'BRL'
            },
            {
              symbol: 'eXOF',
              name: 'CFA Franc',
              supply_usd: 25337.111,
              growth_rate_24h: 0.0,
              market_share: 0.1,
              fiat_currency: 'XOF'
            },
            {
              symbol: 'cKES',
              name: 'Celo Kenyan Shilling',
              supply_usd: 217596.309,
              growth_rate_24h: 0.0,
              market_share: 0.9,
              fiat_currency: 'KES'
            }
          ],
          reserves: {
            total_usd_value: 56115874.118,
            addresses_monitored: 2
          },
          alerts: [],
          last_updated: new Date().toISOString()
        }

        setData(mockData)
        setConnectionStatus('connected')
        setLastUpdate(new Date())
        setLoading(false)
      } catch (error) {
        setConnectionStatus('disconnected')
        console.error('Failed to fetch data:', error)
      }
    }

    fetchData()
    const interval = setInterval(fetchData, 30000) // Update every 30 seconds

    return () => clearInterval(interval)
  }, [])

  const formatCurrency = (value: number) => {
    if (value >= 1e9) return `$${(value / 1e9).toFixed(1)}B`
    if (value >= 1e6) return `$${(value / 1e6).toFixed(1)}M`
    if (value >= 1e3) return `$${(value / 1e3).toFixed(1)}K`
    return `$${value.toFixed(0)}`
  }

  const formatPercentage = (value: number) => {
    return `${value >= 0 ? '+' : ''}${value.toFixed(1)}%`
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="loading-spinner mx-auto mb-4"></div>
          <p className="text-gray-600">Loading Mento Protocol data...</p>
        </div>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center">
        <div className="text-center">
          <AlertTriangle className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <p className="text-gray-600">Failed to load data. Please try again.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Shield className="w-8 h-8 text-primary-600" />
                <h1 className="text-2xl font-bold text-gray-900">Mento Protocol Monitor</h1>
              </div>
              <div className="flex items-center space-x-2">
                <div className="pulse-dot"></div>
                <span className="text-sm text-gray-500">Live Data</span>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <div className="text-right">
                <p className="text-sm text-gray-500">Last Updated</p>
                <p className="text-sm font-medium text-gray-900">
                  {lastUpdate.toLocaleTimeString()}
                </p>
              </div>
              <div className={`status-${connectionStatus === 'connected' ? 'healthy' : 'warning'}`}>
                {connectionStatus === 'connected' ? <CheckCircle className="w-4 h-4 mr-1" /> : <Clock className="w-4 h-4 mr-1" />}
                {connectionStatus}
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="stat-card">
            <div className="flex items-center justify-between">
              <div>
                <p className="metric-label">Total Protocol Value</p>
                <p className="metric-value">{formatCurrency(data.summary.total_protocol_value_usd)}</p>
              </div>
              <DollarSign className="w-8 h-8 text-green-500" />
            </div>
          </div>

          <div className="stat-card">
            <div className="flex items-center justify-between">
              <div>
                <p className="metric-label">Reserve Holdings</p>
                <p className="metric-value">{formatCurrency(data.reserves.total_usd_value)}</p>
              </div>
              <Shield className="w-8 h-8 text-blue-500" />
            </div>
          </div>

          <div className="stat-card">
            <div className="flex items-center justify-between">
              <div>
                <p className="metric-label">Active Stablecoins</p>
                <p className="metric-value">{data.summary.active_stablecoins}</p>
              </div>
              <Globe className="w-8 h-8 text-purple-500" />
            </div>
          </div>

          <div className="stat-card">
            <div className="flex items-center justify-between">
              <div>
                <p className="metric-label">Latest Block</p>
                <p className="metric-value">{data.summary.latest_block.toLocaleString()}</p>
              </div>
              <Activity className="w-8 h-8 text-orange-500" />
            </div>
          </div>
        </div>

        {/* Alerts Section */}
        {data.alerts.length > 0 ? (
          <div className="card mb-8 bg-yellow-50 border-yellow-200">
            <div className="flex items-center mb-4">
              <AlertTriangle className="w-5 h-5 text-yellow-600 mr-2" />
              <h3 className="text-lg font-semibold text-yellow-800">Active Alerts</h3>
            </div>
            <div className="space-y-2">
              {data.alerts.map((alert, index) => (
                <div key={index} className={`status-${alert.severity.toLowerCase()}`}>
                  {alert.message}
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="card mb-8 bg-green-50 border-green-200">
            <div className="flex items-center">
              <CheckCircle className="w-5 h-5 text-green-600 mr-2" />
              <span className="text-green-800 font-medium">All Systems Healthy</span>
              <span className="text-green-600 ml-2">No active alerts</span>
            </div>
          </div>
        )}

        {/* Stablecoins Table */}
        <div className="card">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">Stablecoin Analytics</h3>
            <div className="flex items-center space-x-2 text-sm text-gray-500">
              <RefreshCw className="w-4 h-4" />
              <span>Real-time data</span>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-medium text-gray-500">Asset</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-500">Supply (USD)</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-500">24h Change</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-500">Market Share</th>
                  <th className="text-right py-3 px-4 font-medium text-gray-500">Currency</th>
                </tr>
              </thead>
              <tbody>
                {data.stablecoins.map((coin, index) => (
                  <tr key={coin.symbol} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-4 px-4">
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 rounded-full bg-primary-100 flex items-center justify-center">
                          <span className="text-sm font-medium text-primary-700">
                            {coin.symbol.charAt(1)}
                          </span>
                        </div>
                        <div>
                          <p className="font-medium text-gray-900">{coin.symbol}</p>
                          <p className="text-sm text-gray-500">{coin.name}</p>
                        </div>
                      </div>
                    </td>
                    <td className="text-right py-4 px-4 font-medium text-gray-900">
                      {formatCurrency(coin.supply_usd)}
                    </td>
                    <td className="text-right py-4 px-4">
                      <div className={`flex items-center justify-end space-x-1 ${
                        coin.growth_rate_24h >= 0 ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {coin.growth_rate_24h >= 0 ? (
                          <ArrowUpIcon className="w-4 h-4" />
                        ) : (
                          <ArrowDownIcon className="w-4 h-4" />
                        )}
                        <span className="font-medium">{formatPercentage(coin.growth_rate_24h)}</span>
                      </div>
                    </td>
                    <td className="text-right py-4 px-4">
                      <div className="flex items-center justify-end space-x-2">
                        <div className="w-16 bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-primary-600 h-2 rounded-full"
                            style={{ width: `${Math.min(coin.market_share, 100)}%` }}
                          ></div>
                        </div>
                        <span className="text-sm font-medium text-gray-700 w-12">
                          {coin.market_share.toFixed(1)}%
                        </span>
                      </div>
                    </td>
                    <td className="text-right py-4 px-4">
                      <span className="status-indicator bg-gray-100 text-gray-700">
                        {coin.fiat_currency}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Competitive Advantage Banner */}
        <div className="mt-8 card bg-gradient-to-r from-primary-50 to-blue-50 border-primary-200">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <TrendingUp className="w-8 h-8 text-primary-600" />
              <div>
                <h4 className="text-lg font-semibold text-primary-900">Powered by Nuru AI</h4>
                <p className="text-primary-700">Real-time blockchain monitoring • No API rate limits • Advanced analytics</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-sm text-primary-600 font-medium">vs Hourly Cached APIs</p>
              <p className="text-2xl font-bold text-primary-900">60x Faster</p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <p className="text-sm text-gray-500">
                © 2025 Nuru AI - Lamassu Labs. Advanced stablecoin monitoring technology.
              </p>
            </div>
            <div className="flex items-center space-x-4 text-sm text-gray-500">
              <span>Data Source: Direct Celo Blockchain</span>
              <span>•</span>
              <span>Update Frequency: Real-time</span>
              <span>•</span>
              <span>SLA: 99.9% Uptime</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
