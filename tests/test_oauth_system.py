"""
Test OAuth Authentication System Integration

This script tests the complete OAuth authentication flow:
1. Database tables creation
2. FastAPI auth endpoints
3. Telegram bot OAuth commands
4. Registration system integration
"""

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../src"))

import asyncio
import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv("chatbot_telegram/.env")


async def test_oauth_system():
    """Test the complete OAuth authentication system"""

    print("🔧 Testing OAuth Authentication System")
    print("=" * 50)

    api_base_url = os.getenv(
        "API_BASE_URL", "https://chatbot-api-service-v2-oo6mrfxexq-uc.a.run.app"
    )
    test_telegram_user_id = "test_user_123"

    print(f"API Base URL: {api_base_url}")
    print(f"Test User ID: {test_telegram_user_id}")
    print()

    # Test 1: Check if FastAPI app has auth routes
    print("1️⃣ Testing FastAPI Auth Endpoints")
    print("-" * 30)

    try:
        # Test auth status endpoint
        response = requests.get(
            f"{api_base_url}/auth/status/{test_telegram_user_id}", timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            print("✅ Auth status endpoint working")
            print(f"   Connected platforms: {data.get('total_connected', 0)}")
            platforms = data.get("platforms", {})
            for platform, info in platforms.items():
                status = "✅ Connected" if info.get("connected") else "❌ Not connected"
                print(f"   {platform}: {status}")
        else:
            print(f"❌ Auth status endpoint failed: {response.status_code}")

    except Exception as e:
        print(f"❌ Failed to test auth endpoints: {e}")

    print()

    # Test 2: Test OAuth initiation (without actually going through OAuth)
    print("2️⃣ Testing OAuth URL Generation")
    print("-" * 30)

    for platform in ["google", "meetup", "eventbrite"]:
        try:
            oauth_url = f"{api_base_url}/auth/connect/{platform}?telegram_user_id={test_telegram_user_id}"

            # Just check if the endpoint exists (will redirect)
            response = requests.get(oauth_url, allow_redirects=False, timeout=5)

            if response.status_code in [302, 400]:  # Redirect or missing credentials
                print(f"✅ {platform.title()} OAuth endpoint exists")
                if response.status_code == 302:
                    print(
                        f"   Would redirect to: {response.headers.get('location', 'OAuth provider')[:50]}..."
                    )
                else:
                    print("   OAuth credentials not configured (expected for testing)")
            else:
                print(
                    f"⚠️  {platform.title()} OAuth endpoint returned: {response.status_code}"
                )

        except Exception as e:
            print(f"❌ Failed to test {platform} OAuth: {e}")

    print()

    # Test 3: Check environment variables
    print("3️⃣ Testing Environment Configuration")
    print("-" * 30)

    env_vars = [
        "GOOGLE_OAUTH_CLIENT_ID",
        "GOOGLE_OAUTH_CLIENT_SECRET",
        "API_BASE_URL",
        "SUPABASE_URL",
        "SUPABASE_KEY",
    ]

    for var in env_vars:
        value = os.getenv(var)
        if value:
            masked_value = value[:10] + "..." if len(value) > 10 else value
            print(f"✅ {var}: {masked_value}")
        else:
            print(f"❌ {var}: Not set")

    print()

    # Test 4: Check OAuth handlers are available
    print("4️⃣ Testing Telegram Bot OAuth Handlers")
    print("-" * 30)

    try:
        from telegram_bot.oauth_handlers import oauth_handlers

        print("✅ OAuth handlers imported successfully")
        print(f"   API Base URL: {oauth_handlers.api_base_url}")

        # Test handler methods exist
        handler_methods = [
            "handle_connect_google",
            "handle_connect_meetup",
            "handle_connect_eventbrite",
            "handle_auth_status",
        ]

        for method in handler_methods:
            if hasattr(oauth_handlers, method):
                print(f"✅ {method} handler available")
            else:
                print(f"❌ {method} handler missing")

    except ImportError as e:
        print(f"❌ Failed to import OAuth handlers: {e}")

    print()

    # Test 5: Check authentication service
    print("5️⃣ Testing OAuth Authentication Service")
    print("-" * 30)

    try:
        from api.registration.oauth_authentication_service import oauth_service

        print("✅ OAuth service imported successfully")

        # Check service configuration
        platforms = ["google", "meetup", "eventbrite"]
        for platform in platforms:
            if platform in oauth_service.oauth_configs:
                config = oauth_service.oauth_configs[platform]
                client_id_set = bool(config.client_id)
                client_secret_set = bool(config.client_secret)
                print(
                    f"✅ {platform.title()} config: Client ID: {client_id_set}, Secret: {client_secret_set}"
                )
            else:
                print(f"❌ {platform.title()} config missing")

    except ImportError as e:
        print(f"❌ Failed to import OAuth service: {e}")

    print()

    # Test 6: Database connection test
    print("6️⃣ Testing Database Integration")
    print("-" * 30)

    try:
        from supabase import create_client

        supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

        # Try to query oauth_states table (should exist after migration)
        result = supabase.table("oauth_states").select("*").limit(1).execute()
        print("✅ oauth_states table accessible")

        # Try to query user_platform_credentials table
        result = (
            supabase.table("user_platform_credentials").select("*").limit(1).execute()
        )
        print("✅ user_platform_credentials table accessible")

        print("✅ Database integration working")

    except Exception as e:
        print(f"⚠️  Database test failed (may need manual SQL migration): {e}")

    print()
    print("🎉 OAuth Authentication System Test Complete!")
    print("=" * 50)

    print("\n📋 Next Steps:")
    print("1. Run the SQL migration in Supabase SQL Editor if database test failed")
    print("2. Configure Meetup and Eventbrite OAuth credentials when needed")
    print("3. Test the complete flow with `/connect_google` in Telegram")
    print("4. Deploy the updated API and bot to production")


if __name__ == "__main__":
    asyncio.run(test_oauth_system())
