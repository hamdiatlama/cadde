from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.website_builder.repository import WebsiteRepository
from src.modules.hotel.repository import HotelRepository as HotelRepo


DEFAULT_PAGES = [
    {"slug": "home", "title": "Ana Sayfa", "sort_order": 0},
    {"slug": "rooms", "title": "Odalar", "sort_order": 1},
    {"slug": "gallery", "title": "Galeri", "sort_order": 2},
    {"slug": "contact", "title": "İletişim", "sort_order": 3},
    {"slug": "about", "title": "Hakkımızda", "sort_order": 4},
]


class WebsiteBuilderService:
    def __init__(self, db: AsyncSession):
        self.repo = WebsiteRepository(db)

    async def create_website(self, hotel_id: int, data: dict) -> dict:
        existing = await self.repo.get_hotel_website(hotel_id)
        if existing:
            raise ValueError("Hotel already has a website")

        hotel_repo = HotelRepo(self.repo.db)
        hotel = await hotel_repo.get_hotel(hotel_id)
        if not hotel:
            raise ValueError("Hotel not found")

        hotel_name = hotel.name.lower().replace(" ", "-").replace("ı", "i")
        hotel_name = "".join(c for c in hotel_name if c.isalnum() or c == "-").strip("-")

        subdomain = data.get("subdomain") or f"{hotel_name}.cadde.app"
        site_data = {
            "hotel_id": hotel_id,
            "subdomain": subdomain,
            "domain": data.get("domain"),
            "template_id": data.get("template_id", "default"),
            "primary_color": data.get("primary_color", "#4A7FD4"),
            "secondary_color": data.get("secondary_color", "#EEF4FF"),
            "font_family": data.get("font_family", "Space Grotesk"),
            "logo_url": data.get("logo_url", ""),
            "hero_image_url": data.get("hero_image_url", ""),
            "about_text": data.get("about_text", ""),
        }
        site = await self.repo.create_website(site_data)
        await self.repo.db.flush()

        for pg in DEFAULT_PAGES:
            await self.repo.create_page({
                "website_id": site.id,
                "slug": pg["slug"],
                "title": pg["title"],
                "content": "{}",
                "sort_order": pg["sort_order"],
            })

        seo_data = {
            "website_id": site.id,
            "meta_title": hotel.name,
            "meta_description": hotel.description or "",
            "meta_keywords": f"hotel, {hotel.city}, {hotel.name}" if hotel.city else "hotel",
        }
        await self.repo.create_seo(seo_data)

        await self.repo.create_booking_widget({
            "website_id": site.id,
            "widget_type": "inline",
            "embed_code": "",
        })

        await self.repo.db.flush()
        return self._format_website(site)

    async def get_website(self, hotel_id: int) -> dict | None:
        site = await self.repo.get_hotel_website(hotel_id)
        if not site:
            return None
        pages = await self.repo.list_pages(site.id)
        seo = await self.repo.get_seo_for_page(site.id)
        widget = await self.repo.get_booking_widget(site.id)
        return {
            **self._format_website(site),
            "pages": [self._format_page(p) for p in pages],
            "seo": self._format_seo(seo) if seo else None,
            "booking_widget": self._format_widget(widget) if widget else None,
        }

    async def update_website(self, hotel_id: int, data: dict) -> dict | None:
        site = await self.repo.get_hotel_website(hotel_id)
        if not site:
            return None
        allowed = ["domain", "template_id", "primary_color", "secondary_color",
                    "font_family", "logo_url", "hero_image_url", "about_text"]
        update = {k: v for k, v in data.items() if k in allowed and v is not None}
        site = await self.repo.update_website(site.id, update)
        await self.repo.db.flush()
        return self._format_website(site)

    async def publish_website(self, hotel_id: int) -> dict | None:
        site = await self.repo.get_hotel_website(hotel_id)
        if not site:
            return None
        site.is_published = True
        site.published_at = datetime.now(timezone.utc)
        self.repo.db.add(site)
        await self.repo.db.flush()
        return self._format_website(site)

    async def list_pages(self, website_id: int) -> list[dict]:
        pages = await self.repo.list_pages(website_id)
        return [self._format_page(p) for p in pages]

    async def update_page_content(self, page_id: int, data: dict) -> dict | None:
        page = await self.repo.get_page(page_id)
        if not page:
            return None
        allowed = ["title", "content", "sort_order", "is_active"]
        update = {k: v for k, v in data.items() if k in allowed and v is not None}
        page = await self.repo.update_page(page_id, update)
        await self.repo.db.flush()
        return self._format_page(page)

    async def update_seo(self, seo_id: int, data: dict) -> dict | None:
        allowed = ["meta_title", "meta_description", "meta_keywords",
                    "og_image_url", "canonical_url"]
        update = {k: v for k, v in data.items() if k in allowed and v is not None}
        seo = await self.repo.update_seo(seo_id, update)
        await self.repo.db.flush()
        return self._format_seo(seo)

    async def get_booking_widget(self, website_id: int) -> dict | None:
        widget = await self.repo.get_booking_widget(website_id)
        return self._format_widget(widget) if widget else None

    async def update_widget(self, widget_id: int, data: dict) -> dict | None:
        allowed = ["widget_type", "is_enabled", "embed_code", "custom_css"]
        update = {k: v for k, v in data.items() if k in allowed and v is not None}
        widget = await self.repo.update_widget(widget_id, update)
        await self.repo.db.flush()
        return self._format_widget(widget)

    async def generate_embed_code(self, hotel_id: int) -> dict | None:
        site = await self.repo.get_hotel_website(hotel_id)
        if not site:
            return None
        base = site.domain or f"https://{site.subdomain}"
        embed = f'<iframe src="{base}/book" width="100%" height="600" frameborder="0" style="border:none;border-radius:8px"></iframe>'
        return {"embed_code": embed, "url": f"{base}/book"}

    async def get_seo_analysis(self, hotel_id: int) -> dict | None:
        site = await self.repo.get_hotel_website(hotel_id)
        if not site:
            return None
        seo = await self.repo.get_seo_for_page(site.id)
        issues = []
        if not seo or not seo.meta_title:
            issues.append("Meta başlık eksik")
        if not seo or not seo.meta_description:
            issues.append("Meta açıklama eksik")
        if not seo or not seo.meta_keywords:
            issues.append("Anahtar kelimeler eksik")
        if not site.about_text:
            issues.append("Hakkımızda metni eksik")
        if not site.logo_url:
            issues.append("Logo yüklenmemiş")
        if not site.hero_image_url:
            issues.append("Hero görseli yüklenmemiş")
        return {
            "score": max(0, 100 - len(issues) * 16),
            "issues": issues,
            "total_issues": len(issues),
        }

    def _format_website(self, site) -> dict:
        return {
            "id": site.id,
            "hotel_id": site.hotel_id,
            "domain": site.domain,
            "subdomain": site.subdomain,
            "template_id": site.template_id,
            "primary_color": site.primary_color,
            "secondary_color": site.secondary_color,
            "font_family": site.font_family,
            "logo_url": site.logo_url or "",
            "hero_image_url": site.hero_image_url or "",
            "about_text": site.about_text or "",
            "is_published": site.is_published,
            "published_at": site.published_at.isoformat() if site.published_at else None,
            "created_at": site.created_at.isoformat() if site.created_at else None,
            "updated_at": site.updated_at.isoformat() if site.updated_at else None,
        }

    def _format_page(self, page) -> dict:
        return {
            "id": page.id,
            "website_id": page.website_id,
            "slug": page.slug,
            "title": page.title,
            "content": page.content,
            "sort_order": page.sort_order,
            "is_active": page.is_active,
            "created_at": page.created_at.isoformat() if page.created_at else None,
            "updated_at": page.updated_at.isoformat() if page.updated_at else None,
        }

    def _format_seo(self, seo) -> dict:
        return {
            "id": seo.id,
            "website_id": seo.website_id,
            "page_id": seo.page_id,
            "meta_title": seo.meta_title,
            "meta_description": seo.meta_description,
            "meta_keywords": seo.meta_keywords,
            "og_image_url": seo.og_image_url or "",
            "canonical_url": seo.canonical_url or "",
            "created_at": seo.created_at.isoformat() if seo.created_at else None,
        }

    def _format_widget(self, widget) -> dict:
        return {
            "id": widget.id,
            "website_id": widget.website_id,
            "widget_type": widget.widget_type,
            "is_enabled": widget.is_enabled,
            "embed_code": widget.embed_code or "",
            "custom_css": widget.custom_css or "",
            "created_at": widget.created_at.isoformat() if widget.created_at else None,
        }
