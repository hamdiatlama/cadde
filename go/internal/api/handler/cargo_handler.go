package handler

import (
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/go-chi/chi/v5"
	"github.com/web-platform/backend/internal/repository/postgres"
)

type CargoHandler struct {
	repo *postgres.CargoRepo
}

func NewCargoHandler(repo *postgres.CargoRepo) *CargoHandler {
	return &CargoHandler{repo: repo}
}

func (h *CargoHandler) CreateCompany(w http.ResponseWriter, r *http.Request) {
	userID := r.Context().Value("user_id").(int)
	var body struct {
		CompanyName string `json:"company_name"`
		Slug        string `json:"slug"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid body"})
		return
	}
	c, err := h.repo.CreateCompany(r.Context(), userID, body.CompanyName, body.Slug)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusCreated, c)
}

func (h *CargoHandler) GetMyCompany(w http.ResponseWriter, r *http.Request) {
	userID := r.Context().Value("user_id").(int)
	c, err := h.repo.GetCompanyByUser(r.Context(), userID)
	if err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "company not found"})
		return
	}
	writeJSON(w, http.StatusOK, c)
}

func (h *CargoHandler) GetCompany(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	c, err := h.repo.GetCompany(r.Context(), id)
	if err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "not found"})
		return
	}
	writeJSON(w, http.StatusOK, c)
}

func (h *CargoHandler) ListCompanies(w http.ResponseWriter, r *http.Request) {
	companies, err := h.repo.ListCompanies(r.Context())
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusOK, companies)
}

func (h *CargoHandler) CreateShipment(w http.ResponseWriter, r *http.Request) {
	var body struct {
		CompanyID       int    `json:"company_id"`
		TrackingNo      string `json:"tracking_no"`
		SenderName      string `json:"sender_name"`
		RecipientName   string `json:"recipient_name"`
		RecipientCity   string `json:"recipient_city"`
		RecipientAddress string `json:"recipient_address"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid body"})
		return
	}
	s, err := h.repo.CreateShipment(r.Context(), body.CompanyID, body.TrackingNo,
		body.SenderName, body.RecipientName, body.RecipientCity, body.RecipientAddress)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusCreated, s)
}

func (h *CargoHandler) TrackShipment(w http.ResponseWriter, r *http.Request) {
	trackingNo := chi.URLParam(r, "tracking_no")
	s, err := h.repo.GetShipmentByTracking(r.Context(), trackingNo)
	if err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "not found"})
		return
	}
	writeJSON(w, http.StatusOK, s)
}
