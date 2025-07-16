/**
 * Treasury Monitor Billing Page
 * Subscription management using design system payment components
 */

import React, { useState, useEffect } from 'react'
import { useRouter } from 'next/router'
import { BillingDashboard, type BillingData } from '../../../design-system/components/payments/billing-dashboard'
import { SubscriptionCard, defaultSubscriptionTiers } from '../../../design-system/components/payments/subscription-card'
import { PaymentButton } from '../../../design-system/components/payments/payment-button'
import { Card, CardContent, CardHeader, CardTitle } from '../../../design-system/components/ui/card'
import { Button } from '../../../design-system/components/ui/button'
import { Alert, AlertDescription } from '../../../design-system/components/ui/alert'
import { Badge } from '../../../design-system/components/ui/badge'
import { useAuth } from '../hooks/useAuth'

const BillingPage: React.FC = () => {
  const router = useRouter()
  const { user, token } = useAuth()
  const [billingData, setBillingData] = useState<BillingData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [processingPayment, setProcessingPayment] = useState(false)

  useEffect(() => {
    const fetchBillingData = async () => {
      try {
        setLoading(true)
        setError(null)

        // Fetch current subscription
        const subscriptionResponse = await fetch('/api/billing/subscription', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        })

        if (!subscriptionResponse.ok) {
          throw new Error('Failed to fetch subscription data')
        }

        const subscriptionData = await subscriptionResponse.json()

        // Fetch payment history
        const historyResponse = await fetch('/api/billing/history', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        })

        if (!historyResponse.ok) {
          throw new Error('Failed to fetch payment history')
        }

        const historyData = await historyResponse.json()

        // Combine data for BillingDashboard
        const combinedData: BillingData = {
          currentSubscription: {
            tier: subscriptionData.subscription?.plan_name || 'Free',
            status: subscriptionData.subscription?.status || 'active',
            billingCycle: subscriptionData.subscription?.billing_cycle || 'monthly',
            nextBillingDate: subscriptionData.subscription?.next_billing_date || new Date().toISOString(),
            amount: subscriptionData.subscription?.amount || 0,
            currency: 'USD'
          },
          paymentHistory: historyData.payments || [],
          usage: {
            addresses: subscriptionData.subscription?.usage?.addresses || 0,
            alerts: subscriptionData.subscription?.usage?.alerts || 0,
            apiCalls: subscriptionData.subscription?.usage?.api_calls || 0,
            limit: {
              addresses: subscriptionData.subscription?.limits?.addresses || 5,
              alerts: subscriptionData.subscription?.limits?.alerts || 100,
              apiCalls: subscriptionData.subscription?.limits?.api_calls || 1000
            }
          },
          nextInvoice: {
            amount: subscriptionData.subscription?.amount || 0,
            date: subscriptionData.subscription?.next_billing_date || new Date().toISOString(),
            items: []
          }
        }

        setBillingData(combinedData)

      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load billing data')
      } finally {
        setLoading(false)
      }
    }

    if (token) {
      fetchBillingData()
    }
  }, [token])

  const handleUpgrade = async (planId: string) => {
    try {
      setProcessingPayment(true)
      setError(null)

      const response = await fetch('/api/billing/subscribe', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          plan_id: planId,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to upgrade subscription')
      }

      const result = await response.json()

      // Redirect to payment page or show success
      if (result.payment_url) {
        window.location.href = result.payment_url
      } else {
        // Refresh billing data
        window.location.reload()
      }

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Payment processing failed')
    } finally {
      setProcessingPayment(false)
    }
  }

  const handleCancelSubscription = async () => {
    if (!confirm('Are you sure you want to cancel your subscription? You will lose access to premium features at the end of your billing period.')) {
      return
    }

    try {
      setLoading(true)
      setError(null)

      const response = await fetch('/api/billing/subscription/cancel', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ immediate: false }),
      })

      if (!response.ok) {
        throw new Error('Failed to cancel subscription')
      }

      // Refresh page to show updated status
      window.location.reload()

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to cancel subscription')
    } finally {
      setLoading(false)
    }
  }

  const getTierColor = (tier: string) => {
    switch (tier.toLowerCase()) {
      case 'enterprise': return 'bg-purple-100 text-purple-800 border-purple-200'
      case 'professional': return 'bg-blue-100 text-blue-800 border-blue-200'
      case 'starter': return 'bg-green-100 text-green-800 border-green-200'
      default: return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-purple-100 p-6">
        <div className="max-w-4xl mx-auto">
          <div className="animate-pulse">
            <div className="h-8 bg-purple-200 rounded w-48 mb-6"></div>
            <div className="space-y-6">
              <div className="h-64 bg-white rounded-lg shadow"></div>
              <div className="h-96 bg-white rounded-lg shadow"></div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-purple-100">
      {/* Header */}
      <div className="bg-white border-b border-purple-200 shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => router.push('/dashboard')}
                className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center hover:bg-purple-200 transition-colors"
              >
                <span className="text-purple-600">←</span>
              </button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Billing & Subscription
                </h1>
                <p className="text-gray-600">
                  Manage your Treasury Monitor subscription
                </p>
              </div>
            </div>
            {billingData?.currentSubscription && (
              <Badge className={getTierColor(billingData.currentSubscription.tier)}>
                {billingData.currentSubscription.tier.toUpperCase()}
              </Badge>
            )}
          </div>
        </div>
      </div>

      <div className="max-w-4xl mx-auto p-6">
        {error && (
          <Alert className="mb-6 border-red-200 bg-red-50">
            <AlertDescription className="text-red-800">
              {error}
            </AlertDescription>
          </Alert>
        )}

        {/* Current Subscription Overview */}
        {billingData && (
          <Card className="mb-8">
            <CardHeader>
              <CardTitle>Current Subscription</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <p className="text-sm font-medium text-gray-600 mb-1">Plan</p>
                  <p className="text-lg font-semibold text-gray-900">
                    {billingData.currentSubscription.tier}
                  </p>
                  <Badge className={`mt-1 ${billingData.currentSubscription.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {billingData.currentSubscription.status.toUpperCase()}
                  </Badge>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-600 mb-1">Next Billing</p>
                  <p className="text-lg font-semibold text-gray-900">
                    {new Date(billingData.currentSubscription.nextBillingDate).toLocaleDateString()}
                  </p>
                  <p className="text-sm text-gray-500">
                    ${billingData.currentSubscription.amount}/{billingData.currentSubscription.billingCycle}
                  </p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-600 mb-1">Usage</p>
                  <p className="text-sm text-gray-700">
                    {billingData.usage.addresses}/{billingData.usage.limit.addresses} addresses
                  </p>
                  <p className="text-sm text-gray-700">
                    {billingData.usage.apiCalls}/{billingData.usage.limit.apiCalls} API calls
                  </p>
                </div>
              </div>

              {billingData.currentSubscription.status === 'active' && (
                <div className="mt-6 pt-6 border-t">
                  <Button
                    variant="outline"
                    onClick={handleCancelSubscription}
                    className="text-red-600 border-red-200 hover:bg-red-50"
                  >
                    Cancel Subscription
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* Billing Dashboard */}
        {billingData && (
          <div className="mb-8">
            <BillingDashboard
              data={billingData}
              onUpdatePaymentMethod={() => {
                // Handle payment method update
                console.log('Update payment method')
              }}
              onDownloadInvoice={(invoiceId) => {
                // Handle invoice download
                console.log('Download invoice:', invoiceId)
              }}
            />
          </div>
        )}

        {/* Subscription Plans */}
        <Card>
          <CardHeader>
            <CardTitle>Available Plans</CardTitle>
            <p className="text-sm text-gray-600">
              Upgrade or change your subscription plan
            </p>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {defaultSubscriptionTiers.map((tier) => (
                <div key={tier.id}>
                  <SubscriptionCard
                    tier={tier}
                    isCurrentPlan={billingData?.currentSubscription.tier.toLowerCase() === tier.name.toLowerCase()}
                    onSubscribe={() => handleUpgrade(tier.id)}
                    loading={processingPayment}
                  />
                </div>
              ))}
            </div>

            <div className="mt-8 p-6 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border border-blue-200">
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                Enterprise Solutions
              </h3>
              <p className="text-gray-700 mb-4">
                Need custom limits, dedicated support, or on-premise deployment?
                Contact our enterprise team for a tailored solution.
              </p>
              <div className="flex space-x-4">
                <Button variant="outline">
                  Contact Sales
                </Button>
                <Button variant="outline">
                  Schedule Demo
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Security & Compliance */}
        <Card className="mt-6 bg-gradient-to-r from-green-50 to-blue-50 border-green-200">
          <CardContent className="pt-6">
            <div className="flex items-start space-x-4">
              <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center flex-shrink-0">
                <span className="text-green-600 text-lg">🔒</span>
              </div>
              <div>
                <h3 className="text-sm font-semibold text-gray-900 mb-2">
                  Payment Security & Data Protection
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-gray-700">
                  <div>
                    <strong>Secure Payments:</strong>
                    <br />All payments processed through Stripe with PCI DSS compliance and 3D Secure authentication.
                  </div>
                  <div>
                    <strong>Data Encryption:</strong>
                    <br />Your financial data is encrypted at rest and in transit using enterprise-grade AES-256 encryption.
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default BillingPage
