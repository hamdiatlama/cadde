from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.food_supplier.models import (
    FoodSupplier, FoodSupplierProduct, FoodRestaurantSupplier,
    FoodMenuItemIngredient, FoodTransparencyScore,
)


class SupplierRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **kwargs) -> FoodSupplier:
        obj = FoodSupplier(**kwargs)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def update(self, supplier: FoodSupplier, **kwargs) -> FoodSupplier:
        for k, v in kwargs.items():
            setattr(supplier, k, v)
        await self.db.flush()
        return supplier

    async def get_by_id(self, supplier_id: int) -> FoodSupplier | None:
        r = await self.db.execute(select(FoodSupplier).where(FoodSupplier.id == supplier_id))
        return r.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> FoodSupplier | None:
        r = await self.db.execute(select(FoodSupplier).where(FoodSupplier.slug == slug))
        return r.scalar_one_or_none()

    async def list(self, is_active: bool = True) -> list[FoodSupplier]:
        r = await self.db.execute(
            select(FoodSupplier).where(FoodSupplier.is_active == is_active)
            .order_by(FoodSupplier.company_name)
        )
        return list(r.scalars().all())

    async def list_by_city(self, city: str) -> list[FoodSupplier]:
        r = await self.db.execute(
            select(FoodSupplier).where(FoodSupplier.is_active == True, FoodSupplier.city == city)
            .order_by(FoodSupplier.company_name)
        )
        return list(r.scalars().all())

    async def list_by_certification(self, organic: bool = False, halal: bool = False) -> list[FoodSupplier]:
        q = select(FoodSupplier).where(FoodSupplier.is_active == True)
        if organic:
            q = q.where(FoodSupplier.is_organic_certified == True)
        if halal:
            q = q.where(FoodSupplier.is_halal_certified == True)
        r = await self.db.execute(q.order_by(FoodSupplier.company_name))
        return list(r.scalars().all())


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **kwargs) -> FoodSupplierProduct:
        obj = FoodSupplierProduct(**kwargs)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def update(self, product: FoodSupplierProduct, **kwargs) -> FoodSupplierProduct:
        for k, v in kwargs.items():
            setattr(product, k, v)
        await self.db.flush()
        return product

    async def get_by_id(self, product_id: int) -> FoodSupplierProduct | None:
        r = await self.db.execute(select(FoodSupplierProduct).where(FoodSupplierProduct.id == product_id))
        return r.scalar_one_or_none()

    async def list_by_supplier(self, supplier_id: int) -> list[FoodSupplierProduct]:
        r = await self.db.execute(
            select(FoodSupplierProduct).where(
                FoodSupplierProduct.supplier_id == supplier_id,
                FoodSupplierProduct.is_active == True,
            ).order_by(FoodSupplierProduct.category, FoodSupplierProduct.name)
        )
        return list(r.scalars().all())

    async def list_by_category(self, category: str) -> list[FoodSupplierProduct]:
        r = await self.db.execute(
            select(FoodSupplierProduct).where(
                FoodSupplierProduct.category == category,
                FoodSupplierProduct.is_active == True,
            ).order_by(FoodSupplierProduct.name)
        )
        return list(r.scalars().all())


class RestaurantSupplierRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def link(self, restaurant_id: int, supplier_id: int, **kwargs) -> FoodRestaurantSupplier:
        obj = FoodRestaurantSupplier(restaurant_id=restaurant_id, supplier_id=supplier_id, **kwargs)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def unlink(self, restaurant_id: int, supplier_id: int) -> bool:
        r = await self.db.execute(
            delete(FoodRestaurantSupplier).where(
                FoodRestaurantSupplier.restaurant_id == restaurant_id,
                FoodRestaurantSupplier.supplier_id == supplier_id,
            )
        )
        await self.db.flush()
        return r.rowcount > 0

    async def list_by_restaurant(self, restaurant_id: int) -> list[FoodRestaurantSupplier]:
        r = await self.db.execute(
            select(FoodRestaurantSupplier).where(FoodRestaurantSupplier.restaurant_id == restaurant_id)
        )
        return list(r.scalars().all())

    async def get_by_ids(self, restaurant_id: int, supplier_id: int) -> FoodRestaurantSupplier | None:
        r = await self.db.execute(
            select(FoodRestaurantSupplier).where(
                FoodRestaurantSupplier.restaurant_id == restaurant_id,
                FoodRestaurantSupplier.supplier_id == supplier_id,
            )
        )
        return r.scalar_one_or_none()


class IngredientRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **kwargs) -> FoodMenuItemIngredient:
        obj = FoodMenuItemIngredient(**kwargs)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def update(self, ing: FoodMenuItemIngredient, **kwargs) -> FoodMenuItemIngredient:
        for k, v in kwargs.items():
            setattr(ing, k, v)
        await self.db.flush()
        return ing

    async def get_by_id(self, ingredient_id: int) -> FoodMenuItemIngredient | None:
        r = await self.db.execute(select(FoodMenuItemIngredient).where(FoodMenuItemIngredient.id == ingredient_id))
        return r.scalar_one_or_none()

    async def delete(self, ingredient_id: int) -> bool:
        r = await self.db.execute(delete(FoodMenuItemIngredient).where(FoodMenuItemIngredient.id == ingredient_id))
        await self.db.flush()
        return r.rowcount > 0

    async def list_by_menu_item(self, menu_item_id: int) -> list[FoodMenuItemIngredient]:
        r = await self.db.execute(
            select(FoodMenuItemIngredient).where(FoodMenuItemIngredient.menu_item_id == menu_item_id)
        )
        return list(r.scalars().all())


class TransparencyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, restaurant_id: int) -> FoodTransparencyScore | None:
        r = await self.db.execute(
            select(FoodTransparencyScore).where(FoodTransparencyScore.restaurant_id == restaurant_id)
        )
        return r.scalar_one_or_none()

    async def upsert(self, restaurant_id: int, **kwargs) -> FoodTransparencyScore:
        existing = await self.get(restaurant_id)
        if existing:
            for k, v in kwargs.items():
                setattr(existing, k, v)
        else:
            existing = FoodTransparencyScore(restaurant_id=restaurant_id, **kwargs)
            self.db.add(existing)
        await self.db.flush()
        return existing
