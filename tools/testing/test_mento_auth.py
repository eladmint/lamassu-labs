#!/usr/bin/env python3
"""
Test Mento Dashboard Authentication
Verifies that all authentication methods are properly configured
"""

import os
import sys
from pathlib import Path

import requests


# Load environment variables from .env file
def load_env_file():
    """Load .env file manually"""
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    os.environ[key] = value


# Load environment first
load_env_file()

# Add project path for emergency secret manager
sys.path.append("/Users/eladm/Projects/token/tokenhunter")


def test_dashboard_access():
    """Test basic dashboard access"""
    print("1. Testing Dashboard Access...")
    try:
        response = requests.get(
            "https://cmhvu-6iaaa-aaaal-asg5q-cai.icp0.io", timeout=10
        )
        if response.status_code == 200:
            if "Sign In" in response.text:
                print("✅ Dashboard accessible with Sign In button")
                return True
            else:
                print("⚠️  Dashboard accessible but no Sign In button found")
                return False
        else:
            print(f"❌ Dashboard returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Failed to access dashboard: {e}")
        return False


def test_oauth_configuration():
    """Test OAuth configuration"""
    print("\n2. Testing OAuth Configuration...")

    # Test Google OAuth redirect URL
    client_id = (
        "867263134607-vkkd9avs6a75gmjpzja17a9a0bbdle1.apps.googleusercontent.com"
    )
    redirect_uri = "https://cmhvu-6iaaa-aaaal-asg5q-cai.icp0.io/auth/callback/google"
    scope = "openid email profile"

    oauth_url = f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}&state=mento_dashboard"

    try:
        # Just test that the URL is valid (don't follow redirects)
        response = requests.head(oauth_url, allow_redirects=False, timeout=5)
        if response.status_code in [
            200,
            302,
            400,
        ]:  # 400 is expected for incomplete request
            print("✅ Google OAuth URL properly configured")
            print(f"   Client ID: {client_id}")
            print(f"   Redirect URI: {redirect_uri}")
            return True
        else:
            print(f"❌ OAuth URL returned unexpected status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Failed to test OAuth URL: {e}")
        return False


def test_supabase_connection():
    """Test Supabase connection"""
    print("\n3. Testing Supabase Connection...")

    supabase_url = "https://zzwgtxibhfuynfpcinpy.supabase.co"
    supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inp6d2d0eGliaGZ1eW5mcGNpbnB5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ4MTM1MTgsImV4cCI6MjA2MDM4OTUxOH0.LpIB7rQ4YyTGszEMleJNQju6VuazIg7b9CIyjoqMCpI"

    try:
        # Test Supabase health endpoint
        headers = {"apikey": supabase_key, "Authorization": f"Bearer {supabase_key}"}
        response = requests.get(f"{supabase_url}/rest/v1/", headers=headers, timeout=5)

        if response.status_code == 200:
            print("✅ Supabase connection successful")
            print(f"   URL: {supabase_url}")
            return True
        else:
            print(f"❌ Supabase returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Failed to connect to Supabase: {e}")
        return False


def test_environment_variables():
    """Test that all required environment variables are set"""
    print("\n4. Testing Environment Variables...")

    required_vars = [
        "GOOGLE_OAUTH_CLIENT_ID",
        "GOOGLE_OAUTH_CLIENT_SECRET",
        "SUPABASE_URL",
        "SUPABASE_KEY",
        "MENTO_DASHBOARD_REDIRECT_URI",
    ]

    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
        else:
            value = os.environ.get(var)
            masked = value[:10] + "..." if len(value) > 10 else "***"
            print(f"✅ {var}: {masked}")

    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ All required environment variables are set")
        return True


def test_secret_manager_access():
    """Test that secret manager can access auth credentials"""
    print("\n5. Testing Secret Manager Access...")

    try:
        from google.cloud import secretmanager

        client = secretmanager.SecretManagerServiceClient()

        # Test accessing Google OAuth credentials
        response = client.access_secret_version(
            request={
                "name": "projects/tokenhunter-457310/secrets/GOOGLE_OAUTH_CLIENT_ID/versions/latest"
            }
        )

        if response.payload.data:
            client_id = response.payload.data.decode("UTF-8")
            print(f"✅ Secret Manager access working: {client_id[:20]}...")
            return True
        else:
            print("❌ Secret Manager returned empty data")
            return False

    except Exception as e:
        print(f"❌ Secret Manager access failed: {e}")
        return False


def main():
    """Run all authentication tests"""
    print("🔐 Mento Dashboard Authentication Test")
    print("=" * 50)

    tests = [
        test_dashboard_access,
        test_oauth_configuration,
        test_supabase_connection,
        test_environment_variables,
        test_secret_manager_access,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 50)
    print(f"RESULTS: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All authentication systems are properly configured!")
        print("\nYou can now:")
        print("1. Go to https://cmhvu-6iaaa-aaaal-asg5q-cai.icp0.io")
        print("2. Click 'Sign In'")
        print("3. Choose 'Continue with Google' or other providers")
        print("4. Access the full Mento monitoring dashboard")
    else:
        print(f"⚠️  {total - passed} tests failed. Please check the configuration.")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
