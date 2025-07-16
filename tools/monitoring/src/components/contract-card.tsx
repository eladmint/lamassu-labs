import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Activity, CheckCircle, AlertTriangle, TrendingUp } from "lucide-react"
import { cn, formatNumber } from "@/lib/utils"

interface ContractData {
  name: string
  address: string
  transactions: number
  successRate: number
  gasUsed?: number
  lastActivity?: string
  status: 'healthy' | 'warning' | 'error'
}

interface ContractCardProps {
  contract: ContractData
  className?: string
}

const statusConfig = {
  healthy: {
    icon: CheckCircle,
    variant: 'success' as const,
    color: 'text-green-500',
    bg: 'bg-green-500/10',
  },
  warning: {
    icon: AlertTriangle,
    variant: 'warning' as const,
    color: 'text-yellow-500',
    bg: 'bg-yellow-500/10',
  },
  error: {
    icon: AlertTriangle,
    variant: 'destructive' as const,
    color: 'text-red-500',
    bg: 'bg-red-500/10',
  },
}

export function ContractCard({ contract, className }: ContractCardProps) {
  const config = statusConfig[contract.status]
  const StatusIcon = config.icon

  return (
    <Card className={cn("transition-all hover:shadow-lg", className)}>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-semibold">
            {contract.name}
          </CardTitle>
          <Badge variant={config.variant} className="flex items-center gap-1">
            <StatusIcon className="h-3 w-3" />
            {contract.status.toUpperCase()}
          </Badge>
        </div>
        <p className="text-sm text-muted-foreground font-mono">
          {contract.address}
        </p>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Metrics Grid */}
        <div className="grid grid-cols-2 gap-4">
          <div className={cn("rounded-lg p-3", config.bg)}>
            <div className="flex items-center gap-2">
              <Activity className={cn("h-4 w-4", config.color)} />
              <span className="text-sm font-medium">Transactions</span>
            </div>
            <p className="text-2xl font-bold mt-1">
              {formatNumber(contract.transactions)}
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

        {/* Additional Metrics */}
        {(contract.gasUsed || contract.lastActivity) && (
          <div className="space-y-2 pt-2 border-t">
            {contract.gasUsed && (
              <div className="flex justify-between text-sm">
                <span className="text-muted-foreground">Total Gas Used:</span>
                <span className="font-medium">{formatNumber(contract.gasUsed)}</span>
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
  )
}
