package domain

import "time"

type Ride struct {
	ID                 int        `json:"id"`
	CustomerID         int        `json:"customer_id"`
	DriverID           *int       `json:"driver_id,omitempty"`
	Status             string     `json:"status"`
	PickupAddress      string     `json:"pickup_address"`
	PickupLatitude     float64    `json:"pickup_latitude"`
	PickupLongitude    float64    `json:"pickup_longitude"`
	DropoffAddress     string     `json:"dropoff_address"`
	DropoffLatitude    float64    `json:"dropoff_latitude"`
	DropoffLongitude   float64    `json:"dropoff_longitude"`
	EstimatedFare      float64    `json:"estimated_fare"`
	ActualFare         *float64   `json:"actual_fare,omitempty"`
	SurgeMultiplier    float64    `json:"surge_multiplier"`
	OptimalDistanceKm  float64    `json:"optimal_distance_km"`
	EtaAtBooking       int        `json:"eta_at_booking"`
	PaymentMethod      string     `json:"payment_method"`
	Notes              string     `json:"notes,omitempty"`
	Rating             *int       `json:"rating,omitempty"`
	Feedback           string     `json:"feedback,omitempty"`
	StartedAt          *time.Time `json:"started_at,omitempty"`
	CompletedAt        *time.Time `json:"completed_at,omitempty"`
	CancelledAt        *time.Time `json:"cancelled_at,omitempty"`
	CancelReason       string     `json:"cancel_reason,omitempty"`
	CreatedAt          time.Time  `json:"created_at"`
	UpdatedAt          time.Time  `json:"updated_at"`
}

type Driver struct {
	ID                  int        `json:"id"`
	UserID              int        `json:"user_id"`
	VehicleType         string     `json:"vehicle_type"`
	PlateNumber         string     `json:"plate_number"`
	IsAvailable         bool       `json:"is_available"`
	Status              string     `json:"status"`
	CurrentLatitude     *float64   `json:"current_latitude,omitempty"`
	CurrentLongitude    *float64   `json:"current_longitude,omitempty"`
	Rating              float64    `json:"rating"`
	TotalRides          int        `json:"total_rides"`
	CreatedAt           time.Time  `json:"created_at"`
}
