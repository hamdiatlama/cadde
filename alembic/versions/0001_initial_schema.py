"""initial schema - all tables from all modules

Revision ID: 0001
Revises:
Create Date: 2026-06-13
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=False),
        sa.Column("role", sa.String(), server_default="customer"),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("points", sa.Integer(), server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_phone", "users", ["phone"], unique=True)
    op.create_index("ix_users_id", "users", ["id"])

    op.create_table(
        "sellers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), unique=True),
        sa.Column("store_name", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("rating", sa.Float(), server_default=sa.text("0")),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sellers_id", "sellers", ["id"])
    op.create_index("ix_sellers_slug", "sellers", ["slug"], unique=True)

    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("seller_id", sa.Integer(), sa.ForeignKey("sellers.id"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(), nullable=True),
        sa.Column("subcategory", sa.String(), nullable=True),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("compare_price", sa.Float(), nullable=True),
        sa.Column("original_price", sa.Float(), nullable=True),
        sa.Column("discount_start_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("image_url", sa.String(), nullable=True),
        sa.Column("stock", sa.Integer(), server_default=sa.text("0")),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("is_discounted", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("original_product_id", sa.Integer(), sa.ForeignKey("products.id"), nullable=True),
        sa.Column("tags", sa.String(), nullable=True),
        sa.Column("color", sa.String(), nullable=True),
        sa.Column("occasion", sa.String(), nullable=True),
        sa.Column("care_instructions", sa.Text(), nullable=True),
        sa.Column("season_start_month", sa.Integer(), nullable=True),
        sa.Column("season_end_month", sa.Integer(), nullable=True),
        sa.Column("is_express_eligible", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("rating", sa.Float(), server_default=sa.text("0")),
        sa.Column("review_count", sa.Integer(), server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_products_id", "products", ["id"])
    op.create_index("ix_products_category", "products", ["category"])
    op.create_index("ix_products_subcategory", "products", ["subcategory"])
    op.create_index("ix_products_occasion", "products", ["occasion"])
    op.create_index("ix_products_slug", "products", ["slug"])

    op.create_table(
        "questions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("answer", sa.Text(), nullable=True),
        sa.Column("is_answered", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("is_public", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("answered_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_questions_id", "questions", ["id"])

    op.create_table(
        "carts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_carts_id", "carts", ["id"])

    op.create_table(
        "cart_items",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("cart_id", sa.Integer(), sa.ForeignKey("carts.id"), nullable=False),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("quantity", sa.Integer(), server_default=sa.text("1")),
        sa.Column("variant_label", sa.String(), nullable=True),
        sa.Column("added_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_cart_items_id", "cart_items", ["id"])

    op.create_table(
        "addresses",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("full_address", sa.Text(), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("is_default", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_addresses_id", "addresses", ["id"])

    op.create_table(
        "payment_methods",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("provider", sa.String(), nullable=True),
        sa.Column("is_default", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_payment_methods_id", "payment_methods", ["id"])

    op.create_table(
        "couriers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), unique=True, nullable=False),
        sa.Column("is_available", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("status", sa.String(), server_default="offline"),
        sa.Column("current_latitude", sa.Float(), nullable=True),
        sa.Column("current_longitude", sa.Float(), nullable=True),
        sa.Column("current_speed_kmh", sa.Float(), server_default=sa.text("0")),
        sa.Column("current_heading", sa.Float(), server_default=sa.text("0")),
        sa.Column("current_accuracy_m", sa.Float(), server_default=sa.text("0")),
        sa.Column("last_location_update", sa.DateTime(timezone=True), nullable=True),
        sa.Column("gps_spoofing_score", sa.Float(), server_default=sa.text("0")),
        sa.Column("consecutive_anomalies", sa.Integer(), server_default=sa.text("0")),
        sa.Column("last_anomaly_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("total_deliveries", sa.Integer(), server_default=sa.text("0")),
        sa.Column("total_distance_km", sa.Float(), server_default=sa.text("0")),
        sa.Column("rating", sa.Float(), server_default=sa.text("0")),
        sa.Column("total_ratings", sa.Integer(), server_default=sa.text("0")),
        sa.Column("vehicle_type", sa.String(), server_default="motorcycle"),
        sa.Column("vehicle_plate", sa.String(), nullable=True),
        sa.Column("max_load_kg", sa.Float(), server_default=sa.text("50")),
        sa.Column("service_zone", sa.String(), nullable=True),
        sa.Column("max_delivery_radius_km", sa.Float(), server_default=sa.text("10")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_couriers_id", "couriers", ["id"])

    op.create_table(
        "courier_location_history",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("courier_id", sa.Integer(), sa.ForeignKey("couriers.id"), nullable=False),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("speed_kmh", sa.Float(), server_default=sa.text("0")),
        sa.Column("heading", sa.Float(), server_default=sa.text("0")),
        sa.Column("accuracy_m", sa.Float(), server_default=sa.text("0")),
        sa.Column("source", sa.String(), server_default="gps"),
        sa.Column("was_anomaly", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "drivers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), unique=True, nullable=False),
        sa.Column("is_available", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("current_latitude", sa.Float(), nullable=True),
        sa.Column("current_longitude", sa.Float(), nullable=True),
        sa.Column("current_speed_kmh", sa.Float(), server_default=sa.text("0")),
        sa.Column("current_heading", sa.Float(), server_default=sa.text("0")),
        sa.Column("current_accuracy_m", sa.Float(), server_default=sa.text("0")),
        sa.Column("last_location_update", sa.DateTime(timezone=True), nullable=True),
        sa.Column("total_rides", sa.Integer(), server_default=sa.text("0")),
        sa.Column("cancelled_rides", sa.Integer(), server_default=sa.text("0")),
        sa.Column("gps_spoofing_score", sa.Float(), server_default=sa.text("0")),
        sa.Column("consecutive_anomalies", sa.Integer(), server_default=sa.text("0")),
        sa.Column("penalty_until", sa.DateTime(timezone=True), nullable=True),
        sa.Column("rating", sa.Float(), server_default=sa.text("0")),
        sa.Column("total_ratings", sa.Integer(), server_default=sa.text("0")),
        sa.Column("phone_verified", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("license_plate", sa.String(), nullable=True),
        sa.Column("vehicle_model", sa.String(), nullable=True),
        sa.Column("vehicle_color", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_drivers_id", "drivers", ["id"])

    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("seller_id", sa.Integer(), sa.ForeignKey("sellers.id"), nullable=False),
        sa.Column("courier_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("status", sa.String(), server_default="pending_approval"),
        sa.Column("subtotal", sa.Float(), nullable=False),
        sa.Column("delivery_fee", sa.Float(), server_default=sa.text("0")),
        sa.Column("total", sa.Float(), nullable=False),
        sa.Column("payment_method", sa.String(), server_default="card"),
        sa.Column("payment_status", sa.String(), server_default="pending"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("recipient_name", sa.String(), nullable=True),
        sa.Column("recipient_phone", sa.String(), nullable=True),
        sa.Column("delivery_address", sa.Text(), nullable=True),
        sa.Column("delivery_latitude", sa.Float(), nullable=True),
        sa.Column("delivery_longitude", sa.Float(), nullable=True),
        sa.Column("scheduled_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("delivery_time_slot", sa.String(), nullable=True),
        sa.Column("is_express", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("express_fee", sa.Float(), server_default=sa.text("0")),
        sa.Column("is_gift", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("gift_card_message", sa.Text(), nullable=True),
        sa.Column("gift_card_sender", sa.String(), nullable=True),
        sa.Column("coupon_code", sa.String(), nullable=True),
        sa.Column("discount_amount", sa.Float(), server_default=sa.text("0")),
        sa.Column("tip_amount", sa.Float(), server_default=sa.text("0")),
        sa.Column("contactless_delivery", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("branch_id", sa.Integer(), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("rejected_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("reject_reason", sa.Text(), nullable=True),
        sa.Column("approval_deadline", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancelled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancel_reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_orders_id", "orders", ["id"])

    op.create_table(
        "restaurants",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("seller_id", sa.Integer(), sa.ForeignKey("sellers.id"), unique=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("cuisine_type", sa.String(), nullable=True),
        sa.Column("cuisine_subtypes", sa.String(), nullable=True),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("logo_url", sa.String(), nullable=True),
        sa.Column("cover_image_url", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("is_open", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("accepts_orders", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("opening_time", sa.String(), server_default="09:00"),
        sa.Column("closing_time", sa.String(), server_default="22:00"),
        sa.Column("closed_days", sa.String(), nullable=True),
        sa.Column("min_order_amount", sa.Float(), server_default=sa.text("0")),
        sa.Column("delivery_fee", sa.Float(), server_default=sa.text("19.90")),
        sa.Column("free_delivery_min_amount", sa.Float(), server_default=sa.text("100")),
        sa.Column("max_delivery_radius_km", sa.Float(), server_default=sa.text("5.0")),
        sa.Column("preparation_time_min", sa.Integer(), server_default=sa.text("20")),
        sa.Column("has_thermal_bags", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("hygiene_rating", sa.String(), server_default="pending"),
        sa.Column("verification_status", sa.String(), server_default="pending"),
        sa.Column("verification_docs", sa.Text(), nullable=True),
        sa.Column("commission_rate", sa.Float(), server_default=sa.text("0.15")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_restaurants_id", "restaurants", ["id"])
    op.create_index("ix_restaurants_cuisine_type", "restaurants", ["cuisine_type"])

    op.create_table(
        "subscription_plans",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("interval_days", sa.Integer(), nullable=False),
        sa.Column("duration_months", sa.Integer(), server_default=sa.text("1")),
        sa.Column("price_per_delivery", sa.Float(), nullable=False),
        sa.Column("total_price", sa.Float(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_subscription_plans_id", "subscription_plans", ["id"])

    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("reference_type", sa.String(), nullable=True),
        sa.Column("reference_id", sa.Integer(), nullable=True),
        sa.Column("is_read", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_notifications_id", "notifications", ["id"])

    op.create_table(
        "support_tickets",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=True),
        sa.Column("subject", sa.String(), nullable=False),
        sa.Column("category", sa.String(), server_default="other"),
        sa.Column("status", sa.String(), server_default="open"),
        sa.Column("priority", sa.String(), server_default="normal"),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_support_tickets_id", "support_tickets", ["id"])

    op.create_table(
        "coupon_codes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.String(), nullable=False, unique=True),
        sa.Column("discount_type", sa.String(), server_default="percentage"),
        sa.Column("discount_value", sa.Float(), nullable=False),
        sa.Column("min_order_amount", sa.Float(), server_default=sa.text("0")),
        sa.Column("max_uses", sa.Integer(), nullable=True),
        sa.Column("current_uses", sa.Integer(), server_default=sa.text("0")),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_coupon_codes_code", "coupon_codes", ["code"], unique=True)


def downgrade() -> None:
    op.drop_table("coupon_codes")
    op.drop_table("support_tickets")
    op.drop_table("notifications")
    op.drop_table("subscription_plans")
    op.drop_table("restaurants")
    op.drop_table("orders")
    op.drop_table("drivers")
    op.drop_table("courier_location_history")
    op.drop_table("couriers")
    op.drop_table("payment_methods")
    op.drop_table("addresses")
    op.drop_table("cart_items")
    op.drop_table("carts")
    op.drop_table("questions")
    op.drop_table("products")
    op.drop_table("sellers")
    op.drop_table("users")
