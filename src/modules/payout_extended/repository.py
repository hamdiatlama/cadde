from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.payout_extended.models import PayoutSchedule, MultiCurrencyBalance

FIXED_RATES = {
    "USD": {"EUR": 0.92, "TRY": 34.50, "GBP": 0.79},
    "EUR": {"USD": 1.09, "TRY": 37.50, "GBP": 0.86},
    "TRY": {"USD": 0.029, "EUR": 0.027, "GBP": 0.023},
    "GBP": {"USD": 1.27, "EUR": 1.16, "TRY": 43.50},
}

class PayoutScheduleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def set_schedule(self, seller_id: int, frequency: str, day: int) -> PayoutSchedule:
        r = await self.db.execute(
            select(PayoutSchedule).where(PayoutSchedule.seller_id == seller_id)
        )
        sched = r.scalar_one_or_none()
        if sched:
            sched.frequency = frequency
            if frequency == "weekly":
                sched.day_of_week = day
            elif frequency in ("biweekly", "monthly"):
                sched.day_of_month = day
        else:
            sched = PayoutSchedule(seller_id=seller_id, frequency=frequency)
            if frequency == "weekly":
                sched.day_of_week = day
            elif frequency in ("biweekly", "monthly"):
                sched.day_of_month = day
            self.db.add(sched)
        return sched

    async def get_schedule(self, seller_id: int) -> PayoutSchedule | None:
        r = await self.db.execute(
            select(PayoutSchedule).where(PayoutSchedule.seller_id == seller_id)
        )
        return r.scalar_one_or_none()

    async def get_currency_balance(self, seller_id: int, currency: str) -> MultiCurrencyBalance | None:
        r = await self.db.execute(
            select(MultiCurrencyBalance).where(
                MultiCurrencyBalance.seller_id == seller_id,
                MultiCurrencyBalance.currency == currency,
            )
        )
        return r.scalar_one_or_none()

    async def add_currency_balance(self, seller_id: int, currency: str, amount: float) -> MultiCurrencyBalance:
        r = await self.db.execute(
            select(MultiCurrencyBalance).where(
                MultiCurrencyBalance.seller_id == seller_id,
                MultiCurrencyBalance.currency == currency,
            )
        )
        bal = r.scalar_one_or_none()
        if bal:
            bal.balance += amount
        else:
            bal = MultiCurrencyBalance(seller_id=seller_id, currency=currency, balance=amount)
            self.db.add(bal)
        return bal

    async def convert_currency(self, from_currency: str, to_currency: str, amount: float) -> dict:
        if from_currency == to_currency:
            return {"from": from_currency, "to": to_currency, "amount": amount, "converted": amount, "rate": 1.0}
        rates = FIXED_RATES.get(from_currency, {})
        rate = rates.get(to_currency)
        if rate is None:
            raise ValueError(f"No rate found for {from_currency} -> {to_currency}")
        return {"from": from_currency, "to": to_currency, "amount": amount, "converted": round(amount * rate, 2), "rate": rate}


