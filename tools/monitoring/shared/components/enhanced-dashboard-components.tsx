import React, { useState, useEffect, useCallback, memo, lazy, Suspense } from 'react'
import {
  Shield,
  Activity,
  TrendingUp,
  Users,
  AlertTriangle,
  Crown,
  Settings,
  Loader2,
  CheckCircle,
  XCircle,
  Info,
  RefreshCw
} from 'lucide-react'

// Enhanced types following UX Guidelines
interface AccessibilityProps {
  'aria-label'?: string
  'aria-describedby'?: string
  'aria-expanded'?: boolean
  'aria-controls'?: string
  role?: string
}

interface LoadingState {
  isLoading: boolean
  loadingText?: string
  error?: string | null
}

interface HapticFeedback {
  type?: 'light' | 'medium' | 'heavy'
  enabled?: boolean
}

// Enhanced Button Component following UX Guidelines
interface EnhancedButtonProps extends AccessibilityProps, HapticFeedback {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost'
  size?: 'touch' | 'default' | 'lg' | 'sm'
  loading?: boolean
  loadingText?: string
  disabled?: boolean
  onClick?: () => void
  children: React.ReactNode
  className?: string
}

export const EnhancedButton = memo<EnhancedButtonProps>(({
  variant = 'default',
  size = 'default',
  loading = false,
  loadingText,
  disabled = false,
  onClick,
  children,
  className = '',
  type = 'light',
  enabled: hapticEnabled = true,
  ...accessibilityProps
}) => {
  const handleClick = useCallback(() => {
    // Haptic feedback for mobile/touch devices
    if (hapticEnabled && 'vibrate' in navigator) {
      const vibrationPattern = {
        light: [10],
        medium: [20],
        heavy: [50]
      }
      navigator.vibrate(vibrationPattern[type])
    }

    if (onClick && !loading && !disabled) {
      onClick()
    }
  }, [onClick, loading, disabled, hapticEnabled, type])

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault()
      handleClick()
    }
  }, [handleClick])

  const baseClasses = `
    inline-flex items-center justify-center gap-2 font-medium rounded-lg
    transition-all duration-200 focus:outline-none focus:ring-2
    focus:ring-primary-500 focus:ring-offset-2 disabled:opacity-50
    disabled:cursor-not-allowed
  `

  const variantClasses = {
    primary: 'bg-primary-500 text-white hover:bg-primary-600 active:bg-primary-700',
    secondary: 'bg-accent-500 text-white hover:bg-accent-600 active:bg-accent-700',
    outline: 'border-2 border-primary-500 text-primary-500 hover:bg-primary-50 active:bg-primary-100',
    ghost: 'text-primary-500 hover:bg-primary-50 active:bg-primary-100'
  }

  const sizeClasses = {
    touch: 'px-6 py-3 text-base min-h-[44px]', // 44px minimum for touch
    default: 'px-4 py-2 text-sm min-h-[40px]',
    lg: 'px-6 py-3 text-base min-h-[48px]',
    sm: 'px-3 py-1.5 text-xs min-h-[32px]'
  }

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      disabled={disabled || loading}
      {...accessibilityProps}
    >
      {loading && <Loader2 className="w-4 h-4 animate-spin" />}
      {loading ? (loadingText || 'Loading...') : children}
    </button>
  )
})

// Enhanced Card Component with accessibility
interface EnhancedCardProps extends AccessibilityProps {
  variant?: 'default' | 'interactive'
  onClick?: () => void
  children: React.ReactNode
  className?: string
}

export const EnhancedCard = memo<EnhancedCardProps>(({
  variant = 'default',
  onClick,
  children,
  className = '',
  ...accessibilityProps
}) => {
  const baseClasses = `
    bg-white rounded-xl border border-gray-200 shadow-sm
    transition-all duration-200
  `

  const variantClasses = {
    default: '',
    interactive: `
      cursor-pointer hover:shadow-lg hover:-translate-y-1
      focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2
    `
  }

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (variant === 'interactive' && (e.key === 'Enter' || e.key === ' ')) {
      e.preventDefault()
      onClick?.()
    }
  }, [variant, onClick])

  const CardComponent = variant === 'interactive' ? 'button' : 'div'

  return (
    <CardComponent
      className={`${baseClasses} ${variantClasses[variant]} ${className}`}
      onClick={onClick}
      onKeyDown={handleKeyDown}
      tabIndex={variant === 'interactive' ? 0 : undefined}
      {...accessibilityProps}
    >
      {children}
    </CardComponent>
  )
})

// Enhanced Skeleton Component for loading states
interface SkeletonProps {
  className?: string
  width?: string | number
  height?: string | number
}

export const Skeleton = memo<SkeletonProps>(({ className = '', width, height }) => {
  const style = {
    width: typeof width === 'number' ? `${width}px` : width,
    height: typeof height === 'number' ? `${height}px` : height,
  }

  return (
    <div
      className={`animate-pulse bg-gray-200 rounded ${className}`}
      style={style}
      role="status"
      aria-label="Loading content"
    >
      <span className="sr-only">Loading...</span>
    </div>
  )
})

// Toast Notification System
interface ToastProps {
  variant: 'success' | 'error' | 'warning' | 'info'
  title: string
  description?: string
  duration?: number
  action?: {
    label: string
    onClick: () => void
  }
  onClose: () => void
}

export const Toast = memo<ToastProps>(({
  variant,
  title,
  description,
  duration = 3000,
  action,
  onClose
}) => {
  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(onClose, duration)
      return () => clearTimeout(timer)
    }
  }, [duration, onClose])

  const variantConfig = {
    success: {
      icon: CheckCircle,
      className: 'bg-green-50 border-green-200 text-green-800'
    },
    error: {
      icon: XCircle,
      className: 'bg-red-50 border-red-200 text-red-800'
    },
    warning: {
      icon: AlertTriangle,
      className: 'bg-yellow-50 border-yellow-200 text-yellow-800'
    },
    info: {
      icon: Info,
      className: 'bg-blue-50 border-blue-200 text-blue-800'
    }
  }

  const config = variantConfig[variant]
  const Icon = config.icon

  return (
    <div
      className={`
        fixed bottom-4 right-4 max-w-md p-4 border rounded-lg shadow-lg
        animate-in slide-in-from-bottom-2 ${config.className}
      `}
      role="alert"
      aria-live="polite"
    >
      <div className="flex items-start gap-3">
        <Icon className="w-5 h-5 flex-shrink-0 mt-0.5" />
        <div className="flex-1">
          <h4 className="font-medium">{title}</h4>
          {description && (
            <p className="text-sm opacity-90 mt-1">{description}</p>
          )}
          {action && (
            <button
              onClick={action.onClick}
              className="text-sm underline font-medium mt-2 hover:no-underline focus:outline-none focus:ring-2 focus:ring-current focus:ring-offset-2"
            >
              {action.label}
            </button>
          )}
        </div>
        <button
          onClick={onClose}
          className="text-lg leading-none hover:opacity-70 focus:outline-none focus:ring-2 focus:ring-current focus:ring-offset-2"
          aria-label="Close notification"
        >
          ×
        </button>
      </div>
    </div>
  )
})

// Enhanced Form Components
interface FormFieldProps extends AccessibilityProps {
  name: string
  label: string
  error?: string
  description?: string
  required?: boolean
  children: React.ReactNode
}

export const FormField = memo<FormFieldProps>(({
  name,
  label,
  error,
  description,
  required = false,
  children,
  ...accessibilityProps
}) => {
  const fieldId = `field-${name}`
  const errorId = error ? `${fieldId}-error` : undefined
  const descriptionId = description ? `${fieldId}-description` : undefined

  return (
    <div className="space-y-2">
      <label
        htmlFor={fieldId}
        className="block text-sm font-medium text-gray-700"
      >
        {label}
        {required && <span className="text-red-500 ml-1" aria-label="required">*</span>}
      </label>

      <div>
        {React.cloneElement(children as React.ReactElement, {
          id: fieldId,
          'aria-describedby': [descriptionId, errorId].filter(Boolean).join(' ') || undefined,
          'aria-invalid': !!error,
          ...accessibilityProps
        })}
      </div>

      {description && (
        <p id={descriptionId} className="text-sm text-gray-500">
          {description}
        </p>
      )}

      {error && (
        <p id={errorId} className="text-sm text-red-600" role="alert">
          {error}
        </p>
      )}
    </div>
  )
})

// Enhanced Input Component
interface EnhancedInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  invalid?: boolean
}

export const EnhancedInput = memo<EnhancedInputProps>(({
  invalid = false,
  className = '',
  ...props
}) => {
  const baseClasses = `
    w-full px-3 py-2 border rounded-lg text-sm
    focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent
    disabled:opacity-50 disabled:cursor-not-allowed
    transition-colors duration-200
  `

  const stateClasses = invalid
    ? 'border-red-300 bg-red-50'
    : 'border-gray-300 bg-white hover:border-gray-400'

  return (
    <input
      className={`${baseClasses} ${stateClasses} ${className}`}
      {...props}
    />
  )
})

// Focus Trap Component for Modals
interface FocusTrapProps {
  children: React.ReactNode
  disabled?: boolean
}

export const FocusTrap = memo<FocusTrapProps>(({ children, disabled = false }) => {
  const containerRef = React.useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (disabled) return

    const container = containerRef.current
    if (!container) return

    const focusableElements = container.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    )

    const firstElement = focusableElements[0] as HTMLElement
    const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement

    const handleTabKey = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return

      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          e.preventDefault()
          lastElement?.focus()
        }
      } else {
        if (document.activeElement === lastElement) {
          e.preventDefault()
          firstElement?.focus()
        }
      }
    }

    container.addEventListener('keydown', handleTabKey)
    firstElement?.focus()

    return () => {
      container.removeEventListener('keydown', handleTabKey)
    }
  }, [disabled])

  return (
    <div ref={containerRef}>
      {children}
    </div>
  )
})

// Enhanced Modal Component
interface ModalProps extends AccessibilityProps {
  isOpen: boolean
  onClose: () => void
  title: string
  children: React.ReactNode
  size?: 'sm' | 'md' | 'lg' | 'xl'
}

export const Modal = memo<ModalProps>(({
  isOpen,
  onClose,
  title,
  children,
  size = 'md',
  ...accessibilityProps
}) => {
  const sizeClasses = {
    sm: 'max-w-md',
    md: 'max-w-lg',
    lg: 'max-w-2xl',
    xl: 'max-w-4xl'
  }

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = 'unset'
    }

    return () => {
      document.body.style.overflow = 'unset'
    }
  }, [isOpen])

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose()
      }
    }

    if (isOpen) {
      document.addEventListener('keydown', handleEscape)
    }

    return () => {
      document.removeEventListener('keydown', handleEscape)
    }
  }, [isOpen, onClose])

  if (!isOpen) return null

  return (
    <div
      className="fixed inset-0 z-50 overflow-y-auto"
      role="dialog"
      aria-modal="true"
      aria-labelledby="modal-title"
      {...accessibilityProps}
    >
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Modal Content */}
      <div className="flex min-h-full items-center justify-center p-4">
        <div className={`
          relative bg-white rounded-lg shadow-xl w-full ${sizeClasses[size]}
          transform transition-all animate-in zoom-in-95 duration-200
        `}>
          <FocusTrap>
            {/* Header */}
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <h2 id="modal-title" className="text-lg font-semibold text-gray-900">
                {title}
              </h2>
              <button
                onClick={onClose}
                className="text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 rounded"
                aria-label="Close modal"
              >
                <XCircle className="w-6 h-6" />
              </button>
            </div>

            {/* Content */}
            <div className="p-6">
              {children}
            </div>
          </FocusTrap>
        </div>
      </div>
    </div>
  )
})

// Progressive Disclosure Component
interface ProgressiveDisclosureProps {
  summary: string
  children: React.ReactNode
  defaultOpen?: boolean
}

export const ProgressiveDisclosure = memo<ProgressiveDisclosureProps>(({
  summary,
  children,
  defaultOpen = false
}) => {
  const [isOpen, setIsOpen] = useState(defaultOpen)

  return (
    <details
      className="group"
      open={isOpen}
      onToggle={(e) => setIsOpen((e.target as HTMLDetailsElement).open)}
    >
      <summary
        className="cursor-pointer list-none flex items-center justify-between p-3 hover:bg-gray-50 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
        role="button"
        aria-expanded={isOpen}
      >
        <span className="font-medium">{summary}</span>
        <TrendingUp
          className={`w-4 h-4 transition-transform duration-200 ${
            isOpen ? 'rotate-90' : ''
          }`}
        />
      </summary>

      <div className="pt-2 pb-3 px-3 animate-in slide-in-from-top-2 duration-200">
        {children}
      </div>
    </details>
  )
})

// Lazy Loading Wrapper
interface LazyComponentProps {
  fallback?: React.ReactNode
  children: React.ReactNode
}

export const LazyComponent = memo<LazyComponentProps>(({
  fallback = <Skeleton className="h-32 w-full" />,
  children
}) => {
  return (
    <Suspense fallback={fallback}>
      {children}
    </Suspense>
  )
})

// Performance monitoring hook
export const usePerformanceMonitoring = () => {
  useEffect(() => {
    // Monitor Core Web Vitals
    const observer = new PerformanceObserver((list) => {
      list.getEntries().forEach((entry) => {
        switch (entry.entryType) {
          case 'largest-contentful-paint':
            console.log('LCP:', entry.startTime)
            break
          case 'first-input':
            console.log('FID:', (entry as any).processingStart - entry.startTime)
            break
          case 'layout-shift':
            console.log('CLS:', (entry as any).value)
            break
        }
      })
    })

    observer.observe({ entryTypes: ['largest-contentful-paint', 'first-input', 'layout-shift'] })

    return () => observer.disconnect()
  }, [])
}

// Analytics tracking hook
export const useAnalytics = () => {
  const trackInteraction = useCallback((action: string, context: Record<string, any> = {}) => {
    // Mock analytics tracking - replace with real implementation
    console.log('Analytics:', {
      action,
      context,
      timestamp: Date.now(),
      viewport: {
        width: window.innerWidth,
        height: window.innerHeight
      }
    })
  }, [])

  const trackPageView = useCallback((page: string) => {
    trackInteraction('Page View', { page })
  }, [trackInteraction])

  return { trackInteraction, trackPageView }
}
