# Mento Protocol Monitor - Production Integration

## Overview
This dashboard provides real-time monitoring of the Mento Protocol stablecoins on the Celo blockchain. It integrates directly with blockchain data sources to display live metrics, analytics, and alerts.

## Features

### Real-Time Data Integration
- **Live Blockchain Data**: Direct integration with Celo RPC nodes
- **Automatic Failover**: Multiple RPC endpoints with automatic switching
- **30-Second Refresh**: Configurable auto-refresh intervals
- **CORS Proxy Support**: Built-in solutions for cross-origin requests

### Data Sources
1. **Primary**: Celo Forno RPC (`https://forno.celo.org`)
2. **Backup**: Ankr RPC (`https://rpc.ankr.com/celo`)
3. **Explorer API**: Blockscout API for transaction data
4. **Price Feeds**: CoinGecko API for CELO/USD pricing

### Monitored Metrics
- Total Protocol Value (TVL)
- Reserve Holdings & Collateral Ratios
- Stablecoin Supplies (cUSD, cEUR, cREAL, eXOF, cKES)
- Latest Block Information
- Transaction Volumes
- Historical Analytics with Charts

## Technical Architecture

### Core Modules
1. **mento-api-integration.js**: Main API integration handling all blockchain queries
2. **mento-charts.js**: Chart.js integration for data visualization
3. **cors-proxy-config.js**: CORS proxy configuration for API access

### Libraries Used
- **Web3.js v4.3.0**: Ethereum/Celo blockchain interaction
- **Chart.js v4.4.1**: Data visualization
- **No framework dependencies**: Pure JavaScript for maximum compatibility

## API Integration Details

### Contract Addresses
```javascript
contracts: {
    cUSD: '0x765de816845861e75a25fca122bb6898b8b1282a',
    cEUR: '0xd8763cba276a3738e6de85b4b3bf5fded6d6ca73',
    cREAL: '0xe8537a3d056DA446677B9E9d6c5dB704EaAb4787',
    eXOF: '0x73a210637f6F6B7005512677Ba6B3C96bb4AA44B',
    cKES: '0x456a3D042C0DbD3db53D5489e98dFb038553B0d0'
}
```

### API Endpoints
- **Token Supplies**: ERC20 `totalSupply()` method calls
- **Block Data**: `eth_getBlockByNumber` RPC calls
- **Token Transfers**: Blockscout API `/v2/tokens/{address}/transfers`
- **Price Data**: CoinGecko `/api/v3/simple/price`

## Deployment Instructions

### For ICP/Juno Deployment
1. Deploy all files to your Juno satellite
2. No server-side configuration needed (pure frontend)
3. Update CORS proxy settings if needed

### For Traditional Web Hosting
1. Upload all files to your web server
2. Ensure HTTPS is enabled (required for Web3)
3. Configure CORS headers if hosting API proxy

### Environment Configuration
No environment variables needed - all configuration is in the JavaScript files.

### Optional: Backend Proxy
For production deployments, consider implementing a backend proxy to:
- Cache blockchain queries
- Handle CORS without public proxies
- Add authentication/rate limiting
- Reduce direct blockchain calls

Example backend endpoints to implement:
```
GET /api/blockchain-proxy/block/latest
GET /api/blockchain-proxy/token/supply?address={address}
GET /api/blockchain-proxy/mento/reserves
```

## Error Handling

The dashboard includes comprehensive error handling:
- Automatic RPC endpoint failover
- Cached data fallback when APIs fail
- User-friendly error messages
- Retry mechanisms for failed requests

## Performance Optimizations

- **Caching**: 15-60 second cache for different data types
- **Batch Requests**: Multiple token supplies fetched in parallel
- **Lazy Loading**: Charts initialized only when viewed
- **Minimal Dependencies**: < 500KB total JavaScript

## Security Considerations

1. **No Private Keys**: Dashboard is read-only, no wallet integration
2. **Public Data Only**: All displayed data is publicly available on-chain
3. **CORS Proxy**: Use your own proxy in production for security
4. **Rate Limiting**: Implement on backend proxy to prevent abuse

## Customization

### Refresh Intervals
Edit in `mento-api-integration.js`:
```javascript
refreshIntervals: {
    prices: 30000,      // 30 seconds
    blocks: 15000,      // 15 seconds
    reserves: 60000,    // 1 minute
    supplies: 300000    // 5 minutes
}
```

### Add New Tokens
Add to contracts object in `API_CONFIG`:
```javascript
contracts: {
    // ... existing tokens
    newToken: '0x...' // Add new token address
}
```

### Styling
All styles use CSS variables defined in the HTML. Modify the `:root` section to change colors, spacing, etc.

## Troubleshooting

### CORS Errors
- Use the included CORS proxy configuration
- Deploy your own backend proxy for production
- Check browser console for specific endpoints failing

### Web3 Connection Issues
- Dashboard will fall back to Blockscout API
- Check RPC endpoint status
- Verify network connectivity

### Missing Data
- Some data may take time to load initially
- Check browser console for API errors
- Verify contract addresses are correct

## Future Enhancements

Potential additions for production:
1. WebSocket connections for real-time updates
2. Historical data storage and trending
3. Alert notifications via email/Discord
4. Multi-chain support (Ethereum, Polygon)
5. Governance proposal monitoring
6. Liquidity pool analytics

## Support

For issues or questions:
- Check browser console for detailed error messages
- Verify all files are loaded correctly
- Ensure HTTPS is used for production deployments
- Review CORS proxy configuration

## License

This monitoring dashboard is part of the Nuru AI partnership with Mento Protocol. See main project license for details.
