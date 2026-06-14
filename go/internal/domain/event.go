package domain

import "time"

type Venue struct {
	ID        int       `json:"id"`
	Name      string    `json:"name"`
	City      string    `json:"city"`
	District  *string   `json:"district,omitempty"`
	Address   *string   `json:"address,omitempty"`
	Latitude  *float64  `json:"latitude,omitempty"`
	Longitude *float64  `json:"longitude,omitempty"`
	Capacity  int       `json:"capacity"`
	Phone     *string   `json:"phone,omitempty"`
	VenueType string    `json:"venue_type"`
	CreatedAt time.Time `json:"created_at"`
}

type VenueSection struct {
	ID              int     `json:"id"`
	VenueID         int     `json:"venue_id"`
	Name            string  `json:"name"`
	Capacity        int     `json:"capacity"`
	PriceMultiplier float64 `json:"price_multiplier"`
}

type Event struct {
	ID          int        `json:"id"`
	Title       string     `json:"title"`
	Category    string     `json:"category"`
	VenueID     int        `json:"venue_id"`
	Description *string    `json:"description,omitempty"`
	PosterURL   *string    `json:"poster_url,omitempty"`
	MinAge      int        `json:"min_age"`
	Organizer   *string    `json:"organizer,omitempty"`
	Status      string     `json:"status"`
	CreatedAt   time.Time  `json:"created_at"`
	UpdatedAt   *time.Time `json:"updated_at,omitempty"`
}

type EventSession struct {
	ID        int        `json:"id"`
	EventID   int        `json:"event_id"`
	StartTime time.Time  `json:"start_time"`
	EndTime   *time.Time `json:"end_time,omitempty"`
	IsActive  bool       `json:"is_active"`
	WomenOnly bool       `json:"women_only"`
	CreatedAt time.Time  `json:"created_at"`
}

type SessionPricing struct {
	ID        int     `json:"id"`
	SessionID int     `json:"session_id"`
	SectionID int     `json:"section_id"`
	Price     float64 `json:"price"`
	Currency  string  `json:"currency"`
}

type Seat struct {
	ID         int    `json:"id"`
	SectionID  int    `json:"section_id"`
	RowLabel   *string `json:"row_label,omitempty"`
	SeatNumber *int   `json:"seat_number,omitempty"`
	IsActive   bool   `json:"is_active"`
}

type TicketBooking struct {
	ID          int        `json:"id"`
	UserID      int        `json:"user_id"`
	SessionID   int        `json:"session_id"`
	Status      string     `json:"status"`
	TotalAmount float64    `json:"total_amount"`
	Currency    string     `json:"currency"`
	PaidAt      *time.Time `json:"paid_at,omitempty"`
	CancelledAt *time.Time `json:"cancelled_at,omitempty"`
	CreatedAt   time.Time  `json:"created_at"`
}

type Ticket struct {
	ID        int        `json:"id"`
	BookingID int        `json:"booking_id"`
	SessionID int        `json:"session_id"`
	SectionID int        `json:"section_id"`
	SeatID    *int       `json:"seat_id,omitempty"`
	SeatLabel *string    `json:"seat_label,omitempty"`
	Price     float64    `json:"price"`
	Barcode   string     `json:"barcode"`
	Status    string     `json:"status"`
	UsedAt    *time.Time `json:"used_at,omitempty"`
	CreatedAt time.Time  `json:"created_at"`
}
