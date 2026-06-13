package domain

import "time"

type Product struct {
	ID             int       `json:"id"`
	SellerID       int       `json:"seller_id"`
	Name           string    `json:"name"`
	Description    string    `json:"description,omitempty"`
	Price          float64   `json:"price"`
	ComparePrice   float64   `json:"compare_price,omitempty"`
	Category       string    `json:"category"`
	Subcategory    string    `json:"subcategory,omitempty"`
	Occasion       string    `json:"occasion,omitempty"`
	Color          string    `json:"color,omitempty"`
	Images         []string  `json:"images,omitempty"`
	Stock          int       `json:"stock"`
	IsActive       bool      `json:"is_active"`
	IsFeatured     bool      `json:"is_featured"`
	Rating         float64   `json:"rating"`
	ReviewCount    int       `json:"review_count"`
	CreatedAt      time.Time `json:"created_at"`
	UpdatedAt      time.Time `json:"updated_at"`
}

type Category struct {
	ID       int    `json:"id"`
	Name     string `json:"name"`
	Slug     string `json:"slug"`
	Icon     string `json:"icon,omitempty"`
	ParentID *int   `json:"parent_id,omitempty"`
	Order    int    `json:"order"`
}
