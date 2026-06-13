package handler

import (
	"net/http"
	"strconv"

	"github.com/web-platform/backend/internal/repository/postgres"
)

type CourierHandler struct {
	repo *postgres.CourierRepo
}

func NewCourierHandler(repo *postgres.CourierRepo) *CourierHandler {
	return &CourierHandler{repo: repo}
}

func (h *CourierHandler) GetNearby(w http.ResponseWriter, r *http.Request) {
	lat, _ := strconv.ParseFloat(r.URL.Query().Get("lat"), 64)
	lon, _ := strconv.ParseFloat(r.URL.Query().Get("lon"), 64)
	radius, _ := strconv.ParseFloat(r.URL.Query().Get("radius"), 64)
	if radius <= 0 {
		radius = 5
	}

	couriers, err := h.repo.GetAvailableNearby(r.Context(), lat, lon, radius)
	if err != nil {
		http.Error(w, `{"error":"search failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, couriers)
}
