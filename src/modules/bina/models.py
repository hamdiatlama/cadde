from sqlalchemy import Column, Integer, BigInteger, String, Boolean, DateTime, Text, Float, Date, ForeignKey, Numeric, func
from src.database import Base


class Site(Base):
    __tablename__ = "siteler"
    id = Column(Integer, primary_key=True, index=True)
    adi = Column(String, nullable=False)
    adres = Column(Text)
    sekil = Column(String, default="site")
    kurucu = Column(String)
    kurucu_tel = Column(String)
    banka = Column(String)
    komisyon_yuzde = Column(Float, default=2)
    kurulum_tamam = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


class Blok(Base):
    __tablename__ = "bloklar"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("siteler.id"), nullable=False)
    adi = Column(String, nullable=False)
    kat_adet = Column(Integer, default=4)
    daire_kat = Column(Integer, default=2)


class Daire(Base):
    __tablename__ = "daireler"
    id = Column(Integer, primary_key=True, index=True)
    blok_id = Column(Integer, ForeignKey("bloklar.id"), nullable=False)
    no = Column(String, nullable=False)
    kat = Column(Integer, nullable=False)
    kapi_no = Column(Integer, nullable=False)
    alan = Column(Float)
    sakin_id = Column(Integer, ForeignKey("site_kisiler.id"))


class Kisi(Base):
    __tablename__ = "site_kisiler"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("siteler.id"), nullable=False)
    ad = Column(String, nullable=False)
    tel = Column(String)
    email = Column(String)
    rol = Column(String, default="malik")
    daire_id = Column(Integer, ForeignKey("daireler.id"))
    blok_id = Column(Integer, ForeignKey("bloklar.id"))
    yetki = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Duyuru(Base):
    __tablename__ = "site_duyurulari"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("siteler.id"), nullable=False)
    baslik = Column(String, nullable=False)
    icerik = Column(Text)
    kategori = Column(String, default="genel")
    yapan = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Aidat(Base):
    __tablename__ = "aidat"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("siteler.id"), nullable=False)
    daire_id = Column(Integer, ForeignKey("daireler.id"), nullable=False)
    blok_id = Column(Integer, ForeignKey("bloklar.id"), nullable=False)
    daire_no = Column(String)
    ay = Column(Integer, nullable=False)
    yil = Column(Integer, nullable=False)
    tutar = Column(Float, nullable=False)
    odendi = Column(Boolean, default=False)
    odeme_tarihi = Column(DateTime(timezone=True))
    kapi_no = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Gelir(Base):
    __tablename__ = "site_gelir"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("siteler.id"), nullable=False)
    baslik = Column(String, nullable=False)
    tutar = Column(Float, nullable=False)
    kategori = Column(String, default="aidat")
    aciklama = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Gider(Base):
    __tablename__ = "site_gider"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("siteler.id"), nullable=False)
    baslik = Column(String, nullable=False)
    tutar = Column(Float, nullable=False)
    kategori = Column(String, default="genel")
    firma_id = Column(Integer, ForeignKey("site_firma.id"))
    aciklama = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Arac(Base):
    __tablename__ = "site_arac"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("siteler.id"), nullable=False)
    plaka = Column(String, nullable=False)
    daire_id = Column(Integer, ForeignKey("daireler.id"))
    blok_id = Column(Integer, ForeignKey("bloklar.id"))
    sakin_ad = Column(String)
    tel = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Personel(Base):
    __tablename__ = "site_personel"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("siteler.id"), nullable=False)
    ad = Column(String, nullable=False)
    tel = Column(String)
    gorev = Column(String)
    maas = Column(Float, default=0)
    ise_baslama = Column(Date)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Firma(Base):
    __tablename__ = "site_firma"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("siteler.id"), nullable=False)
    ad = Column(String, nullable=False)
    yetkili = Column(String)
    tel = Column(String)
    adres = Column(Text)
    sektor = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class IsTalebi(Base):
    __tablename__ = "site_is_talepleri"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("siteler.id"), nullable=False)
    baslik = Column(String, nullable=False)
    aciklama = Column(Text)
    sektor = Column(String)
    durum = Column(String, default="bekliyor")
    talep_eden_ad = Column(String)
    atanan_firma_id = Column(Integer, ForeignKey("site_firma.id"))
    teklifler = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True))


class Sayac(Base):
    __tablename__ = "site_sayac"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("siteler.id"), nullable=False)
    daire_id = Column(Integer, ForeignKey("daireler.id"), nullable=False)
    blok_id = Column(Integer, ForeignKey("bloklar.id"), nullable=False)
    daire_no = Column(String)
    tur = Column(String, nullable=False)
    son_endeks = Column(Float, nullable=False)
    onceki_endeks = Column(Float, default=0)
    birim_fiyat = Column(Float, nullable=False)
    tarih = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Kargo(Base):
    __tablename__ = "site_kargo"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("siteler.id"), nullable=False)
    takip_no = Column(String, nullable=False)
    daire_id = Column(Integer, ForeignKey("daireler.id"))
    blok_id = Column(Integer, ForeignKey("bloklar.id"))
    sakin_ad = Column(String)
    tel = Column(String)
    durum = Column(String, default="bekliyor")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Ziyaretci(Base):
    __tablename__ = "site_ziyaretci"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("siteler.id"), nullable=False)
    ad = Column(String, nullable=False)
    daire_id = Column(Integer, ForeignKey("daireler.id"))
    blok_id = Column(Integer, ForeignKey("bloklar.id"))
    giris = Column(DateTime(timezone=True), nullable=False)
    cikis = Column(DateTime(timezone=True))
    plaka = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Anket(Base):
    __tablename__ = "site_anket"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("siteler.id"), nullable=False)
    baslik = Column(String(300), nullable=False)
    aciklama = Column(Text)
    baslangic = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    bitis = Column(DateTime(timezone=True))
    aktif = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AnketSecenek(Base):
    __tablename__ = "site_anket_secenek"
    id = Column(Integer, primary_key=True, index=True)
    anket_id = Column(Integer, ForeignKey("site_anket.id"), nullable=False)
    metin = Column(String(500), nullable=False)
    oy_sayisi = Column(Integer, default=0)


class AnketOy(Base):
    __tablename__ = "site_anket_oy"
    id = Column(Integer, primary_key=True, index=True)
    anket_id = Column(Integer, ForeignKey("site_anket.id"), nullable=False)
    secenek_id = Column(Integer, ForeignKey("site_anket_secenek.id"), nullable=False)
    kisi_id = Column(Integer, ForeignKey("site_kisiler.id"))
    daire_id = Column(Integer, ForeignKey("daireler.id"))
    oy = Column(DateTime(timezone=True), server_default=func.now())


class Icra(Base):
    __tablename__ = "site_icra"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("siteler.id"), nullable=False)
    daire_id = Column(Integer, ForeignKey("daireler.id"), nullable=False)
    blok_id = Column(Integer, ForeignKey("bloklar.id"), nullable=False)
    daire_no = Column(String(20))
    kapi_no = Column(Integer)
    baslik = Column(String(300), nullable=False)
    aciklama = Column(Text)
    borc_turu = Column(String(50), default="aidat")
    tutar = Column(Numeric(12, 2), nullable=False, default=0)
    tarih = Column(Date)
    durum = Column(String(30), default="basiyor")
    avukat = Column(String(100))
    masraf = Column(Numeric(12, 2), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True))


class Otopark(Base):
    __tablename__ = "site_otopark"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("siteler.id"), nullable=False)
    blok_id = Column(Integer, ForeignKey("bloklar.id"))
    no = Column(String(20), nullable=False)
    kat = Column(String(20))
    tip = Column(String(30), default="arac")
    daire_id = Column(Integer, ForeignKey("daireler.id"))
    kisi_id = Column(Integer, ForeignKey("site_kisiler.id"))
    arac_plaka = Column(String(20))
    kira_bedeli = Column(Numeric(10, 2), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Rezervasyon(Base):
    __tablename__ = "site_rezervasyon"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("siteler.id"), nullable=False)
    alan = Column(String(100), nullable=False)
    kisi_id = Column(Integer, ForeignKey("site_kisiler.id"))
    daire_id = Column(Integer, ForeignKey("daireler.id"))
    baslangic = Column(DateTime(timezone=True), nullable=False)
    bitis = Column(DateTime(timezone=True), nullable=False)
    notlar = Column(Text)
    durum = Column(String(20), default="onaylandi")
    ucret = Column(Numeric(10, 2), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Toplanti(Base):
    __tablename__ = "site_toplanti"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("siteler.id"), nullable=False)
    baslik = Column(String(300), nullable=False)
    tarih = Column(DateTime(timezone=True), nullable=False)
    yer = Column(String(200))
    katilanlar = Column(Text)
    gundem = Column(Text)
    kararlar = Column(Text)
    tutanak_url = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BankaHesap(Base):
    __tablename__ = "site_banka"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("siteler.id"), nullable=False)
    banka_adi = Column(String(100), nullable=False)
    sube = Column(String(100))
    hesap_adi = Column(String(200))
    iban = Column(String(50), nullable=False)
    hesap_no = Column(String(30))
    tur = Column(String(20), default="vadesiz")
    bakiye = Column(Numeric(12, 2), default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Isitma(Base):
    __tablename__ = "site_isitma"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("siteler.id"), nullable=False)
    tur = Column(String(30), default="dogalgaz")
    daire_id = Column(Integer, ForeignKey("daireler.id"))
    blok_id = Column(Integer, ForeignKey("bloklar.id"))
    yakilan_m3 = Column(Numeric(10, 2), default=0)
    birim_fiyat = Column(Numeric(8, 4), default=0)
    tutar = Column(Numeric(10, 2), default=0)
    ay = Column(Integer, nullable=False)
    yil = Column(Integer, nullable=False)
    odendi = Column(Boolean, default=False)
    odeme_tarihi = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Butce(Base):
    __tablename__ = "site_butce"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("siteler.id"), nullable=False)
    yil = Column(Integer, nullable=False)
    baslik = Column(String(300), nullable=False)
    kategori = Column(String(50), default="gelir")
    tur = Column(String(50), default="aidat")
    planlanan = Column(Numeric(12, 2), default=0)
    gerceklesen = Column(Numeric(12, 2), default=0)
    aciklama = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True))


class Dosya(Base):
    __tablename__ = "site_dosya"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("siteler.id"), nullable=False)
    baslik = Column(String(300), nullable=False)
    dosya_turu = Column(String(50))
    dosya_url = Column(Text)
    boyut = Column(BigInteger, default=0)
    aciklama = Column(Text)
    yukleyen = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Bildirim(Base):
    __tablename__ = "site_bildirim"
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("siteler.id"), nullable=False)
    baslik = Column(String(300), nullable=False)
    icerik = Column(Text)
    tur = Column(String(30), default="duyuru")
    hedef = Column(String(30), default="herkes")
    hedef_id = Column(Integer)
    gonderildi = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
