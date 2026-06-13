package domain

import "time"

type SupportTicket struct {
	ID         int        `json:"id"`
	UserID     int        `json:"user_id"`
	OrderID    *int       `json:"order_id,omitempty"`
	Subject    string     `json:"subject"`
	Category   string     `json:"category"`
	Status     string     `json:"status"`
	Priority   string     `json:"priority"`
	CreatedAt  time.Time  `json:"created_at"`
	UpdatedAt  *time.Time `json:"updated_at,omitempty"`
	ResolvedAt *time.Time `json:"resolved_at,omitempty"`
	Messages   []TicketMessage `json:"messages,omitempty"`
}

type TicketMessage struct {
	ID        int       `json:"id"`
	TicketID  int       `json:"ticket_id"`
	SenderID  int       `json:"sender_id"`
	Message   string    `json:"message"`
	IsStaff   bool      `json:"is_staff"`
	CreatedAt time.Time `json:"created_at"`
}
