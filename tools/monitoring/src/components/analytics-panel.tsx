import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'
import { TrendingUp, Activity, Zap } from "lucide-react"

interface AnalyticsData {
  timestamp: string
  transactions: number
  successRate: number
  gasUsage: number
}

interface AnalyticsPanelProps {
  data: AnalyticsData[]
  className?: string
}

// Mock data for demonstration
const mockData: AnalyticsData[] = [
  { timestamp: '00:00', transactions: 8, successRate: 100, gasUsage: 1200 },
  { timestamp: '04:00', transactions: 12, successRate: 100, gasUsage: 1800 },
  { timestamp: '08:00', transactions: 15, successRate: 97, gasUsage: 2100 },
  { timestamp: '12:00', transactions: 22, successRate: 95, gasUsage: 3200 },
  { timestamp: '16:00', transactions: 18, successRate: 98, gasUsage: 2600 },
  { timestamp: '20:00', transactions: 10, successRate: 100, gasUsage: 1500 },
]

export function AnalyticsPanel({ data = mockData, className }: AnalyticsPanelProps) {
  const totalTransactions = data.reduce((sum, item) => sum + item.transactions, 0)
  const avgSuccessRate = data.reduce((sum, item) => sum + item.successRate, 0) / data.length
  const totalGasUsage = data.reduce((sum, item) => sum + item.gasUsage, 0)

  return (
    <div className={className}>
      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center gap-2">
              <Activity className="h-5 w-5 text-nuru-primary" />
              <span className="text-sm font-medium">Total Transactions</span>
            </div>
            <p className="text-3xl font-bold mt-2 text-nuru-primary">
              {totalTransactions}
            </p>
            <p className="text-sm text-muted-foreground mt-1">
              Last 24 hours
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-green-500" />
              <span className="text-sm font-medium">Success Rate</span>
            </div>
            <p className="text-3xl font-bold mt-2 text-green-500">
              {avgSuccessRate.toFixed(1)}%
            </p>
            <p className="text-sm text-muted-foreground mt-1">
              Average across all contracts
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="flex items-center gap-2">
              <Zap className="h-5 w-5 text-yellow-500" />
              <span className="text-sm font-medium">Gas Usage</span>
            </div>
            <p className="text-3xl font-bold mt-2 text-yellow-500">
              {(totalGasUsage / 1000).toFixed(1)}K
            </p>
            <p className="text-sm text-muted-foreground mt-1">
              Total consumed
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Transaction Volume Chart */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="h-5 w-5" />
              Transaction Volume
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={data}>
                <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
                <XAxis
                  dataKey="timestamp"
                  tick={{ fontSize: 12 }}
                  tickLine={{ stroke: '#374151' }}
                />
                <YAxis
                  tick={{ fontSize: 12 }}
                  tickLine={{ stroke: '#374151' }}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'hsl(var(--card))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '8px'
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="transactions"
                  stroke="hsl(162, 100%, 47%)"
                  strokeWidth={3}
                  dot={{ fill: 'hsl(162, 100%, 47%)', strokeWidth: 2, r: 4 }}
                  activeDot={{ r: 6, stroke: 'hsl(162, 100%, 47%)', strokeWidth: 2 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Success Rate Chart */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="h-5 w-5" />
              Success Rate Trends
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={data}>
                <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
                <XAxis
                  dataKey="timestamp"
                  tick={{ fontSize: 12 }}
                  tickLine={{ stroke: '#374151' }}
                />
                <YAxis
                  domain={[90, 100]}
                  tick={{ fontSize: 12 }}
                  tickLine={{ stroke: '#374151' }}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'hsl(var(--card))',
                    border: '1px solid hsl(var(--border))',
                    borderRadius: '8px'
                  }}
                  formatter={(value) => [`${value}%`, 'Success Rate']}
                />
                <Bar
                  dataKey="successRate"
                  fill="hsl(142, 76%, 36%)"
                  radius={[4, 4, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
