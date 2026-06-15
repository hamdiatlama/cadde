package postgres

import (
	"context"
	"fmt"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/web-platform/backend/internal/domain"
)

type VehicleListingRepo struct {
	pool *pgxpool.Pool
}

func NewVehicleListingRepo(pool *pgxpool.Pool) *VehicleListingRepo {
	return &VehicleListingRepo{pool: pool}
}

func (r *VehicleListingRepo) CreateListing(ctx context.Context, userID int, title string, year int, price float64) (*domain.VehicleListing, error) {
	var l domain.VehicleListing
	err := r.pool.QueryRow(ctx,
		`INSERT INTO vehicle_listings (user_id, title, year, price)
		 VALUES ($1, $2, $3, $4)
		 RETURNING id, user_id, title, year, price, is_negotiable, status, is_featured, is_active, view_count, created_at`,
		userID, title, year, price,
	).Scan(&l.ID, &l.UserID, &l.Title, &l.Year, &l.Price, &l.IsNegotiable, &l.Status, &l.IsFeatured, &l.IsActive, &l.ViewCount, &l.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("create listing: %w", err)
	}
	return &l, nil
}

func (r *VehicleListingRepo) GetListing(ctx context.Context, id int) (*domain.VehicleListing, error) {
	var l domain.VehicleListing
	err := r.pool.QueryRow(ctx,
		`SELECT id, user_id, title, year, price, is_negotiable, status, is_featured, is_active, view_count, created_at
		 FROM vehicle_listings WHERE id = $1 AND is_active = true`, id,
	).Scan(&l.ID, &l.UserID, &l.Title, &l.Year, &l.Price, &l.IsNegotiable, &l.Status, &l.IsFeatured, &l.IsActive, &l.ViewCount, &l.CreatedAt)
	if err != nil {
		return nil, err
	}
	return &l, nil
}

func (r *VehicleListingRepo) UpdateListing(ctx context.Context, id int, vals map[string]any) error {
	if len(vals) == 0 {
		return nil
	}
	query := "UPDATE vehicle_listings SET "
	args := make([]any, 0, len(vals)+1)
	i := 1
	for k, v := range vals {
		if i > 1 {
			query += ", "
		}
		query += k + " = $" + fmt.Sprintf("%d", i)
		args = append(args, v)
		i++
	}
	query += " WHERE id = $" + fmt.Sprintf("%d", i)
	args = append(args, id)
	_, err := r.pool.Exec(ctx, query, args...)
	return err
}

func (r *VehicleListingRepo) SearchListings(ctx context.Context, brandID, modelID *int, minPrice, maxPrice *float64, city, fuelType string, page, limit int) ([]domain.VehicleListing, int, error) {
	where := "WHERE is_active = true AND status = 'active'"
	args := make([]any, 0)
	i := 1
	if brandID != nil {
		where += fmt.Sprintf(" AND brand_id = $%d", i)
		args = append(args, *brandID)
		i++
	}
	if modelID != nil {
		where += fmt.Sprintf(" AND model_id = $%d", i)
		args = append(args, *modelID)
		i++
	}
	if minPrice != nil {
		where += fmt.Sprintf(" AND price >= $%d", i)
		args = append(args, *minPrice)
		i++
	}
	if maxPrice != nil {
		where += fmt.Sprintf(" AND price <= $%d", i)
		args = append(args, *maxPrice)
		i++
	}
	if city != "" {
		where += fmt.Sprintf(" AND city = $%d", i)
		args = append(args, city)
		i++
	}
	if fuelType != "" {
		where += fmt.Sprintf(" AND fuel_type = $%d", i)
		args = append(args, fuelType)
		i++
	}

	var total int
	err := r.pool.QueryRow(ctx, "SELECT COUNT(*) FROM vehicle_listings "+where, args...).Scan(&total)
	if err != nil {
		return nil, 0, err
	}

	offset := (page - 1) * limit
	query := fmt.Sprintf("SELECT id, user_id, title, year, price, is_negotiable, status, is_featured, is_active, view_count, created_at FROM vehicle_listings %s ORDER BY created_at DESC LIMIT $%d OFFSET $%d", where, i, i+1)
	args = append(args, limit, offset)
	rows, err := r.pool.Query(ctx, query, args...)
	if err != nil {
		return nil, 0, err
	}
	defer rows.Close()
	var items []domain.VehicleListing
	for rows.Next() {
		var l domain.VehicleListing
		if err := rows.Scan(&l.ID, &l.UserID, &l.Title, &l.Year, &l.Price, &l.IsNegotiable, &l.Status, &l.IsFeatured, &l.IsActive, &l.ViewCount, &l.CreatedAt); err != nil {
			return nil, 0, err
		}
		items = append(items, l)
	}
	return items, total, nil
}

func (r *VehicleListingRepo) IncrementView(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, "UPDATE vehicle_listings SET view_count = view_count + 1 WHERE id = $1", id)
	return err
}

func (r *VehicleListingRepo) CreateGallery(ctx context.Context, userID int, companyName, slug string) (*domain.VehicleGalleryCompany, error) {
	var g domain.VehicleGalleryCompany
	err := r.pool.QueryRow(ctx,
		`INSERT INTO vehicle_gallery_companies (user_id, company_name, slug)
		 VALUES ($1, $2, $3)
		 RETURNING id, user_id, company_name, slug, is_verified, verification_status, rating, is_active, created_at`,
		userID, companyName, slug,
	).Scan(&g.ID, &g.UserID, &g.CompanyName, &g.Slug, &g.IsVerified, &g.VerificationStatus, &g.Rating, &g.IsActive, &g.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("create gallery: %w", err)
	}
	return &g, nil
}
