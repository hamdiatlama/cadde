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
