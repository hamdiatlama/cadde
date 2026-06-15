from datetime import datetime, timezone
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.payment_extended.models import CodOrder, BnplInstallment, CryptoPayment, Wallet, WalletTransaction


class CodRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_cod_order(self, order_id: int) -> CodOrder:
        cod = CodOrder(order_id=order_id, status="pending")
        self.db.add(cod)
        return cod

    async def get_cod_order(self, order_id: int):
        r = await self.db.execute(select(CodOrder).where(CodOrder.order_id == order_id))
        return r.scalar_one_or_none()

    async def mark_collected(self, order_id: int, amount: float):
        r = await self.db.execute(select(CodOrder).where(CodOrder.order_id == order_id))
        cod = r.scalar_one_or_none()
        if cod:
            cod.status = "collected"
            cod.collected_amount = amount
            cod.collected_at = datetime.now(timezone.utc)
        return cod


class BnplRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_installment(self, order_id: int, total_amount: float, installment_count: int) -> BnplInstallment:
        installment_amount = round(total_amount / installment_count, 2)
        inst = BnplInstallment(
            order_id=order_id, total_amount=total_amount,
            installment_count=installment_count, installment_amount=installment_amount,
            status="active",
        )
        self.db.add(inst)
        return inst

    async def get_installments(self, order_id: int):
        r = await self.db.execute(
            select(BnplInstallment).where(BnplInstallment.order_id == order_id)
            .order_by(BnplInstallment.created_at.desc())
        )
        return r.scalars().all()

    async def mark_paid(self, installment_id: int):
        r = await self.db.execute(select(BnplInstallment).where(BnplInstallment.id == installment_id))
        inst = r.scalar_one_or_none()
        if inst:
            inst.status = "paid"
        return inst


class CryptoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_payment(self, order_id: int, currency: str, wallet_address: str, amount: float) -> CryptoPayment:
        cp = CryptoPayment(
            order_id=order_id, currency=currency,
            wallet_address=wallet_address, amount=amount, status="pending",
        )
        self.db.add(cp)
        return cp

    async def get_by_tx_hash(self, tx_hash: str):
        r = await self.db.execute(select(CryptoPayment).where(CryptoPayment.tx_hash == tx_hash))
        return r.scalar_one_or_none()

    async def confirm_transaction(self, tx_hash: str):
        cp = await self.get_by_tx_hash(tx_hash)
        if cp:
            cp.status = "confirmed"
            cp.confirmations += 1
        return cp


class WalletRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_wallet(self, user_id: int) -> Wallet:
        r = await self.db.execute(select(Wallet).where(Wallet.user_id == user_id))
        wallet = r.scalar_one_or_none()
        if not wallet:
            wallet = Wallet(user_id=user_id, balance=0)
            self.db.add(wallet)
        return wallet

    async def add_balance(self, wallet_id: int, amount: float) -> Wallet:
        r = await self.db.execute(select(Wallet).where(Wallet.id == wallet_id))
        wallet = r.scalar_one_or_none()
        if wallet:
            wallet.balance += amount
            txn = WalletTransaction(wallet_id=wallet_id, amount=amount, type="deposit")
            self.db.add(txn)
        return wallet

    async def deduct_balance(self, wallet_id: int, amount: float) -> Wallet:
        r = await self.db.execute(select(Wallet).where(Wallet.id == wallet_id))
        wallet = r.scalar_one_or_none()
        if wallet and wallet.balance >= amount:
            wallet.balance -= amount
            txn = WalletTransaction(wallet_id=wallet_id, amount=-amount, type="withdraw")
            self.db.add(txn)
        return wallet

    async def get_balance(self, user_id: int) -> float:
        wallet = await self.get_or_create_wallet(user_id)
        return wallet.balance

    async def list_transactions(self, wallet_id: int, limit: int = 50):
        r = await self.db.execute(
            select(WalletTransaction).where(WalletTransaction.wallet_id == wallet_id)
            .order_by(WalletTransaction.created_at.desc()).limit(limit)
        )
        return r.scalars().all()
