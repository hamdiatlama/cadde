from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db

router = APIRouter(prefix="/bina", tags=["bina"])

# ── Site ──────────────────────────────────────────────────

@router.post("/site", status_code=201)
async def create_site(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    result = await svc.create_site(data)
    await db.commit()
    return result

@router.get("/site/{site_id}")
async def get_site(site_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    site = await svc.get_site(site_id)
    if not site:
        raise HTTPException(404)
    return site

@router.put("/site/{site_id}")
async def update_site(site_id: int, data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    try:
        result = await svc.update_site(site_id, data)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(400, str(e))

# ── Kurulum ────────────────────────────────────────────────

@router.post("/kurulum", status_code=201)
async def kurulum(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    result = await svc.kurulum(data["site_id"], data["blok_adi"], data["kat"], data["dk"])
    await db.commit()
    return result

# ── Blok ─────────────────────────────────────────────────

@router.get("/blok")
async def list_blok(site_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_blok(site_id)

# ── Daire ─────────────────────────────────────────────────

@router.get("/daire")
async def list_daire(site_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_daire(site_id)

# ── Kisi ─────────────────────────────────────────────────

@router.post("/kisi", status_code=201)
async def create_kisi(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    kisi = await svc.create_kisi(data)
    await db.commit()
    return kisi

@router.get("/kisi")
async def list_kisi(site_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_kisi(site_id)

# ── Duyuru ───────────────────────────────────────────────

@router.post("/duyuru", status_code=201)
async def create_duyuru(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    d = await svc.create_duyuru(data)
    await db.commit()
    return d

@router.get("/duyuru")
async def list_duyuru(site_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_duyuru(site_id)

# ── Aidat ────────────────────────────────────────────────

@router.post("/aidat/hesapla", status_code=201)
async def aidat_hesapla(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    try:
        result = await svc.aidat_hesapla(data["site_id"], data["ay"], data["yil"], data["toplam"])
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/aidat")
async def list_aidat(site_id: int, ay: int, yil: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_aidat(site_id, ay, yil)

@router.post("/aidat/{aidat_id}/ode")
async def aidat_ode(aidat_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    await svc.aidat_ode(aidat_id)
    await db.commit()
    return {"status": "odendi"}

# ── Gelir / Gider ────────────────────────────────────────

@router.post("/gelir", status_code=201)
async def create_gelir(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    g = await svc.create_gelir(data)
    await db.commit()
    return g

@router.get("/gelir")
async def list_gelir(site_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_gelir(site_id)

@router.post("/gider", status_code=201)
async def create_gider(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    g = await svc.create_gider(data)
    await db.commit()
    return g

@router.get("/gider")
async def list_gider(site_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_gider(site_id)

# ── Arac ─────────────────────────────────────────────────

@router.post("/arac", status_code=201)
async def create_arac(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    a = await svc.create_arac(data)
    await db.commit()
    return a

@router.get("/arac")
async def list_arac(site_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_arac(site_id)

@router.delete("/arac/{arac_id}", status_code=204)
async def delete_arac(arac_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    await repo.delete_arac(arac_id)
    await db.commit()

# ── Personel ─────────────────────────────────────────────

@router.post("/personel", status_code=201)
async def create_personel(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    p = await svc.create_personel(data)
    await db.commit()
    return p

@router.get("/personel")
async def list_personel(site_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_personel(site_id)

# ── Firma ────────────────────────────────────────────────

@router.post("/firma", status_code=201)
async def create_firma(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    f = await svc.create_firma(data)
    await db.commit()
    return f

@router.get("/firma")
async def list_firma(site_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_firma(site_id)

# ── Is Talebi ────────────────────────────────────────────

@router.post("/is-talebi", status_code=201)
async def create_is_talebi(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    t = await svc.create_is_talebi(data)
    await db.commit()
    return t

@router.get("/is-talebi")
async def list_is_talebi(site_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_is_talebi(site_id)

# ── Sayac ────────────────────────────────────────────────

@router.post("/sayac", status_code=201)
async def create_sayac(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    s = await svc.create_sayac(data)
    await db.commit()
    return s

@router.get("/sayac")
async def list_sayac(site_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_sayac(site_id)

# ── Kargo ────────────────────────────────────────────────

@router.post("/kargo", status_code=201)
async def create_kargo(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    k = await svc.create_kargo(data)
    await db.commit()
    return k

@router.get("/kargo")
async def list_kargo(site_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_kargo(site_id)

# ── Ziyaretci ────────────────────────────────────────────

@router.post("/ziyaretci", status_code=201)
async def ziyaretci_giris(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    z = await svc.ziyaretci_giris(data)
    await db.commit()
    return z

@router.get("/ziyaretci")
async def list_ziyaretci(site_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_ziyaretci(site_id)

@router.post("/ziyaretci/{ziyaretci_id}/cikis")
async def ziyaretci_cikis(ziyaretci_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    await svc.ziyaretci_cikis(ziyaretci_id)
    await db.commit()
    return {"status": "cikis_kaydedildi"}

# ── Anket ────────────────────────────────────────────────

@router.post("/anket", status_code=201)
async def create_anket(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    obj = await svc.create_anket(data)
    await db.commit()
    return obj

@router.get("/anket")
async def list_anket(site_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_anket(site_id)

@router.get("/anket/{anket_id}")
async def get_anket(anket_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    obj = await svc.get_anket(anket_id)
    if not obj:
        raise HTTPException(404)
    return obj

@router.delete("/anket/{anket_id}", status_code=204)
async def delete_anket(anket_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    await repo.delete_anket(anket_id)
    await db.commit()

# ── Anket Secenek ────────────────────────────────────────

@router.post("/anket-secenek", status_code=201)
async def create_anket_secenek(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    obj = await svc.create_anket_secenek(data)
    await db.commit()
    return obj

@router.get("/anket-secenek")
async def list_anket_secenek(anket_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_anket_secenek(anket_id)

@router.get("/anket-secenek/{secenek_id}")
async def get_anket_secenek(secenek_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    obj = await svc.get_anket_secenek(secenek_id)
    if not obj:
        raise HTTPException(404)
    return obj

@router.delete("/anket-secenek/{secenek_id}", status_code=204)
async def delete_anket_secenek(secenek_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    await repo.delete_anket_secenek(secenek_id)
    await db.commit()

# ── Anket Oy ─────────────────────────────────────────────

@router.post("/anket-oy", status_code=201)
async def create_anket_oy(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    obj = await svc.create_anket_oy(data)
    await db.commit()
    return obj

@router.get("/anket-oy")
async def list_anket_oy(anket_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_anket_oy(anket_id)

@router.get("/anket-oy/{oy_id}")
async def get_anket_oy(oy_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    obj = await svc.get_anket_oy(oy_id)
    if not obj:
        raise HTTPException(404)
    return obj

# ── Icra ─────────────────────────────────────────────────

@router.post("/icra", status_code=201)
async def create_icra(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    obj = await svc.create_icra(data)
    await db.commit()
    return obj

@router.get("/icra")
async def list_icra(site_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_icra(site_id)

@router.get("/icra/{icra_id}")
async def get_icra(icra_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    obj = await svc.get_icra(icra_id)
    if not obj:
        raise HTTPException(404)
    return obj

@router.delete("/icra/{icra_id}", status_code=204)
async def delete_icra(icra_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    await repo.delete_icra(icra_id)
    await db.commit()

# ── Otopark ──────────────────────────────────────────────

@router.post("/otopark", status_code=201)
async def create_otopark(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    obj = await svc.create_otopark(data)
    await db.commit()
    return obj

@router.get("/otopark")
async def list_otopark(site_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_otopark(site_id)

@router.get("/otopark/{otopark_id}")
async def get_otopark(otopark_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    obj = await svc.get_otopark(otopark_id)
    if not obj:
        raise HTTPException(404)
    return obj

@router.delete("/otopark/{otopark_id}", status_code=204)
async def delete_otopark(otopark_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    await repo.delete_otopark(otopark_id)
    await db.commit()

# ── Rezervasyon ──────────────────────────────────────────

@router.post("/rezervasyon", status_code=201)
async def create_rezervasyon(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    obj = await svc.create_rezervasyon(data)
    await db.commit()
    return obj

@router.get("/rezervasyon")
async def list_rezervasyon(site_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_rezervasyon(site_id)

@router.get("/rezervasyon/{rezervasyon_id}")
async def get_rezervasyon(rezervasyon_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    obj = await svc.get_rezervasyon(rezervasyon_id)
    if not obj:
        raise HTTPException(404)
    return obj

@router.delete("/rezervasyon/{rezervasyon_id}", status_code=204)
async def delete_rezervasyon(rezervasyon_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    await repo.delete_rezervasyon(rezervasyon_id)
    await db.commit()

# ── Toplanti ─────────────────────────────────────────────

@router.post("/toplanti", status_code=201)
async def create_toplanti(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    obj = await svc.create_toplanti(data)
    await db.commit()
    return obj

@router.get("/toplanti")
async def list_toplanti(site_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_toplanti(site_id)

@router.get("/toplanti/{toplanti_id}")
async def get_toplanti(toplanti_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    obj = await svc.get_toplanti(toplanti_id)
    if not obj:
        raise HTTPException(404)
    return obj

@router.delete("/toplanti/{toplanti_id}", status_code=204)
async def delete_toplanti(toplanti_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    await repo.delete_toplanti(toplanti_id)
    await db.commit()

# ── Banka ────────────────────────────────────────────────

@router.post("/banka", status_code=201)
async def create_banka_hesap(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    obj = await svc.create_banka_hesap(data)
    await db.commit()
    return obj

@router.get("/banka")
async def list_banka_hesap(site_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_banka_hesap(site_id)

@router.get("/banka/{hesap_id}")
async def get_banka_hesap(hesap_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    obj = await svc.get_banka_hesap(hesap_id)
    if not obj:
        raise HTTPException(404)
    return obj

@router.delete("/banka/{hesap_id}", status_code=204)
async def delete_banka_hesap(hesap_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    await repo.delete_banka_hesap(hesap_id)
    await db.commit()

# ── Isitma ───────────────────────────────────────────────

@router.post("/isitma", status_code=201)
async def create_isitma(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    obj = await svc.create_isitma(data)
    await db.commit()
    return obj

@router.get("/isitma")
async def list_isitma(site_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_isitma(site_id)

@router.get("/isitma/{isitma_id}")
async def get_isitma(isitma_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    obj = await svc.get_isitma(isitma_id)
    if not obj:
        raise HTTPException(404)
    return obj

@router.delete("/isitma/{isitma_id}", status_code=204)
async def delete_isitma(isitma_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    await repo.delete_isitma(isitma_id)
    await db.commit()

# ── Butce ────────────────────────────────────────────────

@router.post("/butce", status_code=201)
async def create_butce(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    obj = await svc.create_butce(data)
    await db.commit()
    return obj

@router.get("/butce")
async def list_butce(site_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_butce(site_id)

@router.get("/butce/{butce_id}")
async def get_butce(butce_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    obj = await svc.get_butce(butce_id)
    if not obj:
        raise HTTPException(404)
    return obj

@router.delete("/butce/{butce_id}", status_code=204)
async def delete_butce(butce_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    await repo.delete_butce(butce_id)
    await db.commit()

# ── Dosya ────────────────────────────────────────────────

@router.post("/dosya", status_code=201)
async def create_dosya(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    obj = await svc.create_dosya(data)
    await db.commit()
    return obj

@router.get("/dosya")
async def list_dosya(site_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_dosya(site_id)

@router.get("/dosya/{dosya_id}")
async def get_dosya(dosya_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    obj = await svc.get_dosya(dosya_id)
    if not obj:
        raise HTTPException(404)
    return obj

@router.delete("/dosya/{dosya_id}", status_code=204)
async def delete_dosya(dosya_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    await repo.delete_dosya(dosya_id)
    await db.commit()

# ── Bildirim ─────────────────────────────────────────────

@router.post("/bildirim", status_code=201)
async def create_bildirim(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    obj = await svc.create_bildirim(data)
    await db.commit()
    return obj

@router.get("/bildirim")
async def list_bildirim(site_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    return await repo.list_bildirim(site_id)

@router.get("/bildirim/{bildirim_id}")
async def get_bildirim(bildirim_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.service import BinaService
    svc = BinaService(db)
    obj = await svc.get_bildirim(bildirim_id)
    if not obj:
        raise HTTPException(404)
    return obj

@router.delete("/bildirim/{bildirim_id}", status_code=204)
async def delete_bildirim(bildirim_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.bina.repository import BinaRepository
    repo = BinaRepository(db)
    await repo.delete_bildirim(bildirim_id)
    await db.commit()
