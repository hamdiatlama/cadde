from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.food.repository import (
    RestaurantRepository, MenuRepository, ModifierRepository,
    BranchRepository, ZoneRepository, CourierRepo, ChatRepository, QualityRepository,
)
from src.modules.food.events import publish_event, FoodEvent


class RestaurantService:
    def __init__(self, db: AsyncSession):
        self.repo = RestaurantRepository(db)

    async def register(self, user_id: int, data) -> dict:
        seller = await self.repo.get_seller_by_user_id(user_id)
        if not seller:
            raise ValueError("Seller profile not found")
        existing = await self.repo.get_by_seller_id(seller.id)
        if existing:
            raise ValueError("You already have a restaurant")
        rest = await self.repo.create(seller.id, data.model_dump())
        await publish_event(FoodEvent.RESTAURANT_REGISTERED, {"restaurant_id": rest.id, "seller_id": seller.id})
        return {"status": "restaurant_registered", "id": rest.id}

    async def update(self, rest_id: int, user_id: int, data: dict) -> dict:
        rest = await self.repo.get_by_id(rest_id)
        if not rest:
            raise ValueError("Restaurant not found")
        seller = await self.repo.get_seller_by_user_id(user_id)
        if not seller or rest.seller_id != seller.id:
            raise ValueError("Not your restaurant")
        await self.repo.update(rest, data)
        await publish_event(FoodEvent.RESTAURANT_UPDATED, {"restaurant_id": rest.id})
        return {"status": "updated"}

    async def verify(self, rest_id: int, status: str, hygiene_rating: str) -> dict:
        rest = await self.repo.get_by_id(rest_id)
        if not rest:
            raise ValueError("Restaurant not found")
        await self.repo.verify(rest, status, hygiene_rating)
        await publish_event(FoodEvent.RESTAURANT_VERIFIED, {"restaurant_id": rest.id, "status": status})
        return {"status": f"restaurant_{status}"}

    async def search(self, **kwargs) -> list[dict]:
        return await self.repo.search(**kwargs)


class MenuService:
    def __init__(self, db: AsyncSession):
        self.repo = MenuRepository(db)
        self.rest_repo = RestaurantRepository(db)

    async def create_item(self, user_id: int, data) -> dict:
        seller = await self.rest_repo.get_seller_by_user_id(user_id)
        if not seller:
            raise ValueError("Seller profile not found")
        rest = await self.rest_repo.get_by_seller_id(seller.id)
        if not rest:
            raise ValueError("Restaurant not found")
        item = await self.repo.create_item(rest.id, data.model_dump())
        await publish_event(FoodEvent.MENU_ITEM_CREATED, {"item_id": item.id, "restaurant_id": rest.id})
        return {"status": "menu_item_created", "id": item.id}

    async def update_item(self, item_id: int, user_id: int, data: dict) -> dict:
        seller = await self.rest_repo.get_seller_by_user_id(user_id)
        if not seller:
            raise ValueError("Seller profile not found")
        rest = await self.rest_repo.get_by_seller_id(seller.id)
        if not rest:
            raise ValueError("Restaurant not found")
        item = await self.repo.get_item_for_restaurant(item_id, rest.id)
        if not item:
            raise ValueError("Menu item not found")
        await self.repo.update_item(item, data)
        await publish_event(FoodEvent.MENU_ITEM_UPDATED, {"item_id": item.id})
        return {"status": "updated"}

    async def delete_item(self, item_id: int, user_id: int) -> dict:
        seller = await self.rest_repo.get_seller_by_user_id(user_id)
        if not seller:
            raise ValueError("Seller profile not found")
        rest = await self.rest_repo.get_by_seller_id(seller.id)
        if not rest:
            raise ValueError("Restaurant not found")
        item = await self.repo.get_item_for_restaurant(item_id, rest.id)
        if not item:
            raise ValueError("Menu item not found")
        await self.repo.delete_item(item)
        await publish_event(FoodEvent.MENU_ITEM_DELETED, {"item_id": item.id})
        return {"status": "deleted"}

    async def get_menu(self, rest_id: int, **kwargs) -> list[dict]:
        return await self.repo.get_menu(rest_id, **kwargs)


class ModifierService:
    def __init__(self, db: AsyncSession):
        self.repo = ModifierRepository(db)
        self.menu_repo = MenuRepository(db)
        self.rest_repo = RestaurantRepository(db)

    async def add(self, item_id: int, user_id: int, data) -> dict:
        seller = await self.rest_repo.get_seller_by_user_id(user_id)
        if not seller:
            raise ValueError("Seller profile not found")
        rest = await self.rest_repo.get_by_seller_id(seller.id)
        if not rest:
            raise ValueError("Restaurant not found")
        item = await self.menu_repo.get_item_for_restaurant(item_id, rest.id)
        if not item:
            raise ValueError("Menu item not found")
        mod = await self.repo.create(item_id, data.model_dump())
        await publish_event(FoodEvent.MODIFIER_ADDED, {"modifier_id": mod.id, "item_id": item_id})
        return {"status": "modifier_added", "id": mod.id}

    async def delete(self, mod_id: int, user_id: int) -> dict:
        seller = await self.rest_repo.get_seller_by_user_id(user_id)
        if not seller:
            raise ValueError("Seller profile not found")
        rest = await self.rest_repo.get_by_seller_id(seller.id)
        if not rest:
            raise ValueError("Restaurant not found")
        mod = await self.repo.get_by_id(mod_id)
        if not mod:
            raise ValueError("Modifier not found")
        mi = await self.menu_repo.get_item_by_id(mod.menu_item_id)
        if not mi or mi.restaurant_id != rest.id:
            raise ValueError("Modifier not found")
        await self.repo.delete(mod)
        await publish_event(FoodEvent.MODIFIER_DELETED, {"modifier_id": mod_id})
        return {"status": "deleted"}


class BranchService:
    def __init__(self, db: AsyncSession):
        self.repo = BranchRepository(db)
        self.rest_repo = RestaurantRepository(db)

    async def add(self, rest_id: int, user_id: int, data) -> dict:
        rest = await self.rest_repo.get_by_id(rest_id)
        if not rest:
            raise ValueError("Restaurant not found")
        seller = await self.rest_repo.get_seller_by_user_id(user_id)
        if not seller or rest.seller_id != seller.id:
            raise ValueError("Not your restaurant")
        branch = await self.repo.create(rest_id, data.model_dump())
        await publish_event(FoodEvent.BRANCH_ADDED, {"branch_id": branch.id, "restaurant_id": rest_id})
        return {"status": "branch_added", "id": branch.id}

    async def list(self, rest_id: int) -> list[dict]:
        return await self.repo.list_by_restaurant(rest_id)


class ZoneService:
    def __init__(self, db: AsyncSession):
        self.repo = ZoneRepository(db)
        self.rest_repo = RestaurantRepository(db)

    async def add(self, rest_id: int, user_id: int, data) -> dict:
        rest = await self.rest_repo.get_by_id(rest_id)
        if not rest:
            raise ValueError("Restaurant not found")
        seller = await self.rest_repo.get_seller_by_user_id(user_id)
        if not seller or rest.seller_id != seller.id:
            raise ValueError("Not your restaurant")
        zone = await self.repo.create(rest_id, data.model_dump())
        await publish_event(FoodEvent.ZONE_ADDED, {"zone_id": zone.id, "restaurant_id": rest_id})
        return {"status": "zone_added", "id": zone.id}

    async def list(self, rest_id: int) -> list[dict]:
        return await self.repo.list_by_restaurant(rest_id)


class CourierFoodService:
    def __init__(self, db: AsyncSession):
        self.repo = CourierRepo(db)

    async def get_earnings(self, user_id: int) -> dict:
        courier = await self.repo.get_courier_by_user_id(user_id)
        if not courier:
            raise ValueError("Courier profile not found")
        return await self.repo.get_earnings_summary(courier.id)

    async def start_shift(self, user_id: int) -> dict:
        courier = await self.repo.get_courier_by_user_id(user_id)
        if not courier:
            raise ValueError("Courier profile not found")
        active = await self.repo.get_active_shift(courier.id)
        if active:
            raise ValueError("You already have an active shift")
        shift = await self.repo.start_shift(courier.id)
        courier.is_available = True
        await publish_event(FoodEvent.SHIFT_STARTED, {"courier_id": courier.id, "shift_id": shift.id})
        return {"status": "shift_started"}

    async def end_shift(self, user_id: int) -> dict:
        courier = await self.repo.get_courier_by_user_id(user_id)
        if not courier:
            raise ValueError("Courier profile not found")
        active = await self.repo.get_active_shift(courier.id)
        if not active:
            raise ValueError("No active shift found")
        earnings = await self.repo.get_earnings_summary(courier.id)
        await self.repo.end_shift(active, courier, earnings["total_earned"])
        await publish_event(FoodEvent.SHIFT_ENDED, {"courier_id": courier.id, "shift_id": active.id})
        return {"status": "shift_ended", "total_earned": round(earnings["total_earned"], 2)}


class ChatService:
    def __init__(self, db: AsyncSession):
        self.repo = ChatRepository(db)

    async def send(self, order_id: int, sender_id: int, receiver_role: str, message: str) -> dict:
        order = await self.repo.get_order_by_id(order_id)
        if not order:
            raise ValueError("Order not found")
        msg = await self.repo.send_message(order_id, sender_id, receiver_role, message)
        await publish_event(FoodEvent.CHAT_MESSAGE_SENT, {"message_id": msg.id, "order_id": order_id})
        return {"status": "sent", "id": msg.id}

    async def get_messages(self, order_id: int, user_id: int) -> list[dict]:
        order = await self.repo.get_order_by_id(order_id)
        if not order:
            raise ValueError("Order not found")
        return await self.repo.get_messages(order_id)


class QualityService:
    def __init__(self, db: AsyncSession):
        self.repo = QualityRepository(db)

    async def log_temperature(self, order_id: int, courier_id: int, temp: float,
                               check_type: str, photo_url: str | None, notes: str | None) -> dict:
        tc = await self.repo.log_temperature(order_id, courier_id, temp, check_type, photo_url, notes)
        await publish_event(FoodEvent.TEMPERATURE_LOGGED, {"check_id": tc.id, "order_id": order_id})
        return {"status": "logged", "is_acceptable": tc.is_acceptable}

    async def get_temperature_logs(self, order_id: int) -> list[dict]:
        return await self.repo.get_temperature_logs(order_id)

    async def report_hygiene(self, reporter_id: int, user_role: str, data) -> dict:
        report_type = "customer" if user_role == "customer" else "courier"
        hr = await self.repo.report_hygiene(reporter_id, report_type, data)
        await publish_event(FoodEvent.HYGIENE_REPORTED, {"report_id": hr.id, "order_id": data.order_id})
        return {"status": "reported", "id": hr.id}

    async def list_hygiene_reports(self, status_filter: str | None = None) -> list[dict]:
        return await self.repo.list_hygiene_reports(status_filter)

    async def report_driver(self, reporter_id: int, data) -> dict:
        dr = await self.repo.report_driver(reporter_id, data)
        await publish_event(FoodEvent.DRIVER_REPORTED, {"report_id": dr.id, "courier_id": data.courier_id})
        return {"status": "reported"}

    async def get_driver_reports(self, courier_id: int) -> list[dict]:
        return await self.repo.get_driver_reports(courier_id)

    async def set_batch_prevention(self, order_id: int, max_batch_size: int) -> dict:
        await self.repo.set_batch_prevention(order_id, max_batch_size)
        return {"status": "batch_prevention_set"}

    async def get_batch_prevention(self, order_id: int) -> dict:
        return await self.repo.get_batch_prevention(order_id)
