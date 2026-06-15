import json
from datetime import datetime, timezone
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.storefront.models import PwaManifest, CookieConsent, GdprDataRequest
from src.modules.store.models import Product
from src.modules.user.models import User
from src.modules.review.models import Review
from src.modules.ecommerce.order.models import Order
from src.modules.notification.models import Notification


class PwaManifestRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_or_update_manifest(self, seller_id: int, data: dict) -> PwaManifest:
        r = await self.db.execute(select(PwaManifest).where(PwaManifest.seller_id == seller_id))
        manifest = r.scalar_one_or_none()
        if manifest:
            for k, v in data.items():
                if hasattr(manifest, k):
                    setattr(manifest, k, v)
        else:
            manifest = PwaManifest(seller_id=seller_id, **data)
            self.db.add(manifest)
        return manifest

    async def get_manifest(self, seller_id: int):
        r = await self.db.execute(select(PwaManifest).where(PwaManifest.seller_id == seller_id))
        return r.scalar_one_or_none()


class CookieConsentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def record_consent(self, user_id: int, consent_type: str, session_id: str = None, ip_address: str = None) -> CookieConsent:
        consent = CookieConsent(user_id=user_id, consent_type=consent_type, session_id=session_id, ip_address=ip_address)
        self.db.add(consent)
        return consent

    async def get_user_consent(self, user_id: int):
        r = await self.db.execute(
            select(CookieConsent).where(CookieConsent.user_id == user_id).order_by(CookieConsent.created_at.desc())
        )
        return r.scalars().all()


class GdprRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_request(self, user_id: int, request_type: str) -> GdprDataRequest:
        req = GdprDataRequest(user_id=user_id, request_type=request_type)
        self.db.add(req)
        return req

    async def export_data(self, user_id: int) -> dict:
        user_r = await self.db.execute(select(User).where(User.id == user_id))
        user = user_r.scalar_one_or_none()
        if not user:
            return {}
        orders_r = await self.db.execute(
            select(Order).where(Order.buyer_id == user_id).order_by(Order.created_at.desc())
        )
        products_r = await self.db.execute(
            select(Product).where(Product.seller_id == user_id).order_by(Product.created_at.desc())
        )
        reviews_r = await self.db.execute(
            select(Review).where(Review.user_id == user_id).order_by(Review.created_at.desc())
        )
        notifications_r = await self.db.execute(
            select(Notification).where(Notification.user_id == user_id).order_by(Notification.created_at.desc())
        )
        return {
            "user": {
                "id": user.id, "email": user.email, "phone": user.phone,
                "full_name": user.full_name, "role": user.role,
                "is_active": user.is_active, "points": user.points,
                "created_at": str(user.created_at)
            },
            "orders": [
                {"id": o.id, "total": o.total, "status": o.status, "created_at": str(o.created_at)}
                for o in orders_r.scalars().all()
            ],
            "products": [
                {"id": p.id, "name": p.name, "price": p.price, "created_at": str(p.created_at)}
                for p in products_r.scalars().all()
            ],
            "reviews": [
                {"id": r.id, "rating": r.rating, "comment": r.comment, "created_at": str(r.created_at)}
                for r in reviews_r.scalars().all()
            ],
            "notifications": [
                {"id": n.id, "title": n.title, "message": n.message, "created_at": str(n.created_at)}
                for n in notifications_r.scalars().all()
            ]
        }

    async def process_request(self, request_id: int):
        r = await self.db.execute(select(GdprDataRequest).where(GdprDataRequest.id == request_id))
        req = r.scalar_one_or_none()
        if not req:
            return None
        if req.request_type == "delete":
            await self.db.execute(delete(Notification).where(Notification.user_id == req.user_id))
            await self.db.execute(delete(Review).where(Review.user_id == req.user_id))
            await self.db.execute(delete(Product).where(Product.seller_id == req.user_id))
            await self.db.execute(delete(Order).where(Order.buyer_id == req.user_id))
            await self.db.execute(delete(User).where(User.id == req.user_id))
        req.status = "completed"
        req.completed_at = datetime.now(timezone.utc)
        return req
