from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.loyalty.models import LoyaltyTier, UserLoyalty, LoyaltyPointTransaction


class LoyaltyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_tier(self, name: str, min_spend: float = 0, discount_rate: float = 0,
                          free_shipping: bool = False, badge_color: str = None) -> LoyaltyTier:
        tier = LoyaltyTier(name=name, min_spend=min_spend, discount_rate=discount_rate,
                           free_shipping=free_shipping, badge_color=badge_color)
        self.db.add(tier)
        return tier

    async def list_tiers(self):
        r = await self.db.execute(select(LoyaltyTier).order_by(LoyaltyTier.min_spend.asc()))
        return r.scalars().all()

    async def get_or_create_user_loyalty(self, user_id: int) -> UserLoyalty:
        r = await self.db.execute(select(UserLoyalty).where(UserLoyalty.user_id == user_id))
        ul = r.scalar_one_or_none()
        if not ul:
            ul = UserLoyalty(user_id=user_id, points=0, total_spend=0)
            self.db.add(ul)
        return ul

    async def add_points(self, user_id: int, points: int, type: str, reference_type: str = None, reference_id: int = None) -> UserLoyalty:
        ul = await self.get_or_create_user_loyalty(user_id)
        ul.points += points
        txn = LoyaltyPointTransaction(user_id=user_id, points=points, type=type,
                                       reference_type=reference_type, reference_id=reference_id)
        self.db.add(txn)
        return ul

    async def deduct_points(self, user_id: int, points: int, type: str) -> UserLoyalty:
        ul = await self.get_or_create_user_loyalty(user_id)
        if ul.points >= points:
            ul.points -= points
            txn = LoyaltyPointTransaction(user_id=user_id, points=-points, type=type)
            self.db.add(txn)
        return ul

    async def get_user_tier(self, user_id: int):
        ul = await self.get_or_create_user_loyalty(user_id)
        if ul.tier_id:
            r = await self.db.execute(select(LoyaltyTier).where(LoyaltyTier.id == ul.tier_id))
            return r.scalar_one_or_none()
        return None

    async def recalculate_tier(self, user_id: int) -> UserLoyalty:
        ul = await self.get_or_create_user_loyalty(user_id)
        r = await self.db.execute(
            select(LoyaltyTier).where(LoyaltyTier.min_spend <= ul.total_spend)
            .order_by(LoyaltyTier.min_spend.desc()).limit(1)
        )
        tier = r.scalar_one_or_none()
        ul.tier_id = tier.id if tier else None
        return ul

    async def get_history(self, user_id: int, limit: int = 50):
        r = await self.db.execute(
            select(LoyaltyPointTransaction).where(LoyaltyPointTransaction.user_id == user_id)
            .order_by(LoyaltyPointTransaction.created_at.desc()).limit(limit)
        )
        return r.scalars().all()
