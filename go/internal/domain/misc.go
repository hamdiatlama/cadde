package domain

import "time"

type WishlistItem struct {
	ID        int       `json:"id"`
	UserID    int       `json:"user_id"`
	ProductID int       `json:"product_id"`
	CreatedAt time.Time `json:"created_at"`
}

type Comment struct {
	ID        int       `json:"id"`
	UserID    int       `json:"user_id"`
	ProductID int       `json:"product_id"`
	Text      string    `json:"text"`
	Rating    int       `json:"rating"`
	CreatedAt time.Time `json:"created_at"`
}

type Notification struct {
	ID            int       `json:"id"`
	UserID        int       `json:"user_id"`
	Type          string    `json:"type"`
	Title         string    `json:"title"`
	Body          string    `json:"body"`
	ReferenceType string    `json:"reference_type,omitempty"`
	ReferenceID   int       `json:"reference_id,omitempty"`
	IsRead        bool      `json:"is_read"`
	CreatedAt     time.Time `json:"created_at"`
}

type PaymentTransaction struct {
	ID          int       `json:"id"`
	UserID      int       `json:"user_id"`
	OrderID     *int      `json:"order_id,omitempty"`
	Amount      float64   `json:"amount"`
	Type        string    `json:"type"`
	Method      string    `json:"method"`
	Status      string    `json:"status"`
	CreatedAt   time.Time `json:"created_at"`
}

type PointsTransaction struct {
	ID          int       `json:"id"`
	UserID      int       `json:"user_id"`
	OrderID     *int      `json:"order_id,omitempty"`
	Points      int       `json:"points"`
	Type        string    `json:"type"`
	Description string    `json:"description,omitempty"`
	CreatedAt   time.Time `json:"created_at"`
}

type Campaign struct {
	ID          int       `json:"id"`
	SellerID    int       `json:"seller_id"`
	Title       string    `json:"title"`
	Description string    `json:"description,omitempty"`
	DiscountPct float64   `json:"discount_pct"`
	StartAt     time.Time `json:"start_at"`
	EndAt       time.Time `json:"end_at"`
	IsActive    bool      `json:"is_active"`
	CreatedAt   time.Time `json:"created_at"`
}
