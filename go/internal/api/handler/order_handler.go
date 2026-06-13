package handler

import (
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/go-chi/chi/v5"
	"github.com/web-platform/backend/internal/domain"
	"github.com/web-platform/backend/internal/repository/postgres"
)

type OrderHandler struct {
	repo *postgres.OrderRepo
}

func NewOrderHandler(repo *postgres.OrderRepo) *OrderHandler {
	return &OrderHandler{repo: repo}
}

func (h *OrderHandler) Create(w http.ResponseWriter, r *http.Request) {
	var o domain.Order
	if err := json.NewDecoder(r.Body).Decode(&o); err != nil {
		http.Error(w, `{"error":"invalid request body"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.Create(r.Context(), &o); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, o)
}

func (h *OrderHandler) Get(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	o, err := h.repo.GetByID(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"order not found"}`, http.StatusNotFound)
		return
	}
	writeJSON(w, http.StatusOK, o)
}

func (h *OrderHandler) ListMy(w http.ResponseWriter, r *http.Request) {
	userID, _ := r.Context().Value("user_id").(int)
	page, _ := strconv.Atoi(r.URL.Query().Get("page"))
	if page < 1 {
		page = 1
	}
	perPage, _ := strconv.Atoi(r.URL.Query().Get("per_page"))
	if perPage < 1 || perPage > 100 {
		perPage = 20
	}

	total, orders, err := h.repo.ListByUser(r.Context(), userID, page, perPage)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]interface{}{
		"total": total, "page": page, "per_page": perPage,
		"total_pages": (total + perPage - 1) / perPage,
		"results":     orders,
	})
}
