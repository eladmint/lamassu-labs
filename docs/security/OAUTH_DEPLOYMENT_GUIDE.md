# 🔐 OAuth Authentication System Deployment Guide

**Purpose:** This document provides a comprehensive guide for deploying the OAuth authentication system, enabling secure user authentication with various event platforms (Luma, Meetup, Eventbrite) through the Telegram bot interface.

**Audience:** DevOps Engineers, Developers, Security Engineers

**Last Updated:** June 8, 2025 - Updated with new knowledge management framework.

---

**Scope:**
*   ✅ **INCLUDED:**
    *   Overview of the OAuth system architecture and components.
    *   Step-by-step deployment instructions for database, secrets, API, and bot integration.
    *   Configuration details for Google, GitHub, Meetup, and Eventbrite OAuth.
    *   Guidelines for testing the OAuth flow and security features.
    *   Monitoring and troubleshooting tips for OAuth-related issues.
*   ❌ **EXCLUDED (See Related Docs):**
    *   **Detailed Code Implementation:** Refer to specific source code files (e.g., `chatbot_api/auth_routes.py`).
    *   **General API Architecture:** See [architecture/core/API_ARCHITECTURE.md](../architecture/core/API_ARCHITECTURE.md) for overall API design.
    *   **General Security Architecture:** See [architecture/core/SECURITY_ARCHITECTURE.md](../architecture/core/SECURITY_ARCHITECTURE.md) for the broader security framework.

---

**Quick Links & Related Documents:**
*   **Main Knowledge Index:** [KNOWLEDGE_INDEX.md](../../KNOWLEDGE_INDEX.md) - The central entry point for all project knowledge.
*   **For DevOps:** [FOR_DEVOPS.md](FOR_DEVOPS.md) - Curated documentation for DevOps.
*   **API Architecture:** [architecture/core/API_ARCHITECTURE.md](../architecture/core/API_ARCHITECTURE.md) - Detailed FastAPI backend specifications.
*   **Database Architecture:** [architecture/core/DATABASE_ARCHITECTURE.md](../architecture/core/DATABASE_ARCHITECTURE.md) - Supabase PostgreSQL architecture.
*   **Security Policy:** [SECURITY.md](SECURITY.md) - Comprehensive security measures.

---

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│  Telegram Bot   │───▶│   FastAPI API    │───▶│   Event Platforms   │
│                 │    │  OAuth Endpoints │    │  (Luma, Meetup,     │
│ OAuth Commands  │    │                  │    │   Eventbrite)       │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   Supabase DB    │
                    │ Encrypted Tokens │
                    └──────────────────┘
```

## Components Implemented

### 1. Database Infrastructure
- **File**: `/scripts/migrations/create_oauth_infrastructure.sql`
- **Tables**:
  - `user_platform_credentials` (encrypted OAuth tokens)
  - `oauth_states` (OAuth flow state management)
  - `user_registrations` (registration audit trail)
- **Security**: Row Level Security (RLS) policies

### 2. OAuth Service
- **File**: `/chatbot_api/registration/oauth_authentication_service.py`
- **Features**:
  - Multi-platform OAuth support (Google, GitHub, Meetup, Eventbrite)
  - Encrypted credential storage using Fernet
  - OAuth state management and validation
  - Platform detection and routing

### 3. FastAPI OAuth Routes
- **File**: `/chatbot_api/auth_routes.py`
- **Endpoints**:
  - `GET /auth/connect/{platform}` - Initiate OAuth flow
  - `GET /auth/callback/{platform}` - Handle OAuth callbacks
  - `GET /auth/status/{user_id}` - Check authentication status
  - `POST /auth/disconnect/{platform}` - Revoke platform access

### 4. Telegram Bot OAuth Handlers
- **File**: `/chatbot_telegram/oauth_handlers.py`
- **Commands**:
  - `/connect_google` - Connect Google account
  - `/connect_meetup` - Connect Meetup account
  - `/connect_eventbrite` - Connect Eventbrite account
  - `/connect_github` - Connect GitHub account
  - `/auth_status` - View connected platforms

### 5. Registration Integration
- **File**: `/chatbot_telegram/interactive_handlers.py`
- **Enhanced**: `handle_register_proceed_action` now checks OAuth credentials before registration

## Deployment Steps

### Step 1: Database Setup

Run the OAuth infrastructure migration in Supabase SQL Editor:

```sql
-- Execute the contents of scripts/migrations/create_oauth_infrastructure.sql
-- This creates the required tables and RLS policies
```

### Step 2: Secret Management

Add OAuth credentials to Google Secret Manager:

```bash
# Google OAuth (already configured)
echo -n "your-google-client-id" | gcloud secrets versions add GOOGLE_OAUTH_CLIENT_ID --data-file=-
echo -n "your-google-client-secret" | gcloud secrets versions add GOOGLE_OAUTH_CLIENT_SECRET --data-file=-

# GitHub OAuth (already configured)
echo -n "your-github-client-id" | gcloud secrets versions add GITHUB_OAUTH_CLIENT_ID --data-file=-
echo -n "your-github-client-secret" | gcloud secrets versions add GITHUB_OAUTH_CLIENT_SECRET --data-file=-

# Meetup OAuth (when available)
echo -n "your-meetup-client-id" | gcloud secrets versions add MEETUP_OAUTH_CLIENT_ID --data-file=-
echo -n "your-meetup-client-secret" | gcloud secrets versions add MEETUP_OAUTH_CLIENT_SECRET --data-file=-

# Eventbrite OAuth (when available)
echo -n "your-eventbrite-client-id" | gcloud secrets versions add EVENTBRITE_OAUTH_CLIENT_ID --data-file=-
echo -n "your-eventbrite-client-secret" | gcloud secrets versions add EVENTBRITE_OAUTH_CLIENT_SECRET --data-file=-

# Encryption key for credential storage
openssl rand -base64 32 | tr -d '\n' | gcloud secrets versions add CREDENTIAL_ENCRYPTION_KEY --data-file=-
```

### Step 3: API Deployment

Deploy the OAuth-enabled API using the build configuration:

```bash
cd /Users/eladm/Projects/token/tokenhunter
gcloud builds submit --config=deployment/cloudbuild/cloudbuild.oauth-api.yaml
```

**Current Build Status**: `f5fb5468-ac06-43e1-b176-c37e3afc035b` (WORKING)

### Step 4: Bot Integration

Update the Telegram bot with OAuth support:

1. **Copy OAuth handlers to VM**:
```bash
gcloud compute scp chatbot_telegram/oauth_handlers.py tokennav-telegram-bot-vm:chatbot_telegram/ --zone=europe-west1-b
```

2. **Update bot.py on VM**:
```bash
gcloud compute ssh tokennav-telegram-bot-vm --zone=europe-west1-b
cd chatbot_telegram
cp bot.py bot_backup_$(date +%Y%m%d_%H%M%S).py

# Update bot.py to include OAuth handlers
# Add import: from oauth_handlers import oauth_handlers
# Add handlers to application setup
```

3. **Restart bot service**:
```bash
sudo systemctl restart token-nav-telegram.service
```

### Step 5: Environment Configuration

Update environment variables for OAuth support:

```bash
# API Base URL for OAuth callbacks
API_BASE_URL=https://chatbot-api-oauth-staging-oo6mrfxexq-uc.a.run.app

# OAuth redirect URIs in platform configurations
GOOGLE_REDIRECT_URI=${API_BASE_URL}/auth/callback/google
GITHUB_REDIRECT_URI=${API_BASE_URL}/auth/callback/github
MEETUP_REDIRECT_URI=${API_BASE_URL}/auth/callback/meetup
EVENTBRITE_REDIRECT_URI=${API_BASE_URL}/auth/callback/eventbrite
```

## OAuth Platform Setup

### Google OAuth
1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create OAuth 2.0 Client ID
3. Add authorized redirect URI: `${API_BASE_URL}/auth/callback/google`
4. Configure consent screen with necessary scopes

### GitHub OAuth
1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Create new OAuth App
3. Set authorization callback URL: `${API_BASE_URL}/auth/callback/github`
4. Configure required scopes for user identification

### Meetup OAuth (Future)
1. Register application at [Meetup API](https://www.meetup.com/api/)
2. Configure redirect URI: `${API_BASE_URL}/auth/callback/meetup`
3. Request necessary scopes for event access

### Eventbrite OAuth (Future)
1. Create app at [Eventbrite Developer Portal](https://www.eventbrite.com/platform/)
2. Set redirect URI: `${API_BASE_URL}/auth/callback/eventbrite`
3. Configure scopes for event registration

## Testing OAuth Flow

### Manual Testing Steps

1. **Test OAuth URLs**:
```bash
curl "https://chatbot-api-oauth-staging-oo6mrfxexq-uc.a.run.app/auth/connect/google?telegram_user_id=test123"
```

2. **Test Authentication Status**:
```bash
curl "https://chatbot-api-oauth-staging-oo6mrfxexq-uc.a.run.app/auth/status/test123"
```

3. **Test Bot Commands**:
- Send `/connect_google` to bot
- Verify OAuth URL generation
- Test authentication flow in browser
- Check `/auth_status` command

### Expected User Flow

1. User encounters event requiring registration
2. Bot detects platform requires OAuth (Luma, Meetup, etc.)
3. Bot prompts: "Authentication Required for this platform"
4. User clicks OAuth connection button
5. User completes OAuth flow in browser
6. User returns to bot and proceeds with registration
7. Bot uses stored OAuth tokens for automatic registration

## Security Features

- **Encrypted Storage**: All OAuth tokens encrypted using Fernet
- **State Validation**: OAuth state parameter prevents CSRF attacks
- **Row Level Security**: Database policies restrict access to own credentials
- **Secure Transport**: All OAuth flows use HTTPS
- **Token Rotation**: Support for refreshing OAuth tokens
- **Audit Trail**: All OAuth events logged for security monitoring

## Monitoring and Troubleshooting

### Health Checks
```bash
# Check OAuth service health
curl "https://chatbot-api-oauth-staging-oo6mrfxexq-uc.a.run.app/health"

# Check authentication endpoints
curl "https://chatbot-api-oauth-staging-oo6mrfxexq-uc.a.run.app/auth/status/test"
```

### Common Issues

1. **"Invalid redirect URI"**: Ensure OAuth app configurations match API_BASE_URL
2. **"Invalid state parameter"**: Check OAuth state table for expired/invalid states
3. **"Encryption key error"**: Verify CREDENTIAL_ENCRYPTION_KEY is properly set
4. **"Database access denied"**: Check RLS policies and user permissions

### Logs to Monitor
- OAuth flow initiation and completion
- Token encryption/decryption operations
- Platform authentication failures
- User consent acceptance/denial

## Next Steps

1. **Production Migration**: Move from staging to production API
2. **Platform Expansion**: Add Meetup and Eventbrite OAuth
3. **Token Refresh**: Implement automatic token refresh logic
4. **Enhanced UX**: Add platform-specific registration flows
5. **Analytics**: Track OAuth conversion rates and platform preferences

## Support

For OAuth-related issues:
1. Check service logs in Cloud Logging
2. Verify Secret Manager access permissions
3. Test OAuth flow manually before bot integration
4. Validate platform OAuth app configurations

---

**Status**: OAuth system implemented and ready for production deployment
**Last Updated**: June 5, 2025
**Build ID**: f5fb5468-ac06-43e1-b176-c37e3afc035b (OAuth staging deployment)
