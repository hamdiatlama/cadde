package domain

import "time"

type Order struct {
	ID                 int        `json:"id"`
	UserID             int        `json:"user_id"`
	SellerID           int        `json:"seller_id"`
	CourierID          *int       `json:"courier_id,omitempty"`
	Status             string     `json:"status"`
	Subtotal           float64    `json:"subtotal"`
	DeliveryFee        float64    `json:"delivery_fee"`
	Discount           float64    `json:"discount"`
	Total              float64    `json:"total"`
	PaymentMethod      string     `json:"payment_method"`
	PaymentStatus      string     `json:"payment_status"`
	DeliveryAddress    string     `json:"delivery_address"`
	DeliveryLatitude   float64    `json:"delivery_latitude"`
	DeliveryLongitude  float64    `json:"delivery_longitude"`
	Notes              string     `json:"notes,omitempty"`
	EstimatedAt        *time.Time `json:"estimated_at,omitempty"`
	DeliveredAt        *time.Time `json:"delivered_at,omitempty"`
	CancelledAt        *time.Time `json:"cancelled_at,omitempty"`
	CancelReason       string     `json:"cancel_reason,omitempty"`
	CreatedAt          time.Time  `json:"created_at"`
	UpdatedAt          time.Time  `json:"updated_at"`

	Items []OrderItem `json:"items,omitempty"`
}

type OrderItem struct {
	ID        int     `json:"id"`
	OrderID   int     `json:"order_id"`
	ProductID int     `json:"product_id"`
	Name      string  `json:"name"`
	Price     float64 `json:"price"`
	Quantity  int     `json:"quantity"`
	ImageURL  string  `json:"image_url,omitempty"`
}

type Substitution struct {
	ID              int       `json:"id"`
	OrderID         int       `json:"order_id"`
	OriginalID      int       `json:"original_product_id"`
	SubstituteID    int       `json:"substitute_product_id"`
	Status          string    `json:"status"`
	CreatedAt       time.Time `json:"created_at"`
}

type OrderApproval struct {
	ID          int       `json:"id"`
	OrderID     int       `json:"order_id"`
	Status      string    `json:"status"` // pending, approved, rejected
	ExpiresAt   time.Time `json:"expires_at"`
	CreatedAt   time.Time `json:"created_at"`
}
