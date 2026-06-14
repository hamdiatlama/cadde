package handler

import (
	"encoding/json"
	"net/http"
	"strconv"
	"time"

	"github.com/go-chi/chi/v5"
	"github.com/web-platform/backend/internal/domain"
	"github.com/web-platform/backend/internal/repository/postgres"
)

type RealEstateHandler struct {
	repo *postgres.RealEstateRepo
}

func NewRealEstateHandler(repo *postgres.RealEstateRepo) *RealEstateHandler {
	return &RealEstateHandler{repo: repo}
}

// ── Property Category ─────────────────────────────────────

func (h *RealEstateHandler) CreateCategory(w http.ResponseWriter, r *http.Request) {
	var c domain.PropertyCategory
	if err := json.NewDecoder(r.Body).Decode(&c); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateCategory(r.Context(), &c); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, c)
}

func (h *RealEstateHandler) ListCategories(w http.ResponseWriter, r *http.Request) {
	list, err := h.repo.ListCategories(r.Context())
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *RealEstateHandler) DeleteCategory(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	if err := h.repo.DeleteCategory(r.Context(), id); err != nil {
		http.Error(w, `{"error":"delete failed"}`, http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

// ── Property Type ─────────────────────────────────────────

func (h *RealEstateHandler) CreateType(w http.ResponseWriter, r *http.Request) {
	var t domain.PropertyType
	if err := json.NewDecoder(r.Body).Decode(&t); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateType(r.Context(), &t); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, t)
}

func (h *RealEstateHandler) ListTypes(w http.ResponseWriter, r *http.Request) {
	list, err := h.repo.ListTypes(r.Context())
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *RealEstateHandler) DeleteType(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	if err := h.repo.DeleteType(r.Context(), id); err != nil {
		http.Error(w, `{"error":"delete failed"}`, http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

// ── Contractor Company ────────────────────────────────────

func (h *RealEstateHandler) CreateCompany(w http.ResponseWriter, r *http.Request) {
	var c domain.ContractorCompany
	if err := json.NewDecoder(r.Body).Decode(&c); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateCompany(r.Context(), &c); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, c)
}

func (h *RealEstateHandler) GetCompany(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	c, err := h.repo.GetCompany(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
		return
	}
	writeJSON(w, http.StatusOK, c)
}

func (h *RealEstateHandler) ListCompanies(w http.ResponseWriter, r *http.Request) {
	list, err := h.repo.ListCompanies(r.Context())
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

// ── Contractor Review ─────────────────────────────────────

func (h *RealEstateHandler) CreateReview(w http.ResponseWriter, r *http.Request) {
	var rev domain.ContractorReview
	if err := json.NewDecoder(r.Body).Decode(&rev); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateReview(r.Context(), &rev); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, rev)
}

func (h *RealEstateHandler) ListReviews(w http.ResponseWriter, r *http.Request) {
	companyID, _ := strconv.Atoi(chi.URLParam(r, "company_id"))
	list, err := h.repo.ListReviews(r.Context(), companyID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

// ── Property Listing ──────────────────────────────────────

func (h *RealEstateHandler) CreateListing(w http.ResponseWriter, r *http.Request) {
	var l domain.PropertyListing
	if err := json.NewDecoder(r.Body).Decode(&l); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateListing(r.Context(), &l); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, l)
}

func (h *RealEstateHandler) GetListing(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.ParseInt(chi.URLParam(r, "id"), 10, 64)
	l, err := h.repo.GetListing(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
		return
	}
	photos, _ := h.repo.ListPhotos(r.Context(), id)
	features, _ := h.repo.GetListingFeatures(r.Context(), id)
	writeJSON(w, http.StatusOK, map[string]interface{}{
		"listing":  l,
		"photos":   photos,
		"features": features,
	})
}

func (h *RealEstateHandler) UpdateListing(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.ParseInt(chi.URLParam(r, "id"), 10, 64)
	l, err := h.repo.GetListing(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
		return
	}
	if err := json.NewDecoder(r.Body).Decode(l); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	l.ID = id
	if err := h.repo.UpdateListing(r.Context(), l); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, l)
}

func (h *RealEstateHandler) DeleteListing(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.ParseInt(chi.URLParam(r, "id"), 10, 64)
	if err := h.repo.DeleteListing(r.Context(), id); err != nil {
		http.Error(w, `{"error":"delete failed"}`, http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

func (h *RealEstateHandler) ListListings(w http.ResponseWriter, r *http.Request) {
	q := r.URL.Query()
	filters := map[string]string{
		"category_id": q.Get("category_id"),
		"type_id":     q.Get("type_id"),
		"city":        q.Get("city"),
		"district":    q.Get("district"),
		"min_price":   q.Get("min_price"),
		"max_price":   q.Get("max_price"),
		"room_count":  q.Get("room_count"),
		"status":      q.Get("status"),
		"sort_by":     q.Get("sort_by"),
	}
	page, _ := strconv.Atoi(q.Get("page"))
	if page < 1 {
		page = 1
	}
	limit, _ := strconv.Atoi(q.Get("limit"))
	if limit < 1 || limit > 100 {
		limit = 20
	}
	list, err := h.repo.ListListings(r.Context(), filters, page, limit)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *RealEstateHandler) IncrementViewCount(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.ParseInt(chi.URLParam(r, "id"), 10, 64)
	if err := h.repo.IncrementViewCount(r.Context(), id); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": "ok"})
}

func (h *RealEstateHandler) SearchListings(w http.ResponseWriter, r *http.Request) {
	q := r.URL.Query().Get("q")
	page, _ := strconv.Atoi(r.URL.Query().Get("page"))
	if page < 1 {
		page = 1
	}
	limit, _ := strconv.Atoi(r.URL.Query().Get("limit"))
	if limit < 1 || limit > 100 {
		limit = 20
	}
	list, err := h.repo.SearchListings(r.Context(), q, page, limit)
	if err != nil {
		http.Error(w, `{"error":"search failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

// ── Property Photo ────────────────────────────────────────

func (h *RealEstateHandler) AddPhoto(w http.ResponseWriter, r *http.Request) {
	var p domain.PropertyPhoto
	if err := json.NewDecoder(r.Body).Decode(&p); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.AddPhoto(r.Context(), &p); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, p)
}

func (h *RealEstateHandler) ListPhotos(w http.ResponseWriter, r *http.Request) {
	listingID, _ := strconv.ParseInt(chi.URLParam(r, "listing_id"), 10, 64)
	list, err := h.repo.ListPhotos(r.Context(), listingID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *RealEstateHandler) DeletePhoto(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.ParseInt(chi.URLParam(r, "id"), 10, 64)
	if err := h.repo.DeletePhoto(r.Context(), id); err != nil {
		http.Error(w, `{"error":"delete failed"}`, http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

func (h *RealEstateHandler) SetCoverPhoto(w http.ResponseWriter, r *http.Request) {
	listingID, _ := strconv.ParseInt(chi.URLParam(r, "listing_id"), 10, 64)
	photoID, _ := strconv.ParseInt(chi.URLParam(r, "photo_id"), 10, 64)
	if err := h.repo.SetCoverPhoto(r.Context(), listingID, photoID); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": "ok"})
}

// ── Property Feature ──────────────────────────────────────

func (h *RealEstateHandler) CreateFeature(w http.ResponseWriter, r *http.Request) {
	var f domain.PropertyFeature
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

func (h *RealEstateHandler) ListFeatures(w http.ResponseWriter, r *http.Request) {
	list, err := h.repo.ListFeatures(r.Context())
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *RealEstateHandler) AddListingFeatures(w http.ResponseWriter, r *http.Request) {
	listingID, _ := strconv.ParseInt(chi.URLParam(r, "listing_id"), 10, 64)
	var features []domain.PropertyListingFeature
	if err := json.NewDecoder(r.Body).Decode(&features); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.AddListingFeatures(r.Context(), listingID, features); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": "ok"})
}

func (h *RealEstateHandler) GetListingFeatures(w http.ResponseWriter, r *http.Request) {
	listingID, _ := strconv.ParseInt(chi.URLParam(r, "listing_id"), 10, 64)
	list, err := h.repo.GetListingFeatures(r.Context(), listingID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *RealEstateHandler) RemoveListingFeature(w http.ResponseWriter, r *http.Request) {
	listingID, _ := strconv.ParseInt(chi.URLParam(r, "listing_id"), 10, 64)
	featureID, _ := strconv.Atoi(chi.URLParam(r, "feature_id"))
	if err := h.repo.RemoveListingFeature(r.Context(), listingID, featureID); err != nil {
		http.Error(w, `{"error":"delete failed"}`, http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

// ── Authorization Request ─────────────────────────────────

func (h *RealEstateHandler) CreateAuthorization(w http.ResponseWriter, r *http.Request) {
	var a domain.AuthorizationRequest
	if err := json.NewDecoder(r.Body).Decode(&a); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateAuthorization(r.Context(), &a); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, a)
}

func (h *RealEstateHandler) ListAuthorizations(w http.ResponseWriter, r *http.Request) {
	listingID, _ := strconv.ParseInt(chi.URLParam(r, "listing_id"), 10, 64)
	list, err := h.repo.ListAuthorizations(r.Context(), listingID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *RealEstateHandler) UpdateAuthorizationStatus(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.ParseInt(chi.URLParam(r, "id"), 10, 64)
	var body struct {
		Status string `json:"status"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateAuthorizationStatus(r.Context(), id, body.Status); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": body.Status})
}

// ── Property Appraisal Request ────────────────────────────

func (h *RealEstateHandler) CreateAppraisalRequest(w http.ResponseWriter, r *http.Request) {
	var a domain.PropertyAppraisalRequest
	a.Status = "pending"
	a.RequestedDate = &[]time.Time{time.Now()}[0]
	if err := json.NewDecoder(r.Body).Decode(&a); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateAppraisalRequest(r.Context(), &a); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, a)
}

func (h *RealEstateHandler) GetAppraisalRequest(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.ParseInt(chi.URLParam(r, "id"), 10, 64)
	a, err := h.repo.GetAppraisalRequest(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
		return
	}
	writeJSON(w, http.StatusOK, a)
}

func (h *RealEstateHandler) ListAppraisalRequests(w http.ResponseWriter, r *http.Request) {
	userID := r.URL.Query().Get("user_id")
	list, err := h.repo.ListAppraisalRequests(r.Context(), userID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *RealEstateHandler) UpdateAppraisalStatus(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.ParseInt(chi.URLParam(r, "id"), 10, 64)
	var body struct {
		Status string `json:"status"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateAppraisalStatus(r.Context(), id, body.Status); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": body.Status})
}

// ── Favorite Listing ──────────────────────────────────────

func (h *RealEstateHandler) AddFavorite(w http.ResponseWriter, r *http.Request) {
	var body struct {
		UserID    string `json:"user_id"`
		ListingID int64  `json:"listing_id"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.AddFavorite(r.Context(), body.UserID, body.ListingID); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, map[string]string{"status": "added"})
}

func (h *RealEstateHandler) RemoveFavorite(w http.ResponseWriter, r *http.Request) {
	userID := chi.URLParam(r, "user_id")
	listingID, _ := strconv.ParseInt(chi.URLParam(r, "listing_id"), 10, 64)
	if err := h.repo.RemoveFavorite(r.Context(), userID, listingID); err != nil {
		http.Error(w, `{"error":"delete failed"}`, http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

func (h *RealEstateHandler) ListFavorites(w http.ResponseWriter, r *http.Request) {
	userID := chi.URLParam(r, "user_id")
	list, err := h.repo.ListFavorites(r.Context(), userID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *RealEstateHandler) IsFavorite(w http.ResponseWriter, r *http.Request) {
	userID := chi.URLParam(r, "user_id")
	listingID, _ := strconv.ParseInt(chi.URLParam(r, "listing_id"), 10, 64)
	exists, err := h.repo.IsFavorite(r.Context(), userID, listingID)
	if err != nil {
		http.Error(w, `{"error":"check failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]bool{"favorite": exists})
}

// ── Property Inquiry ──────────────────────────────────────

func (h *RealEstateHandler) SendInquiry(w http.ResponseWriter, r *http.Request) {
	var inq domain.PropertyInquiry
	if err := json.NewDecoder(r.Body).Decode(&inq); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.SendInquiry(r.Context(), &inq); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, inq)
}

func (h *RealEstateHandler) ListInquiriesByListing(w http.ResponseWriter, r *http.Request) {
	listingID, _ := strconv.ParseInt(chi.URLParam(r, "listing_id"), 10, 64)
	list, err := h.repo.ListInquiriesByListing(r.Context(), listingID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *RealEstateHandler) ListInquiriesByUser(w http.ResponseWriter, r *http.Request) {
	userID := chi.URLParam(r, "user_id")
	list, err := h.repo.ListInquiriesByUser(r.Context(), userID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *RealEstateHandler) MarkAsRead(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.ParseInt(chi.URLParam(r, "id"), 10, 64)
	if err := h.repo.MarkAsRead(r.Context(), id); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": "read"})
}

// ── Company Member ──────────────────────────────────────────

func (h *RealEstateHandler) AddMember(w http.ResponseWriter, r *http.Request) {
	var m domain.CompanyMember
	if err := json.NewDecoder(r.Body).Decode(&m); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateMember(r.Context(), &m); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, m)
}

func (h *RealEstateHandler) ListMembers(w http.ResponseWriter, r *http.Request) {
	companyID, _ := strconv.Atoi(chi.URLParam(r, "company_id"))
	list, err := h.repo.ListMembers(r.Context(), companyID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *RealEstateHandler) UpdateMemberRole(w http.ResponseWriter, r *http.Request) {
	memberID, _ := strconv.Atoi(chi.URLParam(r, "member_id"))
	var body struct {
		Role  string `json:"role"`
		Title string `json:"title"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateMemberRole(r.Context(), memberID, body.Role, body.Title); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": "updated"})
}

func (h *RealEstateHandler) RemoveMember(w http.ResponseWriter, r *http.Request) {
	memberID, _ := strconv.Atoi(chi.URLParam(r, "member_id"))
	if err := h.repo.RemoveMember(r.Context(), memberID); err != nil {
		http.Error(w, `{"error":"delete failed"}`, http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

// ── Company Invitation ──────────────────────────────────────

func (h *RealEstateHandler) CreateInvitation(w http.ResponseWriter, r *http.Request) {
	var inv domain.CompanyInvitation
	inv.Status = "pending"
	if err := json.NewDecoder(r.Body).Decode(&inv); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateInvitation(r.Context(), &inv); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, inv)
}

func (h *RealEstateHandler) ListInvitations(w http.ResponseWriter, r *http.Request) {
	companyID, _ := strconv.Atoi(chi.URLParam(r, "company_id"))
	status := r.URL.Query().Get("status")
	list, err := h.repo.ListInvitations(r.Context(), companyID, status)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *RealEstateHandler) AcceptInvitation(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	if err := h.repo.UpdateInvitationStatus(r.Context(), id, "accepted"); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": "accepted"})
}

func (h *RealEstateHandler) RejectInvitation(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	if err := h.repo.UpdateInvitationStatus(r.Context(), id, "rejected"); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": "rejected"})
}

// ── User Companies ──────────────────────────────────────────

func (h *RealEstateHandler) ListMyCompanies(w http.ResponseWriter, r *http.Request) {
	userID := chi.URLParam(r, "user_id")
	list, err := h.repo.ListUserCompanies(r.Context(), userID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

// ── Paid Listing / Pricing ────────────────────────────────────

func (h *RealEstateHandler) GetListingPrice(w http.ResponseWriter, r *http.Request) {
	domain := r.URL.Query().Get("domain")
	userRole := r.URL.Query().Get("user_role")
	if domain == "" {
		http.Error(w, `{"error":"domain required"}`, http.StatusBadRequest)
		return
	}
	p, err := h.repo.GetListingPrice(r.Context(), domain, userRole)
	if err != nil {
		http.Error(w, `{"error":"not found"}`, http.StatusNotFound)
		return
	}
	writeJSON(w, http.StatusOK, p)
}

func (h *RealEstateHandler) GetRegionBenchmark(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.ParseInt(chi.URLParam(r, "id"), 10, 64)
	b, err := h.repo.GetRegionBenchmark(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"benchmark failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, b)
}

func (h *RealEstateHandler) PayForListing(w http.ResponseWriter, r *http.Request) {
	listingID, _ := strconv.ParseInt(chi.URLParam(r, "id"), 10, 64)
	var body struct {
		Domain        string  `json:"domain"`
		UserID        string  `json:"user_id"`
		Amount        float64 `json:"amount"`
		Currency      string  `json:"currency"`
		PaymentMethod string  `json:"payment_method"`
		PaymentRef    string  `json:"payment_ref"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	p := domain.ListingPayment{
		Domain:        body.Domain,
		ListingID:     listingID,
		UserID:        body.UserID,
		Amount:        body.Amount,
		Currency:      body.Currency,
		PaymentMethod: body.PaymentMethod,
		PaymentRef:    body.PaymentRef,
		Status:        "pending",
	}
	if err := h.repo.CreatePayment(r.Context(), &p); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, p)
}

func (h *RealEstateHandler) ListMyPayments(w http.ResponseWriter, r *http.Request) {
	userID := r.URL.Query().Get("user_id")
	domain := r.URL.Query().Get("domain")
	list, err := h.repo.ListUserPayments(r.Context(), userID, domain)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

// ── Document (Tapu / Ruhsat) Verification ────────────────

func (h *RealEstateHandler) UploadDocument(w http.ResponseWriter, r *http.Request) {
	listingID, _ := strconv.ParseInt(chi.URLParam(r, "id"), 10, 64)
	var d domain.ListingDocument
	d.Status = "pending"
	if err := json.NewDecoder(r.Body).Decode(&d); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	d.ListingID = listingID
	if err := h.repo.CreateDocument(r.Context(), &d); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, d)
}

func (h *RealEstateHandler) ListListingDocuments(w http.ResponseWriter, r *http.Request) {
	listingID, _ := strconv.ParseInt(chi.URLParam(r, "id"), 10, 64)
	domain := r.URL.Query().Get("domain")
	list, err := h.repo.ListDocuments(r.Context(), domain, listingID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *RealEstateHandler) SubmitForVerification(w http.ResponseWriter, r *http.Request) {
	listingID, _ := strconv.ParseInt(chi.URLParam(r, "id"), 10, 64)
	var body struct {
		Domain string `json:"domain"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	docs, err := h.repo.ListDocuments(r.Context(), body.Domain, listingID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	for _, d := range docs {
		_ = h.repo.UpdateDocumentStatus(r.Context(), d.ID, "pending_verification", "", "")
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": "submitted"})
}

func (h *RealEstateHandler) VerifyDocument(w http.ResponseWriter, r *http.Request) {
	docID, _ := strconv.ParseInt(chi.URLParam(r, "doc_id"), 10, 64)
	var body struct {
		VerifiedBy string `json:"verified_by"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateDocumentStatus(r.Context(), docID, "verified", "", body.VerifiedBy); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	if err := h.repo.CreateVerificationRecord(r.Context(), docID, body.VerifiedBy, "verify", ""); err != nil {
		http.Error(w, `{"error":"record failed"}`, http.StatusInternalServerError)
		return
	}
	doc, err := h.repo.GetDocument(r.Context(), docID)
	if err == nil {
		count, _ := h.repo.CountVerifiedDocuments(r.Context(), doc.ListingID, doc.Domain)
		if count >= 2 {
			_ = h.repo.UpdateListingStatus(r.Context(), doc.ListingID, "verified")
		}
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": "verified"})
}

func (h *RealEstateHandler) RejectDocument(w http.ResponseWriter, r *http.Request) {
	docID, _ := strconv.ParseInt(chi.URLParam(r, "doc_id"), 10, 64)
	var body struct {
		VerifiedBy      string `json:"verified_by"`
		RejectionReason string `json:"rejection_reason"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateDocumentStatus(r.Context(), docID, "rejected", body.RejectionReason, body.VerifiedBy); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	if err := h.repo.CreateVerificationRecord(r.Context(), docID, body.VerifiedBy, "reject", body.RejectionReason); err != nil {
		http.Error(w, `{"error":"record failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": "rejected"})
}

func (h *RealEstateHandler) ListMyDocuments(w http.ResponseWriter, r *http.Request) {
	userID := r.URL.Query().Get("user_id")
	domain := r.URL.Query().Get("domain")
	list, err := h.repo.ListUserDocuments(r.Context(), userID, domain)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

// ── Company Certification / Verification ──────────────────────

func (h *RealEstateHandler) UploadCompanyDocument(w http.ResponseWriter, r *http.Request) {
	companyID, _ := strconv.Atoi(chi.URLParam(r, "company_id"))
	var d domain.ListingDocument
	d.Status = "pending"
	if err := json.NewDecoder(r.Body).Decode(&d); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	d.CompanyID = &companyID
	d.IsCompanyDoc = true
	if err := h.repo.CreateCompanyDocument(r.Context(), &d); err != nil {
		http.Error(w, `{"error":"create failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, d)
}

func (h *RealEstateHandler) ListCompanyDocuments(w http.ResponseWriter, r *http.Request) {
	companyID, _ := strconv.Atoi(chi.URLParam(r, "company_id"))
	list, err := h.repo.ListCompanyDocuments(r.Context(), companyID)
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}

func (h *RealEstateHandler) SubmitCompanyForVerification(w http.ResponseWriter, r *http.Request) {
	companyID, _ := strconv.Atoi(chi.URLParam(r, "company_id"))
	if err := h.repo.UpdateCompanyVerification(r.Context(), companyID, "pending", "", ""); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": "submitted"})
}

func (h *RealEstateHandler) VerifyCompany(w http.ResponseWriter, r *http.Request) {
	companyID, _ := strconv.Atoi(chi.URLParam(r, "company_id"))
	var body struct {
		VerifiedBy string `json:"verified_by"`
		Note       string `json:"note"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateCompanyVerification(r.Context(), companyID, "approved", body.Note, body.VerifiedBy); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": "approved"})
}

func (h *RealEstateHandler) RejectCompanyVerification(w http.ResponseWriter, r *http.Request) {
	companyID, _ := strconv.Atoi(chi.URLParam(r, "company_id"))
	var body struct {
		VerifiedBy string `json:"verified_by"`
		Note       string `json:"note"`
	}
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
		http.Error(w, `{"error":"invalid request"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateCompanyVerification(r.Context(), companyID, "rejected", body.Note, body.VerifiedBy); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": "rejected"})
}

func (h *RealEstateHandler) ListPendingCompanies(w http.ResponseWriter, r *http.Request) {
	list, err := h.repo.GetPendingVerificationCompanies(r.Context())
	if err != nil {
		http.Error(w, `{"error":"list failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, list)
}
