package domain

import "time"

type VehicleCategory struct {
	ID        int       `json:"id"`
	Name      string    `json:"name"`
	Slug      string    `json:"slug"`
	ParentID  *int      `json:"parent_id,omitempty"`
	SortOrder int       `json:"sort_order"`
	CreatedAt time.Time `json:"created_at"`
}

type VehicleSegment struct {
	Code        string    `json:"code"`
	Name        string    `json:"name"`
	Description string    `json:"description,omitempty"`
	CreatedAt   time.Time `json:"created_at"`
}

type BodyType struct {
	ID        int       `json:"id"`
	Name      string    `json:"name"`
	Slug      string    `json:"slug"`
	CreatedAt time.Time `json:"created_at"`
}

type VehicleBrand struct {
	ID        int        `json:"id"`
	Name      string     `json:"name"`
	Slug      string     `json:"slug"`
	Country   string     `json:"country,omitempty"`
	LogoURL   *string    `json:"logo_url,omitempty"`
	IsActive  bool       `json:"is_active"`
	CreatedAt time.Time  `json:"created_at"`
}

type VehicleModel struct {
	ID              int       `json:"id"`
	BrandID         int       `json:"brand_id"`
	Name            string    `json:"name"`
	SegmentCode     *string   `json:"segment_code,omitempty"`
	ProductionStart *int      `json:"production_start,omitempty"`
	ProductionEnd   *int      `json:"production_end,omitempty"`
	IsActive        bool      `json:"is_active"`
	CreatedAt       time.Time `json:"created_at"`
}

type VehicleModelBodyType struct {
	ModelID    int `json:"model_id"`
	BodyTypeID int `json:"body_type_id"`
}

type VehicleCategoryModel struct {
	CategoryID int `json:"category_id"`
	ModelID    int `json:"model_id"`
}

type VehicleModelYear struct {
	ID            int        `json:"id"`
	ModelID       int        `json:"model_id"`
	Year          int        `json:"year"`
	TrimName      *string    `json:"trim_name,omitempty"`
	EngineVolume  *float64   `json:"engine_volume,omitempty"`
	Horsepower    *int       `json:"horsepower,omitempty"`
	FuelType      *string    `json:"fuel_type,omitempty"`
	Transmission  *string    `json:"transmission,omitempty"`
	CreatedAt     time.Time  `json:"created_at"`
}

type FeatureGroup struct {
	ID        int       `json:"id"`
	Name      string    `json:"name"`
	Slug      string    `json:"slug"`
	SortOrder int       `json:"sort_order"`
	CreatedAt time.Time `json:"created_at"`
}

type Feature struct {
	ID      int       `json:"id"`
	GroupID int       `json:"group_id"`
	Name    string    `json:"name"`
	Slug    string    `json:"slug"`
	CreatedAt time.Time `json:"created_at"`
}

type VehicleModelFeature struct {
	ModelID    int  `json:"model_id"`
	FeatureID  int  `json:"feature_id"`
	IsStandard bool `json:"is_standard"`
}

// --- Vehicle Listing System ---

type VehicleListing struct {
	ID                   int        `json:"id"`
	UserID               int        `json:"user_id"`
	Title                string     `json:"title"`
	Description          *string    `json:"description,omitempty"`
	BrandID              *int       `json:"brand_id,omitempty"`
	ModelID              *int       `json:"model_id,omitempty"`
	Year                 int        `json:"year"`
	BodyTypeID           *int       `json:"body_type_id,omitempty"`
	Mileage              *int       `json:"mileage,omitempty"`
	FuelType             *string    `json:"fuel_type,omitempty"`
	Transmission         *string    `json:"transmission,omitempty"`
	Color                *string    `json:"color,omitempty"`
	Condition            *string    `json:"condition,omitempty"`
	City                 *string    `json:"city,omitempty"`
	District             *string    `json:"district,omitempty"`
	Price                float64    `json:"price"`
	IsNegotiable         bool       `json:"is_negotiable"`
	Status               string     `json:"status"`
	IsFeatured           bool       `json:"is_featured"`
	IsActive             bool       `json:"is_active"`
	ViewCount            int        `json:"view_count"`
	CreatedAt            time.Time  `json:"created_at"`
}

type VehicleGalleryCompany struct {
	ID                 int        `json:"id"`
	UserID             int        `json:"user_id"`
	CompanyName        string     `json:"company_name"`
	Slug               string     `json:"slug"`
	City               *string    `json:"city,omitempty"`
	District           *string    `json:"district,omitempty"`
	Phone              *string    `json:"phone,omitempty"`
	Description        *string    `json:"description,omitempty"`
	IsVerified         bool       `json:"is_verified"`
	VerificationStatus string     `json:"verification_status"`
	Rating             float64    `json:"rating"`
	IsActive           bool       `json:"is_active"`
	CreatedAt          time.Time  `json:"created_at"`
}

type VehicleFavoriteListing struct {
	ID        int       `json:"id"`
	UserID    int       `json:"user_id"`
	ListingID int       `json:"listing_id"`
	CreatedAt time.Time `json:"created_at"`
}

type VehicleInquiry struct {
	ID        int       `json:"id"`
	ListingID int       `json:"listing_id"`
	SenderID  int       `json:"sender_id"`
	Message   string    `json:"message"`
	IsRead    bool      `json:"is_read"`
	CreatedAt time.Time `json:"created_at"`
}
