import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Mento Protocol Monitor - Real-Time Stablecoin Analytics',
  description: 'Professional monitoring dashboard for Mento Protocol stablecoins with real-time blockchain data, AI-powered insights, and advanced analytics. Powered by Nuru AI.',
  keywords: 'mento, stablecoin, monitoring, blockchain, celo, defi, analytics, real-time',
  authors: [{ name: 'Nuru AI - Lamassu Labs' }],
  openGraph: {
    title: 'Mento Protocol Monitor',
    description: 'Real-time monitoring of Mento Protocol stablecoins with advanced analytics',
    type: 'website',
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-gray-50 text-gray-900`}>
        <div className="min-h-screen">
          {children}
        </div>
      </body>
    </html>
  )
}
