from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.payment_extended.repository import CodRepository, BnplRepository, CryptoRepository, WalletRepository

router = APIRouter(prefix="/payment-extended", tags=["payment_extended"])


@router.post("/cod/{order_id}")
async def mark_cod(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = CodRepository(db)
    cod = await repo.create_cod_order(order_id)
    await db.commit()
    return {"id": cod.id, "order_id": cod.order_id, "status": cod.status}


@router.get("/cod/{order_id}")
async def get_cod_status(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = CodRepository(db)
    cod = await repo.get_cod_order(order_id)
    if not cod:
        raise HTTPException(404, "COD order not found")
    return {"id": cod.id, "order_id": cod.order_id, "status": cod.status, "collected_amount": cod.collected_amount, "collected_at": cod.collected_at}


@router.post("/bnpl/{order_id}")
async def create_bnpl(
    order_id: int,
    installment_count: int = Query(..., ge=2, le=12),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = BnplRepository(db)
    inst = await repo.create_installment(order_id, 0, installment_count)
    await db.commit()
    return {"id": inst.id, "order_id": inst.order_id, "installment_count": inst.installment_count, "installment_amount": inst.installment_amount, "status": inst.status}


@router.get("/bnpl/{order_id}")
async def list_bnpl(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = BnplRepository(db)
    installments = await repo.get_installments(order_id)
    return [
        {"id": i.id, "order_id": i.order_id, "total_amount": i.total_amount,
         "installment_count": i.installment_count, "installment_amount": i.installment_amount,
         "status": i.status, "next_payment_date": i.next_payment_date, "created_at": i.created_at}
        for i in installments
    ]


@router.post("/crypto/{order_id}")
async def create_crypto(
    order_id: int,
    currency: str = Query(..., pattern="^(BTC|ETH|USDT|BNB)$"),
    wallet_address: str = "",
    amount: float = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = CryptoRepository(db)
    cp = await repo.create_payment(order_id, currency, wallet_address, amount)
    await db.commit()
    return {"id": cp.id, "order_id": cp.order_id, "currency": cp.currency, "amount": cp.amount, "status": cp.status}


@router.post("/crypto/confirm")
async def confirm_crypto(
    tx_hash: str = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = CryptoRepository(db)
    cp = await repo.confirm_transaction(tx_hash)
    if not cp:
        raise HTTPException(404, "Transaction not found")
    await db.commit()
    return {"id": cp.id, "tx_hash": cp.tx_hash, "status": cp.status, "confirmations": cp.confirmations}


@router.get("/wallet/balance")
async def wallet_balance(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = WalletRepository(db)
    balance = await repo.get_balance(current_user.id)
    return {"user_id": current_user.id, "balance": balance}


@router.post("/wallet/deposit")
async def deposit_wallet(
    amount: float = Query(..., gt=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = WalletRepository(db)
    wallet = await repo.get_or_create_wallet(current_user.id)
    wallet = await repo.add_balance(wallet.id, amount)
    await db.commit()
    return {"wallet_id": wallet.id, "balance": wallet.balance, "message": f"{amount} deposited"}


@router.post("/wallet/withdraw")
async def withdraw_wallet(
    amount: float = Query(..., gt=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = WalletRepository(db)
    wallet = await repo.get_or_create_wallet(current_user.id)
    wallet = await repo.deduct_balance(wallet.id, amount)
    if not wallet:
        raise HTTPException(400, "Insufficient balance")
    await db.commit()
    return {"wallet_id": wallet.id, "balance": wallet.balance, "message": f"{amount} withdrawn"}


@router.get("/wallet/transactions")
async def wallet_transactions(
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = WalletRepository(db)
    wallet = await repo.get_or_create_wallet(current_user.id)
    txns = await repo.list_transactions(wallet.id, limit)
    return [
        {"id": t.id, "amount": t.amount, "type": t.type, "reference_id": t.reference_id,
         "reference_type": t.reference_type, "created_at": t.created_at}
        for t in txns
    ]
