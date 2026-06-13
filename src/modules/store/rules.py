from datetime import datetime, timezone, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.product import Product

MIN_DAYS_BEFORE_DISCOUNT = 7


def normalize_name(name: str) -> str:
    chars = str.maketrans("ıüöçşğİÜÖÇŞĞ", "iuocsgIUOCSG")
    return name.lower().translate(chars).replace("-", " ").replace("_", " ").strip()


async def validate_discount_creation(
    db: AsyncSession,
    seller_id: int,
    name: str,
    price: float,
    compare_price: float | None,
    original_product_id: int | None = None,
) -> list[str]:
    errors = []

    if compare_price is None or compare_price <= price:
        return errors

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=MIN_DAYS_BEFORE_DISCOUNT)

    if original_product_id:
        result = await db.execute(
            select(Product).where(
                Product.id == original_product_id,
                Product.seller_id == seller_id,
                Product.is_active == True,
            )
        )
        original = result.scalar_one_or_none()
        if not original:
            errors.append(f"Original product (id={original_product_id}) not found or does not belong to this seller")
            return errors

        if original.price < compare_price:
            errors.append("Compare price cannot be higher than original product's price")

        if original.created_at > cutoff:
            days_old = (now - original.created_at).days
            errors.append(
                f"Original product must be at least {MIN_DAYS_BEFORE_DISCOUNT} days old before discount. "
                f"Current age: {days_old} day(s)"
            )
    else:
        result = await db.execute(
            select(Product).where(
                Product.seller_id == seller_id,
                Product.is_active == True,
                Product.created_at > cutoff,
                Product.compare_price == None,
            )
        )
        recent_products = result.scalars().all()

        normalized_new = normalize_name(name)
        for existing in recent_products:
            normalized_existing = normalize_name(existing.name)
            if normalized_new == normalized_existing:
                errors.append(
                    f"A recently created product with name '{existing.name}' already exists. "
                    "New discounted products must have a distinct name."
                )
                break

        result2 = await db.execute(
            select(Product).where(
                Product.seller_id == seller_id,
                Product.is_active == True,
                Product.created_at <= cutoff,
            )
        )
        established = result2.scalars().all()

        normalized_new = normalize_name(name)
        for existing in established:
            normalized_existing = normalize_name(existing.name)
            if normalized_new == normalized_existing:
                return errors

        errors.append(
            "New discounted products must specify an 'original_product_id' linking to an established "
            f"product (at least {MIN_DAYS_BEFORE_DISCOUNT} days old) from your catalog."
        )

    return errors


async def validate_discount_update(
    db: AsyncSession,
    product: Product,
    new_price: float | None,
    new_compare_price: float | None,
) -> list[str]:
    errors = []

    effective_price = new_price if new_price is not None else product.price
    effective_compare = new_compare_price if new_compare_price is not None else product.compare_price

    if effective_compare is None or effective_compare <= effective_price:
        return errors

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=MIN_DAYS_BEFORE_DISCOUNT)

    if product.created_at > cutoff:
        days_old = (now - product.created_at).days
        errors.append(
            f"Product must be at least {MIN_DAYS_BEFORE_DISCOUNT} days old before a discount can be applied. "
            f"Current age: {days_old} day(s)"
        )

    return errors
