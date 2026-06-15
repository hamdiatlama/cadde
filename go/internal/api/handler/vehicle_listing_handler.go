package handler

import (
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/go-chi/chi/v5"
	"github.com/web-platform/backend/internal/repository/postgres"
)

type VehicleListingHandler struct {
	repo *postgres.VehicleListingRepo
}

func NewVehicleListingHandler(repo *postgres.VehicleListingRepo) *VehicleListingHandler {
	return &VehicleListingHandler{repo: repo}
}

func (h *VehicleListingHandler) CreateListing(w http.ResponseWriter, r *http.Request) {
	userID := r.Context().Value("user_id").(int)
	var body struct {
		Title string  `json:"title"`
		Year  int     `json:"year"`
		Price float64 `json:"price"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid body"})
		return
	}
	l, err := h.repo.CreateListing(r.Context(), userID, body.Title, body.Year, body.Price)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusCreated, l)
}

func (h *VehicleListingHandler) GetListing(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	l, err := h.repo.GetListing(r.Context(), id)
	if err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "not found"})
		return
	}
	h.repo.IncrementView(r.Context(), id)
	writeJSON(w, http.StatusOK, l)
}

func (h *VehicleListingHandler) UpdateListing(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	var body map[string]any
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid body"})
		return
	}
	if err := h.repo.UpdateListing(r.Context(), id, body); err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": "updated"})
}

func (h *VehicleListingHandler) SearchListings(w http.ResponseWriter, r *http.Request) {
	page, _ := strconv.Atoi(r.URL.Query().Get("page"))
	if page < 1 {
		page = 1
	}
	limit, _ := strconv.Atoi(r.URL.Query().Get("limit"))
	if limit < 1 || limit > 100 {
		limit = 20
	}
	city := r.URL.Query().Get("city")
	fuelType := r.URL.Query().Get("fuel_type")
	var brandID, modelID *int
	if v := r.URL.Query().Get("brand_id"); v != "" {
		if id, err := strconv.Atoi(v); err == nil {
			brandID = &id
		}
	}
	if v := r.URL.Query().Get("model_id"); v != "" {
		if id, err := strconv.Atoi(v); err == nil {
			modelID = &id
		}
	}
	var minPrice, maxPrice *float64
	if v := r.URL.Query().Get("min_price"); v != "" {
		if p, err := strconv.ParseFloat(v, 64); err == nil {
			minPrice = &p
		}
	}
	if v := r.URL.Query().Get("max_price"); v != "" {
		if p, err := strconv.ParseFloat(v, 64); err == nil {
			maxPrice = &p
		}
	}
	items, total, err := h.repo.SearchListings(r.Context(), brandID, modelID, minPrice, maxPrice, city, fuelType, page, limit)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{"items": items, "total": total})
}

func (h *VehicleListingHandler) CreateGallery(w http.ResponseWriter, r *http.Request) {
	userID := r.Context().Value("user_id").(int)
	var body struct {
		CompanyName string `json:"company_name"`
		Slug        string `json:"slug"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid body"})
		return
	}
	g, err := h.repo.CreateGallery(r.Context(), userID, body.CompanyName, body.Slug)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusCreated, g)
}
