from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.payment_gateway.service import PaymentGatewayService
from src.modules.hotel.models import Hotel
from sqlalchemy import select

router = APIRouter(prefix="/payment-gateway", tags=["payment_gateway"])


def get_service(db: AsyncSession = Depends(get_db)) -> PaymentGatewayService:
    return PaymentGatewayService(db)


async def _get_hotel_owner_check(hotel_id: int, current_user: User, db: AsyncSession):
    r = await db.execute(select(Hotel).where(Hotel.id == hotel_id))
    hotel = r.scalar_one_or_none()
    if not hotel:
        raise HTTPException(404, "Hotel not found")
    if hotel.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(403, "You do not own this hotel")
    return hotel


@router.get("/providers")
async def list_providers(
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return await svc.list_providers()


@router.post("/merchant", status_code=201)
async def create_merchant_account(
    hotel_id: int = Query(...),
    provider_id: int = Query(...),
    api_key: str = Query(None),
    api_secret: str = Query(None),
    merchant_id: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await _get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    result, err = await svc.create_merchant_account(
        hotel_id=hotel_id, provider_id=provider_id,
        api_key=api_key, api_secret=api_secret, merchant_id=merchant_id,
    )
    if err:
        raise HTTPException(400, err)
    await db.commit()
    return result


@router.get("/merchant/{hotel_id}")
async def get_merchant_accounts(
    hotel_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await _get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    return await svc.get_merchant_accounts(hotel_id)


@router.post("/pay", status_code=201)
async def process_payment(
    booking_id: int = Query(...),
    amount: float = Query(...),
    currency: str = Query("TRY"),
    payment_method: str = Query(...),
    card_number: str = Query(None),
    card_holder: str = Query(None),
    card_expiry: str = Query(None),
    card_cvv: str = Query(None),
    installment: int = Query(1, ge=1, le=12),
    merchant_account_id: int = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    card_info = None
    if card_number:
        card_info = {
            "card_number": card_number, "card_holder": card_holder,
            "card_expiry": card_expiry, "card_cvv": card_cvv,
            "installment": installment,
        }
    result = await svc.process_payment(
        booking_id=booking_id, amount=amount, currency=currency,
        payment_method=payment_method, card_info=card_info,
        merchant_account_id=merchant_account_id,
    )
    await db.commit()
    return result


@router.post("/complete/{reference_no}")
async def complete_payment(
    reference_no: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    result, err = await svc.complete_payment(reference_no)
    if err:
        raise HTTPException(400, err)
    await db.commit()
    return result


@router.post("/refund/{transaction_id}")
async def refund_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(403, "Only admins can refund transactions")
    svc = get_service(db)
    result, err = await svc.process_refund(transaction_id)
    if err:
        raise HTTPException(400, err)
    await db.commit()
    return result


@router.get("/transactions")
async def list_transactions(
    booking_id: int = Query(None),
    hotel_id: int = Query(None),
    status: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return await svc.list_transactions(booking_id=booking_id, hotel_id=hotel_id, status=status)


@router.post("/payout", status_code=201)
async def request_payout(
    hotel_id: int = Query(...),
    amount: float = Query(...),
    iban: str = Query(...),
    account_holder: str = Query(None),
    bank_name: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await _get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    result, err = await svc.request_payout(
        hotel_id=hotel_id, amount=amount, iban=iban,
        account_holder=account_holder, bank_name=bank_name,
    )
    if err:
        raise HTTPException(400, err)
    await db.commit()
    return result


@router.get("/payouts/{hotel_id}")
async def list_payouts(
    hotel_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await _get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    return await svc.list_payouts(hotel_id)


@router.get("/balance/{hotel_id}")
async def get_balance(
    hotel_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await _get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    return await svc.get_hotel_balance(hotel_id)


@router.get("/report/{hotel_id}")
async def transaction_report(
    hotel_id: int,
    date_from: str = Query(...),
    date_to: str = Query(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await _get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    try:
        dt_from = datetime.fromisoformat(date_from)
        dt_to = datetime.fromisoformat(date_to)
    except ValueError:
        raise HTTPException(400, "Invalid date format. Use ISO format (YYYY-MM-DD)")
    return await svc.get_transaction_report(hotel_id, dt_from, dt_to)
