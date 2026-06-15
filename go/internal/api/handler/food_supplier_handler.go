package handler

import (
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/go-chi/chi/v5"
	"github.com/web-platform/backend/internal/domain"
	"github.com/web-platform/backend/internal/repository/postgres"
)

type FoodSupplierHandler struct {
	repo *postgres.FoodSupplierRepo
}

func NewFoodSupplierHandler(repo *postgres.FoodSupplierRepo) *FoodSupplierHandler {
	return &FoodSupplierHandler{repo: repo}
}

func (h *FoodSupplierHandler) CreateSupplier(w http.ResponseWriter, r *http.Request) {
	var s domain.FoodSupplier
	if err := json.NewDecoder(r.Body).Decode(&s); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid body"})
		return
	}
	created, err := h.repo.Create(r.Context(), &s)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusCreated, created)
}

func (h *FoodSupplierHandler) GetSupplier(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.ParseInt(chi.URLParam(r, "supplier_id"), 10, 64)
	s, err := h.repo.GetByID(r.Context(), id)
	if err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "not found"})
		return
	}
	writeJSON(w, http.StatusOK, s)
}

func (h *FoodSupplierHandler) ListSuppliers(w http.ResponseWriter, r *http.Request) {
	city := r.URL.Query().Get("city")
	organic := r.URL.Query().Get("organic")
	halal := r.URL.Query().Get("halal")
	res, err := h.repo.List(r.Context(), city, organic, halal)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusOK, res)
}

func (h *FoodSupplierHandler) GetSupplierBySlug(w http.ResponseWriter, r *http.Request) {
	slug := chi.URLParam(r, "slug")
	s, err := h.repo.GetBySlug(r.Context(), slug)
	if err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "not found"})
		return
	}
	products, err := h.repo.ListProductsBySupplier(r.Context(), s.ID)
	if err != nil {
		products = []domain.FoodSupplierProduct{}
	}
	page := domain.SupplierPage{
		ID:                  s.ID,
		CompanyName:         s.CompanyName,
		Slug:                s.Slug,
		Description:         s.Description,
		LogoURL:             s.LogoURL,
		CoverURL:            s.CoverURL,
		SupplierType:        s.SupplierType,
		City:                s.City,
		District:            s.District,
		ContactPhone:        s.ContactPhone,
		ContactEmail:        s.ContactEmail,
		WebsiteURL:          s.WebsiteURL,
		IsOrganicCertified:  s.IsOrganicCertified,
		IsHalalCertified:    s.IsHalalCertified,
		Certifications:      s.Certifications,
		ProductCategories:   s.ProductCategories,
		KitchenPhotos:       s.KitchenPhotos,
		Rating:              s.Rating,
		ReviewCount:         s.ReviewCount,
		VerificationStatus:  s.VerificationStatus,
		IsActive:            s.IsActive,
		Products:            products,
	}
	writeJSON(w, http.StatusOK, page)
}

func (h *FoodSupplierHandler) CreateProduct(w http.ResponseWriter, r *http.Request) {
	supplierID, _ := strconv.ParseInt(chi.URLParam(r, "supplier_id"), 10, 64)
	var p domain.FoodSupplierProduct
	if err := json.NewDecoder(r.Body).Decode(&p); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid body"})
		return
	}
	p.SupplierID = supplierID
	created, err := h.repo.CreateProduct(r.Context(), &p)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusCreated, created)
}

func (h *FoodSupplierHandler) ListProducts(w http.ResponseWriter, r *http.Request) {
	supplierID, _ := strconv.ParseInt(chi.URLParam(r, "supplier_id"), 10, 64)
	products, err := h.repo.ListProductsBySupplier(r.Context(), supplierID)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusOK, products)
}

func (h *FoodSupplierHandler) LinkSupplier(w http.ResponseWriter, r *http.Request) {
	restID, _ := strconv.ParseInt(chi.URLParam(r, "rest_id"), 10, 64)
	var body struct {
		SupplierID    int64   `json:"supplier_id"`
		IsPreferred   bool    `json:"is_preferred"`
		ContractStart *string `json:"contract_start"`
		ContractEnd   *string `json:"contract_end"`
		Notes         *string `json:"notes"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid body"})
		return
	}
	link, err := h.repo.LinkSupplier(r.Context(), restID, body.SupplierID, body.IsPreferred, body.ContractStart, body.ContractEnd, body.Notes)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusCreated, link)
}

func (h *FoodSupplierHandler) UnlinkSupplier(w http.ResponseWriter, r *http.Request) {
	restID, _ := strconv.ParseInt(chi.URLParam(r, "rest_id"), 10, 64)
	supplierID, _ := strconv.ParseInt(chi.URLParam(r, "supplier_id"), 10, 64)
	if err := h.repo.UnlinkSupplier(r.Context(), restID, supplierID); err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusOK, map[string]bool{"ok": true})
}

func (h *FoodSupplierHandler) ListRestaurantSuppliers(w http.ResponseWriter, r *http.Request) {
	restID, _ := strconv.ParseInt(chi.URLParam(r, "rest_id"), 10, 64)
	links, err := h.repo.ListRestaurantSuppliers(r.Context(), restID)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	var result []domain.SupplierLinkResponse
	for _, l := range links {
		s, _ := h.repo.GetByID(r.Context(), l.SupplierID)
		name := ""
		if s != nil {
			name = s.CompanyName
		}
		result = append(result, domain.SupplierLinkResponse{
			ID:           l.ID,
			RestaurantID: l.RestaurantID,
			SupplierID:   l.SupplierID,
			SupplierName: name,
			IsPreferred:  l.IsPreferred,
			ContractStart: l.ContractStart,
			ContractEnd:   l.ContractEnd,
			Notes:         l.Notes,
		})
	}
	if result == nil {
		result = []domain.SupplierLinkResponse{}
	}
	writeJSON(w, http.StatusOK, result)
}

func (h *FoodSupplierHandler) CreateIngredient(w http.ResponseWriter, r *http.Request) {
	itemID, _ := strconv.ParseInt(chi.URLParam(r, "item_id"), 10, 64)
	var body struct {
		SupplierProductID   int64    `json:"supplier_product_id"`
		Quantity            *float64 `json:"quantity"`
		Unit                *string  `json:"unit"`
		Notes               *string  `json:"notes"`
		IsVisibleToCustomer bool     `json:"is_visible_to_customer"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "invalid body"})
		return
	}
	ing := &domain.FoodMenuItemIngredient{
		MenuItemID:         itemID,
		SupplierProductID:  body.SupplierProductID,
		Quantity:           body.Quantity,
		Unit:               body.Unit,
		Notes:              body.Notes,
		IsVisibleToCustomer: body.IsVisibleToCustomer,
	}
	created, err := h.repo.CreateIngredient(r.Context(), ing)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusCreated, created)
}

func (h *FoodSupplierHandler) DeleteIngredient(w http.ResponseWriter, r *http.Request) {
	ingID, _ := strconv.ParseInt(chi.URLParam(r, "ingredient_id"), 10, 64)
	if err := h.repo.DeleteIngredient(r.Context(), ingID); err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusOK, map[string]bool{"ok": true})
}

func (h *FoodSupplierHandler) ListIngredients(w http.ResponseWriter, r *http.Request) {
	itemID, _ := strconv.ParseInt(chi.URLParam(r, "item_id"), 10, 64)
	ings, err := h.repo.ListIngredients(r.Context(), itemID)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	var result []domain.IngredientWithDetails
	for _, ing := range ings {
		prod, _ := h.repo.GetProductByID(r.Context(), ing.SupplierProductID)
		prodName, supName, supSlug := "", "", ""
		if prod != nil {
			prodName = prod.Name
			sup, _ := h.repo.GetByID(r.Context(), prod.SupplierID)
			if sup != nil {
				supName = sup.CompanyName
				supSlug = sup.Slug
			}
		}
		result = append(result, domain.IngredientWithDetails{
			ID:                  ing.ID,
			MenuItemID:          ing.MenuItemID,
			SupplierProductID:   ing.SupplierProductID,
			ProductName:         prodName,
			SupplierName:        supName,
			SupplierSlug:        supSlug,
			Quantity:            ing.Quantity,
			Unit:                ing.Unit,
			Notes:               ing.Notes,
			IsVisibleToCustomer: ing.IsVisibleToCustomer,
		})
	}
	if result == nil {
		result = []domain.IngredientWithDetails{}
	}
	writeJSON(w, http.StatusOK, result)
}

func (h *FoodSupplierHandler) TraceMenuItem(w http.ResponseWriter, r *http.Request) {
	itemID, _ := strconv.ParseInt(chi.URLParam(r, "item_id"), 10, 64)
	ings, err := h.repo.ListIngredients(r.Context(), itemID)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	var details []domain.IngredientWithDetails
	for _, ing := range ings {
		if !ing.IsVisibleToCustomer {
			continue
		}
		prod, _ := h.repo.GetProductByID(r.Context(), ing.SupplierProductID)
		prodName, supName, supSlug := "", "", ""
		if prod != nil {
			prodName = prod.Name
			sup, _ := h.repo.GetByID(r.Context(), prod.SupplierID)
			if sup != nil {
				supName = sup.CompanyName
				supSlug = sup.Slug
			}
		}
		details = append(details, domain.IngredientWithDetails{
			ID:                  ing.ID,
			MenuItemID:          ing.MenuItemID,
			SupplierProductID:   ing.SupplierProductID,
			ProductName:         prodName,
			SupplierName:        supName,
			SupplierSlug:        supSlug,
			Quantity:            ing.Quantity,
			Unit:                ing.Unit,
			Notes:               ing.Notes,
			IsVisibleToCustomer: ing.IsVisibleToCustomer,
		})
	}
	if details == nil {
		details = []domain.IngredientWithDetails{}
	}
	writeJSON(w, http.StatusOK, domain.TraceResponse{
		MenuItemID:   itemID,
		MenuItemName: "", // would need a join in prod
		Ingredients:  details,
	})
}
