/**
 * Treasury Monitor Login Page
 * Enterprise login interface using design system components
 */

import React, { useState } from 'react'
import { useRouter } from 'next/router'
import { LoginForm } from '../../../design-system/components/auth/login-form'
import { Alert, AlertDescription } from '../../../design-system/components/ui/alert'
import { Card, CardContent } from '../../../design-system/components/ui/card'
import { useAuth } from '../hooks/useAuth'

const LoginPage: React.FC = () => {
  const router = useRouter()
  const { login, loading } = useAuth()
  const [error, setError] = useState<string | null>(null)

  const handleLogin = async (credentials: { email: string; password: string }) => {
    try {
      setError(null)
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Login failed')
      }

      const data = await response.json()

      // Store tokens
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)

      // Update auth context
      login(data.user, data.access_token)

      // Redirect to dashboard
      router.push('/dashboard')

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed')
    }
  }

  const handleForgotPassword = () => {
    router.push('/auth/forgot-password')
  }

  const handleSignUp = () => {
    router.push('/auth/register')
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
            Treasury Monitor
          </h1>
          <p className="text-gray-600">
            Professional Cardano treasury monitoring
          </p>
        </div>

        {/* Login Form */}
        <LoginForm
          onSubmit={handleLogin}
          loading={loading}
          error={error}
          onForgotPassword={handleForgotPassword}
          onSignUp={handleSignUp}
          variant="enterprise"
        />

        {/* Enterprise Features */}
        <Card className="mt-6 bg-gradient-to-r from-blue-50 to-purple-50 border-blue-200">
          <CardContent className="pt-6">
            <h3 className="text-sm font-semibold text-gray-900 mb-3">
              Enterprise Features
            </h3>
            <ul className="space-y-2 text-sm text-gray-700">
              <li className="flex items-center">
                <div className="w-1.5 h-1.5 bg-purple-500 rounded-full mr-2" />
                Real-time treasury monitoring
              </li>
              <li className="flex items-center">
                <div className="w-1.5 h-1.5 bg-purple-500 rounded-full mr-2" />
                Multi-signature wallet support
              </li>
              <li className="flex items-center">
                <div className="w-1.5 h-1.5 bg-purple-500 rounded-full mr-2" />
                Advanced alerting system
              </li>
              <li className="flex items-center">
                <div className="w-1.5 h-1.5 bg-purple-500 rounded-full mr-2" />
                Compliance reporting
              </li>
            </ul>
          </CardContent>
        </Card>

        {/* Security Notice */}
        <div className="mt-6 text-center text-xs text-gray-500">
          <p>
            🔒 Your data is encrypted and secured with enterprise-grade security.
            <br />
            This application is protected by 2FA and audit logging.
          </p>
        </div>
      </div>
    </div>
  )
}

export default LoginPage
