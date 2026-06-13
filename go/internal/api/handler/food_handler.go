package handler

import (
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/go-chi/chi/v5"
	"github.com/web-platform/backend/internal/api/middleware"
	"github.com/web-platform/backend/internal/domain"
	"github.com/web-platform/backend/internal/repository/postgres"
)

type FoodHandler struct {
	repo *postgres.FoodRepo
}

func NewFoodHandler(repo *postgres.FoodRepo) *FoodHandler {
	return &FoodHandler{repo: repo}
}

// ── Restaurants ───────────────────────────────────────────────

type registerRestaurantRequest struct {
	Name        string  `json:"name"`
	Slug        string  `json:"slug"`
	Description string  `json:"description,omitempty"`
	Category    string  `json:"category"`
	CuisineType string  `json:"cuisine_type,omitempty"`
	MinOrder    float64 `json:"min_order"`
	DeliveryFee float64 `json:"delivery_fee"`
	AvgPrepTime int     `json:"avg_prep_time"`
}

func (h *FoodHandler) RegisterRestaurant(w http.ResponseWriter, r *http.Request) {
	var req registerRestaurantRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, `{"error":"invalid request body"}`, http.StatusBadRequest)
		return
	}
	sellerID, _ := r.Context().Value(middleware.UserIDKey).(int)

	rest := &domain.Restaurant{
		SellerID:    sellerID,
		Name:        req.Name,
		Slug:        req.Slug,
		Description: req.Description,
		Category:    req.Category,
		CuisineType: req.CuisineType,
		IsActive:    true,
		MinOrder:    req.MinOrder,
		DeliveryFee: req.DeliveryFee,
		AvgPrepTime: req.AvgPrepTime,
	}
	if err := h.repo.CreateRestaurant(r.Context(), rest); err != nil {
		http.Error(w, `{"error":"restaurant already exists or create failed"}`, http.StatusConflict)
		return
	}
	writeJSON(w, http.StatusCreated, map[string]interface{}{
		"id": rest.ID, "status": "restaurant_registered",
	})
}

func (h *FoodHandler) UpdateRestaurant(w http.ResponseWriter, r *http.Request) {
	restID, _ := strconv.Atoi(chi.URLParam(r, "rest_id"))
	sellerID, _ := r.Context().Value(middleware.UserIDKey).(int)

	rest, err := h.repo.GetRestaurantByID(r.Context(), restID)
	if err != nil || rest.SellerID != sellerID {
		http.Error(w, `{"error":"not found or not yours"}`, http.StatusNotFound)
		return
	}

	var req registerRestaurantRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}

	rest.Name = req.Name
	rest.Description = req.Description
	rest.Category = req.Category
	rest.CuisineType = req.CuisineType
	rest.MinOrder = req.MinOrder
	rest.DeliveryFee = req.DeliveryFee
	rest.AvgPrepTime = req.AvgPrepTime

	if err := h.repo.UpdateRestaurant(r.Context(), rest); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]interface{}{"status": "restaurant_updated"})
}

func (h *FoodHandler) VerifyRestaurant(w http.ResponseWriter, r *http.Request) {
	restID, _ := strconv.Atoi(chi.URLParam(r, "rest_id"))
	role, _ := r.Context().Value(middleware.UserRoleKey).(string)
	if role != "admin" {
		http.Error(w, `{"error":"only admins can verify"}`, http.StatusForbidden)
		return
	}

	var req struct{ Status string `json:"status"` }
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}

	verified := req.Status == "approved"
	if err := h.repo.UpdateVerification(r.Context(), restID, verified); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]interface{}{"status": "restaurant_" + req.Status})
}

func (h *FoodHandler) ListRestaurants(w http.ResponseWriter, r *http.Request) {
	category := r.URL.Query().Get("category")
	lat, _ := strconv.ParseFloat(r.URL.Query().Get("lat"), 64)
	lon, _ := strconv.ParseFloat(r.URL.Query().Get("lon"), 64)

	rests, err := h.repo.ListRestaurants(r.Context(), category, lat, lon)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, rests)
}

// ── Menu ──────────────────────────────────────────────────────

type createMenuItemRequest struct {
	Name            string  `json:"name"`
	Description     string  `json:"description,omitempty"`
	Price           float64 `json:"price"`
	OriginalPrice   float64 `json:"original_price,omitempty"`
	Category        string  `json:"category"`
	ImageURL        string  `json:"image_url,omitempty"`
	PrepTimeMinutes int     `json:"prep_time_minutes"`
	SortOrder       int     `json:"sort_order"`
}

func (h *FoodHandler) CreateMenuItem(w http.ResponseWriter, r *http.Request) {
	sellerID, _ := r.Context().Value(middleware.UserIDKey).(int)
	rest, err := h.repo.GetRestaurantBySellerID(r.Context(), sellerID)
	if err != nil {
		http.Error(w, `{"error":"restaurant not found"}`, http.StatusNotFound)
		return
	}

	var req createMenuItemRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}

	item := &domain.FoodMenuItem{
		RestaurantID:    rest.ID,
		Name:            req.Name,
		Description:     req.Description,
		Price:           req.Price,
		OriginalPrice:   req.OriginalPrice,
		Category:        req.Category,
		ImageURL:        req.ImageURL,
		PrepTimeMinutes: req.PrepTimeMinutes,
		IsAvailable:     true,
		SortOrder:       req.SortOrder,
	}
	if err := h.repo.CreateMenuItem(r.Context(), item); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, map[string]interface{}{"status": "menu_item_created", "id": item.ID})
}

func (h *FoodHandler) UpdateMenuItem(w http.ResponseWriter, r *http.Request) {
	itemID, _ := strconv.Atoi(chi.URLParam(r, "item_id"))

	item, err := h.repo.GetMenuItemByID(r.Context(), itemID)
	if err != nil {
		http.Error(w, `{"error":"item not found"}`, http.StatusNotFound)
		return
	}

	sellerID, _ := r.Context().Value(middleware.UserIDKey).(int)
	rest, err := h.repo.GetRestaurantBySellerID(r.Context(), sellerID)
	if err != nil || rest.ID != item.RestaurantID {
		http.Error(w, `{"error":"not your restaurant"}`, http.StatusForbidden)
		return
	}

	var req createMenuItemRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}

	item.Name = req.Name
	item.Description = req.Description
	item.Price = req.Price
	item.OriginalPrice = req.OriginalPrice
	item.Category = req.Category
	item.ImageURL = req.ImageURL
	item.PrepTimeMinutes = req.PrepTimeMinutes
	item.SortOrder = req.SortOrder

	if err := h.repo.UpdateMenuItem(r.Context(), item); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]interface{}{"status": "menu_item_updated"})
}

func (h *FoodHandler) DeleteMenuItem(w http.ResponseWriter, r *http.Request) {
	itemID, _ := strconv.Atoi(chi.URLParam(r, "item_id"))
	sellerID, _ := r.Context().Value(middleware.UserIDKey).(int)

	item, err := h.repo.GetMenuItemByID(r.Context(), itemID)
	if err != nil {
		http.Error(w, `{"error":"item not found"}`, http.StatusNotFound)
		return
	}
	rest, err := h.repo.GetRestaurantBySellerID(r.Context(), sellerID)
	if err != nil || rest.ID != item.RestaurantID {
		http.Error(w, `{"error":"not your restaurant"}`, http.StatusForbidden)
		return
	}

	if err := h.repo.DeleteMenuItem(r.Context(), itemID); err != nil {
		http.Error(w, `{"error":"delete failed"}`, http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

func (h *FoodHandler) GetMenu(w http.ResponseWriter, r *http.Request) {
	restID, _ := strconv.Atoi(chi.URLParam(r, "rest_id"))
	items, err := h.repo.GetMenu(r.Context(), restID)
	if err != nil {
		http.Error(w, `{"error":"get menu failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, items)
}

// ── Modifiers ─────────────────────────────────────────────────

type createModifierRequest struct {
	Name       string  `json:"name"`
	Price      float64 `json:"price"`
	IsRequired bool    `json:"is_required"`
	MaxSelect  int     `json:"max_select"`
	SortOrder  int     `json:"sort_order"`
}

func (h *FoodHandler) AddModifier(w http.ResponseWriter, r *http.Request) {
	itemID, _ := strconv.Atoi(chi.URLParam(r, "item_id"))
	sellerID, _ := r.Context().Value(middleware.UserIDKey).(int)

	item, err := h.repo.GetMenuItemByID(r.Context(), itemID)
	if err != nil {
		http.Error(w, `{"error":"item not found"}`, http.StatusNotFound)
		return
	}
	rest, err := h.repo.GetRestaurantBySellerID(r.Context(), sellerID)
	if err != nil || rest.ID != item.RestaurantID {
		http.Error(w, `{"error":"not your restaurant"}`, http.StatusForbidden)
		return
	}

	var req createModifierRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}

	mod := &domain.MenuItemModifier{
		MenuItemID: itemID,
		Name:       req.Name,
		Price:      req.Price,
		IsRequired: req.IsRequired,
		MaxSelect:  req.MaxSelect,
		SortOrder:  req.SortOrder,
	}
	if err := h.repo.CreateModifier(r.Context(), mod); err != nil {
		http.Error(w, `{"error":"create modifier failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, mod)
}

func (h *FoodHandler) DeleteModifier(w http.ResponseWriter, r *http.Request) {
	modID, _ := strconv.Atoi(chi.URLParam(r, "mod_id"))
	if err := h.repo.DeleteModifier(r.Context(), modID); err != nil {
		http.Error(w, `{"error":"delete failed"}`, http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

// ── Branches ──────────────────────────────────────────────────

type createBranchRequest struct {
	Name      string  `json:"name"`
	Address   string  `json:"address"`
	Latitude  float64 `json:"latitude"`
	Longitude float64 `json:"longitude"`
	Phone     string  `json:"phone,omitempty"`
}

func (h *FoodHandler) AddBranch(w http.ResponseWriter, r *http.Request) {
	restID, _ := strconv.Atoi(chi.URLParam(r, "rest_id"))

	var req createBranchRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}

	branch := &domain.RestaurantBranch{
		RestaurantID: restID,
		Name:         req.Name,
		Address:      req.Address,
		Latitude:     req.Latitude,
		Longitude:    req.Longitude,
		Phone:        req.Phone,
		IsActive:     true,
	}
	if err := h.repo.CreateBranch(r.Context(), branch); err != nil {
		http.Error(w, `{"error":"create branch failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, branch)
}

func (h *FoodHandler) ListBranches(w http.ResponseWriter, r *http.Request) {
	restID, _ := strconv.Atoi(chi.URLParam(r, "rest_id"))
	branches, err := h.repo.ListBranches(r.Context(), restID)
	if err != nil {
		http.Error(w, `{"error":"list branches failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, branches)
}

// ── Delivery Zones ────────────────────────────────────────────

type createZoneRequest struct {
	Name        string  `json:"name"`
	MinLat      float64 `json:"min_lat"`
	MaxLat      float64 `json:"max_lat"`
	MinLon      float64 `json:"min_lon"`
	MaxLon      float64 `json:"max_lon"`
	DeliveryFee float64 `json:"delivery_fee,omitempty"`
	MinOrder    float64 `json:"min_order,omitempty"`
}

func (h *FoodHandler) AddZone(w http.ResponseWriter, r *http.Request) {
	restID, _ := strconv.Atoi(chi.URLParam(r, "rest_id"))

	var req createZoneRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}

	zone := &domain.DeliveryZone{
		RestaurantID: restID,
		Name:         req.Name,
		MinLat:       req.MinLat,
		MaxLat:       req.MaxLat,
		MinLon:       req.MinLon,
		MaxLon:       req.MaxLon,
		DeliveryFee:  req.DeliveryFee,
		MinOrder:     req.MinOrder,
		IsActive:     true,
	}
	if err := h.repo.CreateZone(r.Context(), zone); err != nil {
		http.Error(w, `{"error":"create zone failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, zone)
}

func (h *FoodHandler) ListZones(w http.ResponseWriter, r *http.Request) {
	restID, _ := strconv.Atoi(chi.URLParam(r, "rest_id"))
	zones, err := h.repo.ListZones(r.Context(), restID)
	if err != nil {
		http.Error(w, `{"error":"list zones failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, zones)
}
