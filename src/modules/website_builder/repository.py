from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.website_builder.models import (
    HotelWebsite, WebsitePage, WebsiteSEO, WebsiteBookingWidget,
)


class WebsiteRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ─── HotelWebsite ────────────────────────────────────────────

    async def create_website(self, data: dict) -> HotelWebsite:
        site = HotelWebsite(**data)
        self.db.add(site)
        return site

    async def get_website(self, website_id: int) -> HotelWebsite | None:
        r = await self.db.execute(select(HotelWebsite).where(HotelWebsite.id == website_id))
        return r.scalar_one_or_none()

    async def get_hotel_website(self, hotel_id: int) -> HotelWebsite | None:
        r = await self.db.execute(select(HotelWebsite).where(HotelWebsite.hotel_id == hotel_id))
        return r.scalar_one_or_none()

    async def update_website(self, website_id: int, data: dict) -> HotelWebsite | None:
        site = await self.get_website(website_id)
        if not site:
            return None
        for field, val in data.items():
            setattr(site, field, val)
        self.db.add(site)
        return site

    # ─── WebsitePage ─────────────────────────────────────────────

    async def create_page(self, data: dict) -> WebsitePage:
        page = WebsitePage(**data)
        self.db.add(page)
        return page

    async def get_page(self, page_id: int) -> WebsitePage | None:
        r = await self.db.execute(select(WebsitePage).where(WebsitePage.id == page_id))
        return r.scalar_one_or_none()

    async def list_pages(self, website_id: int) -> list[WebsitePage]:
        r = await self.db.execute(
            select(WebsitePage).where(
                WebsitePage.website_id == website_id,
                WebsitePage.is_active == True,
            ).order_by(WebsitePage.sort_order)
        )
        return list(r.scalars().all())

    async def update_page(self, page_id: int, data: dict) -> WebsitePage | None:
        page = await self.get_page(page_id)
        if not page:
            return None
        for field, val in data.items():
            setattr(page, field, val)
        self.db.add(page)
        return page

    # ─── WebsiteSEO ──────────────────────────────────────────────

    async def create_seo(self, data: dict) -> WebsiteSEO:
        seo = WebsiteSEO(**data)
        self.db.add(seo)
        return seo

    async def get_seo(self, seo_id: int) -> WebsiteSEO | None:
        r = await self.db.execute(select(WebsiteSEO).where(WebsiteSEO.id == seo_id))
        return r.scalar_one_or_none()

    async def get_seo_for_page(self, website_id: int, page_id: int | None = None) -> WebsiteSEO | None:
        query = select(WebsiteSEO).where(WebsiteSEO.website_id == website_id)
        if page_id:
            query = query.where(WebsiteSEO.page_id == page_id)
        else:
            query = query.where(WebsiteSEO.page_id == None)
        r = await self.db.execute(query)
        return r.scalar_one_or_none()

    async def update_seo(self, seo_id: int, data: dict) -> WebsiteSEO | None:
        seo = await self.get_seo(seo_id)
        if not seo:
            return None
        for field, val in data.items():
            setattr(seo, field, val)
        self.db.add(seo)
        return seo

    # ─── WebsiteBookingWidget ────────────────────────────────────

    async def create_booking_widget(self, data: dict) -> WebsiteBookingWidget:
        widget = WebsiteBookingWidget(**data)
        self.db.add(widget)
        return widget

    async def get_booking_widget(self, website_id: int) -> WebsiteBookingWidget | None:
        r = await self.db.execute(
            select(WebsiteBookingWidget).where(WebsiteBookingWidget.website_id == website_id)
        )
        return r.scalar_one_or_none()

    async def get_widget(self, widget_id: int) -> WebsiteBookingWidget | None:
        r = await self.db.execute(select(WebsiteBookingWidget).where(WebsiteBookingWidget.id == widget_id))
        return r.scalar_one_or_none()

    async def update_widget(self, widget_id: int, data: dict) -> WebsiteBookingWidget | None:
        widget = await self.get_widget(widget_id)
        if not widget:
            return None
        for field, val in data.items():
            setattr(widget, field, val)
        self.db.add(widget)
        return widget
