package handler

import (
	"encoding/json"
	"net/http"
	"strconv"
	"time"

	"github.com/go-chi/chi/v5"
	"github.com/web-platform/backend/internal/api/middleware"
	"github.com/web-platform/backend/internal/domain"
	"github.com/web-platform/backend/internal/repository/postgres"
)

type BinaHandler struct {
	repo *postgres.BinaRepo
}

func NewBinaHandler(repo *postgres.BinaRepo) *BinaHandler {
	return &BinaHandler{repo: repo}
}

func siteIDFromCtx(r *http.Request) int {
	id, _ := r.Context().Value(middleware.UserIDKey).(int)
	return id
}

// ── Site ─────────────────────────────────────────────────

func (h *BinaHandler) CreateSite(w http.ResponseWriter, r *http.Request) {
	var s domain.Site
	if err := json.NewDecoder(r.Body).Decode(&s); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	s.KomisyonYuzde = 2
	if err := h.repo.CreateSite(r.Context(), &s); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, s)
}

func (h *BinaHandler) GetSite(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	s, err := h.repo.GetSite(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
		return
	}
	writeJSON(w, http.StatusOK, s)
}

func (h *BinaHandler) UpdateSite(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	s, err := h.repo.GetSite(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
		return
	}
	if err := json.NewDecoder(r.Body).Decode(s); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	s.ID = id
	if err := h.repo.UpdateSite(r.Context(), s); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, s)
}

// ── Kurulum (Blok + Daire toplu oluşturma) ────────────────

type kurulumRequest struct {
	SiteID  int    `json:"site_id"`
	BlokAdi string `json:"blok_adi"`
	Kat     int    `json:"kat"`
	DK      int    `json:"dk"` // daire per kat
}

func (h *BinaHandler) Kurulum(w http.ResponseWriter, r *http.Request) {
	var req kurulumRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}

	blok := &domain.Blok{SiteID: req.SiteID, Adi: req.BlokAdi, KatAdet: req.Kat, DaireKat: req.DK}
	if err := h.repo.CreateBlok(r.Context(), blok); err != nil {
		http.Error(w, `{"error":"blok create failed"}`, http.StatusInternalServerError)
		return
	}

	kapiNo := 1
	for k := 1; k <= req.Kat; k++ {
		for d := 1; d <= req.DK; d++ {
			no := strconv.Itoa(k) + strconv.Itoa(d)
			daire := &domain.Daire{BlokID: blok.ID, No: no, Kat: k, KapiNo: kapiNo}
			if err := h.repo.CreateDaire(r.Context(), daire); err != nil {
				http.Error(w, `{"error":"daire create failed"}`, http.StatusInternalServerError)
				return
			}
			kapiNo++
		}
	}

	writeJSON(w, http.StatusCreated, map[string]interface{}{
		"blok_id": blok.ID, "blok_adi": blok.Adi, "daire_sayisi": req.Kat * req.DK,
	})
}

// ── Blok ─────────────────────────────────────────────────

func (h *BinaHandler) ListBlok(w http.ResponseWriter, r *http.Request) {
	siteID, _ := strconv.Atoi(r.URL.Query().Get("site_id"))
	list, err := h.repo.ListBlok(r.Context(), siteID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

// ── Daire ─────────────────────────────────────────────────

func (h *BinaHandler) ListDaire(w http.ResponseWriter, r *http.Request) {
	siteID, _ := strconv.Atoi(r.URL.Query().Get("site_id"))
	list, err := h.repo.ListDaire(r.Context(), siteID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

// ── Kisi ─────────────────────────────────────────────────

func (h *BinaHandler) CreateKisi(w http.ResponseWriter, r *http.Request) {
	var k domain.Kisi
	if err := json.NewDecoder(r.Body).Decode(&k); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateKisi(r.Context(), &k); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, k)
}

func (h *BinaHandler) ListKisi(w http.ResponseWriter, r *http.Request) {
	siteID, _ := strconv.Atoi(r.URL.Query().Get("site_id"))
	list, err := h.repo.ListKisi(r.Context(), siteID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

// ── Duyuru ───────────────────────────────────────────────

func (h *BinaHandler) CreateDuyuru(w http.ResponseWriter, r *http.Request) {
	var d domain.Duyuru
	if err := json.NewDecoder(r.Body).Decode(&d); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateDuyuru(r.Context(), &d); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, d)
}

func (h *BinaHandler) ListDuyuru(w http.ResponseWriter, r *http.Request) {
	siteID, _ := strconv.Atoi(r.URL.Query().Get("site_id"))
	list, err := h.repo.ListDuyuru(r.Context(), siteID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

// ── Aidat ────────────────────────────────────────────────

type aidatHesaplaRequest struct {
	SiteID  int     `json:"site_id"`
	Ay      int     `json:"ay"`
	Yil     int     `json:"yil"`
	Toplam  float64 `json:"toplam"`
}

func (h *BinaHandler) AidatHesapla(w http.ResponseWriter, r *http.Request) {
	var req aidatHesaplaRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}

	daireler, err := h.repo.ListDaire(r.Context(), req.SiteID)
	if err != nil {
		http.Error(w, `{"error":"daire listesi alinamadi"}`, http.StatusInternalServerError)
		return
	}
	if len(daireler) == 0 {
		http.Error(w, `{"error":"site icin daire bulunamadi"}`, http.StatusBadRequest)
		return
	}

	daireBasi := req.Toplam / float64(len(daireler))

	for _, d := range daireler {
		blokID := d.BlokID
		a := &domain.Aidat{
			SiteID:  req.SiteID,
			DaireID: d.ID,
			BlokID:  blokID,
			DaireNo: d.No,
			Ay:      req.Ay,
			Yil:     req.Yil,
			Tutar:   daireBasi,
			KapiNo:  d.KapiNo,
		}
		if err := h.repo.CreateAidat(r.Context(), a); err != nil {
			http.Error(w, `{"error":"aidat create failed: `+err.Error()+`"}`, http.StatusInternalServerError)
			return
		}
	}

	writeJSON(w, http.StatusCreated, map[string]interface{}{
		"mesaj":      "Aidat hesaplandi",
		"daire_sayi": len(daireler),
		"daire_basi": daireBasi,
	})
}

func (h *BinaHandler) ListAidat(w http.ResponseWriter, r *http.Request) {
	siteID, _ := strconv.Atoi(r.URL.Query().Get("site_id"))
	ay, _ := strconv.Atoi(r.URL.Query().Get("ay"))
	yil, _ := strconv.Atoi(r.URL.Query().Get("yil"))
	list, err := h.repo.ListAidat(r.Context(), siteID, ay, yil)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *BinaHandler) AidatOdeme(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	if err := h.repo.OdemeAidat(r.Context(), id); err != nil {
		http.Error(w, `{"error":"odeme kaydedilemedi"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": "odendi"})
}

// ── Gelir/Gider ──────────────────────────────────────────

func (h *BinaHandler) CreateGelir(w http.ResponseWriter, r *http.Request) {
	var g domain.Gelir
	if err := json.NewDecoder(r.Body).Decode(&g); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateGelir(r.Context(), &g); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, g)
}

func (h *BinaHandler) CreateGider(w http.ResponseWriter, r *http.Request) {
	var g domain.Gider
	if err := json.NewDecoder(r.Body).Decode(&g); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateGider(r.Context(), &g); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, g)
}

func (h *BinaHandler) ListGelir(w http.ResponseWriter, r *http.Request) {
	siteID, _ := strconv.Atoi(r.URL.Query().Get("site_id"))
	list, err := h.repo.ListGelir(r.Context(), siteID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *BinaHandler) ListGider(w http.ResponseWriter, r *http.Request) {
	siteID, _ := strconv.Atoi(r.URL.Query().Get("site_id"))
	list, err := h.repo.ListGider(r.Context(), siteID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

// ── Arac ─────────────────────────────────────────────────

func (h *BinaHandler) CreateArac(w http.ResponseWriter, r *http.Request) {
	var a domain.Arac
	if err := json.NewDecoder(r.Body).Decode(&a); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateArac(r.Context(), &a); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, a)
}

func (h *BinaHandler) ListArac(w http.ResponseWriter, r *http.Request) {
	siteID, _ := strconv.Atoi(r.URL.Query().Get("site_id"))
	list, err := h.repo.ListArac(r.Context(), siteID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *BinaHandler) DeleteArac(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	if err := h.repo.DeleteArac(r.Context(), id); err != nil {
		http.Error(w, `{"error":"delete failed"}`, http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

// ── Personel ─────────────────────────────────────────────

func (h *BinaHandler) CreatePersonel(w http.ResponseWriter, r *http.Request) {
	var p domain.Personel
	now := time.Now()
	p.IseBaslama = &now
	if err := json.NewDecoder(r.Body).Decode(&p); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreatePersonel(r.Context(), &p); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, p)
}

func (h *BinaHandler) ListPersonel(w http.ResponseWriter, r *http.Request) {
	siteID, _ := strconv.Atoi(r.URL.Query().Get("site_id"))
	list, err := h.repo.ListPersonel(r.Context(), siteID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

// ── Firma ────────────────────────────────────────────────

func (h *BinaHandler) CreateFirma(w http.ResponseWriter, r *http.Request) {
	var f domain.Firma
	if err := json.NewDecoder(r.Body).Decode(&f); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateFirma(r.Context(), &f); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, f)
}

func (h *BinaHandler) ListFirma(w http.ResponseWriter, r *http.Request) {
	siteID, _ := strconv.Atoi(r.URL.Query().Get("site_id"))
	list, err := h.repo.ListFirma(r.Context(), siteID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

// ── Is Talebi ────────────────────────────────────────────

func (h *BinaHandler) CreateIsTalebi(w http.ResponseWriter, r *http.Request) {
	var t domain.IsTalebi
	t.Durum = "bekliyor"
	if err := json.NewDecoder(r.Body).Decode(&t); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateIsTalebi(r.Context(), &t); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, t)
}

func (h *BinaHandler) ListIsTalebi(w http.ResponseWriter, r *http.Request) {
	siteID, _ := strconv.Atoi(r.URL.Query().Get("site_id"))
	list, err := h.repo.ListIsTalebi(r.Context(), siteID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

// ── Sayac ────────────────────────────────────────────────

func (h *BinaHandler) CreateSayac(w http.ResponseWriter, r *http.Request) {
	var s domain.Sayac
	if err := json.NewDecoder(r.Body).Decode(&s); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateSayac(r.Context(), &s); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, s)
}

func (h *BinaHandler) ListSayac(w http.ResponseWriter, r *http.Request) {
	siteID, _ := strconv.Atoi(r.URL.Query().Get("site_id"))
	list, err := h.repo.ListSayac(r.Context(), siteID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

// ── Kargo ────────────────────────────────────────────────

func (h *BinaHandler) CreateKargo(w http.ResponseWriter, r *http.Request) {
	var k domain.Kargo
	k.Durum = "bekliyor"
	if err := json.NewDecoder(r.Body).Decode(&k); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateKargo(r.Context(), &k); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, k)
}

func (h *BinaHandler) ListKargo(w http.ResponseWriter, r *http.Request) {
	siteID, _ := strconv.Atoi(r.URL.Query().Get("site_id"))
	list, err := h.repo.ListKargo(r.Context(), siteID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

// ── Ziyaretci ────────────────────────────────────────────

func (h *BinaHandler) CreateZiyaretci(w http.ResponseWriter, r *http.Request) {
	var z domain.Ziyaretci
	z.Giris = time.Now()
	if err := json.NewDecoder(r.Body).Decode(&z); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateZiyaretci(r.Context(), &z); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, z)
}

func (h *BinaHandler) ListZiyaretci(w http.ResponseWriter, r *http.Request) {
	siteID, _ := strconv.Atoi(r.URL.Query().Get("site_id"))
	list, err := h.repo.ListZiyaretci(r.Context(), siteID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *BinaHandler) ZiyaretciCikis(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	if err := h.repo.ZiyaretciCikis(r.Context(), id); err != nil {
		http.Error(w, `{"error":"cikis kaydedilemedi"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": "cikis_kaydedildi"})
}

// ── Anket ─────────────────────────────────────────────────

func (h *BinaHandler) CreateAnket(w http.ResponseWriter, r *http.Request) {
	var a domain.Anket
	if err := json.NewDecoder(r.Body).Decode(&a); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateAnket(r.Context(), &a); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, a)
}

func (h *BinaHandler) ListAnket(w http.ResponseWriter, r *http.Request) {
	siteID, _ := strconv.Atoi(r.URL.Query().Get("site_id"))
	list, err := h.repo.ListAnket(r.Context(), siteID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *BinaHandler) AnketOy(w http.ResponseWriter, r *http.Request) {
	var oy domain.AnketOy
	if err := json.NewDecoder(r.Body).Decode(&oy); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	oy.AnketID, _ = strconv.Atoi(chi.URLParam(r, "id"))
	if err := h.repo.AnketOy(r.Context(), &oy); err != nil {
		http.Error(w, `{"error":"oy kaydedilemedi"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, oy)
}

func (h *BinaHandler) GetAnket(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	a, err := h.repo.GetAnket(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
		return
	}
	writeJSON(w, http.StatusOK, a)
}

func (h *BinaHandler) DeleteAnket(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	if err := h.repo.DeleteAnket(r.Context(), id); err != nil {
		http.Error(w, `{"error":"delete failed"}`, http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

func (h *BinaHandler) CreateAnketSecenek(w http.ResponseWriter, r *http.Request) {
	var s domain.AnketSecenek
	if err := json.NewDecoder(r.Body).Decode(&s); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateAnketSecenek(r.Context(), &s); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, s)
}

func (h *BinaHandler) ListAnketSecenek(w http.ResponseWriter, r *http.Request) {
	anketID, _ := strconv.Atoi(chi.URLParam(r, "id"))
	list, err := h.repo.ListAnketSecenek(r.Context(), anketID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *BinaHandler) DeleteAnketSecenek(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	if err := h.repo.DeleteAnketSecenek(r.Context(), id); err != nil {
		http.Error(w, `{"error":"delete failed"}`, http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

// ── Icra ──────────────────────────────────────────────────

func (h *BinaHandler) CreateIcra(w http.ResponseWriter, r *http.Request) {
	var i domain.Icra
	if err := json.NewDecoder(r.Body).Decode(&i); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateIcra(r.Context(), &i); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, i)
}

func (h *BinaHandler) ListIcra(w http.ResponseWriter, r *http.Request) {
	siteID, _ := strconv.Atoi(r.URL.Query().Get("site_id"))
	list, err := h.repo.ListIcra(r.Context(), siteID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *BinaHandler) GetIcra(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	i, err := h.repo.GetIcra(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
		return
	}
	writeJSON(w, http.StatusOK, i)
}

func (h *BinaHandler) DeleteIcra(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	if err := h.repo.DeleteIcra(r.Context(), id); err != nil {
		http.Error(w, `{"error":"delete failed"}`, http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

// ── Otopark ───────────────────────────────────────────────

func (h *BinaHandler) CreateOtopark(w http.ResponseWriter, r *http.Request) {
	var o domain.Otopark
	if err := json.NewDecoder(r.Body).Decode(&o); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateOtopark(r.Context(), &o); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, o)
}

func (h *BinaHandler) ListOtopark(w http.ResponseWriter, r *http.Request) {
	siteID, _ := strconv.Atoi(r.URL.Query().Get("site_id"))
	list, err := h.repo.ListOtopark(r.Context(), siteID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *BinaHandler) DeleteOtopark(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	if err := h.repo.DeleteOtopark(r.Context(), id); err != nil {
		http.Error(w, `{"error":"delete failed"}`, http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

func (h *BinaHandler) GetOtopark(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	o, err := h.repo.GetOtopark(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
		return
	}
	writeJSON(w, http.StatusOK, o)
}

// ── Rezervasyon ───────────────────────────────────────────

func (h *BinaHandler) CreateRezervasyon(w http.ResponseWriter, r *http.Request) {
	var rz domain.Rezervasyon
	if err := json.NewDecoder(r.Body).Decode(&rz); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateRezervasyon(r.Context(), &rz); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, rz)
}

func (h *BinaHandler) ListRezervasyon(w http.ResponseWriter, r *http.Request) {
	siteID, _ := strconv.Atoi(r.URL.Query().Get("site_id"))
	list, err := h.repo.ListRezervasyon(r.Context(), siteID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *BinaHandler) GetRezervasyon(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	rz, err := h.repo.GetRezervasyon(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
		return
	}
	writeJSON(w, http.StatusOK, rz)
}

func (h *BinaHandler) DeleteRezervasyon(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	if err := h.repo.DeleteRezervasyon(r.Context(), id); err != nil {
		http.Error(w, `{"error":"delete failed"}`, http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

// ── Toplanti ──────────────────────────────────────────────

func (h *BinaHandler) CreateToplanti(w http.ResponseWriter, r *http.Request) {
	var t domain.Toplanti
	if err := json.NewDecoder(r.Body).Decode(&t); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateToplanti(r.Context(), &t); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, t)
}

func (h *BinaHandler) ListToplanti(w http.ResponseWriter, r *http.Request) {
	siteID, _ := strconv.Atoi(r.URL.Query().Get("site_id"))
	list, err := h.repo.ListToplanti(r.Context(), siteID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *BinaHandler) GetToplanti(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	t, err := h.repo.GetToplanti(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
		return
	}
	writeJSON(w, http.StatusOK, t)
}

func (h *BinaHandler) DeleteToplanti(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	if err := h.repo.DeleteToplanti(r.Context(), id); err != nil {
		http.Error(w, `{"error":"delete failed"}`, http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

// ── Banka ─────────────────────────────────────────────────

func (h *BinaHandler) CreateBanka(w http.ResponseWriter, r *http.Request) {
	var b domain.BankaHesap
	if err := json.NewDecoder(r.Body).Decode(&b); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateBanka(r.Context(), &b); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, b)
}

func (h *BinaHandler) ListBanka(w http.ResponseWriter, r *http.Request) {
	siteID, _ := strconv.Atoi(r.URL.Query().Get("site_id"))
	list, err := h.repo.ListBanka(r.Context(), siteID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *BinaHandler) GetBankaHesap(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	b, err := h.repo.GetBankaHesap(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
		return
	}
	writeJSON(w, http.StatusOK, b)
}

func (h *BinaHandler) DeleteBankaHesap(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	if err := h.repo.DeleteBankaHesap(r.Context(), id); err != nil {
		http.Error(w, `{"error":"delete failed"}`, http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

// ── Isitma ────────────────────────────────────────────────

func (h *BinaHandler) CreateIsitma(w http.ResponseWriter, r *http.Request) {
	var i domain.Isitma
	if err := json.NewDecoder(r.Body).Decode(&i); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateIsitma(r.Context(), &i); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, i)
}

func (h *BinaHandler) ListIsitma(w http.ResponseWriter, r *http.Request) {
	siteID, _ := strconv.Atoi(r.URL.Query().Get("site_id"))
	list, err := h.repo.ListIsitma(r.Context(), siteID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *BinaHandler) GetIsitma(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	i, err := h.repo.GetIsitma(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
		return
	}
	writeJSON(w, http.StatusOK, i)
}

func (h *BinaHandler) DeleteIsitma(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	if err := h.repo.DeleteIsitma(r.Context(), id); err != nil {
		http.Error(w, `{"error":"delete failed"}`, http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

// ── Butce ─────────────────────────────────────────────────

func (h *BinaHandler) CreateButce(w http.ResponseWriter, r *http.Request) {
	var b domain.Butce
	if err := json.NewDecoder(r.Body).Decode(&b); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateButce(r.Context(), &b); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, b)
}

func (h *BinaHandler) ListButce(w http.ResponseWriter, r *http.Request) {
	siteID, _ := strconv.Atoi(r.URL.Query().Get("site_id"))
	list, err := h.repo.ListButce(r.Context(), siteID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *BinaHandler) GetButce(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	b, err := h.repo.GetButce(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
		return
	}
	writeJSON(w, http.StatusOK, b)
}

func (h *BinaHandler) DeleteButce(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	if err := h.repo.DeleteButce(r.Context(), id); err != nil {
		http.Error(w, `{"error":"delete failed"}`, http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

// ── Dosya ─────────────────────────────────────────────────

func (h *BinaHandler) CreateDosya(w http.ResponseWriter, r *http.Request) {
	var d domain.Dosya
	if err := json.NewDecoder(r.Body).Decode(&d); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateDosya(r.Context(), &d); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, d)
}

func (h *BinaHandler) ListDosya(w http.ResponseWriter, r *http.Request) {
	siteID, _ := strconv.Atoi(r.URL.Query().Get("site_id"))
	list, err := h.repo.ListDosya(r.Context(), siteID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *BinaHandler) GetDosya(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	d, err := h.repo.GetDosya(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
		return
	}
	writeJSON(w, http.StatusOK, d)
}

func (h *BinaHandler) DeleteDosya(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	if err := h.repo.DeleteDosya(r.Context(), id); err != nil {
		http.Error(w, `{"error":"delete failed"}`, http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

// ── Bildirim ──────────────────────────────────────────────

func (h *BinaHandler) CreateBildirim(w http.ResponseWriter, r *http.Request) {
	var b domain.Bildirim
	if err := json.NewDecoder(r.Body).Decode(&b); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateBildirim(r.Context(), &b); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, b)
}

func (h *BinaHandler) ListBildirim(w http.ResponseWriter, r *http.Request) {
	siteID, _ := strconv.Atoi(r.URL.Query().Get("site_id"))
	list, err := h.repo.ListBildirim(r.Context(), siteID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *BinaHandler) GetBildirim(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	b, err := h.repo.GetBildirim(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
		return
	}
	writeJSON(w, http.StatusOK, b)
}

func (h *BinaHandler) DeleteBildirim(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	if err := h.repo.DeleteBildirim(r.Context(), id); err != nil {
		http.Error(w, `{"error":"delete failed"}`, http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}
