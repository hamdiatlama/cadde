package domain

import "time"

type FloristProfile struct {
	ID                  int        `json:"id"`
	SellerID            *int       `json:"seller_id,omitempty"`
	UserID              int        `json:"user_id"`
	ShopName            string     `json:"shop_name"`
	Slug                string     `json:"slug"`
	Description         *string    `json:"description,omitempty"`
	LogoURL             *string    `json:"logo_url,omitempty"`
	CoverURL            *string    `json:"cover_url,omitempty"`
	Phone               *string    `json:"phone,omitempty"`
	City                *string    `json:"city,omitempty"`
	District            *string    `json:"district,omitempty"`
	Address             *string    `json:"address,omitempty"`
	Latitude            *float64   `json:"latitude,omitempty"`
	Longitude           *float64   `json:"longitude,omitempty"`
	IsActive            bool       `json:"is_active"`
	IsOpen              bool       `json:"is_open"`
	PreparationTimeMin  int        `json:"preparation_time_min"`
	DeliveryRadiusKm    float64    `json:"delivery_radius_km"`
	MinOrderAmount      float64    `json:"min_order_amount"`
	DeliveryFee         float64    `json:"delivery_fee"`
	VerificationStatus  string     `json:"verification_status"`
	Rating              float64    `json:"rating"`
	ReviewCount         int        `json:"review_count"`
	TotalScore          int        `json:"total_score"`
	CreatedAt           time.Time  `json:"created_at"`
}

type FlowerProduct struct {
	ID               int        `json:"id"`
	SellerType       string     `json:"seller_type"`
	SellerID         int        `json:"seller_id"`
	Name             string     `json:"name"`
	Slug             *string    `json:"slug,omitempty"`
	Description      *string    `json:"description,omitempty"`
	Category         *string    `json:"category,omitempty"`
	Subcategory      *string    `json:"subcategory,omitempty"`
	Occasion         *string    `json:"occasion,omitempty"`
	Price            float64    `json:"price"`
	Stock            int        `json:"stock"`
	Size             *string    `json:"size,omitempty"`
	Color            *string    `json:"color,omitempty"`
	IsActive         bool       `json:"is_active"`
	IsExpressEligible bool      `json:"is_express_eligible"`
	IsCustomizable   bool       `json:"is_customizable"`
	ImagesJSON       *string    `json:"images_json,omitempty"`
	Rating           float64    `json:"rating"`
	ReviewCount      int        `json:"review_count"`
	CreatedAt        time.Time  `json:"created_at"`
}

type SpecialDayReminder struct {
	ID              int        `json:"id"`
	UserID          int        `json:"user_id"`
	Name            string     `json:"name"`
	ReminderDate    string     `json:"reminder_date"`
	OccasionType    *string    `json:"occasion_type,omitempty"`
	IsYearly        bool       `json:"is_yearly"`
	IsActive        bool       `json:"is_active"`
	CreatedAt       time.Time  `json:"created_at"`
}

type FloristImage struct {
	ID                int        `json:"id"`
	FloristID         int        `json:"florist_id"`
	Category          string     `json:"category"`
	FilePath          string     `json:"file_path"`
	Resolution        *string    `json:"resolution,omitempty"`
	IsActive          bool       `json:"is_active"`
	ScoreContribution int        `json:"score_contribution"`
	CreatedAt         time.Time  `json:"created_at"`
}

type FloristCamera struct {
	ID                     int        `json:"id"`
	FloristID              int        `json:"florist_id"`
	CameraName             *string    `json:"camera_name,omitempty"`
	Resolution             *string    `json:"resolution,omitempty"`
	StreamURL              *string    `json:"stream_url,omitempty"`
	IsActive               bool       `json:"is_active"`
	ScoreContribution      int        `json:"score_contribution"`
	CreatedAt              time.Time  `json:"created_at"`
}

type FloristDocumentScore struct {
	ID            int        `json:"id"`
	FloristID     int        `json:"florist_id"`
	DocumentType  string     `json:"document_type"`
	Score         int        `json:"score"`
	FilePath      *string    `json:"file_path,omitempty"`
	IsConfirmed   bool       `json:"is_confirmed"`
	IsActive      bool       `json:"is_active"`
	CreatedAt     time.Time  `json:"created_at"`
}
