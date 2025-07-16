/**
 * Design System Adapter
 * Simplifies integration with the unified design system
 */

import React from 'react'

// Simplified DashboardLayout adapter
export interface DashboardLayoutProps {
  title: string
  subtitle?: string
  version?: string
  children: React.ReactNode
  userMenu?: {
    user: { name: string; email: string }
    subscription?: any
    onUpgrade?: () => void
  }
  navigation?: Array<{
    name: string
    href: string
    icon?: any
    current?: boolean
  }>
}

export function DashboardLayout({
  title,
  subtitle,
  version, // Will be used for version display
  children,
  userMenu,
  navigation
}: DashboardLayoutProps) {
  return (
    <div className="min-h-screen bg-background">
      {/* Main Layout */}
      <div className="flex">
        {/* Sidebar Navigation */}
        <aside className="hidden md:flex md:w-64 md:flex-col">
          <div className="flex flex-col flex-grow pt-5 pb-4 overflow-y-auto bg-card border-r">
            <div className="flex items-center flex-shrink-0 px-4">
              <h1 className="text-xl font-bold text-primary">{title}</h1>
            </div>
            {navigation && (
              <nav className="mt-5 flex-1 px-2 space-y-1">
                {navigation.map((item) => {
                  const Icon = item.icon
                  return (
                    <a
                      key={item.name}
                      href={item.href}
                      className={`
                        group flex items-center px-2 py-2 text-sm font-medium rounded-md
                        ${item.current
                          ? 'bg-primary/10 text-primary'
                          : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                        }
                      `}
                    >
                      {Icon && <Icon className="mr-3 h-5 w-5" />}
                      {item.name}
                    </a>
                  )
                })}
              </nav>
            )}
          </div>
        </aside>

        {/* Main Content Area */}
        <div className="flex flex-col flex-1">
          {/* Top Header */}
          <header className="bg-card border-b">
            <div className="px-4 sm:px-6 lg:px-8">
              <div className="flex items-center justify-between h-16">
                <div className="flex-1">
                  <h2 className="text-2xl font-bold text-foreground">{title}</h2>
                  {subtitle && (
                    <p className="text-sm text-muted-foreground">{subtitle}</p>
                  )}
                </div>
                {userMenu && (
                  <div className="flex items-center gap-4">
                    {userMenu.subscription && (
                      <span className="text-sm text-muted-foreground">
                        {userMenu.subscription.tier} Plan
                      </span>
                    )}
                    <div className="text-sm">
                      <p className="font-medium">{userMenu.user.name}</p>
                      <p className="text-muted-foreground">{userMenu.user.email}</p>
                    </div>
                    {version && (
                      <span className="text-xs text-muted-foreground ml-4">{version}</span>
                    )}
                  </div>
                )}
              </div>
            </div>
          </header>

          {/* Main Content */}
          <main className="flex-1">
            <div className="py-6">
              <div className="px-4 sm:px-6 lg:px-8">
                {children}
              </div>
            </div>
          </main>
        </div>
      </div>
    </div>
  )
}

// Simplified MetricsDashboard adapter
export interface MetricsDashboardProps {
  data: any
  title?: string
  showExport?: boolean
  className?: string
}

export function MetricsDashboard({
  data,
  title = "Analytics",
  showExport = true,
  className
}: MetricsDashboardProps) {
  const totalTransactions = data.transactions?.reduce((sum: number, t: any) => sum + t.count, 0) || 0

  return (
    <div className={`space-y-6 ${className}`}>
      <div className="flex items-center justify-between">
        <h3 className="text-xl font-semibold">{title}</h3>
        {showExport && (
          <button className="text-sm text-primary hover:underline">
            Export Data
          </button>
        )}
      </div>

      {/* Key Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-card p-6 rounded-lg border">
          <p className="text-sm text-muted-foreground">Total Transactions</p>
          <p className="text-3xl font-bold text-primary mt-2">{totalTransactions}</p>
        </div>
        <div className="bg-card p-6 rounded-lg border">
          <p className="text-sm text-muted-foreground">Success Rate</p>
          <p className="text-3xl font-bold text-green-500 mt-2">
            {data.performance?.successRate || 100}%
          </p>
        </div>
        <div className="bg-card p-6 rounded-lg border">
          <p className="text-sm text-muted-foreground">Avg Response Time</p>
          <p className="text-3xl font-bold text-blue-500 mt-2">
            {data.performance?.avgResponseTime || 1.2}s
          </p>
        </div>
        <div className="bg-card p-6 rounded-lg border">
          <p className="text-sm text-muted-foreground">Uptime</p>
          <p className="text-3xl font-bold text-yellow-500 mt-2">
            {data.performance?.uptime || 99.9}%
          </p>
        </div>
      </div>

      {/* Chart Placeholder */}
      <div className="bg-card p-6 rounded-lg border">
        <p className="text-center text-muted-foreground">
          Transaction volume chart will be displayed here
        </p>
        <div className="h-64 flex items-center justify-center">
          <div className="text-4xl text-primary animate-pulse">📊</div>
        </div>
      </div>
    </div>
  )
}
