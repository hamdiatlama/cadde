package handler

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strconv"
	"time"

	"github.com/go-chi/chi/v5"
	"github.com/web-platform/backend/internal/api/middleware"
	"github.com/web-platform/backend/internal/domain"
	"github.com/web-platform/backend/internal/repository/postgres"
)

type EventHandler struct {
	repo *postgres.EventRepo
}

func NewEventHandler(repo *postgres.EventRepo) *EventHandler {
	return &EventHandler{repo: repo}
}

func (h *EventHandler) CreateVenue(w http.ResponseWriter, r *http.Request) {
	var v domain.Venue
	if err := json.NewDecoder(r.Body).Decode(&v); err != nil {
		http.Error(w, `{"error":"invalid request body"}`, http.StatusBadRequest)
		return
	}
	if v.Name == "" || v.City == "" {
		http.Error(w, `{"error":"name and city are required"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateVenue(r.Context(), &v); err != nil {
		http.Error(w, `{"error":"create venue failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, v)
}

func (h *EventHandler) ListVenues(w http.ResponseWriter, r *http.Request) {
	venues, err := h.repo.ListVenues(r.Context())
	if err != nil {
		http.Error(w, `{"error":"list venues failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, venues)
}

func (h *EventHandler) GetVenue(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	venue, err := h.repo.GetVenue(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"venue not found"}`, http.StatusNotFound)
		return
	}
	writeJSON(w, http.StatusOK, venue)
}

func (h *EventHandler) DeleteVenue(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	if err := h.repo.DeleteVenue(r.Context(), id); err != nil {
		http.Error(w, `{"error":"delete venue failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": "deleted"})
}

func (h *EventHandler) CreateVenueSection(w http.ResponseWriter, r *http.Request) {
	venueID, _ := strconv.Atoi(chi.URLParam(r, "id"))
	var vs domain.VenueSection
	if err := json.NewDecoder(r.Body).Decode(&vs); err != nil {
		http.Error(w, `{"error":"invalid request body"}`, http.StatusBadRequest)
		return
	}
	vs.VenueID = venueID
	if err := h.repo.CreateVenueSection(r.Context(), &vs); err != nil {
		http.Error(w, `{"error":"create section failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, vs)
}

func (h *EventHandler) ListVenueSections(w http.ResponseWriter, r *http.Request) {
	venueID, _ := strconv.Atoi(chi.URLParam(r, "id"))
	sections, err := h.repo.ListVenueSections(r.Context(), venueID)
	if err != nil {
		http.Error(w, `{"error":"list sections failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, sections)
}

func (h *EventHandler) CreateEvent(w http.ResponseWriter, r *http.Request) {
	var e domain.Event
	if err := json.NewDecoder(r.Body).Decode(&e); err != nil {
		http.Error(w, `{"error":"invalid request body"}`, http.StatusBadRequest)
		return
	}
	if e.Title == "" || e.Category == "" || e.VenueID == 0 {
		http.Error(w, `{"error":"title, category, and venue_id are required"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.CreateEvent(r.Context(), &e); err != nil {
		http.Error(w, `{"error":"create event failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, e)
}

func (h *EventHandler) ListEvents(w http.ResponseWriter, r *http.Request) {
	var category, venueType *string
	var venueID *int
	if c := r.URL.Query().Get("category"); c != "" {
		category = &c
	}
	if v := r.URL.Query().Get("venue_id"); v != "" {
		if val, err := strconv.Atoi(v); err == nil {
			venueID = &val
		}
	}
	if vt := r.URL.Query().Get("venue_type"); vt != "" {
		venueType = &vt
	}
	events, err := h.repo.ListEvents(r.Context(), category, venueID, venueType)
	if err != nil {
		http.Error(w, `{"error":"list events failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, events)
}

func (h *EventHandler) GetEvent(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	event, err := h.repo.GetEvent(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"event not found"}`, http.StatusNotFound)
		return
	}
	writeJSON(w, http.StatusOK, event)
}

func (h *EventHandler) UpdateEventStatus(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	var req struct {
		Status string `json:"status"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil || req.Status == "" {
		http.Error(w, `{"error":"status is required"}`, http.StatusBadRequest)
		return
	}
	if err := h.repo.UpdateEventStatus(r.Context(), id, req.Status); err != nil {
		http.Error(w, `{"error":"update status failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]interface{}{"id": id, "status": req.Status})
}

func (h *EventHandler) DeleteEvent(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	if err := h.repo.DeleteEvent(r.Context(), id); err != nil {
		http.Error(w, `{"error":"delete event failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": "deleted"})
}

func (h *EventHandler) CreateEventSession(w http.ResponseWriter, r *http.Request) {
	eventID, _ := strconv.Atoi(chi.URLParam(r, "id"))
	var s domain.EventSession
	if err := json.NewDecoder(r.Body).Decode(&s); err != nil {
		http.Error(w, `{"error":"invalid request body"}`, http.StatusBadRequest)
		return
	}
	s.EventID = eventID
	if err := h.repo.CreateEventSession(r.Context(), &s); err != nil {
		http.Error(w, `{"error":"create session failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, s)
}

func (h *EventHandler) ListEventSessions(w http.ResponseWriter, r *http.Request) {
	eventID, _ := strconv.Atoi(chi.URLParam(r, "id"))
	sessions, err := h.repo.ListEventSessions(r.Context(), eventID)
	if err != nil {
		http.Error(w, `{"error":"list sessions failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, sessions)
}

func (h *EventHandler) CreateSessionPricing(w http.ResponseWriter, r *http.Request) {
	sessionID, _ := strconv.Atoi(chi.URLParam(r, "id"))
	var sp domain.SessionPricing
	if err := json.NewDecoder(r.Body).Decode(&sp); err != nil {
		http.Error(w, `{"error":"invalid request body"}`, http.StatusBadRequest)
		return
	}
	sp.SessionID = sessionID
	if err := h.repo.CreateSessionPricing(r.Context(), &sp); err != nil {
		http.Error(w, `{"error":"create pricing failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, sp)
}

func (h *EventHandler) ListSessionPricing(w http.ResponseWriter, r *http.Request) {
	sessionID, _ := strconv.Atoi(chi.URLParam(r, "id"))
	pricing, err := h.repo.ListSessionPricing(r.Context(), sessionID)
	if err != nil {
		http.Error(w, `{"error":"list pricing failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, pricing)
}

func (h *EventHandler) BulkCreateSeats(w http.ResponseWriter, r *http.Request) {
	var req struct {
		SectionID int            `json:"section_id"`
		Seats     []*domain.Seat `json:"seats"`
	}
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil || len(req.Seats) == 0 {
		http.Error(w, `{"error":"invalid request body"}`, http.StatusBadRequest)
		return
	}
	for _, s := range req.Seats {
		s.SectionID = req.SectionID
	}
	if err := h.repo.BulkCreateSeats(r.Context(), req.Seats); err != nil {
		http.Error(w, `{"error":"create seats failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusCreated, req.Seats)
}

func (h *EventHandler) GetAvailableSeats(w http.ResponseWriter, r *http.Request) {
	sessionID, _ := strconv.Atoi(chi.URLParam(r, "id"))
	sectionID, _ := strconv.Atoi(chi.URLParam(r, "sid"))
	seats, err := h.repo.GetAvailableSeats(r.Context(), sessionID, sectionID)
	if err != nil {
		http.Error(w, `{"error":"get available seats failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, seats)
}

type reserveRequest struct {
	SessionID int           `json:"session_id"`
	Currency  string        `json:"currency,omitempty"`
	Tickets   []ticketInput `json:"tickets"`
}

type ticketInput struct {
	SectionID int    `json:"section_id"`
	SeatID    *int   `json:"seat_id,omitempty"`
	SeatLabel string `json:"seat_label,omitempty"`
	Price     float64 `json:"price"`
}

func (h *EventHandler) Reserve(w http.ResponseWriter, r *http.Request) {
	userID, _ := r.Context().Value(middleware.UserIDKey).(int)

	var req reserveRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil || len(req.Tickets) == 0 {
		http.Error(w, `{"error":"invalid request body"}`, http.StatusBadRequest)
		return
	}
	if req.Currency == "" {
		req.Currency = "TRY"
	}

	var total float64
	for _, t := range req.Tickets {
		total += t.Price
	}

	booking := &domain.TicketBooking{
		UserID:      userID,
		SessionID:   req.SessionID,
		Status:      "pending",
		TotalAmount: total,
		Currency:    req.Currency,
	}
	if err := h.repo.CreateTicketBooking(r.Context(), booking); err != nil {
		http.Error(w, `{"error":"create booking failed"}`, http.StatusInternalServerError)
		return
	}

	barcodeGen := func() string {
		return fmt.Sprintf("TKT-%d-%d", booking.ID, time.Now().UnixNano())
	}

	var createdTickets []*domain.Ticket
	for _, ti := range req.Tickets {
		t := &domain.Ticket{
			BookingID: booking.ID,
			SessionID: req.SessionID,
			SectionID: ti.SectionID,
			SeatID:    ti.SeatID,
			SeatLabel: &ti.SeatLabel,
			Price:     ti.Price,
			Barcode:   barcodeGen(),
			Status:    "active",
		}
		if err := h.repo.CreateTicket(r.Context(), t); err != nil {
			http.Error(w, `{"error":"create ticket failed"}`, http.StatusInternalServerError)
			return
		}
		createdTickets = append(createdTickets, t)
	}

	writeJSON(w, http.StatusCreated, map[string]interface{}{
		"booking": booking,
		"tickets": createdTickets,
	})
}

func (h *EventHandler) GetTicketBooking(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	userID, _ := r.Context().Value(middleware.UserIDKey).(int)
	role, _ := r.Context().Value(middleware.UserRoleKey).(string)

	booking, err := h.repo.GetTicketBooking(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"booking not found"}`, http.StatusNotFound)
		return
	}
	if booking.UserID != userID && role != "admin" {
		http.Error(w, `{"error":"access denied"}`, http.StatusForbidden)
		return
	}

	tickets, err := h.repo.ListTicketsByBooking(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"list tickets failed"}`, http.StatusInternalServerError)
		return
	}

	writeJSON(w, http.StatusOK, map[string]interface{}{
		"booking": booking,
		"tickets": tickets,
	})
}

func (h *EventHandler) ListUserBookings(w http.ResponseWriter, r *http.Request) {
	userID, _ := r.Context().Value(middleware.UserIDKey).(int)
	bookings, err := h.repo.ListUserBookings(r.Context(), userID)
	if err != nil {
		http.Error(w, `{"error":"list bookings failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, bookings)
}

func (h *EventHandler) ConfirmBooking(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	userID, _ := r.Context().Value(middleware.UserIDKey).(int)
	role, _ := r.Context().Value(middleware.UserRoleKey).(string)

	booking, err := h.repo.GetTicketBooking(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"booking not found"}`, http.StatusNotFound)
		return
	}
	if booking.UserID != userID && role != "admin" {
		http.Error(w, `{"error":"access denied"}`, http.StatusForbidden)
		return
	}

	now := time.Now()
	if err := h.repo.UpdateBookingStatus(r.Context(), id, "confirmed", &now, nil); err != nil {
		http.Error(w, `{"error":"confirm booking failed"}`, http.StatusInternalServerError)
		return
	}
	writeJSON(w, http.StatusOK, map[string]interface{}{"id": id, "status": "confirmed"})
}

func (h *EventHandler) CancelBooking(w http.ResponseWriter, r *http.Request) {
	id, _ := strconv.Atoi(chi.URLParam(r, "id"))
	userID, _ := r.Context().Value(middleware.UserIDKey).(int)
	role, _ := r.Context().Value(middleware.UserRoleKey).(string)

	booking, err := h.repo.GetTicketBooking(r.Context(), id)
	if err != nil {
		http.Error(w, `{"error":"booking not found"}`, http.StatusNotFound)
		return
	}
	if booking.UserID != userID && role != "admin" {
		http.Error(w, `{"error":"access denied"}`, http.StatusForbidden)
		return
	}

	now := time.Now()
	if err := h.repo.UpdateBookingStatus(r.Context(), id, "cancelled", nil, &now); err != nil {
		http.Error(w, `{"error":"cancel booking failed"}`, http.StatusInternalServerError)
		return
	}

	tickets, err := h.repo.ListTicketsByBooking(r.Context(), id)
	if err == nil {
		for _, t := range tickets {
			_ = h.repo.UpdateTicketStatus(r.Context(), t.ID, "cancelled", nil)
		}
	}

	writeJSON(w, http.StatusOK, map[string]interface{}{"id": id, "status": "cancelled"})
}
