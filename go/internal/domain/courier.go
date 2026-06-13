package domain

import "time"

type Courier struct {
	ID                  int        `json:"id"`
	UserID              int        `json:"user_id"`
	VehicleType         string     `json:"vehicle_type"` // bike, motorcycle, car
	PlateNumber         string     `json:"plate_number,omitempty"`
	IsAvailable         bool       `json:"is_available"`
	Status              string     `json:"status"` // online, offline, busy
	CurrentLatitude     *float64   `json:"current_latitude,omitempty"`
	CurrentLongitude    *float64   `json:"current_longitude,omitempty"`
	CurrentSpeedKmh     float64    `json:"current_speed_kmh,omitempty"`
	CurrentHeading      float64    `json:"current_heading,omitempty"`
	LastLocationUpdate  *time.Time `json:"last_location_update,omitempty"`
	Rating              float64    `json:"rating"`
	TotalDeliveries     int        `json:"total_deliveries"`
	GPSPpoofingScore    float64    `json:"gps_spoofing_score,omitempty"`
	ConsecutiveAnomalies int       `json:"consecutive_anomalies,omitempty"`
	CreatedAt           time.Time  `json:"created_at"`
}

type LocationHistory struct {
	ID        int       `json:"id"`
	CourierID int       `json:"courier_id"`
	OrderID   *int      `json:"order_id,omitempty"`
	Latitude  float64   `json:"latitude"`
	Longitude float64   `json:"longitude"`
	SpeedKmh  float64   `json:"speed_kmh,omitempty"`
	Heading   float64   `json:"heading,omitempty"`
	CreatedAt time.Time `json:"created_at"`
}

type CourierShift struct {
	ID              int        `json:"id"`
	CourierID       int        `json:"courier_id"`
	StartedAt       time.Time  `json:"started_at"`
	EndedAt         *time.Time `json:"ended_at,omitempty"`
	OrdersCompleted int        `json:"orders_completed"`
	TotalEarned     float64    `json:"total_earned,omitempty"`
}

type Earning struct {
	ID          int       `json:"id"`
	CourierID   int       `json:"courier_id"`
	OrderID     int       `json:"order_id"`
	Amount      float64   `json:"amount"`
	CreatedAt   time.Time `json:"created_at"`
}
