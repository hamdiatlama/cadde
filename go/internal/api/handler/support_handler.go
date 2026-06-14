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

type SupportHandler struct {
	repo *postgres.SupportRepo
}

func NewSupportHandler(repo *postgres.SupportRepo) *SupportHandler {
	return &SupportHandler{repo: repo}
}

type createTicketRequest struct {
	Subject  string `json:"subject"`
	Message  string `json:"message"`
	Category string `json:"category,omitempty"`
	OrderID  *int   `json:"order_id,omitempty"`
}

func (h *SupportHandler) Create(w http.ResponseWriter, r *http.Request) {
	var req createTicketRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, `{"error":"invalid request body"}`, http.StatusBadRequest)
		return
	}
	if req.Subject == "" || req.Message == "" {
		http.Error(w, `{"error":"subject and message are required"}`, http.StatusBadRequest)
		return
	}
	if req.Category == "" {
		req.Category = "other"
	}

	userID, _ := r.Context().Value(middleware.UserIDKey).(int)

	openCount, err := h.repo.CountOpenTickets(r.Context(), userID)
	if err == nil && openCount >= 2 {
		http.Error(w, `{"error":"En fazla 2 acik destek talebiniz olabilir"}`, http.StatusBadRequest)
		return
	}

	ticket := &domain.SupportTicket{
		UserID:   userID,
		OrderID:  req.OrderID,
		Subject:  req.Subject,
		Category: req.Category,
		Status:   "open",
		Priority: "normal",
	}
	if err := h.repo.CreateTicket(r.Context(), ticket); err != nil {
		http.Error(w, `{"error":"create ticket failed"}`, http.StatusInternalServerError)
		return
	}

	msg := &domain.TicketMessage{
		TicketID: ticket.ID,
		SenderID: userID,
		Message:  req.Message,
	}
	if err := h.repo.CreateMessage(r.Context(), msg); err != nil {
		http.Error(w, `{"error":"create message failed"}`, http.StatusInternalServerError)
		return
	}

	writeJSON(w, http.StatusCreated, map[string]interface{}{
		"id":         ticket.ID,
		"status":     ticket.Status,
		"subject":    ticket.Subject,
		"category":   ticket.Category,
		"created_at": ticket.CreatedAt,
	})
}

func (h *SupportHandler) ListMy(w http.ResponseWriter, r *http.Request) {
	userID, _ := r.Context().Value(middleware.UserIDKey).(int)
	tickets, err := h.repo.ListUserTickets(r.Context(), userID)
	if err != nil {
		http.Error(w, `{"error":"list tickets failed"}`, http.StatusInternalServerError)
		return
	}

	result := make([]map[string]interface{}, 0, len(tickets))
	for _, t := range tickets {
		lastMsg, _ := h.repo.GetLastMessage(r.Context(), t.ID)
		var preview string
		if lastMsg != nil {
			runes := []rune(lastMsg.Message)
			if len(runes) > 100 {
				preview = string(runes[:100])
			} else {
				preview = lastMsg.Message
			}
		}
		result = append(result, map[string]interface{}{
			"id":           t.ID,
			"subject":      t.Subject,
			"category":     t.Category,
			"status":       t.Status,
			"priority":     t.Priority,
			"order_id":     t.OrderID,
			"last_message": preview,
			"created_at":   t.CreatedAt,
		})
	}
	writeJSON(w, http.StatusOK, result)
}

func (h *SupportHandler) Get(w http.ResponseWriter, r *http.Request) {
	ticketID, _ := strconv.Atoi(chi.URLParam(r, "ticket_id"))
	userID, _ := r.Context().Value(middleware.UserIDKey).(int)
	role, _ := r.Context().Value(middleware.UserRoleKey).(string)

	ticket, err := h.repo.GetTicket(r.Context(), ticketID)
	if err != nil {
		http.Error(w, `{"error":"ticket not found"}`, http.StatusNotFound)
		return
	}

	if ticket.UserID != userID && role != "admin" {
		http.Error(w, `{"error":"access denied"}`, http.StatusForbidden)
		return
	}

	messages, err := h.repo.GetMessages(r.Context(), ticketID)
	if err != nil {
		http.Error(w, `{"error":"get messages failed"}`, http.StatusInternalServerError)
		return
	}

	msgList := make([]map[string]interface{}, 0, len(messages))
	for _, m := range messages {
		msgList = append(msgList, map[string]interface{}{
			"id":         m.ID,
			"sender_id":  m.SenderID,
			"message":    m.Message,
			"is_staff":   m.IsStaff,
			"created_at": m.CreatedAt,
		})
	}

	writeJSON(w, http.StatusOK, map[string]interface{}{
		"id":         ticket.ID,
		"subject":    ticket.Subject,
		"category":   ticket.Category,
		"status":     ticket.Status,
		"priority":   ticket.Priority,
		"order_id":   ticket.OrderID,
		"created_at": ticket.CreatedAt,
		"messages":   msgList,
	})
}

type addMessageRequest struct {
	Message string `json:"message"`
}

func (h *SupportHandler) AddMessage(w http.ResponseWriter, r *http.Request) {
	ticketID, _ := strconv.Atoi(chi.URLParam(r, "ticket_id"))
	userID, _ := r.Context().Value(middleware.UserIDKey).(int)
	role, _ := r.Context().Value(middleware.UserRoleKey).(string)

	var req addMessageRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil || req.Message == "" {
		http.Error(w, `{"error":"message is required"}`, http.StatusBadRequest)
		return
	}

	ticket, err := h.repo.GetTicket(r.Context(), ticketID)
	if err != nil {
		http.Error(w, `{"error":"ticket not found"}`, http.StatusNotFound)
		return
	}
	if ticket.UserID != userID && role != "admin" {
		http.Error(w, `{"error":"access denied"}`, http.StatusForbidden)
		return
	}

	msg := &domain.TicketMessage{
		TicketID: ticketID,
		SenderID: userID,
		Message:  req.Message,
		IsStaff:  role == "admin",
	}
	if err := h.repo.CreateMessage(r.Context(), msg); err != nil {
		http.Error(w, `{"error":"create message failed"}`, http.StatusInternalServerError)
		return
	}

	if ticket.Status == "open" {
		if err := h.repo.UpdateStatus(r.Context(), ticketID, "in_progress"); err != nil {
			http.Error(w, `{"error":"status update failed"}`, http.StatusInternalServerError)
			return
		}
	}

	writeJSON(w, http.StatusCreated, map[string]interface{}{
		"id":         msg.ID,
		"message":    msg.Message,
		"is_staff":   msg.IsStaff,
		"created_at": msg.CreatedAt,
	})
}

type updateStatusRequest struct {
	Status string `json:"status"`
}

func (h *SupportHandler) ListAll(w http.ResponseWriter, r *http.Request) {
	role, _ := r.Context().Value(middleware.UserRoleKey).(string)
	if role != "admin" {
		http.Error(w, `{"error":"admin only"}`, http.StatusForbidden)
		return
	}

	limit := 50
	offset := 0
	if l := r.URL.Query().Get("limit"); l != "" {
		if v, err := strconv.Atoi(l); err == nil && v > 0 {
			limit = v
		}
	}
	if o := r.URL.Query().Get("offset"); o != "" {
		if v, err := strconv.Atoi(o); err == nil && v >= 0 {
			offset = v
		}
	}

	tickets, err := h.repo.ListAllTickets(r.Context(), limit, offset)
	if err != nil {
		http.Error(w, `{"error":"list tickets failed"}`, http.StatusInternalServerError)
		return
	}

	result := make([]map[string]interface{}, 0, len(tickets))
	for _, t := range tickets {
		lastMsg, _ := h.repo.GetLastMessage(r.Context(), t.ID)
		var preview string
		if lastMsg != nil {
			runes := []rune(lastMsg.Message)
			if len(runes) > 100 {
				preview = string(runes[:100])
			} else {
				preview = lastMsg.Message
			}
		}
		result = append(result, map[string]interface{}{
			"id":           t.ID,
			"user_id":      t.UserID,
			"subject":      t.Subject,
			"category":     t.Category,
			"status":       t.Status,
			"priority":     t.Priority,
			"order_id":     t.OrderID,
			"last_message": preview,
			"created_at":   t.CreatedAt,
		})
	}
	writeJSON(w, http.StatusOK, result)
}

func (h *SupportHandler) UpdateStatus(w http.ResponseWriter, r *http.Request) {
	ticketID, _ := strconv.Atoi(chi.URLParam(r, "ticket_id"))
	role, _ := r.Context().Value(middleware.UserRoleKey).(string)

	if role != "admin" {
		http.Error(w, `{"error":"only admins can update status"}`, http.StatusForbidden)
		return
	}

	var req updateStatusRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil || req.Status == "" {
		http.Error(w, `{"error":"status is required"}`, http.StatusBadRequest)
		return
	}

	ticket, err := h.repo.GetTicket(r.Context(), ticketID)
	if err != nil {
		http.Error(w, `{"error":"ticket not found"}`, http.StatusNotFound)
		return
	}

	ticket.Status = req.Status
	if err := h.repo.UpdateStatus(r.Context(), ticketID, req.Status); err != nil {
		http.Error(w, `{"error":"update failed"}`, http.StatusInternalServerError)
		return
	}

	if req.Status == "resolved" {
		if err := h.repo.UpdateResolvedAt(r.Context(), ticketID); err != nil {
			http.Error(w, `{"error":"resolved_at update failed"}`, http.StatusInternalServerError)
			return
		}
	}

	writeJSON(w, http.StatusOK, map[string]interface{}{
		"id":     ticket.ID,
		"status": ticket.Status,
	})
}
