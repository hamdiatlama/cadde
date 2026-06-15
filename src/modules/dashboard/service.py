from src.modules.dashboard.repository import DashboardRepository


class DashboardService:
    def __init__(self, db):
        self.repo = DashboardRepository(db)

    async def seller_dashboard(self, seller_id: int):
        stats = await self.repo.seller_stats(seller_id)
        monthly = await self.repo.seller_monthly_sales(seller_id)
        top = await self.repo.top_products(seller_id)
        return {"stats": stats, "monthly_sales": monthly, "top_products": top}

    async def admin_dashboard(self):
        return await self.repo.admin_stats()
