package handler

import (
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/go-chi/chi/v5"
	"github.com/web-platform/backend/internal/domain"
	"github.com/web-platform/backend/internal/repository/postgres"
)

type VehicleHandler struct {
	repo *postgres.VehicleRepo
}

func NewVehicleHandler(repo *postgres.VehicleRepo) *VehicleHandler {
	return &VehicleHandler{repo: repo}
}

// ── Brand ─────────────────────────────────────────────────

func (h *VehicleHandler) CreateBrand(w http.ResponseWriter, r *http.Request) {
	var b domain.VehicleBrand
	if err := json.NewDecoder(r.Body).Decode(&b); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateBrand(r.Context(), &b); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, b)
}

func (h *VehicleHandler) ListBrands(w http.ResponseWriter, r *http.Request) {
	list, err := h.repo.ListBrands(r.Context())
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *VehicleHandler) GetBrand(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	b, err := h.repo.GetBrand(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
		return
	}
	writeJSON(w, http.StatusOK, b)
}

// ── Model ─────────────────────────────────────────────────

func (h *VehicleHandler) CreateModel(w http.ResponseWriter, r *http.Request) {
	var m domain.VehicleModel
	if err := json.NewDecoder(r.Body).Decode(&m); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateModel(r.Context(), &m); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, m)
}

func (h *VehicleHandler) ListModels(w http.ResponseWriter, r *http.Request) {
	var brandID *int
	if v := r.URL.Query().Get("brand_id"); v != "" {
		id, _ := strconv.Atoi(v)
		brandID = &id
	}
	list, err := h.repo.ListModels(r.Context(), brandID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *VehicleHandler) GetModel(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	m, err := h.repo.GetModel(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
		return
	}
	writeJSON(w, http.StatusOK, m)
}

// ── Categories / Segments / BodyTypes ─────────────────────

func (h *VehicleHandler) ListCategories(w http.ResponseWriter, r *http.Request) {
	list, err := h.repo.ListCategories(r.Context())
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *VehicleHandler) ListSegments(w http.ResponseWriter, r *http.Request) {
	list, err := h.repo.ListSegments(r.Context())
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *VehicleHandler) ListBodyTypes(w http.ResponseWriter, r *http.Request) {
	list, err := h.repo.ListBodyTypes(r.Context())
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

// ── Model Years ───────────────────────────────────────────

func (h *VehicleHandler) ListModelYears(w http.ResponseWriter, r *http.Request) {
	modelID, _ := strconv.Atoi(chi.URLParam(r, "modelId"))
	list, err := h.repo.ListModelYears(r.Context(), modelID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

// ── Feature Groups & Features ─────────────────────────────

func (h *VehicleHandler) ListFeatureGroups(w http.ResponseWriter, r *http.Request) {
	list, err := h.repo.ListFeatureGroups(r.Context())
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *VehicleHandler) ListFeatures(w http.ResponseWriter, r *http.Request) {
	var groupID *int
	if v := r.URL.Query().Get("group_id"); v != "" {
		id, _ := strconv.Atoi(v)
		groupID = &id
	}
	list, err := h.repo.ListFeatures(r.Context(), groupID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *VehicleHandler) CreateFeatureGroup(w http.ResponseWriter, r *http.Request) {
	var fg domain.FeatureGroup
	if err := json.NewDecoder(r.Body).Decode(&fg); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateFeatureGroup(r.Context(), &fg); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, fg)
}

func (h *VehicleHandler) CreateFeature(w http.ResponseWriter, r *http.Request) {
	var f domain.Feature
	if err := json.NewDecoder(r.Body).Decode(&f); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateFeature(r.Context(), &f); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, f)
}
