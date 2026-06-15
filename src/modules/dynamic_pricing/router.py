from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.dynamic_pricing.repository import PricingRuleRepository, PriceHistoryRepository, InventoryForecastRepository

router = APIRouter(prefix="/dynamic-pricing", tags=["dynamic_pricing"])


@router.post("/rules", status_code=201)
async def create_rule(rule_data: dict, current_user: User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    repo = PricingRuleRepository(db)
    rule_data["seller_id"] = current_user.id
    rule = await repo.create(rule_data)
    await db.commit()
    return {"id": rule.id, "rule_type": rule.rule_type}


@router.get("/rules")
async def list_rules(current_user: User = Depends(get_current_user),
                     db: AsyncSession = Depends(get_db)):
    repo = PricingRuleRepository(db)
    return await repo.list_all(seller_id=current_user.id)


@router.put("/rules/{id}/toggle")
async def toggle_rule(id: int, current_user: User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    repo = PricingRuleRepository(db)
    rule = await repo.toggle(id)
    if not rule:
        raise HTTPException(404, "Rule not found")
    await db.commit()
    return {"id": rule.id, "is_active": rule.is_active}


@router.post("/apply/{product_id}")
async def apply_rules(product_id: int, current_user: User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    rule_repo = PricingRuleRepository(db)
    history_repo = PriceHistoryRepository(db)
    try:
        from src.modules.store.models import Product
        pr = await db.execute(select(Product).where(Product.id == product_id))
        product = pr.scalar_one_or_none()
        if not product:
            raise HTTPException(404, "Product not found")
        old_price = float(product.price)
        new_price = await rule_repo.apply_rules(product_id)
        product.price = new_price
        await history_repo.record_change(product_id, old_price, new_price, "auto_pricing")
        await db.commit()
        return {"product_id": product_id, "old_price": old_price, "new_price": new_price}
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/history/{product_id}")
async def get_price_history(product_id: int, db: AsyncSession = Depends(get_db)):
    repo = PriceHistoryRepository(db)
    return await repo.get_history(product_id)


@router.post("/forecast/{product_id}")
async def calculate_forecast(product_id: int, current_user: User = Depends(get_current_user),
                             db: AsyncSession = Depends(get_db)):
    repo = InventoryForecastRepository(db)
    forecast = await repo.calculate_forecast(product_id)
    await db.commit()
    return {
        "id": forecast.id, "product_id": forecast.product_id,
        "predicted_demand": forecast.predicted_demand,
        "confidence": forecast.confidence, "suggested_order_qty": forecast.suggested_order_qty
    }


@router.get("/forecast/{product_id}")
async def get_forecast(product_id: int, db: AsyncSession = Depends(get_db)):
    repo = InventoryForecastRepository(db)
    forecast = await repo.get_forecast(product_id)
    if not forecast:
        raise HTTPException(404, "No forecast found")
    return forecast
