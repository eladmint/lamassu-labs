/**
 * Authentication hook for Treasury Monitor
 * Manages user authentication state and JWT tokens
 */

import { useState, useEffect, useContext, createContext, ReactNode } from 'react'
import { useRouter } from 'next/router'

interface User {
  id: string
  email: string
  first_name?: string
  last_name?: string
  company?: string
  is_active: boolean
  created_at: string
  last_login?: string
}

interface AuthContextType {
  user: User | null
  token: string | null
  loading: boolean
  login: (user: User, token: string) => void
  logout: () => void
  refreshToken: () => Promise<boolean>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    // Check for stored tokens on mount
    const storedToken = localStorage.getItem('access_token')
    const storedRefreshToken = localStorage.getItem('refresh_token')

    if (storedToken) {
      // Verify token and get user data
      verifyToken(storedToken)
    } else {
      setLoading(false)
    }
  }, [])

  const verifyToken = async (accessToken: string) => {
    try {
      const response = await fetch('/api/auth/profile', {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        const userData = await response.json()
        setUser(userData)
        setToken(accessToken)
      } else {
        // Token invalid, try to refresh
        const refreshed = await refreshToken()
        if (!refreshed) {
          // Refresh failed, clear tokens
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
        }
      }
    } catch (error) {
      console.error('Token verification failed:', error)
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    } finally {
      setLoading(false)
    }
  }

  const login = (userData: User, accessToken: string) => {
    setUser(userData)
    setToken(accessToken)
    localStorage.setItem('access_token', accessToken)
  }

  const logout = async () => {
    const refreshToken = localStorage.getItem('refresh_token')

    if (refreshToken) {
      try {
        await fetch('/api/auth/logout', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ refresh_token: refreshToken }),
        })
      } catch (error) {
        console.error('Logout request failed:', error)
      }
    }

    setUser(null)
    setToken(null)
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    router.push('/login')
  }

  const refreshToken = async (): Promise<boolean> => {
    const storedRefreshToken = localStorage.getItem('refresh_token')

    if (!storedRefreshToken) {
      return false
    }

    try {
      const response = await fetch('/api/auth/refresh', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh_token: storedRefreshToken }),
      })

      if (response.ok) {
        const data = await response.json()
        setToken(data.access_token)
        localStorage.setItem('access_token', data.access_token)

        if (data.refresh_token) {
          localStorage.setItem('refresh_token', data.refresh_token)
        }

        return true
      } else {
        return false
      }
    } catch (error) {
      console.error('Token refresh failed:', error)
      return false
    }
  }

  const contextValue: AuthContextType = {
    user,
    token,
    loading,
    login,
    logout,
    refreshToken,
  }

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

// Higher-order component for protected routes
export const withAuth = <P extends object>(WrappedComponent: React.ComponentType<P>) => {
  const AuthenticatedComponent = (props: P) => {
    const { user, loading } = useAuth()
    const router = useRouter()

    useEffect(() => {
      if (!loading && !user) {
        router.push('/login')
      }
    }, [user, loading, router])

    if (loading) {
      return (
        <div className="min-h-screen bg-gradient-to-br from-purple-50 to-purple-100 flex items-center justify-center">
          <div className="text-center">
            <div className="w-12 h-12 bg-purple-600 rounded-lg flex items-center justify-center mb-4 mx-auto animate-pulse">
              <span className="text-white text-xl font-bold">₳</span>
            </div>
            <p className="text-gray-600">Loading...</p>
          </div>
        </div>
      )
    }

    if (!user) {
      return null // Router will handle redirect
    }

    return <WrappedComponent {...props} />
  }

  return AuthenticatedComponent
}

export default useAuth
