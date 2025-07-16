"""
Treasury Monitor Authentication Service
Production-ready authentication with JWT tokens, password hashing, and session management.
"""

import logging
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import asyncpg
import bcrypt
import jwt
from email_validator import EmailNotValidError, validate_email

logger = logging.getLogger(__name__)


class AuthenticationError(Exception):
    """Base authentication error"""

    pass


class InvalidCredentialsError(AuthenticationError):
    """Invalid username/password"""

    pass


class UserNotFoundError(AuthenticationError):
    """User not found"""

    pass


class EmailAlreadyExistsError(AuthenticationError):
    """Email already registered"""

    pass


class AuthService:
    """Production-ready authentication service for Treasury Monitor"""

    def __init__(self, db_pool: asyncpg.Pool, jwt_secret: str):
        self.db_pool = db_pool
        self.jwt_secret = jwt_secret
        self.jwt_algorithm = "HS256"
        self.access_token_expire_hours = 24
        self.refresh_token_expire_days = 30

    async def register_user(
        self,
        email: str,
        password: str,
        first_name: str = None,
        last_name: str = None,
        company: str = None,
    ) -> Dict[str, Any]:
        """
        Register a new user with email verification.

        Args:
            email: User's email address
            password: Plain text password
            first_name: Optional first name
            last_name: Optional last name
            company: Optional company name

        Returns:
            User data with verification token

        Raises:
            EmailAlreadyExistsError: If email is already registered
        """
        # Validate email format
        try:
            valid_email = validate_email(email)
            email = valid_email.email
        except EmailNotValidError as e:
            raise AuthenticationError(f"Invalid email format: {str(e)}")

        # Validate password strength
        if len(password) < 8:
            raise AuthenticationError("Password must be at least 8 characters long")

        # Hash password
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        # Generate email verification token
        verification_token = secrets.token_urlsafe(32)

        async with self.db_pool.acquire() as conn:
            # Check if email already exists
            existing_user = await conn.fetchrow(
                "SELECT id FROM users WHERE email = $1", email
            )
            if existing_user:
                raise EmailAlreadyExistsError("Email address already registered")

            # Create user
            user_id = await conn.fetchval(
                """
                INSERT INTO users (email, password_hash, first_name, last_name, company, email_verification_token)
                VALUES ($1, $2, $3, $4, $5, $6)
                RETURNING id
                """,
                email,
                password_hash,
                first_name,
                last_name,
                company,
                verification_token,
            )

            # Return user data (without password hash)
            return {
                "id": str(user_id),
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "company": company,
                "email_verified": False,
                "verification_token": verification_token,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }

    async def verify_email(self, verification_token: str) -> bool:
        """
        Verify user's email address using verification token.

        Args:
            verification_token: Email verification token

        Returns:
            True if verification successful
        """
        async with self.db_pool.acquire() as conn:
            result = await conn.execute(
                """
                UPDATE users
                SET email_verified = TRUE, email_verification_token = NULL
                WHERE email_verification_token = $1 AND email_verified = FALSE
                """,
                verification_token,
            )
            return result == "UPDATE 1"

    async def authenticate_user(self, email: str, password: str) -> Dict[str, Any]:
        """
        Authenticate user with email and password.

        Args:
            email: User's email address
            password: Plain text password

        Returns:
            User data and tokens

        Raises:
            InvalidCredentialsError: If credentials are invalid
        """
        async with self.db_pool.acquire() as conn:
            user = await conn.fetchrow(
                """
                SELECT id, email, password_hash, first_name, last_name, company,
                       email_verified, is_active, last_login
                FROM users
                WHERE email = $1
                """,
                email,
            )

            if not user:
                raise InvalidCredentialsError("Invalid email or password")

            # Check password
            if not bcrypt.checkpw(
                password.encode("utf-8"), user["password_hash"].encode("utf-8")
            ):
                raise InvalidCredentialsError("Invalid email or password")

            # Check if user is active
            if not user["is_active"]:
                raise AuthenticationError("Account is deactivated")

            # Update last login
            await conn.execute(
                "UPDATE users SET last_login = NOW() WHERE id = $1", user["id"]
            )

            # Generate tokens
            access_token = self._generate_access_token(user["id"])
            refresh_token = await self._generate_refresh_token(user["id"])

            return {
                "user": {
                    "id": str(user["id"]),
                    "email": user["email"],
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                    "company": user["company"],
                    "email_verified": user["email_verified"],
                    "last_login": (
                        user["last_login"].isoformat() if user["last_login"] else None
                    ),
                },
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
            }

    async def verify_access_token(self, token: str) -> Dict[str, Any]:
        """
        Verify and decode access token.

        Args:
            token: JWT access token

        Returns:
            Token payload with user info

        Raises:
            AuthenticationError: If token is invalid
        """
        try:
            payload = jwt.decode(
                token, self.jwt_secret, algorithms=[self.jwt_algorithm]
            )

            # Check expiration
            if datetime.fromtimestamp(payload["exp"], timezone.utc) < datetime.now(
                timezone.utc
            ):
                raise AuthenticationError("Token has expired")

            # Get current user data
            async with self.db_pool.acquire() as conn:
                user = await conn.fetchrow(
                    "SELECT id, email, first_name, last_name, is_active FROM users WHERE id = $1",
                    uuid.UUID(payload["user_id"]),
                )

                if not user or not user["is_active"]:
                    raise AuthenticationError("User not found or inactive")

                return {
                    "user_id": str(user["id"]),
                    "email": user["email"],
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                }

        except jwt.InvalidTokenError as e:
            raise AuthenticationError(f"Invalid token: {str(e)}")

    async def refresh_access_token(self, refresh_token: str) -> Dict[str, str]:
        """
        Generate new access token using refresh token.

        Args:
            refresh_token: Valid refresh token

        Returns:
            New access token
        """
        async with self.db_pool.acquire() as conn:
            session = await conn.fetchrow(
                """
                SELECT user_id FROM user_sessions
                WHERE session_token = $1 AND expires_at > NOW()
                """,
                refresh_token,
            )

            if not session:
                raise AuthenticationError("Invalid or expired refresh token")

            # Update session last accessed
            await conn.execute(
                "UPDATE user_sessions SET last_accessed = NOW() WHERE session_token = $1",
                refresh_token,
            )

            # Generate new access token
            access_token = self._generate_access_token(session["user_id"])

            return {"access_token": access_token, "token_type": "bearer"}

    async def logout(self, refresh_token: str) -> bool:
        """
        Logout user by invalidating refresh token.

        Args:
            refresh_token: Refresh token to invalidate

        Returns:
            True if logout successful
        """
        async with self.db_pool.acquire() as conn:
            result = await conn.execute(
                "DELETE FROM user_sessions WHERE session_token = $1", refresh_token
            )
            return result == "DELETE 1"

    async def reset_password_request(self, email: str) -> str:
        """
        Generate password reset token for user.

        Args:
            email: User's email address

        Returns:
            Password reset token

        Raises:
            UserNotFoundError: If user not found
        """
        reset_token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=1)  # 1 hour expiry

        async with self.db_pool.acquire() as conn:
            result = await conn.execute(
                """
                UPDATE users
                SET password_reset_token = $1, password_reset_expires = $2
                WHERE email = $3 AND is_active = TRUE
                """,
                reset_token,
                expires_at,
                email,
            )

            if result == "UPDATE 0":
                raise UserNotFoundError("User not found")

            return reset_token

    async def reset_password(self, reset_token: str, new_password: str) -> bool:
        """
        Reset user's password using reset token.

        Args:
            reset_token: Password reset token
            new_password: New plain text password

        Returns:
            True if reset successful
        """
        # Validate password strength
        if len(new_password) < 8:
            raise AuthenticationError("Password must be at least 8 characters long")

        # Hash new password
        password_hash = bcrypt.hashpw(
            new_password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        async with self.db_pool.acquire() as conn:
            result = await conn.execute(
                """
                UPDATE users
                SET password_hash = $1, password_reset_token = NULL, password_reset_expires = NULL
                WHERE password_reset_token = $2 AND password_reset_expires > NOW()
                """,
                password_hash,
                reset_token,
            )

            return result == "UPDATE 1"

    def _generate_access_token(self, user_id: uuid.UUID) -> str:
        """Generate JWT access token"""
        payload = {
            "user_id": str(user_id),
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc)
            + timedelta(hours=self.access_token_expire_hours),
            "type": "access",
        }
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)

    async def _generate_refresh_token(self, user_id: uuid.UUID) -> str:
        """Generate and store refresh token"""
        session_token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(
            days=self.refresh_token_expire_days
        )

        async with self.db_pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO user_sessions (user_id, session_token, expires_at)
                VALUES ($1, $2, $3)
                """,
                user_id,
                session_token,
                expires_at,
            )

        return session_token

    async def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile information"""
        async with self.db_pool.acquire() as conn:
            user = await conn.fetchrow(
                """
                SELECT id, email, first_name, last_name, company,
                       email_verified, created_at, last_login
                FROM users
                WHERE id = $1 AND is_active = TRUE
                """,
                uuid.UUID(user_id),
            )

            if not user:
                raise UserNotFoundError("User not found")

            return {
                "id": str(user["id"]),
                "email": user["email"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "company": user["company"],
                "email_verified": user["email_verified"],
                "created_at": user["created_at"].isoformat(),
                "last_login": (
                    user["last_login"].isoformat() if user["last_login"] else None
                ),
            }

    async def update_user_profile(
        self,
        user_id: str,
        first_name: str = None,
        last_name: str = None,
        company: str = None,
    ) -> Dict[str, Any]:
        """Update user profile information"""
        updates = []
        values = []

        if first_name is not None:
            updates.append(f"first_name = ${len(values) + 2}")
            values.append(first_name)

        if last_name is not None:
            updates.append(f"last_name = ${len(values) + 2}")
            values.append(last_name)

        if company is not None:
            updates.append(f"company = ${len(values) + 2}")
            values.append(company)

        if not updates:
            return await self.get_user_profile(user_id)

        query = f"""
            UPDATE users
            SET {', '.join(updates)}
            WHERE id = $1 AND is_active = TRUE
            RETURNING id, email, first_name, last_name, company, email_verified, created_at
        """

        async with self.db_pool.acquire() as conn:
            user = await conn.fetchrow(query, uuid.UUID(user_id), *values)

            if not user:
                raise UserNotFoundError("User not found")

            return {
                "id": str(user["id"]),
                "email": user["email"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "company": user["company"],
                "email_verified": user["email_verified"],
                "created_at": user["created_at"].isoformat(),
            }
