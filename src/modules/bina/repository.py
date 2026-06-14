from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.bina.models import (
    Site, Blok, Daire, Kisi, Duyuru, Aidat, Gelir, Gider,
    Arac, Personel, Firma, IsTalebi, Sayac, Kargo, Ziyaretci,
    Anket, AnketSecenek, AnketOy, Icra, Otopark, Rezervasyon,
    Toplanti, BankaHesap, Isitma, Butce, Dosya, Bildirim,
)

class BinaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Site
    async def create_site(self, site: Site):
        self.db.add(site)

    async def get_site(self, site_id: int) -> Site | None:
        r = await self.db.execute(select(Site).where(Site.id == site_id))
        return r.scalar_one_or_none()

    # Blok
    async def create_blok(self, blok: Blok):
        self.db.add(blok)

    async def list_blok(self, site_id: int):
        r = await self.db.execute(select(Blok).where(Blok.site_id == site_id).order_by(Blok.adi))
        return r.scalars().all()

    # Daire
    async def create_daire(self, daire: Daire):
        self.db.add(daire)

    async def list_daire(self, site_id: int):
        r = await self.db.execute(
            select(Daire).join(Blok).where(Blok.site_id == site_id).order_by(Blok.adi, Daire.kapi_no)
        )
        return r.scalars().all()

    # Kisi
    async def create_kisi(self, kisi: Kisi):
        self.db.add(kisi)

    async def list_kisi(self, site_id: int):
        r = await self.db.execute(select(Kisi).where(Kisi.site_id == site_id).order_by(Kisi.ad))
        return r.scalars().all()

    # Duyuru
    async def create_duyuru(self, duyuru: Duyuru):
        self.db.add(duyuru)

    async def list_duyuru(self, site_id: int):
        r = await self.db.execute(
            select(Duyuru).where(Duyuru.site_id == site_id).order_by(Duyuru.created_at.desc())
        )
        return r.scalars().all()

    # Aidat
    async def create_aidat(self, aidat: Aidat):
        self.db.add(aidat)

    async def list_aidat(self, site_id: int, ay: int, yil: int):
        r = await self.db.execute(
            select(Aidat).where(Aidat.site_id == site_id, Aidat.ay == ay, Aidat.yil == yil)
            .order_by(Aidat.kapi_no)
        )
        return r.scalars().all()

    async def odemesi_yap(self, aidat_id: int):
        r = await self.db.execute(select(Aidat).where(Aidat.id == aidat_id))
        a = r.scalar_one_or_none()
        if a:
            a.odendi = True
            a.odeme_tarihi = func.now()

    # Gelir
    async def create_gelir(self, g: Gelir):
        self.db.add(g)

    async def list_gelir(self, site_id: int):
        r = await self.db.execute(
            select(Gelir).where(Gelir.site_id == site_id).order_by(Gelir.created_at.desc())
        )
        return r.scalars().all()

    # Gider
    async def create_gider(self, g: Gider):
        self.db.add(g)

    async def list_gider(self, site_id: int):
        r = await self.db.execute(
            select(Gider).where(Gider.site_id == site_id).order_by(Gider.created_at.desc())
        )
        return r.scalars().all()

    # Arac
    async def create_arac(self, a: Arac):
        self.db.add(a)

    async def list_arac(self, site_id: int):
        r = await self.db.execute(select(Arac).where(Arac.site_id == site_id).order_by(Arac.plaka))
        return r.scalars().all()

    async def delete_arac(self, arac_id: int):
        r = await self.db.execute(select(Arac).where(Arac.id == arac_id))
        a = r.scalar_one_or_none()
        if a:
            await self.db.delete(a)

    # Personel
    async def create_personel(self, p: Personel):
        self.db.add(p)

    async def list_personel(self, site_id: int):
        r = await self.db.execute(select(Personel).where(Personel.site_id == site_id).order_by(Personel.ad))
        return r.scalars().all()

    # Firma
    async def create_firma(self, f: Firma):
        self.db.add(f)

    async def list_firma(self, site_id: int):
        r = await self.db.execute(select(Firma).where(Firma.site_id == site_id).order_by(Firma.ad))
        return r.scalars().all()

    # Is Talebi
    async def create_is_talebi(self, t: IsTalebi):
        self.db.add(t)

    async def list_is_talebi(self, site_id: int):
        r = await self.db.execute(
            select(IsTalebi).where(IsTalebi.site_id == site_id).order_by(IsTalebi.created_at.desc())
        )
        return r.scalars().all()

    # Sayac
    async def create_sayac(self, s: Sayac):
        self.db.add(s)

    async def list_sayac(self, site_id: int):
        r = await self.db.execute(
            select(Sayac).where(Sayac.site_id == site_id).order_by(Sayac.tarih.desc())
        )
        return r.scalars().all()

    # Kargo
    async def create_kargo(self, k: Kargo):
        self.db.add(k)

    async def list_kargo(self, site_id: int):
        r = await self.db.execute(
            select(Kargo).where(Kargo.site_id == site_id).order_by(Kargo.created_at.desc())
        )
        return r.scalars().all()

    # Ziyaretci
    async def create_ziyaretci(self, z: Ziyaretci):
        self.db.add(z)

    async def list_ziyaretci(self, site_id: int):
        r = await self.db.execute(
            select(Ziyaretci).where(Ziyaretci.site_id == site_id).order_by(Ziyaretci.giris.desc())
        )
        return r.scalars().all()

    async def ziyaretci_cikis(self, ziyaretci_id: int):
        r = await self.db.execute(select(Ziyaretci).where(Ziyaretci.id == ziyaretci_id))
        z = r.scalar_one_or_none()
        if z:
            z.cikis = func.now()

    # Anket
    async def create_anket(self, obj: Anket):
        self.db.add(obj)

    async def list_anket(self, site_id: int):
        r = await self.db.execute(
            select(Anket).where(Anket.site_id == site_id).order_by(Anket.created_at.desc())
        )
        return r.scalars().all()

    async def get_anket(self, anket_id: int) -> Anket | None:
        r = await self.db.execute(select(Anket).where(Anket.id == anket_id))
        return r.scalar_one_or_none()

    async def delete_anket(self, anket_id: int):
        r = await self.db.execute(select(Anket).where(Anket.id == anket_id))
        obj = r.scalar_one_or_none()
        if obj:
            await self.db.delete(obj)

    # AnketSecenek
    async def create_anket_secenek(self, obj: AnketSecenek):
        self.db.add(obj)

    async def list_anket_secenek(self, anket_id: int):
        r = await self.db.execute(
            select(AnketSecenek).where(AnketSecenek.anket_id == anket_id)
        )
        return r.scalars().all()

    async def get_anket_secenek(self, secenek_id: int) -> AnketSecenek | None:
        r = await self.db.execute(select(AnketSecenek).where(AnketSecenek.id == secenek_id))
        return r.scalar_one_or_none()

    async def delete_anket_secenek(self, secenek_id: int):
        r = await self.db.execute(select(AnketSecenek).where(AnketSecenek.id == secenek_id))
        obj = r.scalar_one_or_none()
        if obj:
            await self.db.delete(obj)

    # AnketOy
    async def create_anket_oy(self, obj: AnketOy):
        self.db.add(obj)

    async def list_anket_oy(self, anket_id: int):
        r = await self.db.execute(
            select(AnketOy).where(AnketOy.anket_id == anket_id)
        )
        return r.scalars().all()

    async def get_anket_oy(self, oy_id: int) -> AnketOy | None:
        r = await self.db.execute(select(AnketOy).where(AnketOy.id == oy_id))
        return r.scalar_one_or_none()

    # Icra
    async def create_icra(self, obj: Icra):
        self.db.add(obj)

    async def list_icra(self, site_id: int):
        r = await self.db.execute(
            select(Icra).where(Icra.site_id == site_id).order_by(Icra.created_at.desc())
        )
        return r.scalars().all()

    async def get_icra(self, icra_id: int) -> Icra | None:
        r = await self.db.execute(select(Icra).where(Icra.id == icra_id))
        return r.scalar_one_or_none()

    async def delete_icra(self, icra_id: int):
        r = await self.db.execute(select(Icra).where(Icra.id == icra_id))
        obj = r.scalar_one_or_none()
        if obj:
            await self.db.delete(obj)

    # Otopark
    async def create_otopark(self, obj: Otopark):
        self.db.add(obj)

    async def list_otopark(self, site_id: int):
        r = await self.db.execute(
            select(Otopark).where(Otopark.site_id == site_id).order_by(Otopark.created_at.desc())
        )
        return r.scalars().all()

    async def get_otopark(self, otopark_id: int) -> Otopark | None:
        r = await self.db.execute(select(Otopark).where(Otopark.id == otopark_id))
        return r.scalar_one_or_none()

    async def delete_otopark(self, otopark_id: int):
        r = await self.db.execute(select(Otopark).where(Otopark.id == otopark_id))
        obj = r.scalar_one_or_none()
        if obj:
            await self.db.delete(obj)

    # Rezervasyon
    async def create_rezervasyon(self, obj: Rezervasyon):
        self.db.add(obj)

    async def list_rezervasyon(self, site_id: int):
        r = await self.db.execute(
            select(Rezervasyon).where(Rezervasyon.site_id == site_id).order_by(Rezervasyon.created_at.desc())
        )
        return r.scalars().all()

    async def get_rezervasyon(self, rezervasyon_id: int) -> Rezervasyon | None:
        r = await self.db.execute(select(Rezervasyon).where(Rezervasyon.id == rezervasyon_id))
        return r.scalar_one_or_none()

    async def delete_rezervasyon(self, rezervasyon_id: int):
        r = await self.db.execute(select(Rezervasyon).where(Rezervasyon.id == rezervasyon_id))
        obj = r.scalar_one_or_none()
        if obj:
            await self.db.delete(obj)

    # Toplanti
    async def create_toplanti(self, obj: Toplanti):
        self.db.add(obj)

    async def list_toplanti(self, site_id: int):
        r = await self.db.execute(
            select(Toplanti).where(Toplanti.site_id == site_id).order_by(Toplanti.created_at.desc())
        )
        return r.scalars().all()

    async def get_toplanti(self, toplanti_id: int) -> Toplanti | None:
        r = await self.db.execute(select(Toplanti).where(Toplanti.id == toplanti_id))
        return r.scalar_one_or_none()

    async def delete_toplanti(self, toplanti_id: int):
        r = await self.db.execute(select(Toplanti).where(Toplanti.id == toplanti_id))
        obj = r.scalar_one_or_none()
        if obj:
            await self.db.delete(obj)

    # BankaHesap
    async def create_banka_hesap(self, obj: BankaHesap):
        self.db.add(obj)

    async def list_banka_hesap(self, site_id: int):
        r = await self.db.execute(
            select(BankaHesap).where(BankaHesap.site_id == site_id).order_by(BankaHesap.created_at.desc())
        )
        return r.scalars().all()

    async def get_banka_hesap(self, hesap_id: int) -> BankaHesap | None:
        r = await self.db.execute(select(BankaHesap).where(BankaHesap.id == hesap_id))
        return r.scalar_one_or_none()

    async def delete_banka_hesap(self, hesap_id: int):
        r = await self.db.execute(select(BankaHesap).where(BankaHesap.id == hesap_id))
        obj = r.scalar_one_or_none()
        if obj:
            await self.db.delete(obj)

    # Isitma
    async def create_isitma(self, obj: Isitma):
        self.db.add(obj)

    async def list_isitma(self, site_id: int):
        r = await self.db.execute(
            select(Isitma).where(Isitma.site_id == site_id).order_by(Isitma.created_at.desc())
        )
        return r.scalars().all()

    async def get_isitma(self, isitma_id: int) -> Isitma | None:
        r = await self.db.execute(select(Isitma).where(Isitma.id == isitma_id))
        return r.scalar_one_or_none()

    async def delete_isitma(self, isitma_id: int):
        r = await self.db.execute(select(Isitma).where(Isitma.id == isitma_id))
        obj = r.scalar_one_or_none()
        if obj:
            await self.db.delete(obj)

    # Butce
    async def create_butce(self, obj: Butce):
        self.db.add(obj)

    async def list_butce(self, site_id: int):
        r = await self.db.execute(
            select(Butce).where(Butce.site_id == site_id).order_by(Butce.created_at.desc())
        )
        return r.scalars().all()

    async def get_butce(self, butce_id: int) -> Butce | None:
        r = await self.db.execute(select(Butce).where(Butce.id == butce_id))
        return r.scalar_one_or_none()

    async def delete_butce(self, butce_id: int):
        r = await self.db.execute(select(Butce).where(Butce.id == butce_id))
        obj = r.scalar_one_or_none()
        if obj:
            await self.db.delete(obj)

    # Dosya
    async def create_dosya(self, obj: Dosya):
        self.db.add(obj)

    async def list_dosya(self, site_id: int):
        r = await self.db.execute(
            select(Dosya).where(Dosya.site_id == site_id).order_by(Dosya.created_at.desc())
        )
        return r.scalars().all()

    async def get_dosya(self, dosya_id: int) -> Dosya | None:
        r = await self.db.execute(select(Dosya).where(Dosya.id == dosya_id))
        return r.scalar_one_or_none()

    async def delete_dosya(self, dosya_id: int):
        r = await self.db.execute(select(Dosya).where(Dosya.id == dosya_id))
        obj = r.scalar_one_or_none()
        if obj:
            await self.db.delete(obj)

    # Bildirim
    async def create_bildirim(self, obj: Bildirim):
        self.db.add(obj)

    async def list_bildirim(self, site_id: int):
        r = await self.db.execute(
            select(Bildirim).where(Bildirim.site_id == site_id).order_by(Bildirim.created_at.desc())
        )
        return r.scalars().all()

    async def get_bildirim(self, bildirim_id: int) -> Bildirim | None:
        r = await self.db.execute(select(Bildirim).where(Bildirim.id == bildirim_id))
        return r.scalar_one_or_none()

    async def delete_bildirim(self, bildirim_id: int):
        r = await self.db.execute(select(Bildirim).where(Bildirim.id == bildirim_id))
        obj = r.scalar_one_or_none()
        if obj:
            await self.db.delete(obj)
