package postgres

import (
	"context"
	"fmt"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/web-platform/backend/internal/domain"
)

type FoodSupplierRepo struct {
	pool *pgxpool.Pool
}

func NewFoodSupplierRepo(pool *pgxpool.Pool) *FoodSupplierRepo {
	return &FoodSupplierRepo{pool: pool}
}

// --- Suppliers ---

func (r *FoodSupplierRepo) Create(ctx context.Context, s *domain.FoodSupplier) (*domain.FoodSupplier, error) {
	row := r.pool.QueryRow(ctx,
		`INSERT INTO food_suppliers (user_id, seller_id, company_name, slug, description, logo_url, cover_url,
		 supplier_type, city, district, address, latitude, longitude, contact_phone, contact_email, website_url,
		 is_organic_certified, is_halal_certified, certifications, product_categories, kitchen_photos, verification_status)
		 VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22)
		 RETURNING id, created_at, updated_at`,
		s.UserID, s.SellerID, s.CompanyName, s.Slug, s.Description, s.LogoURL, s.CoverURL,
		s.SupplierType, s.City, s.District, s.Address, s.Latitude, s.Longitude, s.ContactPhone, s.ContactEmail, s.WebsiteURL,
		s.IsOrganicCertified, s.IsHalalCertified, s.Certifications, s.ProductCategories, s.KitchenPhotos, "pending")
	err := row.Scan(&s.ID, &s.CreatedAt, &s.UpdatedAt)
	return s, err
}

func (r *FoodSupplierRepo) GetByID(ctx context.Context, id int64) (*domain.FoodSupplier, error) {
	row := r.pool.QueryRow(ctx,
		`SELECT id, user_id, seller_id, company_name, slug, description, logo_url, cover_url,
		 supplier_type, city, district, address, latitude, longitude, contact_phone, contact_email, website_url,
		 is_organic_certified, is_halal_certified, certifications, product_categories, kitchen_photos,
		 rating, review_count, verification_status, is_active, created_at, updated_at
		 FROM food_suppliers WHERE id=$1`, id)
	s := &domain.FoodSupplier{}
	err := row.Scan(&s.ID, &s.UserID, &s.SellerID, &s.CompanyName, &s.Slug, &s.Description,
		&s.LogoURL, &s.CoverURL, &s.SupplierType, &s.City, &s.District, &s.Address, &s.Latitude, &s.Longitude,
		&s.ContactPhone, &s.ContactEmail, &s.WebsiteURL,
		&s.IsOrganicCertified, &s.IsHalalCertified, &s.Certifications, &s.ProductCategories, &s.KitchenPhotos,
		&s.Rating, &s.ReviewCount, &s.VerificationStatus, &s.IsActive, &s.CreatedAt, &s.UpdatedAt)
	return s, err
}

func (r *FoodSupplierRepo) GetBySlug(ctx context.Context, slug string) (*domain.FoodSupplier, error) {
	row := r.pool.QueryRow(ctx,
		`SELECT id, user_id, seller_id, company_name, slug, description, logo_url, cover_url,
		 supplier_type, city, district, address, latitude, longitude, contact_phone, contact_email, website_url,
		 is_organic_certified, is_halal_certified, certifications, product_categories, kitchen_photos,
		 rating, review_count, verification_status, is_active, created_at, updated_at
		 FROM food_suppliers WHERE slug=$1`, slug)
	s := &domain.FoodSupplier{}
	err := row.Scan(&s.ID, &s.UserID, &s.SellerID, &s.CompanyName, &s.Slug, &s.Description,
		&s.LogoURL, &s.CoverURL, &s.SupplierType, &s.City, &s.District, &s.Address, &s.Latitude, &s.Longitude,
		&s.ContactPhone, &s.ContactEmail, &s.WebsiteURL,
		&s.IsOrganicCertified, &s.IsHalalCertified, &s.Certifications, &s.ProductCategories, &s.KitchenPhotos,
		&s.Rating, &s.ReviewCount, &s.VerificationStatus, &s.IsActive, &s.CreatedAt, &s.UpdatedAt)
	return s, err
}

func (r *FoodSupplierRepo) Update(ctx context.Context, id int64, vals map[string]interface{}) error {
	// simplified: in production use a query builder
	_, err := r.pool.Exec(ctx, `UPDATE food_suppliers SET updated_at=$1 WHERE id=$2`, time.Now(), id)
	return err
}

func (r *FoodSupplierRepo) List(ctx context.Context, city, organic, halal string) ([]domain.FoodSupplier, error) {
	q := `SELECT id, user_id, seller_id, company_name, slug, description, logo_url, cover_url,
		 supplier_type, city, district, address, latitude, longitude, contact_phone, contact_email, website_url,
		 is_organic_certified, is_halal_certified, certifications, product_categories,
		 rating, review_count, verification_status, is_active, created_at, updated_at
		 FROM food_suppliers WHERE is_active=true`
	var args []interface{}
	n := 1
	if city != "" {
		q += ` AND city=$` + itoa(n) + ` ORDER BY company_name`
		args = append(args, city)
		n++
	} else if organic == "true" || halal == "true" {
		if organic == "true" {
			q += ` AND is_organic_certified=true`
		}
		if halal == "true" {
			q += ` AND is_halal_certified=true`
		}
		q += ` ORDER BY company_name`
	} else {
		q += ` ORDER BY company_name`
	}
	rows, err := r.pool.Query(ctx, q, args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var res []domain.FoodSupplier
	for rows.Next() {
		var s domain.FoodSupplier
		err := rows.Scan(&s.ID, &s.UserID, &s.SellerID, &s.CompanyName, &s.Slug, &s.Description,
			&s.LogoURL, &s.CoverURL, &s.City, &s.District, &s.Address, &s.Latitude, &s.Longitude,
			&s.ContactPhone, &s.ContactEmail, &s.WebsiteURL,
			&s.IsOrganicCertified, &s.IsHalalCertified, &s.Certifications, &s.ProductCategories,
			&s.Rating, &s.ReviewCount, &s.VerificationStatus, &s.IsActive, &s.CreatedAt, &s.UpdatedAt)
		if err != nil {
			return nil, err
		}
		res = append(res, s)
	}
	if res == nil {
		res = []domain.FoodSupplier{}
	}
	return res, nil
}

// --- Products ---

func (r *FoodSupplierRepo) CreateProduct(ctx context.Context, p *domain.FoodSupplierProduct) (*domain.FoodSupplierProduct, error) {
	row := r.pool.QueryRow(ctx,
		`INSERT INTO food_supplier_products (supplier_id, name, description, category, subcategory, unit,
		 price_per_unit, is_organic, is_local, season_start_month, season_end_month, image_url)
		 VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12)
		 RETURNING id, created_at`,
		p.SupplierID, p.Name, p.Description, p.Category, p.Subcategory, p.Unit,
		p.PricePerUnit, p.IsOrganic, p.IsLocal, p.SeasonStartMonth, p.SeasonEndMonth, p.ImageURL)
	err := row.Scan(&p.ID, &p.CreatedAt)
	return p, err
}

func (r *FoodSupplierRepo) GetProductByID(ctx context.Context, id int64) (*domain.FoodSupplierProduct, error) {
	row := r.pool.QueryRow(ctx,
		`SELECT id, supplier_id, name, description, category, subcategory, unit,
		 price_per_unit, is_organic, is_local, season_start_month, season_end_month,
		 image_url, is_active, created_at FROM food_supplier_products WHERE id=$1`, id)
	p := &domain.FoodSupplierProduct{}
	err := row.Scan(&p.ID, &p.SupplierID, &p.Name, &p.Description, &p.Category, &p.Subcategory,
		&p.Unit, &p.PricePerUnit, &p.IsOrganic, &p.IsLocal, &p.SeasonStartMonth, &p.SeasonEndMonth,
		&p.ImageURL, &p.IsActive, &p.CreatedAt)
	return p, err
}

func (r *FoodSupplierRepo) ListProductsBySupplier(ctx context.Context, supplierID int64) ([]domain.FoodSupplierProduct, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, supplier_id, name, description, category, subcategory, unit,
		 price_per_unit, is_organic, is_local, season_start_month, season_end_month,
		 image_url, is_active, created_at FROM food_supplier_products
		 WHERE supplier_id=$1 AND is_active=true ORDER BY category, name`, supplierID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var res []domain.FoodSupplierProduct
	for rows.Next() {
		var p domain.FoodSupplierProduct
		err := rows.Scan(&p.ID, &p.SupplierID, &p.Name, &p.Description, &p.Category, &p.Subcategory,
			&p.Unit, &p.PricePerUnit, &p.IsOrganic, &p.IsLocal, &p.SeasonStartMonth, &p.SeasonEndMonth,
			&p.ImageURL, &p.IsActive, &p.CreatedAt)
		if err != nil {
			return nil, err
		}
		res = append(res, p)
	}
	if res == nil {
		res = []domain.FoodSupplierProduct{}
	}
	return res, nil
}

func (r *FoodSupplierRepo) UpdateProduct(ctx context.Context, id int64, vals map[string]interface{}) error {
	_, err := r.pool.Exec(ctx, `UPDATE food_supplier_products SET is_active=false WHERE id=$1`, id)
	return err
}

// --- Restaurant-Supplier Links ---

func (r *FoodSupplierRepo) LinkSupplier(ctx context.Context, restaurantID, supplierID int64, isPreferred bool, contractStart, contractEnd, notes *string) (*domain.FoodRestaurantSupplier, error) {
	row := r.pool.QueryRow(ctx,
		`INSERT INTO food_restaurant_suppliers (restaurant_id, supplier_id, is_preferred, contract_start, contract_end, notes)
		 VALUES ($1,$2,$3,$4,$5,$6) RETURNING id, created_at`,
		restaurantID, supplierID, isPreferred, contractStart, contractEnd, notes)
	link := &domain.FoodRestaurantSupplier{RestaurantID: restaurantID, SupplierID: supplierID, IsPreferred: isPreferred}
	err := row.Scan(&link.ID, &link.CreatedAt)
	return link, err
}

func (r *FoodSupplierRepo) UnlinkSupplier(ctx context.Context, restaurantID, supplierID int64) error {
	_, err := r.pool.Exec(ctx,
		`DELETE FROM food_restaurant_suppliers WHERE restaurant_id=$1 AND supplier_id=$2`,
		restaurantID, supplierID)
	return err
}

func (r *FoodSupplierRepo) ListRestaurantSuppliers(ctx context.Context, restaurantID int64) ([]domain.FoodRestaurantSupplier, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, restaurant_id, supplier_id, is_preferred, contract_start, contract_end, notes, created_at
		 FROM food_restaurant_suppliers WHERE restaurant_id=$1`, restaurantID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var res []domain.FoodRestaurantSupplier
	for rows.Next() {
		var l domain.FoodRestaurantSupplier
		err := rows.Scan(&l.ID, &l.RestaurantID, &l.SupplierID, &l.IsPreferred, &l.ContractStart, &l.ContractEnd, &l.Notes, &l.CreatedAt)
		if err != nil {
			return nil, err
		}
		res = append(res, l)
	}
	if res == nil {
		res = []domain.FoodRestaurantSupplier{}
	}
	return res, nil
}

// --- Ingredients ---

func (r *FoodSupplierRepo) CreateIngredient(ctx context.Context, ing *domain.FoodMenuItemIngredient) (*domain.FoodMenuItemIngredient, error) {
	row := r.pool.QueryRow(ctx,
		`INSERT INTO food_menu_item_ingredients (menu_item_id, supplier_product_id, quantity, unit, notes, is_visible_to_customer)
		 VALUES ($1,$2,$3,$4,$5,$6) RETURNING id, created_at`,
		ing.MenuItemID, ing.SupplierProductID, ing.Quantity, ing.Unit, ing.Notes, ing.IsVisibleToCustomer)
	err := row.Scan(&ing.ID, &ing.CreatedAt)
	return ing, err
}

func (r *FoodSupplierRepo) DeleteIngredient(ctx context.Context, id int64) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM food_menu_item_ingredients WHERE id=$1`, id)
	return err
}

func (r *FoodSupplierRepo) ListIngredients(ctx context.Context, menuItemID int64) ([]domain.FoodMenuItemIngredient, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, menu_item_id, supplier_product_id, quantity, unit, notes, is_visible_to_customer, created_at
		 FROM food_menu_item_ingredients WHERE menu_item_id=$1`, menuItemID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var res []domain.FoodMenuItemIngredient
	for rows.Next() {
		var ing domain.FoodMenuItemIngredient
		err := rows.Scan(&ing.ID, &ing.MenuItemID, &ing.SupplierProductID, &ing.Quantity, &ing.Unit, &ing.Notes, &ing.IsVisibleToCustomer, &ing.CreatedAt)
		if err != nil {
			return nil, err
		}
		res = append(res, ing)
	}
	if res == nil {
		res = []domain.FoodMenuItemIngredient{}
	}
	return res, nil
}

func itoa(n int) string {
	return fmt.Sprintf("%d", n)
}
