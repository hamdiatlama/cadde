package handler

import (
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/go-chi/chi/v5"
	"github.com/web-platform/backend/internal/domain"
	"github.com/web-platform/backend/internal/infra"
	"github.com/web-platform/backend/internal/repository/postgres"
)

type RideHandler struct {
	repo   *postgres.RideRepo
	osrm   *infra.OSRMClient
}

func NewRideHandler(repo *postgres.RideRepo, osrm *infra.OSRMClient) *RideHandler {
	return &RideHandler{repo: repo, osrm: osrm}
}

func (h *RideHandler) Estimate(w http.ResponseWriter, r *http.Request) {
	var req struct {
		PickupLat  float64 `json:"pickup_latitude"`
		PickupLon  float64 `json:"pickup_longitude"`
		DropoffLat float64 `json:"dropoff_latitude"`
		DropoffLon float64 `json:"dropoff_longitude"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}

	route, err := h.osrm.Route(req.PickupLat, req.PickupLon, req.DropoffLat, req.DropoffLon)
	if err != nil {
		// Fallback to haversine
		dist := infra.HaversineKm(req.PickupLat, req.PickupLon, req.DropoffLat, req.DropoffLon)
		writeJSON(w, http.StatusOK, map[string]interface{}{
			"distance_km":      dist,
			"duration_seconds": int(dist / 30 * 3600),
		})
		return
	}

	writeJSON(w, http.StatusOK, map[string]interface{}{
		"distance_km":      route.DistanceKm,
		"duration_seconds": route.DurationSeconds,
		"polyline":         route.Polyline,
	})
}

func (h *RideHandler) Create(w http.ResponseWriter, r *http.Request) {
	var ride domain.Ride
	if err := json.NewDecoder(r.Body).Decode(&ride); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.Create(r.Context(), &ride); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, ride)
}

func (h *RideHandler) Get(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	ride, err := h.repo.GetByID(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
		return
	}
	writeJSON(w, http.StatusOK, ride)
}
