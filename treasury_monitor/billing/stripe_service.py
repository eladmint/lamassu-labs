"""
Treasury Monitor Stripe Billing Service
Production-ready billing integration with Stripe for subscription management.
"""

import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import asyncpg
import stripe

logger = logging.getLogger(__name__)


class BillingError(Exception):
    """Base billing error"""

    pass


class SubscriptionNotFoundError(BillingError):
    """Subscription not found"""

    pass


class PlanNotFoundError(BillingError):
    """Subscription plan not found"""

    pass


class StripeService:
    """Production-ready Stripe billing service for Treasury Monitor"""

    def __init__(
        self, db_pool: asyncpg.Pool, stripe_secret_key: str, webhook_secret: str = None
    ):
        self.db_pool = db_pool
        stripe.api_key = stripe_secret_key
        self.webhook_secret = webhook_secret

        # Stripe product IDs for Treasury Monitor plans
        self.stripe_products = {
            "small_dao": "prod_treasury_small_dao",
            "medium_org": "prod_treasury_medium_org",
            "enterprise": "prod_treasury_enterprise",
        }

    async def create_customer(self, user_id: str, email: str, name: str = None) -> str:
        """
        Create Stripe customer for user.

        Args:
            user_id: Internal user ID
            email: Customer email
            name: Customer name

        Returns:
            Stripe customer ID
        """
        try:
            customer = stripe.Customer.create(
                email=email, name=name, metadata={"user_id": user_id}
            )
            return customer.id
        except stripe.error.StripeError as e:
            logger.error(f"Failed to create Stripe customer: {str(e)}")
            raise BillingError(f"Failed to create customer: {str(e)}")

    async def get_subscription_plans(self) -> List[Dict[str, Any]]:
        """Get all available subscription plans"""
        async with self.db_pool.acquire() as conn:
            plans = await conn.fetch(
                """
                SELECT id, name, description, price_cents, currency, billing_interval,
                       max_addresses, features, stripe_price_id
                FROM subscription_plans
                WHERE is_active = TRUE
                ORDER BY price_cents ASC
                """
            )

            return [
                {
                    "id": str(plan["id"]),
                    "name": plan["name"],
                    "description": plan["description"],
                    "price_cents": plan["price_cents"],
                    "price_dollars": plan["price_cents"] / 100,
                    "currency": plan["currency"],
                    "billing_interval": plan["billing_interval"],
                    "max_addresses": plan["max_addresses"],
                    "features": plan["features"],
                    "stripe_price_id": plan["stripe_price_id"],
                }
                for plan in plans
            ]

    async def create_subscription(
        self,
        user_id: str,
        plan_id: str,
        payment_method_id: str = None,
        trial_days: int = None,
    ) -> Dict[str, Any]:
        """
        Create subscription for user.

        Args:
            user_id: Internal user ID
            plan_id: Subscription plan ID
            payment_method_id: Stripe payment method ID
            trial_days: Optional trial period in days

        Returns:
            Subscription data with payment status
        """
        async with self.db_pool.acquire() as conn:
            # Get user and plan details
            user = await conn.fetchrow(
                "SELECT id, email, first_name, last_name, company FROM users WHERE id = $1",
                uuid.UUID(user_id),
            )
            if not user:
                raise BillingError("User not found")

            plan = await conn.fetchrow(
                "SELECT id, stripe_price_id, name FROM subscription_plans WHERE id = $1",
                uuid.UUID(plan_id),
            )
            if not plan:
                raise PlanNotFoundError("Plan not found")

            try:
                # Create or get Stripe customer
                customer_name = (
                    f"{user['first_name'] or ''} {user['last_name'] or ''}".strip()
                )
                if user["company"]:
                    customer_name = f"{customer_name} ({user['company']})"

                stripe_customer_id = await self.create_customer(
                    user_id, user["email"], customer_name
                )

                # Attach payment method if provided
                if payment_method_id:
                    stripe.PaymentMethod.attach(
                        payment_method_id, customer=stripe_customer_id
                    )

                    # Set as default payment method
                    stripe.Customer.modify(
                        stripe_customer_id,
                        invoice_settings={"default_payment_method": payment_method_id},
                    )

                # Create subscription
                subscription_params = {
                    "customer": stripe_customer_id,
                    "items": [{"price": plan["stripe_price_id"]}],
                    "metadata": {
                        "user_id": user_id,
                        "plan_id": plan_id,
                        "plan_name": plan["name"],
                    },
                    "expand": ["latest_invoice.payment_intent"],
                }

                if trial_days:
                    subscription_params["trial_period_days"] = trial_days

                subscription = stripe.Subscription.create(**subscription_params)

                # Store subscription in database
                subscription_id = await conn.fetchval(
                    """
                    INSERT INTO user_subscriptions
                    (user_id, plan_id, stripe_subscription_id, stripe_customer_id,
                     status, current_period_start, current_period_end, trial_start, trial_end)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                    RETURNING id
                    """,
                    uuid.UUID(user_id),
                    uuid.UUID(plan_id),
                    subscription.id,
                    stripe_customer_id,
                    subscription.status,
                    datetime.fromtimestamp(
                        subscription.current_period_start, timezone.utc
                    ),
                    datetime.fromtimestamp(
                        subscription.current_period_end, timezone.utc
                    ),
                    (
                        datetime.fromtimestamp(subscription.trial_start, timezone.utc)
                        if subscription.trial_start
                        else None
                    ),
                    (
                        datetime.fromtimestamp(subscription.trial_end, timezone.utc)
                        if subscription.trial_end
                        else None
                    ),
                )

                return {
                    "subscription_id": str(subscription_id),
                    "stripe_subscription_id": subscription.id,
                    "status": subscription.status,
                    "client_secret": (
                        subscription.latest_invoice.payment_intent.client_secret
                        if subscription.latest_invoice.payment_intent
                        else None
                    ),
                    "current_period_end": datetime.fromtimestamp(
                        subscription.current_period_end, timezone.utc
                    ).isoformat(),
                    "trial_end": (
                        datetime.fromtimestamp(
                            subscription.trial_end, timezone.utc
                        ).isoformat()
                        if subscription.trial_end
                        else None
                    ),
                }

            except stripe.error.StripeError as e:
                logger.error(f"Stripe subscription creation failed: {str(e)}")
                raise BillingError(f"Failed to create subscription: {str(e)}")

    async def get_user_subscription(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user's current subscription"""
        async with self.db_pool.acquire() as conn:
            subscription = await conn.fetchrow(
                """
                SELECT us.id, us.stripe_subscription_id, us.status,
                       us.current_period_start, us.current_period_end,
                       us.cancel_at_period_end, us.trial_end,
                       sp.name as plan_name, sp.price_cents, sp.max_addresses, sp.features
                FROM user_subscriptions us
                JOIN subscription_plans sp ON us.plan_id = sp.id
                WHERE us.user_id = $1 AND us.status IN ('active', 'trialing', 'past_due')
                ORDER BY us.created_at DESC
                LIMIT 1
                """,
                uuid.UUID(user_id),
            )

            if not subscription:
                return None

            return {
                "id": str(subscription["id"]),
                "stripe_subscription_id": subscription["stripe_subscription_id"],
                "status": subscription["status"],
                "plan_name": subscription["plan_name"],
                "price_cents": subscription["price_cents"],
                "price_dollars": subscription["price_cents"] / 100,
                "max_addresses": subscription["max_addresses"],
                "features": subscription["features"],
                "current_period_start": subscription[
                    "current_period_start"
                ].isoformat(),
                "current_period_end": subscription["current_period_end"].isoformat(),
                "cancel_at_period_end": subscription["cancel_at_period_end"],
                "trial_end": (
                    subscription["trial_end"].isoformat()
                    if subscription["trial_end"]
                    else None
                ),
            }

    async def cancel_subscription(self, user_id: str, immediate: bool = False) -> bool:
        """
        Cancel user's subscription.

        Args:
            user_id: User ID
            immediate: If True, cancel immediately; if False, cancel at period end

        Returns:
            True if cancellation successful
        """
        async with self.db_pool.acquire() as conn:
            subscription = await conn.fetchrow(
                """
                SELECT stripe_subscription_id
                FROM user_subscriptions
                WHERE user_id = $1 AND status IN ('active', 'trialing')
                ORDER BY created_at DESC
                LIMIT 1
                """,
                uuid.UUID(user_id),
            )

            if not subscription:
                raise SubscriptionNotFoundError("No active subscription found")

            try:
                if immediate:
                    # Cancel immediately
                    stripe.Subscription.delete(subscription["stripe_subscription_id"])
                    await conn.execute(
                        """
                        UPDATE user_subscriptions
                        SET status = 'canceled', canceled_at = NOW()
                        WHERE stripe_subscription_id = $1
                        """,
                        subscription["stripe_subscription_id"],
                    )
                else:
                    # Cancel at period end
                    stripe.Subscription.modify(
                        subscription["stripe_subscription_id"],
                        cancel_at_period_end=True,
                    )
                    await conn.execute(
                        """
                        UPDATE user_subscriptions
                        SET cancel_at_period_end = TRUE
                        WHERE stripe_subscription_id = $1
                        """,
                        subscription["stripe_subscription_id"],
                    )

                return True

            except stripe.error.StripeError as e:
                logger.error(f"Stripe subscription cancellation failed: {str(e)}")
                raise BillingError(f"Failed to cancel subscription: {str(e)}")

    async def reactivate_subscription(self, user_id: str) -> bool:
        """Reactivate a cancelled subscription (before period end)"""
        async with self.db_pool.acquire() as conn:
            subscription = await conn.fetchrow(
                """
                SELECT stripe_subscription_id
                FROM user_subscriptions
                WHERE user_id = $1 AND cancel_at_period_end = TRUE AND status = 'active'
                ORDER BY created_at DESC
                LIMIT 1
                """,
                uuid.UUID(user_id),
            )

            if not subscription:
                raise SubscriptionNotFoundError("No cancellable subscription found")

            try:
                # Remove cancellation
                stripe.Subscription.modify(
                    subscription["stripe_subscription_id"], cancel_at_period_end=False
                )

                await conn.execute(
                    """
                    UPDATE user_subscriptions
                    SET cancel_at_period_end = FALSE
                    WHERE stripe_subscription_id = $1
                    """,
                    subscription["stripe_subscription_id"],
                )

                return True

            except stripe.error.StripeError as e:
                logger.error(f"Stripe subscription reactivation failed: {str(e)}")
                raise BillingError(f"Failed to reactivate subscription: {str(e)}")

    async def update_subscription_plan(
        self, user_id: str, new_plan_id: str
    ) -> Dict[str, Any]:
        """Update user's subscription to a different plan"""
        async with self.db_pool.acquire() as conn:
            # Get current subscription and new plan
            current_sub = await conn.fetchrow(
                """
                SELECT id, stripe_subscription_id, plan_id
                FROM user_subscriptions
                WHERE user_id = $1 AND status IN ('active', 'trialing')
                ORDER BY created_at DESC
                LIMIT 1
                """,
                uuid.UUID(user_id),
            )

            if not current_sub:
                raise SubscriptionNotFoundError("No active subscription found")

            new_plan = await conn.fetchrow(
                "SELECT stripe_price_id FROM subscription_plans WHERE id = $1",
                uuid.UUID(new_plan_id),
            )

            if not new_plan:
                raise PlanNotFoundError("New plan not found")

            try:
                # Get current Stripe subscription
                subscription = stripe.Subscription.retrieve(
                    current_sub["stripe_subscription_id"]
                )

                # Update subscription item
                stripe.Subscription.modify(
                    current_sub["stripe_subscription_id"],
                    items=[
                        {
                            "id": subscription["items"]["data"][0].id,
                            "price": new_plan["stripe_price_id"],
                        }
                    ],
                    proration_behavior="create_prorations",  # Prorate the change
                )

                # Update database
                await conn.execute(
                    "UPDATE user_subscriptions SET plan_id = $1 WHERE id = $2",
                    uuid.UUID(new_plan_id),
                    current_sub["id"],
                )

                return await self.get_user_subscription(user_id)

            except stripe.error.StripeError as e:
                logger.error(f"Stripe subscription update failed: {str(e)}")
                raise BillingError(f"Failed to update subscription: {str(e)}")

    async def get_payment_history(
        self, user_id: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get user's payment history"""
        async with self.db_pool.acquire() as conn:
            payments = await conn.fetch(
                """
                SELECT stripe_payment_intent_id, amount_cents, currency, status,
                       failure_reason, created_at
                FROM payment_history
                WHERE user_id = $1
                ORDER BY created_at DESC
                LIMIT $2
                """,
                uuid.UUID(user_id),
                limit,
            )

            return [
                {
                    "id": payment["stripe_payment_intent_id"],
                    "amount_cents": payment["amount_cents"],
                    "amount_dollars": payment["amount_cents"] / 100,
                    "currency": payment["currency"],
                    "status": payment["status"],
                    "failure_reason": payment["failure_reason"],
                    "created_at": payment["created_at"].isoformat(),
                }
                for payment in payments
            ]

    async def handle_webhook(self, payload: bytes, signature: str) -> bool:
        """
        Handle Stripe webhook events.

        Args:
            payload: Raw webhook payload
            signature: Stripe signature header

        Returns:
            True if event handled successfully
        """
        if not self.webhook_secret:
            logger.warning("Webhook secret not configured, skipping verification")
            return False

        try:
            event = stripe.Webhook.construct_event(
                payload, signature, self.webhook_secret
            )
        except stripe.error.SignatureVerificationError:
            logger.error("Invalid webhook signature")
            return False

        # Handle different event types
        if event["type"] == "invoice.payment_succeeded":
            await self._handle_payment_succeeded(event["data"]["object"])
        elif event["type"] == "invoice.payment_failed":
            await self._handle_payment_failed(event["data"]["object"])
        elif event["type"] == "customer.subscription.updated":
            await self._handle_subscription_updated(event["data"]["object"])
        elif event["type"] == "customer.subscription.deleted":
            await self._handle_subscription_deleted(event["data"]["object"])

        return True

    async def _handle_payment_succeeded(self, invoice):
        """Handle successful payment"""
        subscription_id = invoice.get("subscription")
        if not subscription_id:
            return

        async with self.db_pool.acquire() as conn:
            # Update subscription status
            await conn.execute(
                """
                UPDATE user_subscriptions
                SET status = 'active'
                WHERE stripe_subscription_id = $1
                """,
                subscription_id,
            )

            # Record payment
            user_id = await conn.fetchval(
                "SELECT user_id FROM user_subscriptions WHERE stripe_subscription_id = $1",
                subscription_id,
            )

            if user_id:
                await conn.execute(
                    """
                    INSERT INTO payment_history
                    (user_id, stripe_payment_intent_id, amount_cents, currency, status)
                    VALUES ($1, $2, $3, $4, 'succeeded')
                    """,
                    user_id,
                    invoice.get("payment_intent"),
                    invoice.get("amount_paid", 0),
                    invoice.get("currency", "usd"),
                )

    async def _handle_payment_failed(self, invoice):
        """Handle failed payment"""
        subscription_id = invoice.get("subscription")
        if not subscription_id:
            return

        async with self.db_pool.acquire() as conn:
            # Update subscription status
            await conn.execute(
                """
                UPDATE user_subscriptions
                SET status = 'past_due'
                WHERE stripe_subscription_id = $1
                """,
                subscription_id,
            )

            # Record failed payment
            user_id = await conn.fetchval(
                "SELECT user_id FROM user_subscriptions WHERE stripe_subscription_id = $1",
                subscription_id,
            )

            if user_id:
                await conn.execute(
                    """
                    INSERT INTO payment_history
                    (user_id, stripe_payment_intent_id, amount_cents, currency, status, failure_reason)
                    VALUES ($1, $2, $3, $4, 'failed', $5)
                    """,
                    user_id,
                    invoice.get("payment_intent"),
                    invoice.get("amount_due", 0),
                    invoice.get("currency", "usd"),
                    invoice.get("charge", {}).get("failure_message"),
                )

    async def _handle_subscription_updated(self, subscription):
        """Handle subscription updates"""
        async with self.db_pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE user_subscriptions
                SET status = $1, current_period_start = $2, current_period_end = $3,
                    cancel_at_period_end = $4
                WHERE stripe_subscription_id = $5
                """,
                subscription["status"],
                datetime.fromtimestamp(
                    subscription["current_period_start"], timezone.utc
                ),
                datetime.fromtimestamp(
                    subscription["current_period_end"], timezone.utc
                ),
                subscription.get("cancel_at_period_end", False),
                subscription["id"],
            )

    async def _handle_subscription_deleted(self, subscription):
        """Handle subscription deletion"""
        async with self.db_pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE user_subscriptions
                SET status = 'canceled', canceled_at = NOW()
                WHERE stripe_subscription_id = $1
                """,
                subscription["id"],
            )
