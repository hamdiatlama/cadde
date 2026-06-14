"""Business logic for bina/site management."""
from datetime import datetime, timezone
from src.modules.bina.repository import BinaRepository
from src.modules.bina.models import (
    Site, Blok, Daire, Kisi, Duyuru, Aidat, Gelir, Gider,
    Arac, Personel, Firma, IsTalebi, Sayac, Kargo, Ziyaretci,
    Anket, AnketSecenek, AnketOy, Icra, Otopark, Rezervasyon,
    Toplanti, BankaHesap, Isitma, Butce, Dosya, Bildirim,
)

class BinaService:
    def __init__(self, db):
        self.repo = BinaRepository(db)

    async def create_site(self, data) -> dict:
        site = Site(**data.dict())
        await self.repo.create_site(site)
        return {"id": site.id, "status": "site_created"}

    async def get_site(self, site_id: int) -> Site:
        return await self.repo.get_site(site_id)

    async def update_site(self, site_id: int, data) -> dict:
        site = await self.repo.get_site(site_id)
        if not site:
            raise ValueError("Site bulunamadi")
        for k, v in data.dict(exclude_unset=True).items():
            setattr(site, k, v)
        return {"status": "site_updated"}

    async def kurulum(self, site_id: int, blok_adi: str, kat: int, dk: int) -> dict:
        blok = Blok(site_id=site_id, adi=blok_adi, kat_adet=kat, daire_kat=dk)
        await self.repo.create_blok(blok)
        kapi_no = 1
        for k in range(1, kat + 1):
            for _ in range(1, dk + 1):
                no = f"{k}{_}"
                daire = Daire(blok_id=blok.id, no=no, kat=k, kapi_no=kapi_no)
                await self.repo.create_daire(daire)
                kapi_no += 1
        return {"blok_id": blok.id, "daire_sayisi": kat * dk}

    async def create_kisi(self, data) -> Kisi:
        kisi = Kisi(**data.dict())
        await self.repo.create_kisi(kisi)
        return kisi

    async def create_duyuru(self, data) -> Duyuru:
        duyuru = Duyuru(**data.dict())
        await self.repo.create_duyuru(duyuru)
        return duyuru

    async def aidat_hesapla(self, site_id: int, ay: int, yil: int, toplam: float) -> dict:
        daireler = await self.repo.list_daire(site_id)
        if not daireler:
            raise ValueError("Daire bulunamadi")
        daire_basi = toplam / len(daireler)
        for d in daireler:
            a = Aidat(site_id=site_id, daire_id=d.id, blok_id=d.blok_id,
                       daire_no=d.no, ay=ay, yil=yil, tutar=daire_basi, kapi_no=d.kapi_no)
            await self.repo.create_aidat(a)
        return {"daire_sayi": len(daireler), "daire_basi": daire_basi}

    async def aidat_ode(self, aidat_id: int):
        await self.repo.odemesi_yap(aidat_id)

    async def create_gelir(self, data) -> Gelir:
        g = Gelir(**data.dict())
        await self.repo.create_gelir(g)
        return g

    async def create_gider(self, data) -> Gider:
        g = Gider(**data.dict())
        await self.repo.create_gider(g)
        return g

    async def create_arac(self, data) -> Arac:
        a = Arac(**data.dict())
        await self.repo.create_arac(a)
        return a

    async def create_personel(self, data) -> Personel:
        p = Personel(**data.dict())
        await self.repo.create_personel(p)
        return p

    async def create_firma(self, data) -> Firma:
        f = Firma(**data.dict())
        await self.repo.create_firma(f)
        return f

    async def create_is_talebi(self, data) -> IsTalebi:
        t = IsTalebi(**data.dict())
        await self.repo.create_is_talebi(t)
        return t

    async def create_sayac(self, data) -> Sayac:
        s = Sayac(**data.dict())
        await self.repo.create_sayac(s)
        return s

    async def create_kargo(self, data) -> Kargo:
        k = Kargo(**data.dict())
        await self.repo.create_kargo(k)
        return k

    async def ziyaretci_giris(self, data) -> Ziyaretci:
        z = Ziyaretci(**data.dict())
        await self.repo.create_ziyaretci(z)
        return z

    async def ziyaretci_cikis(self, ziyaretci_id: int):
        await self.repo.ziyaretci_cikis(ziyaretci_id)

    async def create_anket(self, data) -> Anket:
        obj = Anket(**data.dict())
        await self.repo.create_anket(obj)
        return obj

    async def list_anket(self, site_id: int):
        return await self.repo.list_anket(site_id)

    async def get_anket(self, anket_id: int) -> Anket | None:
        return await self.repo.get_anket(anket_id)

    async def delete_anket(self, anket_id: int):
        await self.repo.delete_anket(anket_id)

    async def create_anket_secenek(self, data) -> AnketSecenek:
        obj = AnketSecenek(**data.dict())
        await self.repo.create_anket_secenek(obj)
        return obj

    async def list_anket_secenek(self, anket_id: int):
        return await self.repo.list_anket_secenek(anket_id)

    async def get_anket_secenek(self, secenek_id: int) -> AnketSecenek | None:
        return await self.repo.get_anket_secenek(secenek_id)

    async def delete_anket_secenek(self, secenek_id: int):
        await self.repo.delete_anket_secenek(secenek_id)

    async def create_anket_oy(self, data) -> AnketOy:
        obj = AnketOy(**data.dict())
        await self.repo.create_anket_oy(obj)
        return obj

    async def list_anket_oy(self, anket_id: int):
        return await self.repo.list_anket_oy(anket_id)

    async def get_anket_oy(self, oy_id: int) -> AnketOy | None:
        return await self.repo.get_anket_oy(oy_id)

    async def create_icra(self, data) -> Icra:
        obj = Icra(**data.dict())
        await self.repo.create_icra(obj)
        return obj

    async def list_icra(self, site_id: int):
        return await self.repo.list_icra(site_id)

    async def get_icra(self, icra_id: int) -> Icra | None:
        return await self.repo.get_icra(icra_id)

    async def delete_icra(self, icra_id: int):
        await self.repo.delete_icra(icra_id)

    async def create_otopark(self, data) -> Otopark:
        obj = Otopark(**data.dict())
        await self.repo.create_otopark(obj)
        return obj

    async def list_otopark(self, site_id: int):
        return await self.repo.list_otopark(site_id)

    async def get_otopark(self, otopark_id: int) -> Otopark | None:
        return await self.repo.get_otopark(otopark_id)

    async def delete_otopark(self, otopark_id: int):
        await self.repo.delete_otopark(otopark_id)

    async def create_rezervasyon(self, data) -> Rezervasyon:
        obj = Rezervasyon(**data.dict())
        await self.repo.create_rezervasyon(obj)
        return obj

    async def list_rezervasyon(self, site_id: int):
        return await self.repo.list_rezervasyon(site_id)

    async def get_rezervasyon(self, rezervasyon_id: int) -> Rezervasyon | None:
        return await self.repo.get_rezervasyon(rezervasyon_id)

    async def delete_rezervasyon(self, rezervasyon_id: int):
        await self.repo.delete_rezervasyon(rezervasyon_id)

    async def create_toplanti(self, data) -> Toplanti:
        obj = Toplanti(**data.dict())
        await self.repo.create_toplanti(obj)
        return obj

    async def list_toplanti(self, site_id: int):
        return await self.repo.list_toplanti(site_id)

    async def get_toplanti(self, toplanti_id: int) -> Toplanti | None:
        return await self.repo.get_toplanti(toplanti_id)

    async def delete_toplanti(self, toplanti_id: int):
        await self.repo.delete_toplanti(toplanti_id)

    async def create_banka_hesap(self, data) -> BankaHesap:
        obj = BankaHesap(**data.dict())
        await self.repo.create_banka_hesap(obj)
        return obj

    async def list_banka_hesap(self, site_id: int):
        return await self.repo.list_banka_hesap(site_id)

    async def get_banka_hesap(self, hesap_id: int) -> BankaHesap | None:
        return await self.repo.get_banka_hesap(hesap_id)

    async def delete_banka_hesap(self, hesap_id: int):
        await self.repo.delete_banka_hesap(hesap_id)

    async def create_isitma(self, data) -> Isitma:
        obj = Isitma(**data.dict())
        await self.repo.create_isitma(obj)
        return obj

    async def list_isitma(self, site_id: int):
        return await self.repo.list_isitma(site_id)

    async def get_isitma(self, isitma_id: int) -> Isitma | None:
        return await self.repo.get_isitma(isitma_id)

    async def delete_isitma(self, isitma_id: int):
        await self.repo.delete_isitma(isitma_id)

    async def create_butce(self, data) -> Butce:
        obj = Butce(**data.dict())
        await self.repo.create_butce(obj)
        return obj

    async def list_butce(self, site_id: int):
        return await self.repo.list_butce(site_id)

    async def get_butce(self, butce_id: int) -> Butce | None:
        return await self.repo.get_butce(butce_id)

    async def delete_butce(self, butce_id: int):
        await self.repo.delete_butce(butce_id)

    async def create_dosya(self, data) -> Dosya:
        obj = Dosya(**data.dict())
        await self.repo.create_dosya(obj)
        return obj

    async def list_dosya(self, site_id: int):
        return await self.repo.list_dosya(site_id)

    async def get_dosya(self, dosya_id: int) -> Dosya | None:
        return await self.repo.get_dosya(dosya_id)

    async def delete_dosya(self, dosya_id: int):
        await self.repo.delete_dosya(dosya_id)

    async def create_bildirim(self, data) -> Bildirim:
        obj = Bildirim(**data.dict())
        await self.repo.create_bildirim(obj)
        return obj

    async def list_bildirim(self, site_id: int):
        return await self.repo.list_bildirim(site_id)

    async def get_bildirim(self, bildirim_id: int) -> Bildirim | None:
        return await self.repo.get_bildirim(bildirim_id)

    async def delete_bildirim(self, bildirim_id: int):
        await self.repo.delete_bildirim(bildirim_id)
