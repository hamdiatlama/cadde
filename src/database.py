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
            from src.modules.food.models import Restaurant, RestaurantBranch, FoodMenuItem, MenuItemModifier, DeliveryZone, ChatMessage, TemperatureCheck, HygieneReport
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
            await conn.run_sync(Base.metadata.create_all)
        else:
            await conn.execute(sa.text("CREATE EXTENSION IF NOT EXISTS postgis"))
            await conn.execute(sa.text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\""))
            await conn.run_sync(Base.metadata.create_all)
