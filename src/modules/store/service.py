from src.modules.store.repository import ProductRepository
from src.modules.store.schemas import ProductResponse
from src.core.search import search

class ProductService:
    def __init__(self, db):
        self.repo = ProductRepository(db)

    async def create_product(self, data, current_user):
        if current_user.role not in ("seller", "admin"):
            return None, "Only sellers can create products"
        seller = await self.repo.get_seller_by_user(current_user.id)
        if not seller and current_user.role != "admin":
            return None, "Seller profile not found"
        seller_id = seller.id if seller else 1
        product, err = await self.repo.create_product(data, seller_id)
        if err:
            return None, err
        try:
            search.add_documents("products", [{
                "id": product.id, "name": product.name,
                "description": product.description, "category": product.category,
                "price": product.price, "seller_id": product.seller_id,
            }], primary_key="id")
        except Exception:
            pass
        return ProductResponse.model_validate(product), None

    async def update_product(self, product_id, data, current_user):
        if current_user.role not in ("seller", "admin"):
            return None, "Only sellers can update products"
        seller = await self.repo.get_seller_by_user(current_user.id)
        if not seller and current_user.role != "admin":
            return None, "Seller profile not found"
        result = await self.repo.update_product(product_id, seller.id if seller else 1, data)
        if isinstance(result, tuple):
            return None, result[1]
        if not result:
            return None, "Product not found"
        return ProductResponse.model_validate(result), None

    async def search_products(self, q=None, category=None, subcategory=None, occasion=None,
                               min_price=None, max_price=None, color=None, seller_id=None,
                               sort_by="created_at", sort_order="desc", page=1, per_page=20):
        total, products = await self.repo.search_products(
            q, category, subcategory, occasion, min_price, max_price,
            color, seller_id, sort_by, sort_order, page, per_page
        )
        return {
            "total": total, "page": page, "per_page": per_page,
            "total_pages": -(-total // per_page),
            "results": [ProductResponse.model_validate(p) for p in products],
        }

    async def get_categories(self):
        return await self.repo.get_categories()

    async def get_product(self, product_id):
        product = await self.repo.get_product_by_id(product_id)
        if not product:
            return None
        return ProductResponse.model_validate(product)
