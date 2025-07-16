/**
 * Treasury Monitor Registration Page
 * New user registration using design system components
 */

import React, { useState } from 'react'
import { useRouter } from 'next/router'
import { RegistrationForm } from '../../../design-system/components/auth/registration-form'
import { Card, CardContent } from '../../../design-system/components/ui/card'
import { Alert, AlertDescription } from '../../../design-system/components/ui/alert'

const RegisterPage: React.FC = () => {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  const handleRegister = async (userData: {
    email: string
    password: string
    firstName?: string
    lastName?: string
    company?: string
  }) => {
    try {
      setLoading(true)
      setError(null)

      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: userData.email,
          password: userData.password,
          first_name: userData.firstName,
          last_name: userData.lastName,
          company: userData.company,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Registration failed')
      }

      const data = await response.json()
      setSuccess(true)

      // Redirect to login after successful registration
      setTimeout(() => {
        router.push('/login?message=registration_success')
      }, 2000)

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  const handleLoginRedirect = () => {
    router.push('/login')
  }

  if (success) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-purple-100 flex items-center justify-center p-4">
        <div className="w-full max-w-md">
          <Card className="bg-green-50 border-green-200">
            <CardContent className="pt-6">
              <div className="text-center">
                <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-green-600 text-2xl">✓</span>
                </div>
                <h2 className="text-xl font-bold text-gray-900 mb-2">
                  Registration Successful!
                </h2>
                <p className="text-gray-600 mb-4">
                  Please check your email to verify your account before signing in.
                </p>
                <p className="text-sm text-gray-500">
                  Redirecting to login page...
                </p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-purple-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <div className="w-12 h-12 bg-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white text-xl font-bold">₳</span>
            </div>
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Join Treasury Monitor
          </h1>
          <p className="text-gray-600">
            Start monitoring your Cardano treasury today
          </p>
        </div>

        {error && (
          <Alert className="mb-6 border-red-200 bg-red-50">
            <AlertDescription className="text-red-800">
              {error}
            </AlertDescription>
          </Alert>
        )}

        {/* Registration Form */}
        <RegistrationForm
          onSubmit={handleRegister}
          loading={loading}
          error={error}
          onSignIn={handleLoginRedirect}
          variant="enterprise"
        />

        {/* Enterprise Value Proposition */}
        <Card className="mt-6 bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
          <CardContent className="pt-6">
            <h3 className="text-sm font-semibold text-gray-900 mb-3">
              Why Choose Treasury Monitor?
            </h3>
            <ul className="space-y-2 text-sm text-gray-700">
              <li className="flex items-center">
                <div className="w-1.5 h-1.5 bg-purple-500 rounded-full mr-2" />
                Real-time monitoring of treasury addresses
              </li>
              <li className="flex items-center">
                <div className="w-1.5 h-1.5 bg-purple-500 rounded-full mr-2" />
                Enterprise-grade security and compliance
              </li>
              <li className="flex items-center">
                <div className="w-1.5 h-1.5 bg-purple-500 rounded-full mr-2" />
                Advanced alerting and reporting
              </li>
              <li className="flex items-center">
                <div className="w-1.5 h-1.5 bg-purple-500 rounded-full mr-2" />
                Multi-signature wallet support
              </li>
              <li className="flex items-center">
                <div className="w-1.5 h-1.5 bg-purple-500 rounded-full mr-2" />
                24/7 dedicated support team
              </li>
            </ul>
          </CardContent>
        </Card>

        {/* Pricing Preview */}
        <Card className="mt-6 bg-gradient-to-r from-green-50 to-emerald-50 border-green-200">
          <CardContent className="pt-6">
            <div className="text-center">
              <h3 className="text-sm font-semibold text-gray-900 mb-2">
                🎉 Special Launch Offer
              </h3>
              <p className="text-xs text-gray-600 mb-3">
                Start with our Professional plan for just $99/month
                <br />
                <span className="font-medium text-green-600">30-day free trial included</span>
              </p>
              <div className="grid grid-cols-3 gap-3 text-xs">
                <div className="text-center">
                  <div className="font-medium text-gray-900">Starter</div>
                  <div className="text-gray-600">$29/month</div>
                  <div className="text-gray-500">Up to 5 addresses</div>
                </div>
                <div className="text-center border-l border-r border-gray-200 px-3">
                  <div className="font-medium text-purple-600">Professional</div>
                  <div className="text-purple-600">$99/month</div>
                  <div className="text-gray-500">Up to 50 addresses</div>
                </div>
                <div className="text-center">
                  <div className="font-medium text-gray-900">Enterprise</div>
                  <div className="text-gray-600">$299/month</div>
                  <div className="text-gray-500">Unlimited addresses</div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Trust Indicators */}
        <div className="mt-6 text-center text-xs text-gray-500">
          <p>
            🔒 Your data is encrypted and secured with enterprise-grade security.
            <br />
            🛡️ SOC 2 Type II certified • 99.9% uptime SLA • GDPR compliant
            <br />
            🏆 Trusted by 500+ enterprises managing $2B+ in digital assets
          </p>
        </div>
      </div>
    </div>
  )
}

export default RegisterPage
