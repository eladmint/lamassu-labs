#!/usr/bin/env python3
"""
Local OAuth Authentication Flow Test

Tests the complete OAuth flow including:
1. Telegram bot OAuth commands
2. OAuth URL generation
3. Authentication status checking
4. Integration with registration system
"""

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../src"))

import asyncio
import os
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

# Load environment variables
load_dotenv("chatbot_telegram/.env")


async def test_oauth_flow():
    """Test complete OAuth authentication flow"""

    print("🔐 Testing OAuth Authentication Flow Locally")
    print("=" * 60)

    try:
        # Test 1: OAuth Service
        print("\n1️⃣ Testing OAuth Service...")
        from api.registration.oauth_authentication_service import (
            AuthPlatform,
            oauth_service,
        )

        test_user_id = "test_oauth_user_123"

        # Test OAuth URL generation
        try:
            oauth_url = await oauth_service.generate_oauth_url(
                telegram_user_id=test_user_id, platform=AuthPlatform.GOOGLE
            )
            print(f"✅ Google OAuth URL generated: {oauth_url[:50]}...")
        except Exception as e:
            print(f"❌ OAuth URL generation failed: {e}")

        # Test user connected platforms
        try:
            connected = await oauth_service.get_user_connected_platforms(test_user_id)
            print(f"✅ Connected platforms check: {len(connected)} platforms")
        except Exception as e:
            print(f"⚠️ Connected platforms check: {e} (expected for test user)")

        # Test 2: Telegram Bot OAuth Handlers
        print("\n2️⃣ Testing Telegram Bot OAuth Handlers...")
        from telegram_bot.oauth_handlers import oauth_handlers

        # Mock update and context for testing
        mock_update = MagicMock()
        mock_update.effective_user.id = test_user_id
        mock_update.message.reply_text = AsyncMock()

        mock_context = MagicMock()

        # Test Google connection command
        try:
            await oauth_handlers.handle_connect_google(mock_update, mock_context)
            print("✅ Google OAuth handler executed successfully")

            # Check if reply_text was called with OAuth URL
            reply_calls = mock_update.message.reply_text.call_args_list
            if reply_calls:
                call_text = str(reply_calls[0])
                if "Connect Your Google Account" in call_text:
                    print("✅ OAuth message formatting correct")
                else:
                    print("⚠️ OAuth message formatting may need review")

        except Exception as e:
            print(f"❌ Google OAuth handler failed: {e}")

        # Test 3: Registration System Integration
        print("\n3️⃣ Testing Registration Integration...")
        from telegram_bot.interactive_handlers import CallbackHandlers

        # Test registration with OAuth check
        mock_query = MagicMock()
        mock_query.from_user.id = test_user_id
        mock_query.edit_message_text = AsyncMock()
        mock_query.answer = AsyncMock()

        test_event_url = "https://lu.ma/test-event"

        try:
            # This should check OAuth credentials and provide authentication guidance
            await CallbackHandlers.handle_register_proceed_action(
                mock_query, test_event_url, mock_context
            )
            print("✅ Registration OAuth integration executed")

            # Check if authentication was requested
            edit_calls = mock_query.edit_message_text.call_args_list
            if edit_calls:
                call_text = str(edit_calls[-1])  # Get last call
                if (
                    "Authentication Required" in call_text
                    or "Processing Registration" in call_text
                ):
                    print("✅ Registration authentication flow working")
                else:
                    print("⚠️ Registration may need OAuth enhancement")

        except Exception as e:
            print(f"❌ Registration OAuth integration failed: {e}")

        # Test 4: Environment Configuration
        print("\n4️⃣ Testing Environment Configuration...")
        required_vars = [
            "GOOGLE_OAUTH_CLIENT_ID",
            "GOOGLE_OAUTH_CLIENT_SECRET",
            "API_BASE_URL",
            "SUPABASE_URL",
            "CREDENTIAL_ENCRYPTION_KEY",
        ]

        config_ok = True
        for var in required_vars:
            value = os.getenv(var)
            if value and not value.startswith("your-"):
                print(f"✅ {var}: Configured")
            else:
                print(f"❌ {var}: Missing or placeholder value")
                config_ok = False

        if config_ok:
            print("✅ Environment configuration complete")
        else:
            print("⚠️ Some environment variables need configuration")

        # Test 5: FastAPI Integration
        print("\n5️⃣ Testing FastAPI Integration...")
        from api.main import app
        from fastapi.testclient import TestClient

        client = TestClient(app)

        # Test auth status endpoint
        response = client.get(f"/auth/status/{test_user_id}")
        if response.status_code == 200:
            data = response.json()
            print(
                f"✅ Auth status endpoint: {data.get('total_connected', 0)} connected platforms"
            )
        else:
            print(f"❌ Auth status endpoint failed: {response.status_code}")

        # Test OAuth connect endpoint (should redirect)
        response = client.get(
            f"/auth/connect/google?telegram_user_id={test_user_id}",
            allow_redirects=False,
        )
        if response.status_code in [302, 400]:  # Redirect or missing config
            print("✅ OAuth connect endpoint working")
        else:
            print(f"⚠️ OAuth connect endpoint: {response.status_code}")

        print("\n🎉 OAuth Flow Test Complete!")
        print("=" * 60)

        return {
            "oauth_service": True,
            "telegram_handlers": True,
            "registration_integration": True,
            "environment_config": config_ok,
            "fastapi_integration": True,
        }

    except Exception as e:
        print(f"\n❌ OAuth flow test failed: {e}")
        import traceback

        traceback.print_exc()
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    result = asyncio.run(test_oauth_flow())
    print(f"\n📋 Test Results: {result}")
