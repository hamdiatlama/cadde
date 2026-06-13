package domain

import "time"

type Restaurant struct {
	ID            int        `json:"id"`
	SellerID      int        `json:"seller_id"`
	Name          string     `json:"name"`
	Slug          string     `json:"slug"`
	Description   string     `json:"description,omitempty"`
	Category      string     `json:"category"`
	CuisineType   string     `json:"cuisine_type,omitempty"`
	LogoURL       string     `json:"logo_url,omitempty"`
	CoverURL      string     `json:"cover_url,omitempty"`
	Rating        float64    `json:"rating"`
	ReviewCount   int        `json:"review_count"`
	IsActive      bool       `json:"is_active"`
	IsVerified    bool       `json:"is_verified"`
	MinOrder      float64    `json:"min_order"`
	DeliveryFee   float64    `json:"delivery_fee"`
	AvgPrepTime   int        `json:"avg_prep_time"`
	CreatedAt     time.Time  `json:"created_at"`
	UpdatedAt     time.Time  `json:"updated_at"`
}

type RestaurantBranch struct {
	ID           int        `json:"id"`
	RestaurantID int        `json:"restaurant_id"`
	Name         string     `json:"name"`
	Address      string     `json:"address"`
	Latitude     float64    `json:"latitude"`
	Longitude    float64    `json:"longitude"`
	Phone        string     `json:"phone,omitempty"`
	IsActive     bool       `json:"is_active"`
	CreatedAt    time.Time  `json:"created_at"`
}

type FoodMenuItem struct {
	ID              int        `json:"id"`
	RestaurantID    int        `json:"restaurant_id"`
	BranchID        *int       `json:"branch_id,omitempty"`
	Name            string     `json:"name"`
	Description     string     `json:"description,omitempty"`
	Price           float64    `json:"price"`
	OriginalPrice   float64    `json:"original_price,omitempty"`
	Category        string     `json:"category"`
	ImageURL        string     `json:"image_url,omitempty"`
	PrepTimeMinutes int        `json:"prep_time_minutes"`
	IsAvailable     bool       `json:"is_available"`
	IsFeatured      bool       `json:"is_featured"`
	SortOrder       int        `json:"sort_order"`
	CreatedAt       time.Time  `json:"created_at"`
	UpdatedAt       time.Time  `json:"updated_at"`
	Modifiers       []MenuItemModifier `json:"modifiers,omitempty"`
}

type MenuItemModifier struct {
	ID         int     `json:"id"`
	MenuItemID int     `json:"menu_item_id"`
	Name       string  `json:"name"`
	Price      float64 `json:"price"`
	IsRequired bool    `json:"is_required"`
	MaxSelect  int     `json:"max_select"`
	SortOrder  int     `json:"sort_order"`
}

type DeliveryZone struct {
	ID           int       `json:"id"`
	RestaurantID int       `json:"restaurant_id"`
	Name         string    `json:"name"`
	MinLat       float64   `json:"min_lat"`
	MaxLat       float64   `json:"max_lat"`
	MinLon       float64   `json:"min_lon"`
	MaxLon       float64   `json:"max_lon"`
	DeliveryFee  float64   `json:"delivery_fee,omitempty"`
	MinOrder     float64   `json:"min_order,omitempty"`
	IsActive     bool      `json:"is_active"`
	CreatedAt    time.Time `json:"created_at"`
}
