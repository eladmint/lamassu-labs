# Mento Protocol Monitor Dashboard

Professional real-time monitoring dashboard for Mento Protocol stablecoins with advanced analytics and AI-powered insights.

## 🚀 Features

- **Real-Time Monitoring**: Live blockchain data updated every 30 seconds
- **Advanced Analytics**: Growth tracking, volatility analysis, market share insights
- **Reserve Monitoring**: $56M+ in live reserve tracking
- **Professional UI**: Enterprise-grade dashboard with responsive design
- **No Rate Limits**: Direct blockchain access vs API dependencies
- **AI-Powered Alerts**: Intelligent anomaly detection and notifications

## 📊 Live Data

Currently monitoring:
- **$25.6M Total Protocol Value**
- **5 Active Stablecoins** (cUSD, cEUR, cREAL, eXOF, cKES)
- **$56.1M Reserve Holdings**
- **Real-time Celo blockchain integration**

## 🛠 Technology Stack

- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Viem**: Ethereum library for blockchain interaction
- **Lucide React**: Beautiful icons
- **Vercel**: Edge deployment platform

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend Architecture                     │
├─────────────────────────────────────────────────────────────┤
│  [Next.js App] ←→ [Real-time Updates] ←→ [Celo RPC]        │
│        ↓                    ↓                    ↓          │
│  [Dashboard UI] ←→ [Data Processing] ←→ [Blockchain]        │
│        ↓                    ↓                    ↓          │
│  [Analytics] ←→ [Alert System] ←→ [Contract Calls]          │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## 📋 Environment Variables

```env
CELO_RPC_URL=https://forno.celo.org
NEXT_PUBLIC_APP_NAME=Mento Protocol Monitor
NEXT_PUBLIC_POWERED_BY=Nuru AI
```

## 🌐 Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy to Vercel
vercel

# Deploy to production
vercel --prod
```

### Custom Domain Setup

1. Add custom domain in Vercel dashboard
2. Configure DNS records:
   - A record: `185.199.108.153`
   - CNAME record: `cname.vercel-dns.com`

## 📈 Performance

- **Data Latency**: <1 second from blockchain
- **Page Load**: <2 seconds initial load
- **Updates**: Real-time every 30 seconds
- **Uptime**: 99.9% SLA target

## 🔒 Security

- **HTTPS**: All traffic encrypted
- **No Private Keys**: Read-only blockchain access
- **Rate Limiting**: Built-in DDoS protection
- **Input Validation**: All data sanitized

## 📊 Competitive Advantages

| Feature | Mento API | Our Solution |
|---------|-----------|--------------|
| Data Freshness | 1 hour cache | Real-time |
| Rate Limits | Yes | None |
| Uptime | Server dependent | 99.9% SLA |
| Analytics | Basic | AI-powered |
| Alerts | None | Intelligent |

## 🤝 Partnership Integration

This dashboard demonstrates:

1. **Technical Superiority**: Real-time vs hourly cached data
2. **Enterprise Readiness**: Professional UI and reliability
3. **Business Value**: Enhanced transparency and trust
4. **Competitive Edge**: No other protocol has this level of monitoring

## 📞 Contact

**Nuru AI - Lamassu Labs**
- Technical Lead: [Technical Contact]
- Partnership Lead: [Partnership Contact]
- Business Development: [Business Contact]

## 📄 License

MIT License - See LICENSE file for details

---

**Powered by Nuru AI** | **Built for Mento Protocol Partnership** | **Enterprise-Grade Monitoring**
