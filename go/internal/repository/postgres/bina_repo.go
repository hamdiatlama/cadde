package postgres

import (
	"context"
	"fmt"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/web-platform/backend/internal/domain"
)

type BinaRepo struct {
	pool *pgxpool.Pool
}

func NewBinaRepo(pool *pgxpool.Pool) *BinaRepo {
	return &BinaRepo{pool: pool}
}

// ── Site ──────────────────────────────────────────────────

func (r *BinaRepo) CreateSite(ctx context.Context, s *domain.Site) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO siteler (adi, adres, sekil, kurucu, kurucu_tel, banka, komisyon_yuzde, kurulum_tamam)
		 VALUES ($1,$2,$3,$4,$5,$6,$7,$8) RETURNING id, created_at, updated_at`,
		s.Adi, s.Adres, s.Sekil, s.Kurucu, s.KurucuTel, s.Banka, s.KomisyonYuzde, s.KurulumTamam,
	).Scan(&s.ID, &s.CreatedAt, &s.UpdatedAt)
}

func (r *BinaRepo) GetSite(ctx context.Context, id int) (*domain.Site, error) {
	s := &domain.Site{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, adi, adres, sekil, kurucu, kurucu_tel, banka, komisyon_yuzde, kurulum_tamam, created_at, updated_at
		 FROM siteler WHERE id=$1`, id,
	).Scan(&s.ID, &s.Adi, &s.Adres, &s.Sekil, &s.Kurucu, &s.KurucuTel, &s.Banka, &s.KomisyonYuzde, &s.KurulumTamam, &s.CreatedAt, &s.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("get site: %w", err)
	}
	return s, nil
}

func (r *BinaRepo) UpdateSite(ctx context.Context, s *domain.Site) error {
	err := r.pool.QueryRow(ctx,
		`UPDATE siteler SET adi=$1, adres=$2, sekil=$3, kurucu=$4, kurucu_tel=$5, banka=$6, komisyon_yuzde=$7, kurulum_tamam=$8, updated_at=NOW() WHERE id=$9 RETURNING updated_at`,
		s.Adi, s.Adres, s.Sekil, s.Kurucu, s.KurucuTel, s.Banka, s.KomisyonYuzde, s.KurulumTamam, s.ID).Scan(&s.UpdatedAt)
	return err
}

// ── Blok ──────────────────────────────────────────────────

func (r *BinaRepo) CreateBlok(ctx context.Context, b *domain.Blok) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO bloklar (site_id, adi, kat_adet, daire_kat) VALUES ($1,$2,$3,$4) RETURNING id`,
		b.SiteID, b.Adi, b.KatAdet, b.DaireKat).Scan(&b.ID)
}

func (r *BinaRepo) ListBlok(ctx context.Context, siteID int) ([]*domain.Blok, error) {
	rows, err := r.pool.Query(ctx, `SELECT id, site_id, adi, kat_adet, daire_kat FROM bloklar WHERE site_id=$1 ORDER BY adi`, siteID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.Blok
	for rows.Next() {
		b := &domain.Blok{}
		if err := rows.Scan(&b.ID, &b.SiteID, &b.Adi, &b.KatAdet, &b.DaireKat); err != nil {
			return nil, err
		}
		list = append(list, b)
	}
	return list, nil
}

func (r *BinaRepo) DeleteBlok(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM bloklar WHERE id=$1`, id)
	return err
}

// ── Daire ─────────────────────────────────────────────────

func (r *BinaRepo) CreateDaire(ctx context.Context, d *domain.Daire) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO daireler (blok_id, no, kat, kapi_no, alan) VALUES ($1,$2,$3,$4,$5) RETURNING id`,
		d.BlokID, d.No, d.Kat, d.KapiNo, d.Alan).Scan(&d.ID)
}

func (r *BinaRepo) GetDaire(ctx context.Context, id int) (*domain.Daire, error) {
	d := &domain.Daire{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, blok_id, no, kat, kapi_no, COALESCE(alan,0), sakin_id FROM daireler WHERE id=$1`, id,
	).Scan(&d.ID, &d.BlokID, &d.No, &d.Kat, &d.KapiNo, &d.Alan, &d.SakinID)
	if err != nil {
		return nil, fmt.Errorf("get daire: %w", err)
	}
	return d, nil
}

func (r *BinaRepo) ListDaire(ctx context.Context, siteID int) ([]*domain.Daire, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT d.id, d.blok_id, d.no, d.kat, d.kapi_no, COALESCE(d.alan,0), d.sakin_id
		 FROM daireler d JOIN bloklar b ON b.id=d.blok_id WHERE b.site_id=$1 ORDER BY b.adi, d.kapi_no`, siteID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.Daire
	for rows.Next() {
		d := &domain.Daire{}
		if err := rows.Scan(&d.ID, &d.BlokID, &d.No, &d.Kat, &d.KapiNo, &d.Alan, &d.SakinID); err != nil {
			return nil, err
		}
		list = append(list, d)
	}
	return list, nil
}

func (r *BinaRepo) UpdateDaireSakin(ctx context.Context, daireID int, kisiID *int) error {
	_, err := r.pool.Exec(ctx, `UPDATE daireler SET sakin_id=$1 WHERE id=$2`, kisiID, daireID)
	return err
}

// ── Kisi ──────────────────────────────────────────────────

func (r *BinaRepo) CreateKisi(ctx context.Context, k *domain.Kisi) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO site_kisiler (site_id, ad, tel, email, rol, daire_id, blok_id, yetki)
		 VALUES ($1,$2,$3,$4,$5,$6,$7,$8) RETURNING id, created_at`,
		k.SiteID, k.Ad, k.Tel, k.Email, k.Rol, k.DaireID, k.BlokID, k.Yetki,
	).Scan(&k.ID, &k.CreatedAt)
}

func (r *BinaRepo) ListKisi(ctx context.Context, siteID int) ([]*domain.Kisi, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, site_id, ad, tel, COALESCE(email,''), rol, daire_id, blok_id, COALESCE(yetki,''), created_at
		 FROM site_kisiler WHERE site_id=$1 ORDER BY ad`, siteID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.Kisi
	for rows.Next() {
		k := &domain.Kisi{}
		if err := rows.Scan(&k.ID, &k.SiteID, &k.Ad, &k.Tel, &k.Email, &k.Rol, &k.DaireID, &k.BlokID, &k.Yetki, &k.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, k)
	}
	return list, nil
}

// ── Duyuru ────────────────────────────────────────────────

func (r *BinaRepo) CreateDuyuru(ctx context.Context, d *domain.Duyuru) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO site_duyurulari (site_id, baslik, icerik, kategori, yapan) VALUES ($1,$2,$3,$4,$5) RETURNING id, created_at`,
		d.SiteID, d.Baslik, d.Icerik, d.Kategori, d.Yapan).Scan(&d.ID, &d.CreatedAt)
}

func (r *BinaRepo) ListDuyuru(ctx context.Context, siteID int) ([]*domain.Duyuru, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, site_id, baslik, icerik, kategori, yapan, created_at
		 FROM site_duyurulari WHERE site_id=$1 ORDER BY created_at DESC`, siteID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.Duyuru
	for rows.Next() {
		d := &domain.Duyuru{}
		if err := rows.Scan(&d.ID, &d.SiteID, &d.Baslik, &d.Icerik, &d.Kategori, &d.Yapan, &d.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, d)
	}
	return list, nil
}

// ── Aidat ─────────────────────────────────────────────────

func (r *BinaRepo) CreateAidat(ctx context.Context, a *domain.Aidat) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO aidat (site_id, daire_id, blok_id, daire_no, ay, yil, tutar, kapi_no)
		 VALUES ($1,$2,$3,$4,$5,$6,$7,$8) RETURNING id, created_at`,
		a.SiteID, a.DaireID, a.BlokID, a.DaireNo, a.Ay, a.Yil, a.Tutar, a.KapiNo,
	).Scan(&a.ID, &a.CreatedAt)
}

func (r *BinaRepo) ListAidat(ctx context.Context, siteID, ay, yil int) ([]*domain.Aidat, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, site_id, daire_id, blok_id, daire_no, ay, yil, tutar, odendi, odeme_tarihi, kapi_no, created_at
		 FROM aidat WHERE site_id=$1 AND ay=$2 AND yil=$3 ORDER BY kapi_no`, siteID, ay, yil)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.Aidat
	for rows.Next() {
		a := &domain.Aidat{}
		if err := rows.Scan(&a.ID, &a.SiteID, &a.DaireID, &a.BlokID, &a.DaireNo, &a.Ay, &a.Yil, &a.Tutar, &a.Odendi, &a.OdemeTarihi, &a.KapiNo, &a.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, a)
	}
	return list, nil
}

func (r *BinaRepo) OdemeAidat(ctx context.Context, aidatID int) error {
	_, err := r.pool.Exec(ctx, `UPDATE aidat SET odendi=true, odeme_tarihi=NOW() WHERE id=$1`, aidatID)
	return err
}

func (r *BinaRepo) CountAidatOdenmemis(ctx context.Context, siteID int) (int, error) {
	var c int
	err := r.pool.QueryRow(ctx, `SELECT COUNT(*) FROM aidat WHERE site_id=$1 AND odendi=false`, siteID).Scan(&c)
	return c, err
}

// ── Gelir/Gider ───────────────────────────────────────────

func (r *BinaRepo) CreateGelir(ctx context.Context, g *domain.Gelir) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO site_gelir (site_id, baslik, tutar, kategori, aciklama) VALUES ($1,$2,$3,$4,$5) RETURNING id, created_at`,
		g.SiteID, g.Baslik, g.Tutar, g.Kategori, g.Aciklama).Scan(&g.ID, &g.CreatedAt)
}

func (r *BinaRepo) CreateGider(ctx context.Context, g *domain.Gider) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO site_gider (site_id, baslik, tutar, kategori, firma_id, aciklama) VALUES ($1,$2,$3,$4,$5,$6) RETURNING id, created_at`,
		g.SiteID, g.Baslik, g.Tutar, g.Kategori, g.FirmaID, g.Aciklama).Scan(&g.ID, &g.CreatedAt)
}

func (r *BinaRepo) ListGelir(ctx context.Context, siteID int) ([]*domain.Gelir, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, site_id, baslik, tutar, kategori, COALESCE(aciklama,''), created_at
		 FROM site_gelir WHERE site_id=$1 ORDER BY created_at DESC`, siteID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.Gelir
	for rows.Next() {
		g := &domain.Gelir{}
		if err := rows.Scan(&g.ID, &g.SiteID, &g.Baslik, &g.Tutar, &g.Kategori, &g.Aciklama, &g.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, g)
	}
	return list, nil
}

func (r *BinaRepo) ListGider(ctx context.Context, siteID int) ([]*domain.Gider, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, site_id, baslik, tutar, kategori, firma_id, COALESCE(aciklama,''), created_at
		 FROM site_gider WHERE site_id=$1 ORDER BY created_at DESC`, siteID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.Gider
	for rows.Next() {
		g := &domain.Gider{}
		if err := rows.Scan(&g.ID, &g.SiteID, &g.Baslik, &g.Tutar, &g.Kategori, &g.FirmaID, &g.Aciklama, &g.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, g)
	}
	return list, nil
}

// ── Arac ──────────────────────────────────────────────────

func (r *BinaRepo) CreateArac(ctx context.Context, a *domain.Arac) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO site_arac (site_id, plaka, daire_id, blok_id, sakin_ad, tel) VALUES ($1,$2,$3,$4,$5,$6) RETURNING id, created_at`,
		a.SiteID, a.Plaka, a.DaireID, a.BlokID, a.SakinAd, a.Tel).Scan(&a.ID, &a.CreatedAt)
}

func (r *BinaRepo) ListArac(ctx context.Context, siteID int) ([]*domain.Arac, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, site_id, plaka, daire_id, blok_id, sakin_ad, COALESCE(tel,''), created_at
		 FROM site_arac WHERE site_id=$1 ORDER BY plaka`, siteID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.Arac
	for rows.Next() {
		a := &domain.Arac{}
		if err := rows.Scan(&a.ID, &a.SiteID, &a.Plaka, &a.DaireID, &a.BlokID, &a.SakinAd, &a.Tel, &a.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, a)
	}
	return list, nil
}

func (r *BinaRepo) DeleteArac(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM site_arac WHERE id=$1`, id)
	return err
}

// ── Personel ──────────────────────────────────────────────

func (r *BinaRepo) CreatePersonel(ctx context.Context, p *domain.Personel) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO site_personel (site_id, ad, tel, gorev, maas, ise_baslama, is_active)
		 VALUES ($1,$2,$3,$4,$5,$6,$7) RETURNING id, created_at`,
		p.SiteID, p.Ad, p.Tel, p.Gorev, p.Maas, p.IseBaslama, p.IsActive).Scan(&p.ID, &p.CreatedAt)
}

func (r *BinaRepo) ListPersonel(ctx context.Context, siteID int) ([]*domain.Personel, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, site_id, ad, tel, gorev, maas, ise_baslama, is_active, created_at
		 FROM site_personel WHERE site_id=$1 ORDER BY ad`, siteID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.Personel
	for rows.Next() {
		p := &domain.Personel{}
		if err := rows.Scan(&p.ID, &p.SiteID, &p.Ad, &p.Tel, &p.Gorev, &p.Maas, &p.IseBaslama, &p.IsActive, &p.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, p)
	}
	return list, nil
}

// ── Firma ─────────────────────────────────────────────────

func (r *BinaRepo) CreateFirma(ctx context.Context, f *domain.Firma) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO site_firma (site_id, ad, yetkili, tel, adres, sektor) VALUES ($1,$2,$3,$4,$5,$6) RETURNING id, created_at`,
		f.SiteID, f.Ad, f.Yetkili, f.Tel, f.Adres, f.Sektor).Scan(&f.ID, &f.CreatedAt)
}

func (r *BinaRepo) ListFirma(ctx context.Context, siteID int) ([]*domain.Firma, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, site_id, ad, yetkili, tel, COALESCE(adres,''), sektor, created_at
		 FROM site_firma WHERE site_id=$1 ORDER BY ad`, siteID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.Firma
	for rows.Next() {
		f := &domain.Firma{}
		if err := rows.Scan(&f.ID, &f.SiteID, &f.Ad, &f.Yetkili, &f.Tel, &f.Adres, &f.Sektor, &f.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, f)
	}
	return list, nil
}

// ── Is Talebi ─────────────────────────────────────────────

func (r *BinaRepo) CreateIsTalebi(ctx context.Context, t *domain.IsTalebi) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO site_is_talepleri (site_id, baslik, aciklama, sektor, durum, talep_eden_ad)
		 VALUES ($1,$2,$3,$4,$5,$6) RETURNING id, created_at, updated_at`,
		t.SiteID, t.Baslik, t.Aciklama, t.Sektor, t.Durum, t.TalepEdenAd).Scan(&t.ID, &t.CreatedAt, &t.UpdatedAt)
}

func (r *BinaRepo) ListIsTalebi(ctx context.Context, siteID int) ([]*domain.IsTalebi, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, site_id, baslik, COALESCE(aciklama,''), sektor, durum, talep_eden_ad, atanan_firma_id, COALESCE(teklifler,''), created_at, updated_at
		 FROM site_is_talepleri WHERE site_id=$1 ORDER BY created_at DESC`, siteID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.IsTalebi
	for rows.Next() {
		t := &domain.IsTalebi{}
		if err := rows.Scan(&t.ID, &t.SiteID, &t.Baslik, &t.Aciklama, &t.Sektor, &t.Durum, &t.TalepEdenAd, &t.AtananFirmaID, &t.Teklifler, &t.CreatedAt, &t.UpdatedAt); err != nil {
			return nil, err
		}
		list = append(list, t)
	}
	return list, nil
}

// ── Sayac ─────────────────────────────────────────────────

func (r *BinaRepo) CreateSayac(ctx context.Context, s *domain.Sayac) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO site_sayac (site_id, daire_id, blok_id, daire_no, tur, son_endeks, onceki_endeks, birim_fiyat, tarih)
		 VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9) RETURNING id, created_at`,
		s.SiteID, s.DaireID, s.BlokID, s.DaireNo, s.Tur, s.SonEndeks, s.OncekiEndeks, s.BirimFiyat, s.Tarih).Scan(&s.ID, &s.CreatedAt)
}

func (r *BinaRepo) ListSayac(ctx context.Context, siteID int) ([]*domain.Sayac, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, site_id, daire_id, blok_id, daire_no, tur, son_endeks, onceki_endeks, birim_fiyat, tarih, created_at
		 FROM site_sayac WHERE site_id=$1 ORDER BY tarih DESC`, siteID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.Sayac
	for rows.Next() {
		s := &domain.Sayac{}
		if err := rows.Scan(&s.ID, &s.SiteID, &s.DaireID, &s.BlokID, &s.DaireNo, &s.Tur, &s.SonEndeks, &s.OncekiEndeks, &s.BirimFiyat, &s.Tarih, &s.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, s)
	}
	return list, nil
}

// ── Kargo ─────────────────────────────────────────────────

func (r *BinaRepo) CreateKargo(ctx context.Context, k *domain.Kargo) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO site_kargo (site_id, takip_no, daire_id, blok_id, sakin_ad, tel, durum)
		 VALUES ($1,$2,$3,$4,$5,$6,$7) RETURNING id, created_at`,
		k.SiteID, k.TakipNo, k.DaireID, k.BlokID, k.SakinAd, k.Tel, k.Durum).Scan(&k.ID, &k.CreatedAt)
}

func (r *BinaRepo) ListKargo(ctx context.Context, siteID int) ([]*domain.Kargo, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, site_id, takip_no, daire_id, blok_id, sakin_ad, COALESCE(tel,''), durum, created_at
		 FROM site_kargo WHERE site_id=$1 ORDER BY created_at DESC`, siteID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.Kargo
	for rows.Next() {
		k := &domain.Kargo{}
		if err := rows.Scan(&k.ID, &k.SiteID, &k.TakipNo, &k.DaireID, &k.BlokID, &k.SakinAd, &k.Tel, &k.Durum, &k.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, k)
	}
	return list, nil
}

// ── Ziyaretci ─────────────────────────────────────────────

func (r *BinaRepo) CreateZiyaretci(ctx context.Context, z *domain.Ziyaretci) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO site_ziyaretci (site_id, ad, daire_id, blok_id, giris, plaka)
		 VALUES ($1,$2,$3,$4,$5,$6) RETURNING id, created_at`,
		z.SiteID, z.Ad, z.DaireID, z.BlokID, z.Giris, z.Plaka).Scan(&z.ID, &z.CreatedAt)
}

func (r *BinaRepo) ListZiyaretci(ctx context.Context, siteID int) ([]*domain.Ziyaretci, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, site_id, ad, daire_id, blok_id, giris, cikis, COALESCE(plaka,''), created_at
		 FROM site_ziyaretci WHERE site_id=$1 ORDER BY giris DESC`, siteID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.Ziyaretci
	for rows.Next() {
		z := &domain.Ziyaretci{}
		if err := rows.Scan(&z.ID, &z.SiteID, &z.Ad, &z.DaireID, &z.BlokID, &z.Giris, &z.Cikis, &z.Plaka, &z.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, z)
	}
	return list, nil
}

func (r *BinaRepo) ZiyaretciCikis(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, `UPDATE site_ziyaretci SET cikis=NOW() WHERE id=$1`, id)
	return err
}

// ── Anket ─────────────────────────────────────────────────

func (r *BinaRepo) CreateAnket(ctx context.Context, a *domain.Anket) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO site_anket (site_id, baslik, aciklama, baslangic, bitis, aktif) VALUES ($1,$2,$3,$4,$5,$6) RETURNING id, created_at`,
		a.SiteID, a.Baslik, a.Aciklama, a.Baslangic, a.Bitis, a.Aktif).Scan(&a.ID, &a.CreatedAt)
}

func (r *BinaRepo) ListAnket(ctx context.Context, siteID int) ([]*domain.Anket, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, site_id, baslik, COALESCE(aciklama,''), baslangic, bitis, aktif, created_at FROM site_anket WHERE site_id=$1 ORDER BY created_at DESC`, siteID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.Anket
	for rows.Next() {
		a := &domain.Anket{}
		if err := rows.Scan(&a.ID, &a.SiteID, &a.Baslik, &a.Aciklama, &a.Baslangic, &a.Bitis, &a.Aktif, &a.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, a)
	}
	return list, nil
}

func (r *BinaRepo) GetAnket(ctx context.Context, id int) (*domain.Anket, error) {
	a := &domain.Anket{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, site_id, baslik, COALESCE(aciklama,''), baslangic, bitis, aktif, created_at FROM site_anket WHERE id=$1`, id,
	).Scan(&a.ID, &a.SiteID, &a.Baslik, &a.Aciklama, &a.Baslangic, &a.Bitis, &a.Aktif, &a.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("get anket: %w", err)
	}
	return a, nil
}

func (r *BinaRepo) AnketOy(ctx context.Context, oy *domain.AnketOy) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO site_anket_oy (anket_id, secenek_id, kisi_id, daire_id) VALUES ($1,$2,$3,$4) RETURNING id, oy`,
		oy.AnketID, oy.SecenekID, oy.KisiID, oy.DaireID).Scan(&oy.ID, &oy.Oy)
}

func (r *BinaRepo) DeleteAnket(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM site_anket WHERE id=$1`, id)
	return err
}

func (r *BinaRepo) CreateAnketSecenek(ctx context.Context, s *domain.AnketSecenek) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO site_anket_secenek (anket_id, metin) VALUES ($1,$2) RETURNING id`,
		s.AnketID, s.Metin).Scan(&s.ID)
}

func (r *BinaRepo) ListAnketSecenek(ctx context.Context, anketID int) ([]*domain.AnketSecenek, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, anket_id, metin, COALESCE(oy_sayisi,0) FROM site_anket_secenek WHERE anket_id=$1 ORDER BY id`, anketID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.AnketSecenek
	for rows.Next() {
		s := &domain.AnketSecenek{}
		if err := rows.Scan(&s.ID, &s.AnketID, &s.Metin, &s.OySayisi); err != nil {
			return nil, err
		}
		list = append(list, s)
	}
	return list, nil
}

func (r *BinaRepo) DeleteAnketSecenek(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM site_anket_secenek WHERE id=$1`, id)
	return err
}

// ── Icra ──────────────────────────────────────────────────

func (r *BinaRepo) CreateIcra(ctx context.Context, i *domain.Icra) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO site_icra (site_id, daire_id, blok_id, daire_no, kapi_no, baslik, aciklama, borc_turu, tutar, tarih, durum, avukat, masraf) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13) RETURNING id, created_at`,
		i.SiteID, i.DaireID, i.BlokID, i.DaireNo, i.KapiNo, i.Baslik, i.Aciklama, i.BorcTuru, i.Tutar, i.Tarih, i.Durum, i.Avukat, i.Masraf).Scan(&i.ID, &i.CreatedAt)
}

func (r *BinaRepo) ListIcra(ctx context.Context, siteID int) ([]*domain.Icra, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, site_id, daire_id, blok_id, COALESCE(daire_no,''), kapi_no, baslik, COALESCE(aciklama,''), borc_turu, tutar, tarih, durum, COALESCE(avukat,''), masraf, created_at, updated_at FROM site_icra WHERE site_id=$1 ORDER BY created_at DESC`, siteID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.Icra
	for rows.Next() {
		i := &domain.Icra{}
		if err := rows.Scan(&i.ID, &i.SiteID, &i.DaireID, &i.BlokID, &i.DaireNo, &i.KapiNo, &i.Baslik, &i.Aciklama, &i.BorcTuru, &i.Tutar, &i.Tarih, &i.Durum, &i.Avukat, &i.Masraf, &i.CreatedAt, &i.UpdatedAt); err != nil {
			return nil, err
		}
		list = append(list, i)
	}
	return list, nil
}

func (r *BinaRepo) GetIcra(ctx context.Context, id int) (*domain.Icra, error) {
	i := &domain.Icra{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, site_id, daire_id, blok_id, COALESCE(daire_no,''), kapi_no, baslik, COALESCE(aciklama,''), borc_turu, tutar, tarih, durum, COALESCE(avukat,''), masraf, created_at, updated_at FROM site_icra WHERE id=$1`, id,
	).Scan(&i.ID, &i.SiteID, &i.DaireID, &i.BlokID, &i.DaireNo, &i.KapiNo, &i.Baslik, &i.Aciklama, &i.BorcTuru, &i.Tutar, &i.Tarih, &i.Durum, &i.Avukat, &i.Masraf, &i.CreatedAt, &i.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("get icra: %w", err)
	}
	return i, nil
}

func (r *BinaRepo) DeleteIcra(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM site_icra WHERE id=$1`, id)
	return err
}

// ── Otopark ───────────────────────────────────────────────

func (r *BinaRepo) CreateOtopark(ctx context.Context, o *domain.Otopark) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO site_otopark (site_id, blok_id, no, kat, tip, daire_id, kisi_id, arac_plaka, kira_bedeli) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9) RETURNING id, created_at`,
		o.SiteID, o.BlokID, o.No, o.Kat, o.Tip, o.DaireID, o.KisiID, o.AracPlaka, o.KiraBedeli).Scan(&o.ID, &o.CreatedAt)
}

func (r *BinaRepo) ListOtopark(ctx context.Context, siteID int) ([]*domain.Otopark, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, site_id, blok_id, no, COALESCE(kat,''), tip, daire_id, kisi_id, COALESCE(arac_plaka,''), kira_bedeli, created_at FROM site_otopark WHERE site_id=$1 ORDER BY created_at DESC`, siteID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.Otopark
	for rows.Next() {
		o := &domain.Otopark{}
		if err := rows.Scan(&o.ID, &o.SiteID, &o.BlokID, &o.No, &o.Kat, &o.Tip, &o.DaireID, &o.KisiID, &o.AracPlaka, &o.KiraBedeli, &o.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, o)
	}
	return list, nil
}

func (r *BinaRepo) GetOtopark(ctx context.Context, id int) (*domain.Otopark, error) {
	o := &domain.Otopark{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, site_id, blok_id, no, COALESCE(kat,''), tip, daire_id, kisi_id, COALESCE(arac_plaka,''), kira_bedeli, created_at FROM site_otopark WHERE id=$1`, id,
	).Scan(&o.ID, &o.SiteID, &o.BlokID, &o.No, &o.Kat, &o.Tip, &o.DaireID, &o.KisiID, &o.AracPlaka, &o.KiraBedeli, &o.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("get otopark: %w", err)
	}
	return o, nil
}

func (r *BinaRepo) DeleteOtopark(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM site_otopark WHERE id=$1`, id)
	return err
}

// ── Rezervasyon ───────────────────────────────────────────

func (r *BinaRepo) CreateRezervasyon(ctx context.Context, rz *domain.Rezervasyon) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO site_rezervasyon (site_id, alan, kisi_id, daire_id, baslangic, bitis, notlar, durum, ucret) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9) RETURNING id, created_at`,
		rz.SiteID, rz.Alan, rz.KisiID, rz.DaireID, rz.Baslangic, rz.Bitis, rz.Notlar, rz.Durum, rz.Ucret).Scan(&rz.ID, &rz.CreatedAt)
}

func (r *BinaRepo) ListRezervasyon(ctx context.Context, siteID int) ([]*domain.Rezervasyon, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, site_id, alan, kisi_id, daire_id, baslangic, bitis, COALESCE(notlar,''), durum, ucret, created_at FROM site_rezervasyon WHERE site_id=$1 ORDER BY baslangic DESC`, siteID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.Rezervasyon
	for rows.Next() {
		rz := &domain.Rezervasyon{}
		if err := rows.Scan(&rz.ID, &rz.SiteID, &rz.Alan, &rz.KisiID, &rz.DaireID, &rz.Baslangic, &rz.Bitis, &rz.Notlar, &rz.Durum, &rz.Ucret, &rz.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, rz)
	}
	return list, nil
}

func (r *BinaRepo) GetRezervasyon(ctx context.Context, id int) (*domain.Rezervasyon, error) {
	rz := &domain.Rezervasyon{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, site_id, alan, kisi_id, daire_id, baslangic, bitis, COALESCE(notlar,''), durum, ucret, created_at FROM site_rezervasyon WHERE id=$1`, id,
	).Scan(&rz.ID, &rz.SiteID, &rz.Alan, &rz.KisiID, &rz.DaireID, &rz.Baslangic, &rz.Bitis, &rz.Notlar, &rz.Durum, &rz.Ucret, &rz.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("get rezervasyon: %w", err)
	}
	return rz, nil
}

func (r *BinaRepo) DeleteRezervasyon(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM site_rezervasyon WHERE id=$1`, id)
	return err
}

// ── Toplanti ──────────────────────────────────────────────

func (r *BinaRepo) CreateToplanti(ctx context.Context, t *domain.Toplanti) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO site_toplanti (site_id, baslik, tarih, yer, katilanlar, gundem, kararlar, tutanak_url) VALUES ($1,$2,$3,$4,$5,$6,$7,$8) RETURNING id, created_at`,
		t.SiteID, t.Baslik, t.Tarih, t.Yer, t.Katilanlar, t.Gundem, t.Kararlar, t.TutanakURL).Scan(&t.ID, &t.CreatedAt)
}

func (r *BinaRepo) ListToplanti(ctx context.Context, siteID int) ([]*domain.Toplanti, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, site_id, baslik, tarih, COALESCE(yer,''), COALESCE(katilanlar,''), COALESCE(gundem,''), COALESCE(kararlar,''), COALESCE(tutanak_url,''), created_at FROM site_toplanti WHERE site_id=$1 ORDER BY tarih DESC`, siteID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.Toplanti
	for rows.Next() {
		t := &domain.Toplanti{}
		if err := rows.Scan(&t.ID, &t.SiteID, &t.Baslik, &t.Tarih, &t.Yer, &t.Katilanlar, &t.Gundem, &t.Kararlar, &t.TutanakURL, &t.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, t)
	}
	return list, nil
}

func (r *BinaRepo) GetToplanti(ctx context.Context, id int) (*domain.Toplanti, error) {
	t := &domain.Toplanti{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, site_id, baslik, tarih, COALESCE(yer,''), COALESCE(katilanlar,''), COALESCE(gundem,''), COALESCE(kararlar,''), COALESCE(tutanak_url,''), created_at FROM site_toplanti WHERE id=$1`, id,
	).Scan(&t.ID, &t.SiteID, &t.Baslik, &t.Tarih, &t.Yer, &t.Katilanlar, &t.Gundem, &t.Kararlar, &t.TutanakURL, &t.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("get toplanti: %w", err)
	}
	return t, nil
}

func (r *BinaRepo) DeleteToplanti(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM site_toplanti WHERE id=$1`, id)
	return err
}

// ── Banka ─────────────────────────────────────────────────

func (r *BinaRepo) CreateBanka(ctx context.Context, b *domain.BankaHesap) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO site_banka (site_id, banka_adi, sube, hesap_adi, iban, hesap_no, tur, bakiye) VALUES ($1,$2,$3,$4,$5,$6,$7,$8) RETURNING id, created_at`,
		b.SiteID, b.BankaAdi, b.Sube, b.HesapAdi, b.Iban, b.HesapNo, b.Tur, b.Bakiye).Scan(&b.ID, &b.CreatedAt)
}

func (r *BinaRepo) ListBanka(ctx context.Context, siteID int) ([]*domain.BankaHesap, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, site_id, banka_adi, COALESCE(sube,''), COALESCE(hesap_adi,''), iban, COALESCE(hesap_no,''), tur, bakiye, created_at FROM site_banka WHERE site_id=$1 ORDER BY created_at DESC`, siteID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.BankaHesap
	for rows.Next() {
		b := &domain.BankaHesap{}
		if err := rows.Scan(&b.ID, &b.SiteID, &b.BankaAdi, &b.Sube, &b.HesapAdi, &b.Iban, &b.HesapNo, &b.Tur, &b.Bakiye, &b.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, b)
	}
	return list, nil
}

func (r *BinaRepo) GetBankaHesap(ctx context.Context, id int) (*domain.BankaHesap, error) {
	b := &domain.BankaHesap{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, site_id, banka_adi, COALESCE(sube,''), COALESCE(hesap_adi,''), iban, COALESCE(hesap_no,''), tur, bakiye, created_at FROM site_banka WHERE id=$1`, id,
	).Scan(&b.ID, &b.SiteID, &b.BankaAdi, &b.Sube, &b.HesapAdi, &b.Iban, &b.HesapNo, &b.Tur, &b.Bakiye, &b.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("get banka: %w", err)
	}
	return b, nil
}

func (r *BinaRepo) DeleteBankaHesap(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM site_banka WHERE id=$1`, id)
	return err
}

// ── Isitma ────────────────────────────────────────────────

func (r *BinaRepo) CreateIsitma(ctx context.Context, i *domain.Isitma) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO site_isitma (site_id, tur, daire_id, blok_id, yakilan_m3, birim_fiyat, tutar, ay, yil, odendi) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10) RETURNING id, created_at`,
		i.SiteID, i.Tur, i.DaireID, i.BlokID, i.YakilanM3, i.BirimFiyat, i.Tutar, i.Ay, i.Yil, i.Odendi).Scan(&i.ID, &i.CreatedAt)
}

func (r *BinaRepo) ListIsitma(ctx context.Context, siteID int) ([]*domain.Isitma, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, site_id, tur, daire_id, blok_id, yakilan_m3, birim_fiyat, tutar, ay, yil, odendi, odeme_tarihi, created_at FROM site_isitma WHERE site_id=$1 ORDER BY yil DESC, ay DESC`, siteID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.Isitma
	for rows.Next() {
		i := &domain.Isitma{}
		if err := rows.Scan(&i.ID, &i.SiteID, &i.Tur, &i.DaireID, &i.BlokID, &i.YakilanM3, &i.BirimFiyat, &i.Tutar, &i.Ay, &i.Yil, &i.Odendi, &i.OdemeTarihi, &i.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, i)
	}
	return list, nil
}

func (r *BinaRepo) GetIsitma(ctx context.Context, id int) (*domain.Isitma, error) {
	i := &domain.Isitma{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, site_id, tur, daire_id, blok_id, yakilan_m3, birim_fiyat, tutar, ay, yil, odendi, odeme_tarihi, created_at FROM site_isitma WHERE id=$1`, id,
	).Scan(&i.ID, &i.SiteID, &i.Tur, &i.DaireID, &i.BlokID, &i.YakilanM3, &i.BirimFiyat, &i.Tutar, &i.Ay, &i.Yil, &i.Odendi, &i.OdemeTarihi, &i.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("get isitma: %w", err)
	}
	return i, nil
}

func (r *BinaRepo) DeleteIsitma(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM site_isitma WHERE id=$1`, id)
	return err
}

// ── Butce ─────────────────────────────────────────────────

func (r *BinaRepo) CreateButce(ctx context.Context, b *domain.Butce) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO site_butce (site_id, yil, baslik, kategori, tur, planlanan, gerceklesen, aciklama) VALUES ($1,$2,$3,$4,$5,$6,$7,$8) RETURNING id, created_at`,
		b.SiteID, b.Yil, b.Baslik, b.Kategori, b.Tur, b.Planlanan, b.Gerceklesen, b.Aciklama).Scan(&b.ID, &b.CreatedAt)
}

func (r *BinaRepo) ListButce(ctx context.Context, siteID int) ([]*domain.Butce, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, site_id, yil, baslik, kategori, tur, planlanan, gerceklesen, COALESCE(aciklama,''), created_at, updated_at FROM site_butce WHERE site_id=$1 ORDER BY yil DESC, created_at DESC`, siteID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.Butce
	for rows.Next() {
		b := &domain.Butce{}
		if err := rows.Scan(&b.ID, &b.SiteID, &b.Yil, &b.Baslik, &b.Kategori, &b.Tur, &b.Planlanan, &b.Gerceklesen, &b.Aciklama, &b.CreatedAt, &b.UpdatedAt); err != nil {
			return nil, err
		}
		list = append(list, b)
	}
	return list, nil
}

func (r *BinaRepo) GetButce(ctx context.Context, id int) (*domain.Butce, error) {
	b := &domain.Butce{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, site_id, yil, baslik, kategori, tur, planlanan, gerceklesen, COALESCE(aciklama,''), created_at, updated_at FROM site_butce WHERE id=$1`, id,
	).Scan(&b.ID, &b.SiteID, &b.Yil, &b.Baslik, &b.Kategori, &b.Tur, &b.Planlanan, &b.Gerceklesen, &b.Aciklama, &b.CreatedAt, &b.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("get butce: %w", err)
	}
	return b, nil
}

func (r *BinaRepo) DeleteButce(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM site_butce WHERE id=$1`, id)
	return err
}

// ── Dosya ─────────────────────────────────────────────────

func (r *BinaRepo) CreateDosya(ctx context.Context, d *domain.Dosya) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO site_dosya (site_id, baslik, dosya_turu, dosya_url, boyut, aciklama, yukleyen) VALUES ($1,$2,$3,$4,$5,$6,$7) RETURNING id, created_at`,
		d.SiteID, d.Baslik, d.DosyaTuru, d.DosyaURL, d.Boyut, d.Aciklama, d.Yukleyen).Scan(&d.ID, &d.CreatedAt)
}

func (r *BinaRepo) ListDosya(ctx context.Context, siteID int) ([]*domain.Dosya, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, site_id, baslik, COALESCE(dosya_turu,''), COALESCE(dosya_url,''), boyut, COALESCE(aciklama,''), COALESCE(yukleyen,''), created_at FROM site_dosya WHERE site_id=$1 ORDER BY created_at DESC`, siteID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.Dosya
	for rows.Next() {
		d := &domain.Dosya{}
		if err := rows.Scan(&d.ID, &d.SiteID, &d.Baslik, &d.DosyaTuru, &d.DosyaURL, &d.Boyut, &d.Aciklama, &d.Yukleyen, &d.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, d)
	}
	return list, nil
}

func (r *BinaRepo) GetDosya(ctx context.Context, id int) (*domain.Dosya, error) {
	d := &domain.Dosya{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, site_id, baslik, COALESCE(dosya_turu,''), COALESCE(dosya_url,''), boyut, COALESCE(aciklama,''), COALESCE(yukleyen,''), created_at FROM site_dosya WHERE id=$1`, id,
	).Scan(&d.ID, &d.SiteID, &d.Baslik, &d.DosyaTuru, &d.DosyaURL, &d.Boyut, &d.Aciklama, &d.Yukleyen, &d.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("get dosya: %w", err)
	}
	return d, nil
}

func (r *BinaRepo) DeleteDosya(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM site_dosya WHERE id=$1`, id)
	return err
}

// ── Bildirim ──────────────────────────────────────────────

func (r *BinaRepo) CreateBildirim(ctx context.Context, b *domain.Bildirim) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO site_bildirim (site_id, baslik, icerik, tur, hedef, hedef_id, gonderildi) VALUES ($1,$2,$3,$4,$5,$6,$7) RETURNING id, created_at`,
		b.SiteID, b.Baslik, b.Icerik, b.Tur, b.Hedef, b.HedefID, b.Gonderildi).Scan(&b.ID, &b.CreatedAt)
}

func (r *BinaRepo) ListBildirim(ctx context.Context, siteID int) ([]*domain.Bildirim, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, site_id, baslik, COALESCE(icerik,''), tur, hedef, hedef_id, gonderildi, created_at FROM site_bildirim WHERE site_id=$1 ORDER BY created_at DESC`, siteID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.Bildirim
	for rows.Next() {
		b := &domain.Bildirim{}
		if err := rows.Scan(&b.ID, &b.SiteID, &b.Baslik, &b.Icerik, &b.Tur, &b.Hedef, &b.HedefID, &b.Gonderildi, &b.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, b)
	}
	return list, nil
}

func (r *BinaRepo) GetBildirim(ctx context.Context, id int) (*domain.Bildirim, error) {
	b := &domain.Bildirim{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, site_id, baslik, COALESCE(icerik,''), tur, hedef, hedef_id, gonderildi, created_at FROM site_bildirim WHERE id=$1`, id,
	).Scan(&b.ID, &b.SiteID, &b.Baslik, &b.Icerik, &b.Tur, &b.Hedef, &b.HedefID, &b.Gonderildi, &b.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("get bildirim: %w", err)
	}
	return b, nil
}

func (r *BinaRepo) DeleteBildirim(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM site_bildirim WHERE id=$1`, id)
	return err
}
