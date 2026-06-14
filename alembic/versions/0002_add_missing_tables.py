"""add missing tables (food, support, payments, subscriptions, reviews, bina)

Revision ID: 0002
Revises: 0001
Create Date: 2026-06-14
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── Food: Restaurant Branches (already has restaurants from 0001) ──
    op.create_table(
        "restaurant_branches",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("restaurant_id", sa.Integer(), sa.ForeignKey("restaurants.id"), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("opening_time", sa.String(), nullable=True),
        sa.Column("closing_time", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_branches_restaurant", "restaurant_branches", ["restaurant_id"])

    op.create_table(
        "delivery_zones",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("restaurant_id", sa.Integer(), sa.ForeignKey("restaurants.id"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("min_latitude", sa.Float(), nullable=False),
        sa.Column("max_latitude", sa.Float(), nullable=False),
        sa.Column("min_longitude", sa.Float(), nullable=False),
        sa.Column("max_longitude", sa.Float(), nullable=False),
        sa.Column("delivery_fee", sa.Float(), server_default=sa.text("0")),
        sa.Column("min_order", sa.Float(), server_default=sa.text("0")),
        sa.Column("estimated_delivery_min", sa.Integer(), server_default=sa.text("30")),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_delivery_zones_restaurant", "delivery_zones", ["restaurant_id"])

    op.create_table(
        "food_menu_items",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("restaurant_id", sa.Integer(), sa.ForeignKey("restaurants.id"), nullable=False),
        sa.Column("branch_id", sa.Integer(), sa.ForeignKey("restaurant_branches.id"), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(), nullable=True),
        sa.Column("subcategory", sa.String(), nullable=True),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("compare_price", sa.Float(), nullable=True),
        sa.Column("calories_kcal", sa.Integer(), nullable=True),
        sa.Column("protein_g", sa.Float(), nullable=True),
        sa.Column("carbs_g", sa.Float(), nullable=True),
        sa.Column("fat_g", sa.Float(), nullable=True),
        sa.Column("fiber_g", sa.Float(), nullable=True),
        sa.Column("serving_size", sa.String(), nullable=True),
        sa.Column("is_vegetarian", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("is_vegan", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("is_gluten_free", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("is_halal", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("is_spicy", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("dietary_tags", sa.String(), nullable=True),
        sa.Column("allergens", sa.String(), nullable=True),
        sa.Column("image_url", sa.String(), nullable=True),
        sa.Column("image_urls", sa.String(), nullable=True),
        sa.Column("is_available", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("preparation_time_min", sa.Integer(), server_default=sa.text("10")),
        sa.Column("sort_order", sa.Integer(), server_default=sa.text("0")),
        sa.Column("total_orders", sa.Integer(), server_default=sa.text("0")),
        sa.Column("rating", sa.Float(), server_default=sa.text("0")),
        sa.Column("review_count", sa.Integer(), server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_menu_items_restaurant", "food_menu_items", ["restaurant_id"])
    op.create_index("ix_menu_items_category", "food_menu_items", ["category"])

    op.create_table(
        "menu_item_modifiers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("menu_item_id", sa.Integer(), sa.ForeignKey("food_menu_items.id"), nullable=False),
        sa.Column("group_name", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("price_modifier", sa.Float(), server_default=sa.text("0")),
        sa.Column("max_select", sa.Integer(), server_default=sa.text("1")),
        sa.Column("sort_order", sa.Integer(), server_default=sa.text("0")),
        sa.Column("is_default", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_modifiers_item", "menu_item_modifiers", ["menu_item_id"])

    # ── Food extras ──
    op.create_table(
        "chat_messages",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("sender_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("receiver_role", sa.String(), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("is_read", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_chat_order", "chat_messages", ["order_id"])

    op.create_table(
        "temperature_checks",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("courier_id", sa.Integer(), sa.ForeignKey("couriers.id"), nullable=False),
        sa.Column("temperature_celsius", sa.Float(), nullable=False),
        sa.Column("check_type", sa.String(), server_default=sa.text("'pickup'")),
        sa.Column("photo_url", sa.String(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("is_acceptable", sa.Boolean(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "hygiene_reports",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("reporter_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("report_type", sa.String(), server_default=sa.text("'customer'")),
        sa.Column("issue_type", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("photo_urls", sa.String(), nullable=True),
        sa.Column("status", sa.String(), server_default=sa.text("'pending'")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "driver_reports",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("reporter_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("courier_id", sa.Integer(), sa.ForeignKey("couriers.id"), nullable=False),
        sa.Column("rating", sa.Integer(), server_default=sa.text("5")),
        sa.Column("issue_type", sa.String(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_anonymous", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )

    # ── Ticket messages ──
    op.create_table(
        "ticket_messages",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("ticket_id", sa.Integer(), sa.ForeignKey("support_tickets.id"), nullable=False),
        sa.Column("sender_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("is_staff", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ticket_messages_ticket", "ticket_messages", ["ticket_id"])

    # ── Reviews ──
    op.create_table(
        "reviews",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=True),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("photo_urls", sa.Text(), nullable=True),
        sa.Column("is_approved", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_reviews_product", "reviews", ["product_id"])
    op.create_index("ix_reviews_user", "reviews", ["user_id"])

    # ── Payments ──
    op.create_table(
        "payments",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("method", sa.String(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("points_used", sa.Integer(), server_default=sa.text("0")),
        sa.Column("points_earned", sa.Integer(), server_default=sa.text("0")),
        sa.Column("installment", sa.Integer(), server_default=sa.text("1")),
        sa.Column("status", sa.String(), server_default=sa.text("'pending'")),
        sa.Column("provider_ref", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_payments_order", "payments", ["order_id"])

    op.create_table(
        "points_transactions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_points_transactions_user", "points_transactions", ["user_id"])

    op.create_table(
        "invoices",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("invoice_no", sa.String(), nullable=False, unique=True),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("status", sa.String(), server_default=sa.text("'pending'")),
        sa.Column("pdf_url", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_invoices_invoice_no", "invoices", ["invoice_no"])

    op.create_table(
        "refunds",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("payment_id", sa.Integer(), sa.ForeignKey("payments.id"), nullable=True),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("status", sa.String(), server_default=sa.text("'pending'")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )

    # ── Subscriptions ──
    op.create_table(
        "subscriptions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("plan_id", sa.Integer(), sa.ForeignKey("subscription_plans.id"), nullable=False),
        sa.Column("seller_id", sa.Integer(), sa.ForeignKey("sellers.id"), nullable=False),
        sa.Column("product_id", sa.Integer(), sa.ForeignKey("products.id"), nullable=False),
        sa.Column("status", sa.String(), server_default=sa.text("'active'")),
        sa.Column("start_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("next_delivery_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("recipient_name", sa.String(), nullable=True),
        sa.Column("recipient_phone", sa.String(), nullable=True),
        sa.Column("delivery_address", sa.Text(), nullable=True),
        sa.Column("delivery_latitude", sa.Float(), nullable=True),
        sa.Column("delivery_longitude", sa.Float(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("card_message", sa.Text(), nullable=True),
        sa.Column("is_gift", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("paused_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancelled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancel_reason", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_subscriptions_user", "subscriptions", ["user_id"])

    op.create_table(
        "subscription_deliveries",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("subscription_id", sa.Integer(), sa.ForeignKey("subscriptions.id"), nullable=False),
        sa.Column("order_id", sa.Integer(), sa.ForeignKey("orders.id"), nullable=True),
        sa.Column("delivery_number", sa.Integer(), nullable=False),
        sa.Column("scheduled_date", sa.DateTime(timezone=True), nullable=True),
        sa.Column("status", sa.String(), server_default=sa.text("'pending'")),
        sa.Column("is_gift", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_subdeliveries_sub", "subscription_deliveries", ["subscription_id"])

    # ── Bina / Site Management ──
    op.create_table(
        "siteler",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("adi", sa.String(), nullable=False),
        sa.Column("adres", sa.Text(), nullable=True),
        sa.Column("sekil", sa.String(), server_default=sa.text("'site'")),
        sa.Column("kurucu", sa.String(), nullable=True),
        sa.Column("kurucu_tel", sa.String(), nullable=True),
        sa.Column("banka", sa.String(), nullable=True),
        sa.Column("komisyon_yuzde", sa.Float(), server_default=sa.text("2")),
        sa.Column("kurulum_tamam", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "bloklar",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("siteler.id"), nullable=False),
        sa.Column("adi", sa.String(), nullable=False),
        sa.Column("kat_adet", sa.Integer(), server_default=sa.text("4")),
        sa.Column("daire_kat", sa.Integer(), server_default=sa.text("2")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_bloklar_site", "bloklar", ["site_id"])

    op.create_table(
        "site_kisiler",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("siteler.id"), nullable=False),
        sa.Column("ad", sa.String(), nullable=False),
        sa.Column("tel", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("rol", sa.String(), server_default=sa.text("'malik'")),
        sa.Column("daire_id", sa.Integer(), nullable=True),
        sa.Column("blok_id", sa.Integer(), nullable=True),
        sa.Column("yetki", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_kisiler_site", "site_kisiler", ["site_id"])

    op.create_table(
        "daireler",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("blok_id", sa.Integer(), sa.ForeignKey("bloklar.id"), nullable=False),
        sa.Column("no", sa.String(), nullable=False),
        sa.Column("kat", sa.Integer(), nullable=False),
        sa.Column("kapi_no", sa.Integer(), nullable=False),
        sa.Column("alan", sa.Float(), nullable=True),
        sa.Column("sakin_id", sa.Integer(), sa.ForeignKey("site_kisiler.id"), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_daireler_blok", "daireler", ["blok_id"])

    op.create_table(
        "site_duyurulari",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("siteler.id"), nullable=False),
        sa.Column("baslik", sa.String(), nullable=False),
        sa.Column("icerik", sa.Text(), nullable=True),
        sa.Column("kategori", sa.String(), server_default=sa.text("'genel'")),
        sa.Column("yapan", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_duyuru_site", "site_duyurulari", ["site_id"])

    op.create_table(
        "aidat",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("siteler.id"), nullable=False),
        sa.Column("daire_id", sa.Integer(), sa.ForeignKey("daireler.id"), nullable=False),
        sa.Column("blok_id", sa.Integer(), sa.ForeignKey("bloklar.id"), nullable=False),
        sa.Column("daire_no", sa.String(), nullable=True),
        sa.Column("ay", sa.Integer(), nullable=False),
        sa.Column("yil", sa.Integer(), nullable=False),
        sa.Column("tutar", sa.Float(), nullable=False),
        sa.Column("odendi", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("odeme_tarihi", sa.DateTime(timezone=True), nullable=True),
        sa.Column("kapi_no", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_aidat_site", "aidat", ["site_id"])
    op.create_index("ix_aidat_daire", "aidat", ["daire_id"])
    op.create_index("ix_aidat_donem", "aidat", ["yil", "ay"])

    op.create_table(
        "site_gelir",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("siteler.id"), nullable=False),
        sa.Column("baslik", sa.String(), nullable=False),
        sa.Column("tutar", sa.Float(), nullable=False),
        sa.Column("kategori", sa.String(), server_default=sa.text("'aidat'")),
        sa.Column("aciklama", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_gelir_site", "site_gelir", ["site_id"])

    op.create_table(
        "site_gider",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("siteler.id"), nullable=False),
        sa.Column("baslik", sa.String(), nullable=False),
        sa.Column("tutar", sa.Float(), nullable=False),
        sa.Column("kategori", sa.String(), server_default=sa.text("'genel'")),
        sa.Column("firma_id", sa.Integer(), nullable=True),
        sa.Column("aciklama", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_gider_site", "site_gider", ["site_id"])

    op.create_table(
        "site_arac",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("siteler.id"), nullable=False),
        sa.Column("plaka", sa.String(), nullable=False),
        sa.Column("daire_id", sa.Integer(), sa.ForeignKey("daireler.id"), nullable=True),
        sa.Column("blok_id", sa.Integer(), sa.ForeignKey("bloklar.id"), nullable=True),
        sa.Column("sakin_ad", sa.String(), nullable=True),
        sa.Column("tel", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_arac_site", "site_arac", ["site_id"])
    op.create_index("ix_arac_plaka", "site_arac", ["plaka"])

    op.create_table(
        "site_personel",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("siteler.id"), nullable=False),
        sa.Column("ad", sa.String(), nullable=False),
        sa.Column("tel", sa.String(), nullable=True),
        sa.Column("gorev", sa.String(), nullable=True),
        sa.Column("maas", sa.Float(), server_default=sa.text("0")),
        sa.Column("ise_baslama", sa.Date(), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_personel_site", "site_personel", ["site_id"])

    op.create_table(
        "site_firma",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("siteler.id"), nullable=False),
        sa.Column("ad", sa.String(), nullable=False),
        sa.Column("yetkili", sa.String(), nullable=True),
        sa.Column("tel", sa.String(), nullable=True),
        sa.Column("adres", sa.Text(), nullable=True),
        sa.Column("sektor", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_firma_site", "site_firma", ["site_id"])

    op.create_table(
        "site_is_talepleri",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("siteler.id"), nullable=False),
        sa.Column("baslik", sa.String(), nullable=False),
        sa.Column("aciklama", sa.Text(), nullable=True),
        sa.Column("sektor", sa.String(), nullable=True),
        sa.Column("durum", sa.String(), server_default=sa.text("'bekliyor'")),
        sa.Column("talep_eden_ad", sa.String(), nullable=True),
        sa.Column("atanan_firma_id", sa.Integer(), sa.ForeignKey("site_firma.id"), nullable=True),
        sa.Column("teklifler", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_istalepleri_site", "site_is_talepleri", ["site_id"])

    op.create_table(
        "site_sayac",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("siteler.id"), nullable=False),
        sa.Column("daire_id", sa.Integer(), sa.ForeignKey("daireler.id"), nullable=False),
        sa.Column("blok_id", sa.Integer(), sa.ForeignKey("bloklar.id"), nullable=False),
        sa.Column("daire_no", sa.String(), nullable=True),
        sa.Column("tur", sa.String(), nullable=False),
        sa.Column("son_endeks", sa.Float(), nullable=False),
        sa.Column("onceki_endeks", sa.Float(), server_default=sa.text("0")),
        sa.Column("birim_fiyat", sa.Float(), nullable=False),
        sa.Column("tarih", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sayac_site", "site_sayac", ["site_id"])
    op.create_index("ix_sayac_daire", "site_sayac", ["daire_id"])

    op.create_table(
        "site_kargo",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("siteler.id"), nullable=False),
        sa.Column("takip_no", sa.String(), nullable=False),
        sa.Column("daire_id", sa.Integer(), sa.ForeignKey("daireler.id"), nullable=True),
        sa.Column("blok_id", sa.Integer(), sa.ForeignKey("bloklar.id"), nullable=True),
        sa.Column("sakin_ad", sa.String(), nullable=True),
        sa.Column("tel", sa.String(), nullable=True),
        sa.Column("durum", sa.String(), server_default=sa.text("'bekliyor'")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_kargo_site", "site_kargo", ["site_id"])

    op.create_table(
        "site_ziyaretci",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("site_id", sa.Integer(), sa.ForeignKey("siteler.id"), nullable=False),
        sa.Column("ad", sa.String(), nullable=False),
        sa.Column("daire_id", sa.Integer(), sa.ForeignKey("daireler.id"), nullable=True),
        sa.Column("blok_id", sa.Integer(), sa.ForeignKey("bloklar.id"), nullable=True),
        sa.Column("giris", sa.DateTime(timezone=True), nullable=False),
        sa.Column("cikis", sa.DateTime(timezone=True), nullable=True),
        sa.Column("plaka", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ziyaretci_site", "site_ziyaretci", ["site_id"])


def downgrade() -> None:
    tables = [
        "site_ziyaretci", "site_kargo", "site_sayac",
        "site_is_talepleri", "site_firma", "site_personel", "site_arac",
        "site_gider", "site_gelir", "aidat", "site_duyurulari",
        "daireler", "bloklar", "site_kisiler", "siteler",
        "subscription_deliveries", "subscriptions",
        "refunds", "invoices", "points_transactions", "payments",
        "reviews", "ticket_messages",
        "driver_reports", "hygiene_reports", "temperature_checks",
        "chat_messages",
        "menu_item_modifiers", "food_menu_items",
        "delivery_zones", "restaurant_branches",
    ]
    for t in tables:
        op.drop_table(t)
