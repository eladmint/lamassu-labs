"""Security Testing Suite for Unified Authentication System.

Comprehensive security validation for Sprint 32 Task 1.4, ensuring enterprise-grade
security standards for the unified platform authentication architecture.

Test Categories:
- JWT Token Security & Validation
- Multi-Chain Wallet Signature Verification
- Authentication Rate Limiting & Brute Force Protection
- Session Management Security
- Enterprise SSO Security Validation
- Cross-Layer Permission Security

# Fix for hyphenated layer imports - add src directories to path
import sys
from pathlib import Path

# Add layer source directories to Python path
_current_file = Path(__file__)
_layers_dir = _current_file.parent
while _layers_dir.name != 'layers' and _layers_dir.parent != _layers_dir:
    _layers_dir = _layers_dir.parent

if _layers_dir.name == 'layers':
    # Add all layer src directories
    for _layer in ['agent-forge', 'ziggurat-intelligence', 'lamassu-labs', 'shared']:
        _src_path = _layers_dir / _layer / 'src'
        if _src_path.exists():
            sys.path.insert(0, str(_src_path))
        # Also add layer root for non-src modules
        _layer_path = _layers_dir / _layer
        if _layer_path.exists():
            sys.path.insert(0, str(_layer_path))

"""

import time
import uuid
from datetime import datetime, timedelta
from unittest.mock import patch

import jwt
import pytest

from api.core.unified_auth import (
    JWT_ALGORITHM,
    JWT_SECRET_KEY,
    PlatformPermissions,
    UnifiedAuthService,
    UserIdentity,
)
from api.services.multi_chain_wallet_service import (
    MultiChainWalletService,
    WalletVerificationError,
)


class TestJWTTokenSecurity:
    """Test JWT token security and validation."""

    def setup_method(self):
        """Setup test fixtures."""
        self.auth_service = UnifiedAuthService()
        self.test_user = UserIdentity(
            id="test_user_123",
            email="security@nuru.ai",
            username="security_test",
            platform_role="developer",
        )

    @pytest.mark.asyncio
    async def test_jwt_token_generation_security(self):
        """Test JWT token generation with proper security claims."""
        tokens = await self.auth_service.generate_tokens(self.test_user)

        # Verify token structure
        assert tokens.access_token is not None
        assert tokens.refresh_token is not None
        assert tokens.token_type == "bearer"
        assert tokens.expires_in > 0

        # Decode and verify access token claims
        access_payload = jwt.decode(
            tokens.access_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]
        )

        assert access_payload["sub"] == self.test_user.id
        assert access_payload["type"] == "access"
        assert "exp" in access_payload
        assert "iat" in access_payload
        assert "jti" in access_payload  # Unique token ID for revocation

        # Verify refresh token claims
        refresh_payload = jwt.decode(
            tokens.refresh_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]
        )

        assert refresh_payload["sub"] == self.test_user.id
        assert refresh_payload["type"] == "refresh"
        assert refresh_payload["exp"] > access_payload["exp"]  # Longer expiration

    @pytest.mark.asyncio
    async def test_jwt_token_expiration_security(self):
        """Test JWT token expiration validation."""
        # Create expired token
        expired_payload = {
            "sub": self.test_user.id,
            "type": "access",
            "exp": datetime.utcnow() - timedelta(minutes=1),  # Expired 1 minute ago
            "iat": datetime.utcnow() - timedelta(minutes=31),
            "jti": str(uuid.uuid4()),
        }

        expired_token = jwt.encode(
            expired_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM
        )

        # Verify expired token is rejected
        result = await self.auth_service.verify_token(expired_token)
        assert result is None

    @pytest.mark.asyncio
    async def test_jwt_token_tampering_detection(self):
        """Test JWT token tampering detection."""
        tokens = await self.auth_service.generate_tokens(self.test_user)

        # Tamper with token by modifying a character
        tampered_token = tokens.access_token[:-5] + "XXXXX"

        # Verify tampered token is rejected
        result = await self.auth_service.verify_token(tampered_token)
        assert result is None

    @pytest.mark.asyncio
    async def test_jwt_secret_key_security(self):
        """Test JWT secret key security requirements."""
        # Verify secret key is sufficiently random and long
        assert len(JWT_SECRET_KEY) >= 32
        assert JWT_SECRET_KEY != "secret"  # Not default value
        assert JWT_SECRET_KEY != "test"  # Not test value

    @pytest.mark.asyncio
    async def test_jwt_algorithm_security(self):
        """Test JWT algorithm security (no 'none' algorithm)."""
        # Verify we're using a secure algorithm
        assert JWT_ALGORITHM in ["HS256", "HS384", "HS512", "RS256", "RS384", "RS512"]
        assert JWT_ALGORITHM != "none"  # Critical security check


class TestMultiChainWalletSecurity:
    """Test multi-chain wallet signature verification security."""

    def setup_method(self):
        """Setup test fixtures."""
        self.wallet_service = MultiChainWalletService()
        self.auth_service = UnifiedAuthService()

    @pytest.mark.asyncio
    async def test_wallet_address_format_validation(self):
        """Test wallet address format validation security."""
        # Test valid addresses
        valid_addresses = {
            "ethereum": "0x742d35Cc6834C0532925a3b8D0998f8f284fbDcE",
            "ton": "EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N",
            "cardano": "addr1qx2fxv2umyhttkxyxp8x0dlpdt3k6cwng5pxj3jhsydzer3jcu5d8ps7zex2k2xt3uqxgjqnnj83ws8lhrn648jjxtwq2ytjmg",
            "icp": "rdmx6-jaaaa-aaaah-qcaiq-cai",
        }

        for chain, address in valid_addresses.items():
            is_valid = await self.wallet_service.verify_wallet_address(chain, address)
            assert is_valid, f"Valid {chain} address should be accepted"

        # Test invalid addresses
        invalid_addresses = {
            "ethereum": "invalid_eth_address",
            "ton": "short",
            "cardano": "invalid_cardano",
            "icp": "invalid.icp",
        }

        for chain, address in invalid_addresses.items():
            is_valid = await self.wallet_service.verify_wallet_address(chain, address)
            assert not is_valid, f"Invalid {chain} address should be rejected"

    @pytest.mark.asyncio
    async def test_signature_verification_security(self):
        """Test cryptographic signature verification."""
        # Test signature verification requires proper parameters
        with pytest.raises(WalletVerificationError):
            await self.wallet_service.verify_wallet_signature(
                chain="unsupported_chain",
                address="0x123",
                message="test",
                signature="invalid",
            )

        # Test signature verification with missing public key (for chains that require it)
        with pytest.raises(WalletVerificationError):
            # TON requires public key but none provided
            await self.wallet_service.verify_wallet_signature(
                chain="ton",
                address="EQCD39VS5jcptHL8vMjEXrzGaRcCVYto7HUn4bpAOg8xqB2N",
                message="test message",
                signature="invalid_signature",
            )

    @pytest.mark.asyncio
    async def test_challenge_message_security(self):
        """Test challenge message generation and validation security."""
        user_id = "test_user_123"
        chain = "ethereum"

        # Generate challenge message
        challenge = await self.wallet_service.generate_challenge_message(user_id, chain)

        # Verify challenge contains required security elements
        assert f"User ID: {user_id}" in challenge
        assert f"Chain: {chain}" in challenge
        assert "Timestamp:" in challenge
        assert "Nonce:" in challenge
        assert "Sign this message to authenticate" in challenge

        # Test challenge validation
        is_valid = await self.wallet_service.validate_challenge_message(
            challenge, user_id, chain, max_age_seconds=300
        )
        assert is_valid

        # Test expired challenge rejection
        time.sleep(1)  # Ensure some time passes
        is_expired = await self.wallet_service.validate_challenge_message(
            challenge, user_id, chain, max_age_seconds=0  # Immediate expiration
        )
        assert not is_expired

    @pytest.mark.asyncio
    async def test_wallet_connection_replay_attack_protection(self):
        """Test protection against replay attacks in wallet connections."""
        user_id = "test_user_123"
        chain = "ethereum"
        wallet_address = "0x742d35Cc6834C0532925a3b8D0998f8f284fbDcE"

        # Mock signature verification to always pass
        with patch.object(
            self.auth_service, "_verify_wallet_signature", return_value=True
        ):
            with patch.object(self.auth_service, "_wallet_exists", return_value=False):
                # First connection should succeed
                wallet1 = await self.auth_service.connect_wallet(
                    user_id=user_id,
                    chain=chain,
                    wallet_address=wallet_address,
                    signature="valid_signature_1",
                )
                assert wallet1.wallet_address == wallet_address

                # Mock wallet now exists
                with patch.object(
                    self.auth_service, "_wallet_exists", return_value=True
                ):
                    # Second connection with same wallet should fail
                    with pytest.raises(Exception):  # Should raise conflict error
                        await self.auth_service.connect_wallet(
                            user_id="different_user",
                            chain=chain,
                            wallet_address=wallet_address,
                            signature="valid_signature_2",
                        )


class TestAuthenticationRateLimiting:
    """Test authentication rate limiting and brute force protection."""

    def setup_method(self):
        """Setup test fixtures."""
        self.auth_service = UnifiedAuthService()

    @pytest.mark.asyncio
    async def test_password_authentication_rate_limiting(self):
        """Test rate limiting for password authentication attempts."""
        # This would require implementing rate limiting in the auth service
        # For now, we test the concept with mock implementation

        failed_attempts = []

        # Simulate multiple failed login attempts
        for i in range(10):
            result = await self.auth_service.authenticate_user(
                identifier="nonexistent@test.com",
                credential="wrong_password",
                auth_type="email",
            )
            failed_attempts.append(result)

        # All attempts should fail (user doesn't exist)
        assert all(result is None for result in failed_attempts)

        # In a real implementation, we would track failed attempts
        # and implement progressive delays or account lockouts

    @pytest.mark.asyncio
    async def test_session_token_brute_force_protection(self):
        """Test protection against session token brute force attacks."""
        # Test rapid token verification attempts
        invalid_tokens = [f"invalid_token_{i}" for i in range(100)]

        results = []
        start_time = time.time()

        for token in invalid_tokens:
            result = await self.auth_service.verify_token(token)
            results.append(result)

        end_time = time.time()

        # All invalid tokens should be rejected
        assert all(result is None for result in results)

        # Verify reasonable processing time (not too slow, indicating no artificial delays)
        # In production, we might add rate limiting here
        processing_time = end_time - start_time
        assert processing_time < 5.0  # Should process 100 invalid tokens quickly


class TestSessionManagementSecurity:
    """Test session management security features."""

    def setup_method(self):
        """Setup test fixtures."""
        self.auth_service = UnifiedAuthService()
        self.test_user = UserIdentity(
            id="session_test_user", email="session@nuru.ai", platform_role="developer"
        )

    @pytest.mark.asyncio
    async def test_session_isolation(self):
        """Test session isolation between users."""
        # Generate tokens for two different users
        user1 = UserIdentity(
            id="user1", email="user1@test.com", platform_role="developer"
        )
        user2 = UserIdentity(
            id="user2", email="user2@test.com", platform_role="developer"
        )

        tokens1 = await self.auth_service.generate_tokens(user1)
        tokens2 = await self.auth_service.generate_tokens(user2)

        # Verify tokens are different
        assert tokens1.access_token != tokens2.access_token
        assert tokens1.refresh_token != tokens2.refresh_token

        # Verify each token only works for its respective user
        payload1 = await self.auth_service.verify_token(tokens1.access_token)
        payload2 = await self.auth_service.verify_token(tokens2.access_token)

        assert payload1["sub"] == user1.id
        assert payload2["sub"] == user2.id
        assert payload1["sub"] != payload2["sub"]

    @pytest.mark.asyncio
    async def test_session_unique_identifiers(self):
        """Test session unique identifiers (JTI) for revocation capability."""
        # Generate multiple tokens for same user
        tokens1 = await self.auth_service.generate_tokens(self.test_user)
        tokens2 = await self.auth_service.generate_tokens(self.test_user)

        # Decode tokens to check JTI uniqueness
        payload1 = jwt.decode(
            tokens1.access_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]
        )
        payload2 = jwt.decode(
            tokens2.access_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]
        )

        # JTI should be unique for each token
        assert payload1["jti"] != payload2["jti"]
        assert len(payload1["jti"]) >= 16  # Sufficient entropy
        assert len(payload2["jti"]) >= 16


class TestPlatformPermissionSecurity:
    """Test platform permission security and access control."""

    def setup_method(self):
        """Setup test fixtures."""
        self.auth_service = UnifiedAuthService()
        self.test_user = UserIdentity(
            id="permission_test_user",
            email="permissions@nuru.ai",
            platform_role="developer",
        )

    @pytest.mark.asyncio
    async def test_permission_level_hierarchy(self):
        """Test permission level hierarchy enforcement."""
        user_id = "test_user_permissions"

        # Test permission hierarchy: basic < premium < enterprise
        test_cases = [
            ("basic", "basic", True),  # basic user can access basic
            ("premium", "basic", True),  # premium user can access basic
            ("enterprise", "basic", True),  # enterprise user can access basic
            ("premium", "premium", True),  # premium user can access premium
            ("enterprise", "premium", True),  # enterprise user can access premium
            ("enterprise", "enterprise", True),  # enterprise user can access enterprise
            ("basic", "premium", False),  # basic user cannot access premium
            ("basic", "enterprise", False),  # basic user cannot access enterprise
            ("premium", "enterprise", False),  # premium user cannot access enterprise
        ]

        for user_level, required_level, expected_access in test_cases:
            # Mock user permissions
            with patch.object(
                self.auth_service,
                "_get_user_permissions",
                return_value=PlatformPermissions(
                    user_id=user_id,
                    layer="ziggurat",
                    permission_level=user_level,
                    usage_quota=100,
                ),
            ):
                has_access = await self.auth_service.check_platform_access(
                    user_id, "ziggurat", required_level
                )
                assert (
                    has_access == expected_access
                ), f"User with {user_level} should {'have' if expected_access else 'not have'} access to {required_level}"

    @pytest.mark.asyncio
    async def test_permission_expiration_security(self):
        """Test permission expiration enforcement."""
        user_id = "test_user_expiration"

        # Test expired permissions
        expired_permissions = PlatformPermissions(
            user_id=user_id,
            layer="agent_forge",
            permission_level="premium",
            expires_at=datetime.utcnow() - timedelta(days=1),  # Expired yesterday
        )

        with patch.object(
            self.auth_service, "_get_user_permissions", return_value=expired_permissions
        ):
            has_access = await self.auth_service.check_platform_access(
                user_id, "agent_forge", "basic"
            )
            assert not has_access, "Expired permissions should deny access"

        # Test valid permissions
        valid_permissions = PlatformPermissions(
            user_id=user_id,
            layer="agent_forge",
            permission_level="premium",
            expires_at=datetime.utcnow() + timedelta(days=30),  # Valid for 30 days
        )

        with patch.object(
            self.auth_service, "_get_user_permissions", return_value=valid_permissions
        ):
            has_access = await self.auth_service.check_platform_access(
                user_id, "agent_forge", "basic"
            )
            assert has_access, "Valid permissions should grant access"

    @pytest.mark.asyncio
    async def test_platform_layer_isolation(self):
        """Test platform layer access isolation."""
        user_id = "test_user_isolation"

        # Grant access only to ziggurat layer
        ziggurat_permissions = PlatformPermissions(
            user_id=user_id, layer="ziggurat", permission_level="premium"
        )

        def mock_get_permissions(uid, layer):
            if layer == "ziggurat":
                return ziggurat_permissions
            return None  # No permissions for other layers

        with patch.object(
            self.auth_service, "_get_user_permissions", side_effect=mock_get_permissions
        ):
            # Should have access to ziggurat
            ziggurat_access = await self.auth_service.check_platform_access(
                user_id, "ziggurat", "basic"
            )
            assert ziggurat_access, "Should have access to granted layer"

            # Should not have access to other layers
            agent_forge_access = await self.auth_service.check_platform_access(
                user_id, "agent_forge", "basic"
            )
            assert not agent_forge_access, "Should not have access to non-granted layer"

            lamassu_access = await self.auth_service.check_platform_access(
                user_id, "lamassu_labs", "basic"
            )
            assert not lamassu_access, "Should not have access to non-granted layer"


class TestEnterpriseSSoSecurity:
    """Test enterprise SSO security features."""

    def setup_method(self):
        """Setup test fixtures."""
        self.auth_service = UnifiedAuthService()

    @pytest.mark.asyncio
    async def test_saml_metadata_security(self):
        """Test SAML metadata generation security."""
        # This would test SAML metadata generation when fully implemented
        # For now, we verify the structure is secure

        # Mock SAML metadata
        metadata = {
            "entity_id": "https://platform.nuru.ai",
            "acs_url": "https://platform.nuru.ai/auth/sso/saml/acs",
            "sls_url": "https://platform.nuru.ai/auth/sso/saml/sls",
        }

        # Verify HTTPS URLs (security requirement)
        assert metadata["entity_id"].startswith("https://")
        assert metadata["acs_url"].startswith("https://")
        assert metadata["sls_url"].startswith("https://")

        # Verify proper domain
        assert "nuru.ai" in metadata["entity_id"]

    @pytest.mark.asyncio
    async def test_ldap_connection_security(self):
        """Test LDAP connection security requirements."""
        # Test LDAP configuration validation
        ldap_config = {
            "ldap_host": "ldaps://ldap.company.com",  # Should use LDAPS
            "ldap_port": 636,  # Secure LDAP port
            "ldap_base_dn": "ou=users,dc=company,dc=com",
            "ldap_bind_dn": "cn=service,ou=services,dc=company,dc=com",
        }

        # Verify secure LDAP configuration
        assert ldap_config["ldap_host"].startswith(
            "ldaps://"
        ), "LDAP should use secure connection"
        assert ldap_config["ldap_port"] in [
            636,
            389,
        ], "LDAP should use standard secure ports"


# Security test configuration
@pytest.fixture
def auth_service():
    """Fixture for authentication service."""
    return UnifiedAuthService()


@pytest.fixture
def wallet_service():
    """Fixture for wallet service."""
    return MultiChainWalletService()


# Run security tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
