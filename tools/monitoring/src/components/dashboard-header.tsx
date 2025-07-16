import { Card, CardContent } from "@/components/ui/card"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Shield, Wifi, WifiOff, RefreshCw, ExternalLink } from "lucide-react"
import { cn } from "@/lib/utils"

interface DashboardHeaderProps {
  isConnected: boolean
  lastUpdate?: string
  onRefresh?: () => void
  className?: string
}

export function DashboardHeader({
  isConnected,
  lastUpdate,
  onRefresh,
  className
}: DashboardHeaderProps) {
  return (
    <div className={cn("space-y-4", className)}>
      {/* Main Header */}
      <Card className="bg-gradient-to-r from-nuru-background to-nuru-card border-nuru-primary/20">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="p-3 rounded-lg bg-nuru-primary/10">
                <Shield className="h-8 w-8 text-nuru-primary" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-foreground">
                  TrustWrapper Dashboard
                </h1>
                <p className="text-muted-foreground">
                  Universal AI Trust Infrastructure Monitoring
                </p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <Button
                variant="outline"
                size="sm"
                onClick={onRefresh}
                className="gap-2"
              >
                <RefreshCw className="h-4 w-4" />
                Refresh
              </Button>
              <Button
                variant="nuru"
                size="sm"
                className="gap-2"
                asChild
              >
                <a
                  href="https://trustwrapper.ai"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <ExternalLink className="h-4 w-4" />
                  Visit Site
                </a>
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Connection Status */}
      <Alert variant={isConnected ? "success" : "warning"}>
        <div className="flex items-center gap-2">
          {isConnected ? (
            <Wifi className="h-4 w-4" />
          ) : (
            <WifiOff className="h-4 w-4" />
          )}
          <Badge
            variant={isConnected ? "success" : "warning"}
            className="animate-pulse-glow"
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
    </div>
  )
}
