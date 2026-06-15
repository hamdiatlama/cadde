package handler

import (
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/go-chi/chi/v5"
	"github.com/web-platform/backend/internal/repository/postgres"
)

type CicekHandler struct {
	repo *postgres.CicekRepo
}

func NewCicekHandler(repo *postgres.CicekRepo) *CicekHandler {
	return &CicekHandler{repo: repo}
}

// --- Florist Profiles ---

func (h *CicekHandler) CreateFlorist(w http.ResponseWriter, r *http.Request) {
	userID := r.Context().Value("user_id").(int)
	var body struct {
		ShopName string `json:"shop_name"`
		Slug     string `json:"slug"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid body"})
		return
	}
	f, err := h.repo.CreateFlorist(r.Context(), userID, body.ShopName, body.Slug)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusCreated, f)
}

func (h *CicekHandler) GetMyFlorist(w http.ResponseWriter, r *http.Request) {
	userID := r.Context().Value("user_id").(int)
	f, err := h.repo.GetFloristByUser(r.Context(), userID)
	if err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "florist not found"})
		return
	}
	writeJSON(w, http.StatusOK, f)
}

func (h *CicekHandler) GetFlorist(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	f, err := h.repo.GetFloristByID(r.Context(), id)
	if err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "not found"})
		return
	}
	writeJSON(w, http.StatusOK, f)
}

func (h *CicekHandler) UpdateFlorist(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	var body map[string]any
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid body"})
		return
	}
	if err := h.repo.UpdateFlorist(r.Context(), id, body); err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": "updated"})
}

func (h *CicekHandler) ToggleFlorist(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	open, err := h.repo.ToggleFloristOpen(r.Context(), id)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusOK, map[string]bool{"is_open": open})
}

func (h *CicekHandler) ListFlorists(w http.ResponseWriter, r *http.Request) {
	city := r.URL.Query().Get("city")
	page, _ := strconv.Atoi(r.URL.Query().Get("page"))
	if page < 1 {
		page = 1
	}
	limit, _ := strconv.Atoi(r.URL.Query().Get("limit"))
	if limit < 1 || limit > 100 {
		limit = 20
	}
	items, total, err := h.repo.ListActiveFlorists(r.Context(), city, page, limit)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusOK, map[string]any{"items": items, "total": total})
}

func (h *CicekHandler) GetFloristBySlug(w http.ResponseWriter, r *http.Request) {
	slug := chi.URLParam(r, "slug")
	f, err := h.repo.GetFloristBySlug(r.Context(), slug)
	if err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "not found"})
		return
	}
	writeJSON(w, http.StatusOK, f)
}

// --- Products ---

func (h *CicekHandler) CreateProduct(w http.ResponseWriter, r *http.Request) {
	floristID, _ := strconv.Atoi(chi.URLParam(r, "id"))
	var body struct {
		Name  string  `json:"name"`
		Price float64 `json:"price"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid body"})
		return
	}
	p, err := h.repo.CreateProduct(r.Context(), "florist", floristID, body.Name, body.Price)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusCreated, p)
}

func (h *CicekHandler) ListFloristProducts(w http.ResponseWriter, r *http.Request) {
	floristID, _ := strconv.Atoi(chi.URLParam(r, "id"))
	items, _, _ := h.repo.ListActiveFlorists(r.Context(), "", 1, 100)
	_ = floristID
	writeJSON(w, http.StatusOK, items)
}
