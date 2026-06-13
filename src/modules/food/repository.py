from datetime import datetime, timezone
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.seller import Seller
from src.models.user import User
from src.models.order import Order
from src.models.courier import Courier
from src.modules.food.models import (
    Restaurant, RestaurantBranch, FoodMenuItem, MenuItemModifier,
    DeliveryZone, ChatMessage, TemperatureCheck, HygieneReport,
    DriverReport, BatchDeliveryPrevention,
)
from src.modules.courier.models import CourierEarning, CourierShift
from src.modules.food.geo import haversine_km


class RestaurantRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_seller_id(self, seller_id: int) -> Restaurant | None:
        r = await self.db.execute(select(Restaurant).where(Restaurant.seller_id == seller_id))
        return r.scalar_one_or_none()

    async def get_by_id(self, rest_id: int) -> Restaurant | None:
        r = await self.db.execute(select(Restaurant).where(Restaurant.id == rest_id))
        return r.scalar_one_or_none()

    async def get_seller_by_user_id(self, user_id: int) -> Seller | None:
        r = await self.db.execute(select(Seller).where(Seller.user_id == user_id))
        return r.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> User | None:
        r = await self.db.execute(select(User).where(User.id == user_id))
        return r.scalar_one_or_none()

    async def create(self, seller_id: int, data) -> Restaurant:
        rest = Restaurant(seller_id=seller_id, **data)
        self.db.add(rest)
        return rest

    async def update(self, rest: Restaurant, data: dict) -> Restaurant:
        for field, val in data.items():
            setattr(rest, field, val)
        self.db.add(rest)
        return rest

    async def verify(self, rest: Restaurant, status: str, hygiene_rating: str) -> Restaurant:
        rest.verification_status = status
        rest.hygiene_rating = hygiene_rating
        self.db.add(rest)
        return rest

    async def search(
        self,
        cuisine_type: str | None = None,
        cuisine_subtypes: str | None = None,
        dietary: str | None = None,
        verified_only: bool = True,
        search: str | None = None,
        is_open: bool | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
        radius_km: float | None = None,
        min_rating: float | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        sort_by: str | None = None,
    ) -> list[dict]:
        query = select(Restaurant).where(Restaurant.is_active == True)
        if verified_only:
            query = query.where(Restaurant.verification_status == "verified")
        if cuisine_type:
            query = query.where(Restaurant.cuisine_type == cuisine_type)
        if cuisine_subtypes:
            subtypes = [s.strip() for s in cuisine_subtypes.split(",")]
            query = query.where(
                or_(Restaurant.cuisine_subtypes.ilike(f"%{s}%") for s in subtypes)
            )
        if is_open is not None:
            query = query.where(Restaurant.is_open == is_open)
        if search:
            query = query.where(
                or_(
                    Restaurant.name.ilike(f"%{search}%"),
                    Restaurant.cuisine_type.ilike(f"%{search}%"),
                    Restaurant.cuisine_subtypes.ilike(f"%{search}%"),
                )
            )

        result = await self.db.execute(query.order_by(Restaurant.name))
        rests = list(result.scalars().all())

        branch_cache = {}
        if latitude and longitude:
            for r in rests:
                b_r = await self.db.execute(
                    select(RestaurantBranch).where(
                        RestaurantBranch.restaurant_id == r.id,
                        RestaurantBranch.is_active == True,
                    )
                )
                branch_cache[r.id] = list(b_r.scalars().all())

        out = []
        for r in rests:
            s_r = await self.db.execute(select(Seller).where(Seller.id == r.seller_id))
            s = s_r.scalar_one_or_none()

            distance_km = None
            if latitude and longitude:
                branches = branch_cache.get(r.id, [])
                dists = []
                for b in branches:
                    if b.latitude and b.longitude:
                        dists.append(haversine_km(latitude, longitude, b.latitude, b.longitude))
                if dists:
                    distance_km = min(dists)

            if radius_km and distance_km is not None and distance_km > radius_km:
                continue
            if min_rating and (s is None or (s.rating or 0) < min_rating):
                continue

            if dietary:
                diet_map = {
                    "vegetarian": FoodMenuItem.is_vegetarian == True,
                    "vegan": FoodMenuItem.is_vegan == True,
                    "gluten-free": FoodMenuItem.is_gluten_free == True,
                    "halal": FoodMenuItem.is_halal == True,
                }
                if dietary in diet_map:
                    match = await self.db.execute(
                        select(func.count(FoodMenuItem.id)).where(
                            FoodMenuItem.restaurant_id == r.id,
                            FoodMenuItem.is_available == True,
                            diet_map[dietary],
                        )
                    )
                    if match.scalar() == 0:
                        continue

            if min_price is not None or max_price is not None:
                price_q = select(func.count(FoodMenuItem.id)).where(
                    FoodMenuItem.restaurant_id == r.id, FoodMenuItem.is_available == True,
                )
                if min_price is not None:
                    price_q = price_q.where(FoodMenuItem.price >= min_price)
                if max_price is not None:
                    price_q = price_q.where(FoodMenuItem.price <= max_price)
                match = await self.db.execute(price_q)
                if match.scalar() == 0:
                    continue

            menu_count = (await self.db.execute(
                select(func.count(FoodMenuItem.id)).where(
                    FoodMenuItem.restaurant_id == r.id, FoodMenuItem.is_available == True
                )
            )).scalar()
            halal_count = (await self.db.execute(
                select(func.count(FoodMenuItem.id)).where(
                    FoodMenuItem.restaurant_id == r.id,
                    FoodMenuItem.is_available == True,
                    FoodMenuItem.is_halal == True,
                )
            )).scalar()

            out.append({
                "id": r.id, "name": r.name, "cuisine_type": r.cuisine_type,
                "cuisine_subtypes": r.cuisine_subtypes,
                "description": r.description, "logo_url": r.logo_url,
                "cover_image_url": r.cover_image_url,
                "is_open": r.is_open, "accepts_orders": r.accepts_orders,
                "min_order_amount": r.min_order_amount,
                "delivery_fee": r.delivery_fee,
                "free_delivery_min_amount": r.free_delivery_min_amount,
                "max_delivery_radius_km": r.max_delivery_radius_km,
                "preparation_time_min": r.preparation_time_min,
                "hygiene_rating": r.hygiene_rating,
                "verification_status": r.verification_status,
                "opening_time": r.opening_time, "closing_time": r.closing_time,
                "rating": round(s.rating, 1) if s and s.rating else 0,
                "menu_count": menu_count,
                "has_halal": halal_count > 0,
                "distance_km": round(distance_km, 2) if distance_km is not None else None,
            })

        if sort_by == "rating":
            out.sort(key=lambda x: x["rating"], reverse=True)
        elif sort_by == "distance" and latitude and longitude:
            out.sort(key=lambda x: x["distance_km"] or 999)
        elif sort_by == "min_order_amount":
            out.sort(key=lambda x: x["min_order_amount"])

        return out


class MenuRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_item(self, restaurant_id: int, data: dict) -> FoodMenuItem:
        item = FoodMenuItem(restaurant_id=restaurant_id, **data)
        self.db.add(item)
        return item

    async def get_item_by_id(self, item_id: int) -> FoodMenuItem | None:
        r = await self.db.execute(select(FoodMenuItem).where(FoodMenuItem.id == item_id))
        return r.scalar_one_or_none()

    async def get_item_for_restaurant(self, item_id: int, restaurant_id: int) -> FoodMenuItem | None:
        r = await self.db.execute(
            select(FoodMenuItem).where(
                FoodMenuItem.id == item_id, FoodMenuItem.restaurant_id == restaurant_id
            )
        )
        return r.scalar_one_or_none()

    async def update_item(self, item: FoodMenuItem, data: dict) -> FoodMenuItem:
        for field, val in data.items():
            setattr(item, field, val)
        self.db.add(item)
        return item

    async def delete_item(self, item: FoodMenuItem) -> None:
        await self.db.delete(item)

    async def get_menu(
        self, rest_id: int, category: str | None = None,
        dietary: str | None = None, min_price: float | None = None,
        max_price: float | None = None, search: str | None = None,
    ) -> list[dict]:
        query = select(FoodMenuItem).where(
            FoodMenuItem.restaurant_id == rest_id, FoodMenuItem.is_available == True,
        )
        if category:
            query = query.where(FoodMenuItem.category == category)
        if min_price is not None:
            query = query.where(FoodMenuItem.price >= min_price)
        if max_price is not None:
            query = query.where(FoodMenuItem.price <= max_price)
        if search:
            query = query.where(FoodMenuItem.name.ilike(f"%{search}%"))
        if dietary:
            diet_map = {
                "vegetarian": FoodMenuItem.is_vegetarian == True,
                "vegan": FoodMenuItem.is_vegan == True,
                "gluten-free": FoodMenuItem.is_gluten_free == True,
                "halal": FoodMenuItem.is_halal == True,
            }
            if dietary in diet_map:
                query = query.where(diet_map[dietary])

        result = await self.db.execute(query.order_by(FoodMenuItem.sort_order, FoodMenuItem.name))
        items = []
        for item in result.scalars().all():
            mod_r = await self.db.execute(
                select(MenuItemModifier).where(
                    MenuItemModifier.menu_item_id == item.id,
                    MenuItemModifier.is_active == True,
                ).order_by(MenuItemModifier.sort_order)
            )
            items.append({
                "id": item.id, "name": item.name, "description": item.description,
                "category": item.category, "subcategory": item.subcategory,
                "price": item.price, "compare_price": item.compare_price,
                "calories_kcal": item.calories_kcal, "protein_g": item.protein_g,
                "carbs_g": item.carbs_g, "fat_g": item.fat_g,
                "serving_size": item.serving_size,
                "is_vegetarian": item.is_vegetarian, "is_vegan": item.is_vegan,
                "is_gluten_free": item.is_gluten_free, "is_halal": item.is_halal,
                "is_spicy": item.is_spicy, "dietary_tags": item.dietary_tags,
                "allergens": item.allergens, "image_url": item.image_url,
                "preparation_time_min": item.preparation_time_min,
                "rating": item.rating, "total_orders": item.total_orders,
                "modifiers": [{
                    "id": m.id, "group_name": m.group_name, "name": m.name,
                    "price_modifier": m.price_modifier, "max_select": m.max_select,
                    "is_default": m.is_default,
                } for m in mod_r.scalars().all()],
            })
        return items


class ModifierRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, menu_item_id: int, data: dict) -> MenuItemModifier:
        mod = MenuItemModifier(menu_item_id=menu_item_id, **data)
        self.db.add(mod)
        return mod

    async def get_by_id(self, mod_id: int) -> MenuItemModifier | None:
        r = await self.db.execute(select(MenuItemModifier).where(MenuItemModifier.id == mod_id))
        return r.scalar_one_or_none()

    async def delete(self, mod: MenuItemModifier) -> None:
        await self.db.delete(mod)


class BranchRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, restaurant_id: int, data: dict) -> RestaurantBranch:
        branch = RestaurantBranch(restaurant_id=restaurant_id, **data)
        self.db.add(branch)
        return branch

    async def list_by_restaurant(self, rest_id: int) -> list[dict]:
        r = await self.db.execute(
            select(RestaurantBranch).where(
                RestaurantBranch.restaurant_id == rest_id,
                RestaurantBranch.is_active == True,
            )
        )
        return [{"id": b.id, "name": b.name, "address": b.address,
                 "latitude": b.latitude, "longitude": b.longitude,
                 "phone": b.phone, "opening_time": b.opening_time,
                 "closing_time": b.closing_time} for b in r.scalars().all()]


class ZoneRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, restaurant_id: int, data: dict) -> DeliveryZone:
        zone = DeliveryZone(restaurant_id=restaurant_id, **data)
        self.db.add(zone)
        return zone

    async def list_by_restaurant(self, rest_id: int) -> list[dict]:
        r = await self.db.execute(
            select(DeliveryZone).where(
                DeliveryZone.restaurant_id == rest_id, DeliveryZone.is_active == True
            )
        )
        return [{"id": z.id, "name": z.name, "delivery_fee": z.delivery_fee,
                 "min_order": z.min_order, "estimated_delivery_min": z.estimated_delivery_min}
                for z in r.scalars().all()]


class CourierRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_courier_by_user_id(self, user_id: int) -> Courier | None:
        r = await self.db.execute(select(Courier).where(Courier.user_id == user_id))
        return r.scalar_one_or_none()

    async def get_earnings_summary(self, courier_id: int) -> dict:
        e_r = await self.db.execute(
            select(func.sum(CourierEarning.delivery_fee_earned),
                   func.sum(CourierEarning.tip_amount),
                   func.sum(CourierEarning.bonus_amount),
                   func.count(CourierEarning.id))
            .where(CourierEarning.courier_id == courier_id, CourierEarning.status == "paid")
        )
        fees, tips, bonuses, total = e_r.one()
        return {
            "total_delivery_fees": round(fees or 0, 2),
            "total_tips": round(tips or 0, 2),
            "total_bonuses": round(bonuses or 0, 2),
            "total_earned": round((fees or 0) + (tips or 0) + (bonuses or 0), 2),
            "total_deliveries": total or 0,
        }

    async def get_active_shift(self, courier_id: int) -> CourierShift | None:
        r = await self.db.execute(
            select(CourierShift).where(
                CourierShift.courier_id == courier_id, CourierShift.status == "active"
            )
        )
        return r.scalar_one_or_none()

    async def start_shift(self, courier_id: int) -> CourierShift:
        shift = CourierShift(courier_id=courier_id, start_time=datetime.now(timezone.utc))
        self.db.add(shift)
        return shift

    async def end_shift(self, shift: CourierShift, courier: Courier, total_earned: float) -> CourierShift:
        shift.status = "completed"
        shift.end_time = datetime.now(timezone.utc)
        shift.total_earned = total_earned
        courier.is_available = False
        self.db.add(shift)
        self.db.add(courier)
        return shift


class ChatRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_order_by_id(self, order_id: int) -> Order | None:
        r = await self.db.execute(select(Order).where(Order.id == order_id))
        return r.scalar_one_or_none()

    async def send_message(self, order_id: int, sender_id: int, receiver_role: str, message: str) -> ChatMessage:
        msg = ChatMessage(order_id=order_id, sender_id=sender_id, receiver_role=receiver_role, message=message)
        self.db.add(msg)
        return msg

    async def get_messages(self, order_id: int) -> list[dict]:
        msgs = await self.db.execute(
            select(ChatMessage).where(ChatMessage.order_id == order_id)
            .order_by(ChatMessage.created_at.asc())
        )
        return [{
            "id": m.id, "sender_id": m.sender_id,
            "receiver_role": m.receiver_role, "message": m.message,
            "is_read": m.is_read, "created_at": m.created_at.isoformat() if m.created_at else None,
        } for m in msgs.scalars().all()]


class QualityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_temperature(self, order_id: int, courier_id: int, temp: float, check_type: str,
                               photo_url: str | None, notes: str | None) -> TemperatureCheck:
        tc = TemperatureCheck(
            order_id=order_id, courier_id=courier_id,
            temperature_celsius=temp, check_type=check_type,
            photo_url=photo_url, notes=notes,
            is_acceptable=4 <= temp <= 65,
        )
        self.db.add(tc)
        return tc

    async def get_temperature_logs(self, order_id: int) -> list[dict]:
        r = await self.db.execute(
            select(TemperatureCheck).where(TemperatureCheck.order_id == order_id)
            .order_by(TemperatureCheck.created_at)
        )
        return [{"id": t.id, "temperature_celsius": t.temperature_celsius,
                 "check_type": t.check_type, "is_acceptable": t.is_acceptable,
                 "created_at": t.created_at.isoformat() if t.created_at else None}
                for t in r.scalars().all()]

    async def report_hygiene(self, reporter_id: int, report_type: str, data) -> HygieneReport:
        hr = HygieneReport(
            order_id=data.order_id, reporter_id=reporter_id,
            report_type=report_type, issue_type=data.issue_type,
            description=data.description, photo_urls=data.photo_urls,
        )
        self.db.add(hr)
        return hr

    async def list_hygiene_reports(self, status_filter: str | None = None) -> list[dict]:
        q = select(HygieneReport)
        if status_filter:
            q = q.where(HygieneReport.status == status_filter)
        r = await self.db.execute(q.order_by(HygieneReport.created_at.desc()))
        return [{"id": h.id, "order_id": h.order_id, "issue_type": h.issue_type,
                 "status": h.status, "created_at": h.created_at.isoformat() if h.created_at else None}
                for h in r.scalars().all()]

    async def report_driver(self, reporter_id: int, data) -> DriverReport:
        dr = DriverReport(
            order_id=data.order_id, reporter_id=reporter_id,
            courier_id=data.courier_id, rating=data.rating,
            issue_type=data.issue_type, description=data.description,
            is_anonymous=data.is_anonymous,
        )
        self.db.add(dr)
        return dr

    async def get_driver_reports(self, courier_id: int) -> list[dict]:
        r = await self.db.execute(
            select(DriverReport).where(DriverReport.courier_id == courier_id)
            .order_by(DriverReport.created_at.desc())
        )
        return [{"id": d.id, "rating": d.rating, "issue_type": d.issue_type,
                 "description": d.description, "created_at": d.created_at.isoformat() if d.created_at else None}
                for d in r.scalars().all()]

    async def set_batch_prevention(self, order_id: int, max_batch_size: int) -> BatchDeliveryPrevention:
        r = await self.db.execute(
            select(BatchDeliveryPrevention).where(BatchDeliveryPrevention.order_id == order_id)
        )
        bp = r.scalar_one_or_none()
        if bp:
            bp.max_batch_size = max_batch_size
        else:
            bp = BatchDeliveryPrevention(order_id=order_id, max_batch_size=max_batch_size)
        self.db.add(bp)
        return bp

    async def get_batch_prevention(self, order_id: int) -> dict:
        r = await self.db.execute(
            select(BatchDeliveryPrevention).where(BatchDeliveryPrevention.order_id == order_id)
        )
        bp = r.scalar_one_or_none()
        if not bp:
            return {"prevented": False}
        return {"prevented": True, "max_batch_size": bp.max_batch_size}
