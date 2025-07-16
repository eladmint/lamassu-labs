import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Activity, CheckCircle, XCircle, Clock } from "lucide-react"
import { formatTime, cn } from "@/lib/utils"

interface Transaction {
  id: string
  contract: string
  type: string
  status: 'success' | 'failed' | 'pending'
  timestamp: string
  gasUsed?: number
  value?: string
}

interface TransactionFeedProps {
  transactions: Transaction[]
  className?: string
  maxItems?: number
}

const statusConfig = {
  success: {
    icon: CheckCircle,
    variant: 'success' as const,
    color: 'text-green-500',
  },
  failed: {
    icon: XCircle,
    variant: 'destructive' as const,
    color: 'text-red-500',
  },
  pending: {
    icon: Clock,
    variant: 'warning' as const,
    color: 'text-yellow-500',
  },
}

// Mock transaction data
const mockTransactions: Transaction[] = [
  {
    id: 'tx_001',
    contract: 'hallucination_verifier.aleo',
    type: 'verify_output',
    status: 'success',
    timestamp: new Date(Date.now() - 1000 * 60 * 2).toISOString(),
    gasUsed: 1250,
  },
  {
    id: 'tx_002',
    contract: 'agent_registry_v2.aleo',
    type: 'register_agent',
    status: 'success',
    timestamp: new Date(Date.now() - 1000 * 60 * 5).toISOString(),
    gasUsed: 980,
  },
  {
    id: 'tx_003',
    contract: 'trust_verifier_v2.aleo',
    type: 'calculate_trust',
    status: 'pending',
    timestamp: new Date(Date.now() - 1000 * 60 * 8).toISOString(),
  },
  {
    id: 'tx_004',
    contract: 'hallucination_verifier.aleo',
    type: 'verify_output',
    status: 'success',
    timestamp: new Date(Date.now() - 1000 * 60 * 12).toISOString(),
    gasUsed: 1100,
  },
  {
    id: 'tx_005',
    contract: 'agent_registry_v2.aleo',
    type: 'update_metrics',
    status: 'failed',
    timestamp: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
  },
]

export function TransactionFeed({
  transactions = mockTransactions,
  className,
  maxItems = 10
}: TransactionFeedProps) {
  const displayTransactions = transactions.slice(0, maxItems)

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Activity className="h-5 w-5" />
          Live Transaction Feed
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {displayTransactions.map((tx) => {
            const config = statusConfig[tx.status]
            const StatusIcon = config.icon

            return (
              <div
                key={tx.id}
                className="flex items-center justify-between p-3 rounded-lg border bg-card/50 hover:bg-card/80 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <StatusIcon className={cn("h-4 w-4", config.color)} />
                  <div className="min-w-0">
                    <p className="font-medium text-sm truncate">
                      {tx.contract}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {tx.type}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  {tx.gasUsed && (
                    <span className="text-xs text-muted-foreground">
                      {tx.gasUsed} gas
                    </span>
                  )}
                  <Badge variant={config.variant} className="text-xs">
                    {tx.status}
                  </Badge>
                  <span className="text-xs text-muted-foreground whitespace-nowrap">
                    {formatTime(tx.timestamp)}
                  </span>
                </div>
              </div>
            )
          })}
        </div>

        {transactions.length === 0 && (
          <div className="text-center py-8 text-muted-foreground">
            <Activity className="h-8 w-8 mx-auto mb-2 opacity-50" />
            <p>No transactions yet</p>
            <p className="text-sm">Transaction data will appear here when available</p>
          </div>
        )}

        {transactions.length > maxItems && (
          <div className="text-center mt-4">
            <p className="text-sm text-muted-foreground">
              Showing {maxItems} of {transactions.length} transactions
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
