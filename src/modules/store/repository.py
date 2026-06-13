from datetime import datetime, timezone
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.product import Product
from src.models.seller import Seller
from src.modules.store.schemas import ProductResponse, ProductCreate, ProductUpdate
from src.modules.store.rules import validate_discount_creation, validate_discount_update

class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_seller_by_user(self, user_id: int):
        r = await self.db.execute(select(Seller).where(Seller.user_id == user_id))
        return r.scalar_one_or_none()

    def _generate_slug(self, name: str) -> str:
        tr_map = {"ı": "i", "ü": "u", "ö": "o", "ç": "c", "ş": "s", "ğ": "g"}
        slug = name.lower().replace(" ", "-")
        for k, v in tr_map.items():
            slug = slug.replace(k, v)
        return slug[:80]

    async def create_product(self, data: ProductCreate, seller_id: int):
        discount_errors = await validate_discount_creation(
            self.db, seller_id, data.name, data.price, data.compare_price, data.original_product_id
        )
        if discount_errors:
            return None, "; ".join(discount_errors)

        product = Product(
            seller_id=seller_id, name=data.name, description=data.description,
            category=data.category, subcategory=data.subcategory,
            price=data.price, compare_price=data.compare_price,
            original_price=data.compare_price if data.compare_price and data.compare_price > data.price else data.price,
            original_product_id=data.original_product_id,
            is_discounted=bool(data.compare_price and data.compare_price > data.price),
            image_url=data.image_url, stock=data.stock, tags=data.tags,
            color=data.color, occasion=data.occasion,
        )
        product.slug = self._generate_slug(data.name)
        if product.is_discounted:
            product.discount_start_at = datetime.now(timezone.utc)
        self.db.add(product)
        return product, None

    async def get_product_by_id(self, product_id: int):
        r = await self.db.execute(
            select(Product).where(Product.id == product_id, Product.is_active == True)
        )
        return r.scalar_one_or_none()

    async def update_product(self, product_id: int, seller_id: int, data: ProductUpdate):
        r = await self.db.execute(
            select(Product).where(Product.id == product_id, Product.seller_id == seller_id)
        )
        product = r.scalar_one_or_none()
        if not product:
            return None

        discount_errors = await validate_discount_update(self.db, product, data.price, data.compare_price)
        if discount_errors:
            return None, "; ".join(discount_errors)

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        if product.compare_price and product.compare_price > product.price:
            if not product.is_discounted:
                product.is_discounted = True
                product.discount_start_at = datetime.now(timezone.utc)
        else:
            product.is_discounted = False
            product.discount_start_at = None
        return product, None

    async def search_products(self, q=None, category=None, subcategory=None, occasion=None,
                               min_price=None, max_price=None, color=None, seller_id=None,
                               sort_by="created_at", sort_order="desc",
                               page=1, per_page=20):
        query = select(Product).where(Product.is_active == True)
        if q:
            query = query.where(or_(
                Product.name.ilike(f"%{q}%"), Product.description.ilike(f"%{q}%"),
                Product.tags.ilike(f"%{q}%"),
            ))
        if category:
            query = query.where(Product.category == category)
        if subcategory:
            query = query.where(Product.subcategory == subcategory)
        if occasion:
            query = query.where(Product.occasion == occasion)
        if min_price is not None:
            query = query.where(Product.price >= min_price)
        if max_price is not None:
            query = query.where(Product.price <= max_price)
        if color:
            query = query.where(Product.color.ilike(f"%{color}%"))
        if seller_id:
            query = query.where(Product.seller_id == seller_id)

        count_q = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_q)).scalar()

        sort_map = {"price": Product.price, "rating": Product.rating,
                     "created_at": Product.created_at, "name": Product.name}
        col = sort_map.get(sort_by, Product.created_at)
        query = query.order_by(col.asc() if sort_order == "asc" else col.desc())
        query = query.offset((page - 1) * per_page).limit(per_page)

        r = await self.db.execute(query)
        return total, r.scalars().all()

    async def get_categories(self):
        r = await self.db.execute(
            select(Product.category, func.count(Product.id))
            .where(Product.is_active == True, Product.category.isnot(None))
            .group_by(Product.category)
        )
        categories = [{"name": row[0], "count": row[1]} for row in r.all()]
        r2 = await self.db.execute(
            select(Product.occasion, func.count(Product.id))
            .where(Product.is_active == True, Product.occasion.isnot(None))
            .group_by(Product.occasion)
        )
        occasions = [{"name": row[0], "count": row[1]} for row in r2.all()]
        return {"categories": categories, "occasions": occasions}
