package domain

import "time"

type FoodSupplier struct {
	ID                  int64     `json:"id"`
	UserID              *int64    `json:"user_id,omitempty"`
	SellerID            *int64    `json:"seller_id,omitempty"`
	CompanyName         string    `json:"company_name"`
	Slug                string    `json:"slug"`
	Description         *string   `json:"description,omitempty"`
	LogoURL             *string   `json:"logo_url,omitempty"`
	CoverURL            *string   `json:"cover_url,omitempty"`
	SupplierType        string    `json:"supplier_type"`
	City                *string   `json:"city,omitempty"`
	District            *string   `json:"district,omitempty"`
	Address             *string   `json:"address,omitempty"`
	Latitude            *float64  `json:"latitude,omitempty"`
	Longitude           *float64  `json:"longitude,omitempty"`
	ContactPhone        *string   `json:"contact_phone,omitempty"`
	ContactEmail        *string   `json:"contact_email,omitempty"`
	WebsiteURL          *string   `json:"website_url,omitempty"`
	IsOrganicCertified  bool      `json:"is_organic_certified"`
	IsHalalCertified    bool      `json:"is_halal_certified"`
	Certifications      *string   `json:"certifications,omitempty"`
	ProductCategories   *string   `json:"product_categories,omitempty"`
	KitchenPhotos       *string   `json:"kitchen_photos,omitempty"`
	Rating              float64   `json:"rating"`
	ReviewCount         int       `json:"review_count"`
	VerificationStatus  string    `json:"verification_status"`
	IsActive            bool      `json:"is_active"`
	CreatedAt           time.Time `json:"created_at"`
	UpdatedAt           time.Time `json:"updated_at"`
}

type FoodSupplierProduct struct {
	ID               int64      `json:"id"`
	SupplierID       int64      `json:"supplier_id"`
	Name             string     `json:"name"`
	Description      *string    `json:"description,omitempty"`
	Category         string     `json:"category"`
	Subcategory      *string    `json:"subcategory,omitempty"`
	Unit             string     `json:"unit"`
	PricePerUnit     *float64   `json:"price_per_unit,omitempty"`
	IsOrganic        bool       `json:"is_organic"`
	IsLocal          bool       `json:"is_local"`
	SeasonStartMonth *int       `json:"season_start_month,omitempty"`
	SeasonEndMonth   *int       `json:"season_end_month,omitempty"`
	ImageURL         *string    `json:"image_url,omitempty"`
	IsActive         bool       `json:"is_active"`
	CreatedAt        time.Time  `json:"created_at"`
}

type FoodRestaurantSupplier struct {
	ID            int64      `json:"id"`
	RestaurantID  int64      `json:"restaurant_id"`
	SupplierID    int64      `json:"supplier_id"`
	IsPreferred   bool       `json:"is_preferred"`
	ContractStart *string    `json:"contract_start,omitempty"`
	ContractEnd   *string    `json:"contract_end,omitempty"`
	Notes         *string    `json:"notes,omitempty"`
	CreatedAt     time.Time  `json:"created_at"`
}

type FoodMenuItemIngredient struct {
	ID                 int64      `json:"id"`
	MenuItemID         int64      `json:"menu_item_id"`
	SupplierProductID  int64      `json:"supplier_product_id"`
	Quantity           *float64   `json:"quantity,omitempty"`
	Unit               *string    `json:"unit,omitempty"`
	Notes              *string    `json:"notes,omitempty"`
	IsVisibleToCustomer bool      `json:"is_visible_to_customer"`
	CreatedAt          time.Time  `json:"created_at"`
}

type FoodTransparencyScore struct {
	ID                    int64     `json:"id"`
	RestaurantID          int64     `json:"restaurant_id"`
	TotalMenuItems        int       `json:"total_menu_items"`
	ItemsWithIngredients  int       `json:"items_with_ingredients"`
	TotalSuppliersLinked  int       `json:"total_suppliers_linked"`
	TransparencyPercentage float64  `json:"transparency_percentage"`
	TotalPoints           int       `json:"total_points"`
	LastCalculatedAt      string    `json:"last_calculated_at"`
	CreatedAt             time.Time `json:"created_at"`
}

// Response helpers
type SupplierLinkResponse struct {
	ID           int64   `json:"id"`
	RestaurantID int64   `json:"restaurant_id"`
	SupplierID   int64   `json:"supplier_id"`
	SupplierName string  `json:"supplier_name"`
	IsPreferred  bool    `json:"is_preferred"`
	ContractStart *string `json:"contract_start,omitempty"`
	ContractEnd   *string `json:"contract_end,omitempty"`
	Notes         *string `json:"notes,omitempty"`
}

type IngredientWithDetails struct {
	ID                 int64   `json:"id"`
	MenuItemID         int64   `json:"menu_item_id"`
	SupplierProductID  int64   `json:"supplier_product_id"`
	ProductName        string  `json:"product_name"`
	SupplierName       string  `json:"supplier_name"`
	SupplierSlug       string  `json:"supplier_slug"`
	Quantity           *float64 `json:"quantity,omitempty"`
	Unit               *string `json:"unit,omitempty"`
	Notes              *string `json:"notes,omitempty"`
	IsVisibleToCustomer bool   `json:"is_visible_to_customer"`
}

type SupplierPage struct {
	ID                  int64                `json:"id"`
	CompanyName         string               `json:"company_name"`
	Slug                string               `json:"slug"`
	Description         *string              `json:"description,omitempty"`
	LogoURL             *string              `json:"logo_url,omitempty"`
	CoverURL            *string              `json:"cover_url,omitempty"`
	SupplierType        string               `json:"supplier_type"`
	City                *string              `json:"city,omitempty"`
	District            *string              `json:"district,omitempty"`
	ContactPhone        *string              `json:"contact_phone,omitempty"`
	ContactEmail        *string              `json:"contact_email,omitempty"`
	WebsiteURL          *string              `json:"website_url,omitempty"`
	IsOrganicCertified  bool                 `json:"is_organic_certified"`
	IsHalalCertified    bool                 `json:"is_halal_certified"`
	Certifications      *string              `json:"certifications,omitempty"`
	ProductCategories   *string              `json:"product_categories,omitempty"`
	KitchenPhotos       *string              `json:"kitchen_photos,omitempty"`
	Rating              float64              `json:"rating"`
	ReviewCount         int                  `json:"review_count"`
	VerificationStatus  string               `json:"verification_status"`
	IsActive            bool                 `json:"is_active"`
	Products            []FoodSupplierProduct `json:"products"`
}

type TraceResponse struct {
	MenuItemID   int64                   `json:"menu_item_id"`
	MenuItemName string                  `json:"menu_item_name"`
	Ingredients  []IngredientWithDetails `json:"ingredients"`
}
