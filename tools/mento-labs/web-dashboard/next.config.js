/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  typescript: {
    ignoreBuildErrors: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  experimental: {
    serverComponentsExternalPackages: ['viem']
  },
  env: {
    CELO_RPC_URL: process.env.CELO_RPC_URL || 'https://forno.celo.org',
    NEXT_PUBLIC_APP_NAME: 'Mento Monitor',
    NEXT_PUBLIC_POWERED_BY: 'Nuru AI'
  }
}

module.exports = nextConfig
