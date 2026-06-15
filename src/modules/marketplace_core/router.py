from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.store.models import Product
from src.modules.marketplace_core.repository import (
    MultiVendorCartRepository,
    SellerApplicationRepository,
    PreOrderRepository,
    GuestCheckoutRepository,
)

router = APIRouter(prefix="/marketplace", tags=["marketplace"])


@router.post("/cart", status_code=201)
async def create_cart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = MultiVendorCartRepository(db)
    cart = await repo.create_cart(current_user.id)
    await db.commit()
    await db.refresh(cart)
    return cart


@router.post("/cart/items", status_code=201)
async def add_cart_item(
    seller_id: int, product_id: int, quantity: int = 1,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = MultiVendorCartRepository(db)
    cart = await repo.get_cart(current_user.id)
    if not cart:
        cart = await repo.create_cart(current_user.id)
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(404, "Product not found")
    item = await repo.add_item(cart.id, seller_id, product_id, quantity, product.price)
    cart.total_amount += product.price * quantity
    await db.commit()
    await db.refresh(item)
    return item


@router.get("/cart")
async def get_cart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = MultiVendorCartRepository(db)
    cart = await repo.get_cart(current_user.id)
    if not cart:
        raise HTTPException(404, "Cart not found")
    items = await repo.get_cart_items(cart.id)
    return {"cart": {"id": cart.id, "total_amount": cart.total_amount, "created_at": cart.created_at}, "items": [{"id": i.id, "seller_id": i.seller_id, "product_id": i.product_id, "quantity": i.quantity, "price": i.price} for i in items]}


@router.post("/cart/checkout", status_code=201)
async def checkout_cart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = MultiVendorCartRepository(db)
    cart = await repo.get_cart(current_user.id)
    if not cart:
        raise HTTPException(400, "No active cart")
    orders = await repo.checkout(cart.id, current_user.id)
    if not orders:
        raise HTTPException(400, "Cart is empty")
    await db.commit()
    return {"orders": [{"id": o.id, "seller_id": o.seller_id, "total": o.total, "status": o.status} for o in orders]}


@router.post("/seller/apply", status_code=201)
async def apply_seller(
    company_name: str, tax_number: str, phone: str, business_type: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = SellerApplicationRepository(db)
    existing = await repo.get_status(current_user.id)
    if existing and existing.status == "pending":
        raise HTTPException(400, "Application already pending")
    app = await repo.apply(current_user.id, company_name, tax_number, phone, business_type)
    await db.commit()
    await db.refresh(app)
    return app


@router.get("/seller/application/status")
async def get_application_status(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = SellerApplicationRepository(db)
    app = await repo.get_status(current_user.id)
    if not app:
        raise HTTPException(404, "No application found")
    return app


@router.get("/admin/applications")
async def list_pending_applications(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = SellerApplicationRepository(db)
    apps = await repo.list_pending()
    return apps


@router.put("/admin/applications/{application_id}/approve")
async def approve_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = SellerApplicationRepository(db)
    app = await repo.approve(application_id, current_user.id)
    if not app:
        raise HTTPException(404, "Application not found")
    await db.commit()
    return app


@router.put("/admin/applications/{application_id}/reject")
async def reject_application(
    application_id: int, notes: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = SellerApplicationRepository(db)
    app = await repo.reject(application_id, current_user.id, notes)
    if not app:
        raise HTTPException(404, "Application not found")
    await db.commit()
    return app


@router.post("/pre-orders", status_code=201)
async def create_pre_order(
    product_id: int, quantity: int = 1, expected_stock_date: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = PreOrderRepository(db)
    po = await repo.create_pre_order(current_user.id, product_id, quantity, expected_stock_date)
    await db.commit()
    await db.refresh(po)
    return po


@router.get("/pre-orders/my")
async def get_my_pre_orders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = PreOrderRepository(db)
    return await repo.list_by_user(current_user.id)


@router.post("/guest/checkout", status_code=201)
async def guest_checkout(
    email: str, session_id: str, order_id: int,
    db: AsyncSession = Depends(get_db),
):
    repo = GuestCheckoutRepository(db)
    guest = await repo.create_guest(email, session_id, order_id)
    await db.commit()
    await db.refresh(guest)
    return guest


@router.post("/guest/convert/{guest_id}")
async def convert_guest(
    guest_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = GuestCheckoutRepository(db)
    guest = await repo.convert_to_account(guest_id, current_user.id)
    if not guest:
        raise HTTPException(404, "Guest checkout not found")
    await db.commit()
    return guest
