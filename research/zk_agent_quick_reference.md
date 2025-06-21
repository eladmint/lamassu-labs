# ZK Professional Agents: Quick Reference Guide

## One-Line Pitches

**PayRadar**: "Glassdoor with real salaries that nobody can trace to you"

**GhostConsult**: "Uber for anonymous expertise - FAANG engineers help startups without getting fired"

**CompetitorWatch**: "Split the cost of competitive intelligence 10 ways without revealing what you track"

**DealRoom Ghost**: "Do M&A due diligence without opening the kimono to competitors"

**R&D Alliance**: "Share what doesn't work in research without revealing what you're building"

## Build Order & Rationale

### 1️⃣ PayRadar (Month 1-2)
- **Why First**: Easiest UX, viral growth, immediate value
- **Complexity**: ⭐⭐ (Simple ZK proofs)
- **Market Risk**: ⭐ (Everyone wants salary data)
- **Revenue Speed**: 💰💰💰 (Freemium from day 1)

### 2️⃣ GhostConsult (Month 3-4)
- **Why Second**: High revenue per transaction, builds on PayRadar trust
- **Complexity**: ⭐⭐⭐ (Escrow + messaging)
- **Market Risk**: ⭐⭐ (Need two-sided marketplace)
- **Revenue Speed**: 💰💰💰💰 ($1-50k transactions)

### 3️⃣ CompetitorWatch (Month 5-6)
- **Why Third**: Enterprise sales, network effects
- **Complexity**: ⭐⭐⭐⭐ (Distributed systems)
- **Market Risk**: ⭐⭐⭐ (Requires critical mass)
- **Revenue Speed**: 💰💰 (Long sales cycle)

## Quick Technical Decisions

**ZK Library**: SnarkJS (browser compatible, 3-second proofs)

**Blockchain**: Polygon (cheap verification, EVM compatible)

**Frontend**: Next.js (SEO + performance)

**Backend**: Node.js + PostgreSQL (familiar stack)

**Deployment**: Vercel + Railway (simple scaling)

## Key Metrics to Track

### PayRadar
- **North Star**: Weekly active salary checkers
- **Health**: % verified vs. unverified users
- **Revenue**: Premium conversion rate
- **Viral**: Referral acceptance rate

### GhostConsult  
- **North Star**: GMV (Gross Merchandise Value)
- **Health**: Consultation completion rate
- **Revenue**: Average transaction size
- **Quality**: Client satisfaction score

### CompetitorWatch
- **North Star**: URLs monitored per pool
- **Health**: Pool participation rate
- **Revenue**: MRR per vertical
- **Value**: Cost savings per company

## Investor FAQ Responses

**"How is this different from Glassdoor?"**
> Glassdoor has stale, unverified data. We have real-time, cryptographically verified salaries. Plus, Glassdoor users fear retaliation - ours are truly anonymous.

**"What if LinkedIn copies you?"**
> They can't. Their whole model depends on real identities. Adding ZK would break their core value prop. Plus, we have 2 years head start on the technology.

**"Is the market big enough?"**
> 50M professionals negotiate salary yearly. At $50/year average, that's $2.5B. Add consulting and B2B, we're looking at $17B TAM.

**"Why will enterprises pay?"**
> CompetitorWatch saves them 90% on intelligence gathering. DealRoom Ghost cuts DD time by 80%. The ROI is immediate and massive.

## Common Objections & Responses

**"Nobody will trust anonymous data"**
> They already do on Blind (5M users). We add cryptographic verification on top.

**"ZK proofs are too complex"**
> Our beta users generate proofs in 3 seconds. It's one click, like posting on Twitter.

**"This enables corporate espionage"**
> Actually the opposite - it reduces espionage by letting companies share non-sensitive insights without revealing strategies.

## PR Hook Lines

- "We helped 1,000 engineers discover they were underpaid"
- "Anonymous Google engineer makes $50k/month consulting for competitors"  
- "10 companies save $4M by pooling competitive intelligence"
- "The $50B of expertise trapped behind non-competes"
- "How zero-knowledge proofs are fixing the gender pay gap"

## Partnership Targets

### Distribution Partners
- **Blind**: 5M anonymous professionals
- **Hacker News**: Technical early adopters
- **YC**: Startup customers for GhostConsult

### Verification Partners
- **GitHub**: Verify code contributions
- **Google Scholar**: Verify publications
- **Patent Office**: Verify inventions

### Enterprise Partners
- **AWS**: Secure enclaves for computation
- **Polygon**: Blockchain verification
- **Signal**: Encrypted messaging

## Emergency Pivots

If PayRadar doesn't work:
→ Pivot to GhostConsult (higher value per user)

If B2C doesn't scale:
→ Focus on B2B CompetitorWatch

If US regulatory issues:
→ Launch in Europe (stronger privacy laws)

If ZK too complex:
→ Use trusted execution environments (Intel SGX)

## Success Celebrations 🎉

- First verified salary: Team dinner
- 1,000 users: Champagne
- First premium subscriber: Ring bell
- $10k MRR: Team offsite
- First enterprise deal: Founder tattoos
- Series A: Two-week vacation

## Remember

**The Mission**: Unlock $50B of trapped professional value through privacy

**The Insight**: Privacy enables sharing, not prevents it

**The Principle**: Don't sell privacy, sell superpowers

**The Goal**: "PayRadar" becomes a verb by 2027