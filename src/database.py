import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.config import DATABASE_URL, IS_SQLITE

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        if IS_SQLITE:
            from src.modules.user.models import User
            from src.modules.seller.models import Seller, Question
            from src.modules.store.models import Product, ProductExtra, Bouquet, Coupon
            from src.modules.food.models import Restaurant, RestaurantBranch, FoodMenuItem, MenuItemModifier, DeliveryZone, FoodChatMessage, TemperatureCheck, HygieneReport
            from src.modules.courier.models import Courier, CourierLocationHistory
            from src.modules.ride.models import Driver, DriverLocationHistory, Ride, RideSafety, RideRating
            from src.modules.ecommerce.cart.models import Cart, CartItem
            from src.modules.ecommerce.order.models import Order, OrderItem, Substitution
            from src.modules.ecommerce.payment.models import Payment, PaymentMethod, PointsTransaction, Invoice, Refund
            from src.modules.account.address.models import Address
            from src.modules.notification.models import Notification
            from src.modules.review.models import Review
            from src.modules.support.models import SupportTicket, TicketMessage
            from src.modules.subscription.models import SubscriptionPlan, Subscription, SubscriptionDelivery
            from src.models.delivery import DeliveryPhoto
            import src.modules.bina.models  # registers all 27 bina tables
            import src.modules.event.models  # registers all 10 event tables
            import src.modules.vehicle.models
            import src.modules.expert.models
            import src.modules.realestate.models
            import src.modules.food_supplier.models
            import src.modules.cicek.models
            import src.modules.cargo.models
            import src.modules.wishlist.models
            import src.modules.campaign.models
            import src.modules.escrow.models
            import src.modules.payout.models
            import src.modules.advertising.models
            import src.modules.comparison.models
            import src.modules.variant.models
            import src.modules.chat.models
            import src.modules.b2b.models
            import src.modules.tax.models
            import src.modules.warehouse.models
            import src.modules.abandoned_cart.models
            import src.modules.seller_performance.models
            import src.modules.multiseller.models
            import src.modules.auction.models
            import src.modules.gift_card.models
            import src.modules.payment_extended.models
            import src.modules.commission.models
            import src.modules.loyalty.models
            import src.modules.marketing.models
            import src.modules.fulfillment.models
            import src.modules.delivery_extended.models
            import src.modules.subscribe_save.models
            import src.modules.recommendation.models
            import src.modules.live_shopping.models
            import src.modules.return_management.models
            import src.modules.trade_in.models
            import src.modules.handmade.models
            import src.modules.brand.models
            import src.modules.dropshipping.models
            import src.modules.verification.models
            import src.modules.marketplace_core.models
            import src.modules.social_commerce.models
            import src.modules.developer.models
            import src.modules.fraud.models
            import src.modules.product_enhanced.models
            import src.modules.tax_extended.models
            import src.modules.logistics_advanced.models
            import src.modules.compliance.models
            import src.modules.seller_tools.models
            import src.modules.customer_service.models
            import src.modules.storefront.models
            import src.modules.pos.models
            import src.modules.messaging.models
            import src.modules.payment_vault.models
            import src.modules.dynamic_pricing.models
            import src.modules.analytics.models
            import src.modules.integration.models
            import src.modules.payout_extended.models
            import src.modules.marketing_automation.models
            import src.modules.chatbot.models
            import src.modules.hotel.models
            import src.modules.digital_compendium.models
            import src.modules.accommodation.models
            import src.modules.payment_gateway.models
            import src.modules.energy_manager.models
            import src.modules.iot_manager.models
            import src.modules.channel_manager.models
            import src.modules.hotel_revenue.models
            import src.modules.multi_property.models
            import src.modules.mobile_checkin.models
            import src.modules.reputation.models
            import src.modules.upselling.models
            import src.modules.website_builder.models
            import src.modules.digital_compendium.models
            import src.modules.ai_concierge.models
            import src.modules.agency.models
            import src.modules.tourism.models
            import src.modules.rental.models
            import src.modules.trip_planner.models
            import src.modules.transport.models
            await conn.run_sync(Base.metadata.create_all)
        else:
            await conn.execute(sa.text("CREATE EXTENSION IF NOT EXISTS postgis"))
            await conn.execute(sa.text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\""))
            await conn.run_sync(Base.metadata.create_all)
