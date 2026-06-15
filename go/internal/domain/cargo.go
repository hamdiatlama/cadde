package domain

import "time"

type CargoCompany struct {
	ID                 int        `json:"id"`
	UserID             int        `json:"user_id"`
	CompanyName        string     `json:"company_name"`
	Slug               string     `json:"slug"`
	TaxID              *string    `json:"tax_id,omitempty"`
	Phone              *string    `json:"phone,omitempty"`
	Email              *string    `json:"email,omitempty"`
	City               *string    `json:"city,omitempty"`
	District           *string    `json:"district,omitempty"`
	Address            *string    `json:"address,omitempty"`
	APIKey             *string    `json:"api_key,omitempty"`
	IsVerified         bool       `json:"is_verified"`
	VerificationStatus string     `json:"verification_status"`
	IsActive           bool       `json:"is_active"`
	Rating             float64    `json:"rating"`
	ShipmentCount      int        `json:"shipment_count"`
	CreatedAt          time.Time  `json:"created_at"`
}

type CargoShipment struct {
	ID                 int        `json:"id"`
	CompanyID          int        `json:"company_id"`
	TrackingNo         string     `json:"tracking_no"`
	SenderName         string     `json:"sender_name"`
	SenderCity         *string    `json:"sender_city,omitempty"`
	RecipientName      string     `json:"recipient_name"`
	RecipientCity      string     `json:"recipient_city"`
	RecipientAddress   string     `json:"recipient_address"`
	Status             string     `json:"status"`
	DeliveryCode       *string    `json:"delivery_code,omitempty"`
	IsFragile          bool       `json:"is_fragile"`
	SensitivityNote    *string    `json:"sensitivity_note,omitempty"`
	CreatedAt          time.Time  `json:"created_at"`
}

type CargoTracking struct {
	ID           int       `json:"id"`
	ShipmentID   int       `json:"shipment_id"`
	Status       string    `json:"status"`
	LocationName *string   `json:"location_name,omitempty"`
	Notes        *string   `json:"notes,omitempty"`
	CreatedAt    time.Time `json:"created_at"`
}

type CargoBranch struct {
	ID          int    `json:"id"`
	CompanyID   int    `json:"company_id"`
	BranchName  string `json:"branch_name"`
	City        string `json:"city"`
	District    *string `json:"district,omitempty"`
	Address     string `json:"address"`
	IsActive    bool   `json:"is_active"`
}

type CargoCourier struct {
	ID             int        `json:"id"`
	CompanyID      int        `json:"company_id"`
	FullName       string     `json:"full_name"`
	Phone          string     `json:"phone"`
	IsActive       bool       `json:"is_active"`
	IsAvailable    bool       `json:"is_available"`
	TotalDeliveries int       `json:"total_deliveries"`
	Rating         float64    `json:"rating"`
}
