/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,

  // API proxy for development
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8080/api/:path*', // Treasury Monitor API
      },
    ]
  },

  // Environment variables
  env: {
    CUSTOM_KEY: 'my-value',
  },

  // Image optimization
  images: {
    domains: ['localhost'],
    formats: ['image/webp', 'image/avif'],
  },

  // Experimental features
  experimental: {
    appDir: false, // Using pages directory
    serverComponentsExternalPackages: [],
  },

  // Build optimization
  compiler: {
    removeConsole: process.env.NODE_ENV === 'production',
  },

  // TypeScript configuration
  typescript: {
    // Dangerously allow production builds to successfully complete even if
    // your project has type errors.
    ignoreBuildErrors: false,
  },

  // ESLint configuration
  eslint: {
    // Warning: This allows production builds to successfully complete even if
    // your project has ESLint errors.
    ignoreDuringBuilds: false,
  },

  // Output configuration for production
  output: 'standalone',

  // Webpack configuration
  webpack: (config, { buildId, dev, isServer, defaultLoaders, nextRuntime, webpack }) => {
    // Add custom webpack configurations here

    // Alias for design system imports
    config.resolve.alias = {
      ...config.resolve.alias,
      '@design-system': path.resolve(__dirname, '../../../design-system'),
      '@components': path.resolve(__dirname, 'components'),
      '@utils': path.resolve(__dirname, 'utils'),
      '@hooks': path.resolve(__dirname, 'hooks'),
      '@pages': path.resolve(__dirname, 'pages'),
    }

    return config
  },

  // Headers for security
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=()',
          },
        ],
      },
    ]
  },

  // Redirects
  async redirects() {
    return [
      {
        source: '/',
        destination: '/dashboard',
        permanent: false,
      },
    ]
  },
}

const path = require('path')

module.exports = nextConfig
