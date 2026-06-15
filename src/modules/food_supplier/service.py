import math
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.food.models import FoodMenuItem, Restaurant
from src.modules.food_supplier.models import (
    FoodSupplier, FoodSupplierProduct, FoodRestaurantSupplier,
    FoodMenuItemIngredient, FoodTransparencyScore,
)
from src.modules.food_supplier.repository import (
    SupplierRepository, ProductRepository, RestaurantSupplierRepository,
    IngredientRepository, TransparencyRepository,
)


class FoodSupplierService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.suppliers = SupplierRepository(db)
        self.products = ProductRepository(db)
        self.links = RestaurantSupplierRepository(db)
        self.ingredients = IngredientRepository(db)
        self.scores = TransparencyRepository(db)

    # --- Suppliers ---

    async def register(self, user_id: int, data) -> FoodSupplier:
        vals = data.model_dump()
        if vals.get("supplier_type") == "home_chef":
            vals["verification_status"] = "verified"
            vals["is_organic_certified"] = False
            vals["is_halal_certified"] = False
        return await self.suppliers.create(user_id=user_id, **vals)

    async def update(self, supplier_id: int, data, user_id: int) -> FoodSupplier | None:
        sup = await self.suppliers.get_by_id(supplier_id)
        if not sup or sup.user_id != user_id:
            return None
        return await self.suppliers.update(sup, **data.model_dump(exclude_none=True))

    async def get_supplier(self, supplier_id: int) -> FoodSupplier | None:
        return await self.suppliers.get_by_id(supplier_id)

    async def get_supplier_by_slug(self, slug: str) -> FoodSupplier | None:
        return await self.suppliers.get_by_slug(slug)

    async def list_suppliers(self, city: str = None, organic: bool = False, halal: bool = False) -> list[FoodSupplier]:
        if city:
            return await self.suppliers.list_by_city(city)
        if organic or halal:
            return await self.suppliers.list_by_certification(organic, halal)
        return await self.suppliers.list()

    # --- Products ---

    async def add_product(self, supplier_id: int, data, user_id: int) -> FoodSupplierProduct | None:
        sup = await self.suppliers.get_by_id(supplier_id)
        if not sup or sup.user_id != user_id:
            return None
        return await self.products.create(supplier_id=supplier_id, **data.model_dump())

    async def update_product(self, product_id: int, data, user_id: int) -> FoodSupplierProduct | None:
        prod = await self.products.get_by_id(product_id)
        if not prod:
            return None
        sup = await self.suppliers.get_by_id(prod.supplier_id)
        if not sup or sup.user_id != user_id:
            return None
        return await self.products.update(prod, **data.model_dump(exclude_none=True))

    async def delete_product(self, product_id: int, user_id: int) -> bool:
        prod = await self.products.get_by_id(product_id)
        if not prod:
            return False
        sup = await self.suppliers.get_by_id(prod.supplier_id)
        if not sup or sup.user_id != user_id:
            return False
        return await self.products.update(prod, is_active=False) is not None

    async def list_products(self, supplier_id: int) -> list[FoodSupplierProduct]:
        return await self.products.list_by_supplier(supplier_id)

    # --- Supplier-Restaurant Links ---

    async def link_supplier(self, restaurant_id: int, supplier_id: int, data, user_id: int) -> FoodRestaurantSupplier | None:
        r = await self.db.execute(select(Restaurant).where(Restaurant.id == restaurant_id))
        rest = r.scalar_one_or_none()
        if not rest:
            return None
        r = await self.db.execute(select(FoodSupplier).where(FoodSupplier.id == supplier_id))
        sup = r.scalar_one_or_none()
        if not sup:
            return None
        existing = await self.links.get_by_ids(restaurant_id, supplier_id)
        if existing:
            return existing
        vals = data.model_dump(exclude={"supplier_id"})
        return await self.links.link(restaurant_id, supplier_id, **vals)

    async def unlink_supplier(self, restaurant_id: int, supplier_id: int, user_id: int) -> bool:
        return await self.links.unlink(restaurant_id, supplier_id)

    async def list_restaurant_suppliers(self, restaurant_id: int) -> list[dict]:
        links = await self.links.list_by_restaurant(restaurant_id)
        result = []
        for link in links:
            sup = await self.suppliers.get_by_id(link.supplier_id)
            result.append({
                "id": link.id,
                "restaurant_id": link.restaurant_id,
                "supplier_id": link.supplier_id,
                "supplier_name": sup.company_name if sup else "",
                "is_preferred": link.is_preferred,
                "contract_start": link.contract_start,
                "contract_end": link.contract_end,
                "notes": link.notes,
            })
        return result

    # --- Menu Item Ingredients ---

    async def add_ingredient(self, menu_item_id: int, data) -> FoodMenuItemIngredient | None:
        return await self.ingredients.create(menu_item_id=menu_item_id, **data.model_dump())

    async def update_ingredient(self, ingredient_id: int, data) -> FoodMenuItemIngredient | None:
        ing = await self.ingredients.get_by_id(ingredient_id)
        if not ing:
            return None
        return await self.ingredients.update(ing, **data.model_dump(exclude_none=True))

    async def delete_ingredient(self, ingredient_id: int) -> bool:
        return await self.ingredients.delete(ingredient_id)

    async def list_ingredients(self, menu_item_id: int) -> list[dict]:
        ings = await self.ingredients.list_by_menu_item(menu_item_id)
        result = []
        for ing in ings:
            prod = await self.products.get_by_id(ing.supplier_product_id)
            supplier_name = ""
            supplier_slug = ""
            product_name = ""
            if prod:
                product_name = prod.name
                sup = await self.suppliers.get_by_id(prod.supplier_id)
                if sup:
                    supplier_name = sup.company_name
                    supplier_slug = sup.slug
            result.append({
                "id": ing.id,
                "menu_item_id": ing.menu_item_id,
                "supplier_product_id": ing.supplier_product_id,
                "product_name": product_name,
                "supplier_name": supplier_name,
                "supplier_slug": supplier_slug,
                "quantity": ing.quantity,
                "unit": ing.unit,
                "notes": ing.notes,
                "is_visible_to_customer": ing.is_visible_to_customer,
            })
        return result

    # --- Transparency Score ---

    async def calculate_score(self, restaurant_id: int) -> FoodTransparencyScore:
        r = await self.db.execute(
            select(FoodMenuItem).where(FoodMenuItem.restaurant_id == restaurant_id, FoodMenuItem.is_available == True)
        )
        all_items = list(r.scalars().all())
        total_items = len(all_items)

        items_with_ingredients = 0
        total_suppliers = 0
        for item in all_items:
            ings = await self.ingredients.list_by_menu_item(item.id)
            if ings:
                items_with_ingredients += 1
                linked_suppliers = set()
                for ing in ings:
                    prod = await self.products.get_by_id(ing.supplier_product_id)
                    if prod:
                        linked_suppliers.add(prod.supplier_id)
                total_suppliers += len(linked_suppliers)

        percentage = (items_with_ingredients / total_items * 100) if total_items > 0 else 0
        points = int(percentage) + (total_suppliers * 5)

        return await self.scores.upsert(
            restaurant_id=restaurant_id,
            total_menu_items=total_items,
            items_with_ingredients=items_with_ingredients,
            total_suppliers_linked=total_suppliers,
            transparency_percentage=round(percentage, 1),
            total_points=points,
        )

    async def get_score(self, restaurant_id: int) -> FoodTransparencyScore | None:
        return await self.scores.get(restaurant_id)

    # --- Traceability (public) ---

    async def get_trace(self, menu_item_id: int) -> dict | None:
        r = await self.db.execute(select(FoodMenuItem).where(FoodMenuItem.id == menu_item_id))
        item = r.scalar_one_or_none()
        if not item:
            return None
        ings = await self.list_ingredients(menu_item_id)
        return {
            "menu_item_id": item.id,
            "menu_item_name": item.name,
            "ingredients": [i for i in ings if i["is_visible_to_customer"]],
        }

    # --- Supplier public page ---

    async def get_supplier_page(self, slug: str) -> dict | None:
        sup = await self.suppliers.get_by_slug(slug)
        if not sup or not sup.is_active:
            return None
        products = await self.products.list_by_supplier(sup.id)
        return {
            "id": sup.id,
            "company_name": sup.company_name,
            "slug": sup.slug,
            "description": sup.description,
            "logo_url": sup.logo_url,
            "cover_url": sup.cover_url,
            "city": sup.city,
            "district": sup.district,
            "supplier_type": sup.supplier_type,
            "contact_phone": sup.contact_phone,
            "contact_email": sup.contact_email,
            "website_url": sup.website_url,
            "is_organic_certified": sup.is_organic_certified,
            "is_halal_certified": sup.is_halal_certified,
            "certifications": sup.certifications,
            "product_categories": sup.product_categories,
            "kitchen_photos": sup.kitchen_photos,
            "rating": sup.rating,
            "review_count": sup.review_count,
            "verification_status": sup.verification_status,
            "is_active": sup.is_active,
            "products": [
                {
                    "id": p.id,
                    "supplier_id": p.supplier_id,
                    "name": p.name,
                    "description": p.description,
                    "category": p.category,
                    "subcategory": p.subcategory,
                    "unit": p.unit,
                    "price_per_unit": p.price_per_unit,
                    "is_organic": p.is_organic,
                    "is_local": p.is_local,
                    "season_start_month": p.season_start_month,
                    "season_end_month": p.season_end_month,
                    "image_url": p.image_url,
                    "is_active": p.is_active,
                }
                for p in products
            ],
        }
