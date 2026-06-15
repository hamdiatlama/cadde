import json
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.fraud.models import FraudRule, FraudCheck, FraudTransactionHistory


class FraudRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_rule(self, name: str, rule_type: str, threshold_value: float, score: int = 10) -> FraudRule:
        r = FraudRule(name=name, rule_type=rule_type, threshold_value=threshold_value, score=score)
        self.db.add(r)
        return r

    async def list_rules(self):
        r = await self.db.execute(select(FraudRule).order_by(FraudRule.created_at.desc()))
        return r.scalars().all()

    async def toggle_rule(self, rule_id: int) -> FraudRule:
        r = await self.db.execute(select(FraudRule).where(FraudRule.id == rule_id))
        rule = r.scalar_one_or_none()
        if rule:
            rule.is_active = not rule.is_active
        return rule

    async def check_order(self, order_id: int, user_id: int, ip_address: str, amount: float) -> FraudCheck:
        r = await self.db.execute(select(FraudRule).where(FraudRule.is_active == True))
        rules = r.scalars().all()
        total_score = 0
        flags = []

        for rule in rules:
            triggered = False
            if rule.rule_type == "amount" and amount > rule.threshold_value:
                triggered = True
            elif rule.rule_type == "velocity":
                count = await self.get_user_velocity(user_id, 1)
                if count >= rule.threshold_value:
                    triggered = True
            elif rule.rule_type == "ip_geo" and ip_address:
                count_r = await self.db.execute(
                    select(func.count(FraudTransactionHistory.id)).where(
                        FraudTransactionHistory.ip_address == ip_address,
                        FraudTransactionHistory.created_at >= datetime.now(timezone.utc) - timedelta(hours=1)
                    )
                )
                if count_r.scalar() >= rule.threshold_value:
                    triggered = True
            elif rule.rule_type == "device":
                pass
            elif rule.rule_type == "email":
                pass

            if triggered:
                total_score += rule.score
                flags.append({"rule": rule.name, "score": rule.score})

        if total_score < 30:
            risk_level = "low"
        elif total_score < 60:
            risk_level = "medium"
        elif total_score < 80:
            risk_level = "high"
        else:
            risk_level = "critical"

        is_blocked = risk_level in ("high", "critical")
        check = FraudCheck(
            order_id=order_id, total_score=total_score,
            risk_level=risk_level, flags=json.dumps(flags), is_blocked=is_blocked
        )
        self.db.add(check)
        return check

    async def record_transaction(self, user_id: int, ip_address: str, device_fingerprint: str, amount: float, success: bool) -> FraudTransactionHistory:
        t = FraudTransactionHistory(
            user_id=user_id, ip_address=ip_address,
            device_fingerprint=device_fingerprint, amount=amount, success=success
        )
        self.db.add(t)
        return t

    async def get_order_risk(self, order_id: int):
        r = await self.db.execute(
            select(FraudCheck).where(FraudCheck.order_id == order_id).order_by(FraudCheck.checked_at.desc()).limit(1)
        )
        return r.scalar_one_or_none()

    async def get_user_velocity(self, user_id: int, hours: int = 1) -> int:
        since = datetime.now(timezone.utc) - timedelta(hours=hours)
        r = await self.db.execute(
            select(func.count(FraudTransactionHistory.id)).where(
                FraudTransactionHistory.user_id == user_id,
                FraudTransactionHistory.created_at >= since
            )
        )
        return r.scalar() or 0
