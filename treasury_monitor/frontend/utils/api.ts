/**
 * Treasury Monitor API Client
 * Centralized API utilities with authentication and error handling
 */

export class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public code?: string
  ) {
    super(message)
    this.name = 'APIError'
  }
}

export interface APIResponse<T = any> {
  data: T
  status: number
  message?: string
}

class APIClient {
  private baseURL: string
  private defaultHeaders: Record<string, string>

  constructor(baseURL: string = '/api') {
    this.baseURL = baseURL
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    }
  }

  private getAuthToken(): string | null {
    if (typeof window === 'undefined') return null
    return localStorage.getItem('access_token')
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<APIResponse<T>> {
    const token = this.getAuthToken()
    const url = `${this.baseURL}${endpoint}`

    const headers = {
      ...this.defaultHeaders,
      ...options.headers,
    }

    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      })

      let data: any
      const contentType = response.headers.get('content-type')

      if (contentType && contentType.includes('application/json')) {
        data = await response.json()
      } else {
        data = await response.text()
      }

      if (!response.ok) {
        throw new APIError(
          data.detail || data.message || `Request failed with status ${response.status}`,
          response.status,
          data.code
        )
      }

      return {
        data,
        status: response.status,
        message: data.message,
      }
    } catch (error) {
      if (error instanceof APIError) {
        throw error
      }

      throw new APIError(
        error instanceof Error ? error.message : 'Network request failed',
        0
      )
    }
  }

  // HTTP methods
  async get<T>(endpoint: string, params?: Record<string, any>): Promise<APIResponse<T>> {
    const url = params ? `${endpoint}?${new URLSearchParams(params)}` : endpoint
    return this.request<T>(url, { method: 'GET' })
  }

  async post<T>(endpoint: string, data?: any): Promise<APIResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  async put<T>(endpoint: string, data?: any): Promise<APIResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    })
  }

  async delete<T>(endpoint: string): Promise<APIResponse<T>> {
    return this.request<T>(endpoint, { method: 'DELETE' })
  }

  // Authentication methods
  async login(email: string, password: string) {
    return this.post('/auth/login', { email, password })
  }

  async register(userData: {
    email: string
    password: string
    first_name?: string
    last_name?: string
    company?: string
  }) {
    return this.post('/auth/register', userData)
  }

  async logout() {
    const refreshToken = localStorage.getItem('refresh_token')
    if (refreshToken) {
      await this.post('/auth/logout', { refresh_token: refreshToken })
    }
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  async refreshToken() {
    const refreshToken = localStorage.getItem('refresh_token')
    if (!refreshToken) {
      throw new APIError('No refresh token available', 401)
    }

    const response = await this.post('/auth/refresh', { refresh_token: refreshToken })

    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token)
    }

    if (response.data.refresh_token) {
      localStorage.setItem('refresh_token', response.data.refresh_token)
    }

    return response
  }

  async getProfile() {
    return this.get('/auth/profile')
  }

  async updateProfile(data: {
    first_name?: string
    last_name?: string
    company?: string
  }) {
    return this.put('/auth/profile', data)
  }

  // Billing methods
  async getSubscriptionPlans() {
    return this.get('/billing/plans')
  }

  async createSubscription(planId: string, paymentMethodId?: string, trialDays?: number) {
    return this.post('/billing/subscribe', {
      plan_id: planId,
      payment_method_id: paymentMethodId,
      trial_days: trialDays,
    })
  }

  async getSubscription() {
    return this.get('/billing/subscription')
  }

  async cancelSubscription(immediate: boolean = false) {
    return this.post('/billing/subscription/cancel', { immediate })
  }

  async reactivateSubscription() {
    return this.post('/billing/subscription/reactivate')
  }

  async getPaymentHistory(limit: number = 10) {
    return this.get('/billing/history', { limit })
  }

  // API Key methods
  async createAPIKey(data: {
    name?: string
    permissions?: string[]
    expires_days?: number
  }) {
    return this.post('/api-keys', data)
  }

  async getAPIKeys() {
    return this.get('/api-keys')
  }

  async revokeAPIKey(keyId: string) {
    return this.delete(`/api-keys/${keyId}`)
  }

  async getAPIUsage(days: number = 30) {
    return this.get('/api-keys/usage', { days })
  }

  // Treasury monitoring methods
  async monitorAddresses(addresses: string[], durationMinutes: number = 1) {
    return this.post('/monitor', {
      addresses,
      duration_minutes: durationMinutes,
    })
  }

  // Admin methods
  async getUsers(limit: number = 50, offset: number = 0) {
    return this.get('/admin/users', { limit, offset })
  }
}

// Export singleton instance
export const api = new APIClient()

// Export types
export type { APIResponse }

// Utility functions
export const handleAPIError = (error: unknown): string => {
  if (error instanceof APIError) {
    return error.message
  }

  if (error instanceof Error) {
    return error.message
  }

  return 'An unexpected error occurred'
}

export const isAuthError = (error: unknown): boolean => {
  return error instanceof APIError && (error.status === 401 || error.status === 403)
}

export default api
