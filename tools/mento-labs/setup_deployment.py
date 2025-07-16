#!/usr/bin/env python3
"""
Interactive setup for Celo deployment
This will help you create the .env file securely
"""

import getpass
import os


def setup_deployment():
    """Interactive setup for deployment environment"""

    print("🚀 Celo Oracle Deployment Setup")
    print("=" * 50)

    # Check if .env already exists
    env_file = ".env"
    if os.path.exists(env_file):
        print("📄 .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != "y":
            print("❌ Setup cancelled")
            return

    print("\n🔑 Please enter your Celo private key:")
    print("💡 This will be stored securely in .env file")
    print("⚠️  Make sure this is your TESTNET private key only!")

    # Get private key securely
    private_key = getpass.getpass("Private Key (hidden input): ")

    if not private_key:
        print("❌ No private key provided")
        return

    # Validate private key format
    if private_key.startswith("0x"):
        private_key = private_key[2:]

    if len(private_key) != 64:
        print(
            f"⚠️  Warning: Private key should be 64 characters, got {len(private_key)}"
        )
        response = input("Continue anyway? (y/N): ")
        if response.lower() != "y":
            print("❌ Setup cancelled")
            return

    # Write .env file
    try:
        with open(env_file, "w") as f:
            f.write(f"CELO_PRIVATE_KEY={private_key}\n")

        # Set secure permissions
        os.chmod(env_file, 0o600)  # Read/write for owner only

        print("✅ .env file created successfully!")
        print("🔒 File permissions set to secure (600)")
        print("\n🧪 Testing your account...")

        # Test the setup
        from test_your_account import test_your_celo_account

        success = test_your_celo_account()

        if success:
            print("\n🚀 Ready for deployment!")
            print("Run: python deploy_oracle_real.py")
        else:
            print("\n❌ Account test failed. Please check your private key.")

    except Exception as e:
        print(f"❌ Error creating .env file: {e}")


if __name__ == "__main__":
    setup_deployment()
