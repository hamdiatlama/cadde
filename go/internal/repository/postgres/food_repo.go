package postgres

import (
	"context"
	"fmt"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/web-platform/backend/internal/domain"
)

type FoodRepo struct {
	pool *pgxpool.Pool
}

func NewFoodRepo(pool *pgxpool.Pool) *FoodRepo {
	return &FoodRepo{pool: pool}
}

// ── Restaurants ───────────────────────────────────────────────

func (r *FoodRepo) CreateRestaurant(ctx context.Context, rest *domain.Restaurant) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO restaurants (seller_id, name, slug, description, category, cuisine_type,
		 logo_url, cover_url, is_active, min_order, delivery_fee, avg_prep_time)
		 VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12)
		 RETURNING id, rating, review_count, is_verified, created_at, updated_at`,
		rest.SellerID, rest.Name, rest.Slug, rest.Description, rest.Category, rest.CuisineType,
		rest.LogoURL, rest.CoverURL, rest.IsActive, rest.MinOrder, rest.DeliveryFee, rest.AvgPrepTime,
	).Scan(&rest.ID, &rest.Rating, &rest.ReviewCount, &rest.IsVerified, &rest.CreatedAt, &rest.UpdatedAt)
}

func (r *FoodRepo) GetRestaurantByID(ctx context.Context, id int) (*domain.Restaurant, error) {
	rest := &domain.Restaurant{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, seller_id, name, slug, COALESCE(description,''), category, COALESCE(cuisine_type,''),
		 COALESCE(logo_url,''), COALESCE(cover_url,''), rating, review_count, is_active, is_verified,
		 min_order, delivery_fee, avg_prep_time, created_at, updated_at
		 FROM restaurants WHERE id=$1`, id,
	).Scan(&rest.ID, &rest.SellerID, &rest.Name, &rest.Slug, &rest.Description, &rest.Category,
		&rest.CuisineType, &rest.LogoURL, &rest.CoverURL, &rest.Rating, &rest.ReviewCount,
		&rest.IsActive, &rest.IsVerified, &rest.MinOrder, &rest.DeliveryFee, &rest.AvgPrepTime,
		&rest.CreatedAt, &rest.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("get restaurant: %w", err)
	}
	return rest, nil
}

func (r *FoodRepo) GetRestaurantBySellerID(ctx context.Context, sellerID int) (*domain.Restaurant, error) {
	rest := &domain.Restaurant{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, seller_id, name, slug, COALESCE(description,''), category, COALESCE(cuisine_type,''),
		 COALESCE(logo_url,''), COALESCE(cover_url,''), rating, review_count, is_active, is_verified,
		 min_order, delivery_fee, avg_prep_time, created_at, updated_at
		 FROM restaurants WHERE seller_id=$1`, sellerID,
	).Scan(&rest.ID, &rest.SellerID, &rest.Name, &rest.Slug, &rest.Description, &rest.Category,
		&rest.CuisineType, &rest.LogoURL, &rest.CoverURL, &rest.Rating, &rest.ReviewCount,
		&rest.IsActive, &rest.IsVerified, &rest.MinOrder, &rest.DeliveryFee, &rest.AvgPrepTime,
		&rest.CreatedAt, &rest.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("get restaurant by seller: %w", err)
	}
	return rest, nil
}

func (r *FoodRepo) ListRestaurants(ctx context.Context, category string, lat, lon float64) ([]*domain.Restaurant, error) {
	// For nearby sorting, a proper PostGIS query would be used.
	// Simplified version: filter by category + active + verified, order by rating.
	var rows pgx.Rows
	var err error
	if category != "" {
		rows, err = r.pool.Query(ctx,
			`SELECT id, seller_id, name, slug, COALESCE(description,''), category, COALESCE(cuisine_type,''),
			 COALESCE(logo_url,''), COALESCE(cover_url,''), rating, review_count, is_active, is_verified,
			 min_order, delivery_fee, avg_prep_time, created_at, updated_at
			 FROM restaurants WHERE is_active=true AND is_verified=true AND category=$1
			 ORDER BY rating DESC`, category)
	} else {
		rows, err = r.pool.Query(ctx,
			`SELECT id, seller_id, name, slug, COALESCE(description,''), category, COALESCE(cuisine_type,''),
			 COALESCE(logo_url,''), COALESCE(cover_url,''), rating, review_count, is_active, is_verified,
			 min_order, delivery_fee, avg_prep_time, created_at, updated_at
			 FROM restaurants WHERE is_active=true AND is_verified=true
			 ORDER BY rating DESC`)
	}
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var rests []*domain.Restaurant
	for rows.Next() {
		rest := &domain.Restaurant{}
		if err := rows.Scan(&rest.ID, &rest.SellerID, &rest.Name, &rest.Slug, &rest.Description,
			&rest.Category, &rest.CuisineType, &rest.LogoURL, &rest.CoverURL, &rest.Rating,
			&rest.ReviewCount, &rest.IsActive, &rest.IsVerified, &rest.MinOrder,
			&rest.DeliveryFee, &rest.AvgPrepTime, &rest.CreatedAt, &rest.UpdatedAt); err != nil {
			return nil, err
		}
		rests = append(rests, rest)
	}
	return rests, nil
}

func (r *FoodRepo) UpdateRestaurant(ctx context.Context, rest *domain.Restaurant) error {
	_, err := r.pool.Exec(ctx,
		`UPDATE restaurants SET name=$1, description=$2, category=$3, cuisine_type=$4,
		 logo_url=$5, cover_url=$6, min_order=$7, delivery_fee=$8, avg_prep_time=$9, is_active=$10
		 WHERE id=$11`,
		rest.Name, rest.Description, rest.Category, rest.CuisineType,
		rest.LogoURL, rest.CoverURL, rest.MinOrder, rest.DeliveryFee,
		rest.AvgPrepTime, rest.IsActive, rest.ID)
	return err
}

func (r *FoodRepo) UpdateVerification(ctx context.Context, restID int, verified bool) error {
	_, err := r.pool.Exec(ctx,
		`UPDATE restaurants SET is_verified=$1 WHERE id=$2`, verified, restID)
	return err
}

// ── Menu Items ────────────────────────────────────────────────

func (r *FoodRepo) CreateMenuItem(ctx context.Context, item *domain.FoodMenuItem) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO food_menu_items (restaurant_id, branch_id, name, description, price,
		 original_price, category, image_url, prep_time_minutes, is_available, is_featured, sort_order)
		 VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12)
		 RETURNING id, created_at, updated_at`,
		item.RestaurantID, item.BranchID, item.Name, item.Description, item.Price,
		item.OriginalPrice, item.Category, item.ImageURL, item.PrepTimeMinutes,
		item.IsAvailable, item.IsFeatured, item.SortOrder,
	).Scan(&item.ID, &item.CreatedAt, &item.UpdatedAt)
}

func (r *FoodRepo) GetMenuItemByID(ctx context.Context, id int) (*domain.FoodMenuItem, error) {
	item := &domain.FoodMenuItem{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, restaurant_id, branch_id, name, COALESCE(description,''), price,
		 COALESCE(original_price,0), category, COALESCE(image_url,''), prep_time_minutes,
		 is_available, is_featured, sort_order, created_at, updated_at
		 FROM food_menu_items WHERE id=$1`, id,
	).Scan(&item.ID, &item.RestaurantID, &item.BranchID, &item.Name, &item.Description,
		&item.Price, &item.OriginalPrice, &item.Category, &item.ImageURL,
		&item.PrepTimeMinutes, &item.IsAvailable, &item.IsFeatured, &item.SortOrder,
		&item.CreatedAt, &item.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("get menu item: %w", err)
	}
	return item, nil
}

func (r *FoodRepo) GetMenu(ctx context.Context, restID int) ([]*domain.FoodMenuItem, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, restaurant_id, branch_id, name, COALESCE(description,''), price,
		 COALESCE(original_price,0), category, COALESCE(image_url,''), prep_time_minutes,
		 is_available, is_featured, sort_order, created_at, updated_at
		 FROM food_menu_items WHERE restaurant_id=$1 AND is_available=true
		 ORDER BY sort_order ASC, category ASC, name ASC`, restID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var items []*domain.FoodMenuItem
	for rows.Next() {
		item := &domain.FoodMenuItem{}
		if err := rows.Scan(&item.ID, &item.RestaurantID, &item.BranchID, &item.Name,
			&item.Description, &item.Price, &item.OriginalPrice, &item.Category,
			&item.ImageURL, &item.PrepTimeMinutes, &item.IsAvailable, &item.IsFeatured,
			&item.SortOrder, &item.CreatedAt, &item.UpdatedAt); err != nil {
			return nil, err
		}

		// Load modifiers
		modRows, err := r.pool.Query(ctx,
			`SELECT id, menu_item_id, name, price, is_required, max_select, sort_order
			 FROM menu_item_modifiers WHERE menu_item_id=$1 ORDER BY sort_order ASC`, item.ID)
		if err == nil {
			for modRows.Next() {
				mod := domain.MenuItemModifier{}
				if err := modRows.Scan(&mod.ID, &mod.MenuItemID, &mod.Name, &mod.Price,
					&mod.IsRequired, &mod.MaxSelect, &mod.SortOrder); err == nil {
					item.Modifiers = append(item.Modifiers, mod)
				}
			}
			modRows.Close()
		}

		items = append(items, item)
	}
	return items, nil
}

func (r *FoodRepo) UpdateMenuItem(ctx context.Context, item *domain.FoodMenuItem) error {
	_, err := r.pool.Exec(ctx,
		`UPDATE food_menu_items SET name=$1, description=$2, price=$3, original_price=$4,
		 category=$5, image_url=$6, prep_time_minutes=$7, is_available=$8, is_featured=$9, sort_order=$10
		 WHERE id=$11`,
		item.Name, item.Description, item.Price, item.OriginalPrice, item.Category,
		item.ImageURL, item.PrepTimeMinutes, item.IsAvailable, item.IsFeatured,
		item.SortOrder, item.ID)
	return err
}

func (r *FoodRepo) DeleteMenuItem(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM food_menu_items WHERE id=$1`, id)
	return err
}

// ── Modifiers ─────────────────────────────────────────────────

func (r *FoodRepo) CreateModifier(ctx context.Context, mod *domain.MenuItemModifier) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO menu_item_modifiers (menu_item_id, name, price, is_required, max_select, sort_order)
		 VALUES ($1,$2,$3,$4,$5,$6) RETURNING id`,
		mod.MenuItemID, mod.Name, mod.Price, mod.IsRequired, mod.MaxSelect, mod.SortOrder,
	).Scan(&mod.ID)
}

func (r *FoodRepo) DeleteModifier(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM menu_item_modifiers WHERE id=$1`, id)
	return err
}

// ── Branches ──────────────────────────────────────────────────

func (r *FoodRepo) CreateBranch(ctx context.Context, b *domain.RestaurantBranch) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO restaurant_branches (restaurant_id, name, address, latitude, longitude, phone)
		 VALUES ($1,$2,$3,$4,$5,$6) RETURNING id, created_at`,
		b.RestaurantID, b.Name, b.Address, b.Latitude, b.Longitude, b.Phone,
	).Scan(&b.ID, &b.CreatedAt)
}

func (r *FoodRepo) ListBranches(ctx context.Context, restID int) ([]*domain.RestaurantBranch, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, restaurant_id, name, address, latitude, longitude, COALESCE(phone,''), is_active, created_at
		 FROM restaurant_branches WHERE restaurant_id=$1 ORDER BY name`, restID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var branches []*domain.RestaurantBranch
	for rows.Next() {
		b := &domain.RestaurantBranch{}
		if err := rows.Scan(&b.ID, &b.RestaurantID, &b.Name, &b.Address, &b.Latitude,
			&b.Longitude, &b.Phone, &b.IsActive, &b.CreatedAt); err != nil {
			return nil, err
		}
		branches = append(branches, b)
	}
	return branches, nil
}

// ── Delivery Zones ────────────────────────────────────────────

func (r *FoodRepo) CreateZone(ctx context.Context, z *domain.DeliveryZone) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO delivery_zones (restaurant_id, name, min_lat, max_lat, min_lon, max_lon, delivery_fee, min_order)
		 VALUES ($1,$2,$3,$4,$5,$6,$7,$8) RETURNING id, created_at`,
		z.RestaurantID, z.Name, z.MinLat, z.MaxLat, z.MinLon, z.MaxLon, z.DeliveryFee, z.MinOrder,
	).Scan(&z.ID, &z.CreatedAt)
}

func (r *FoodRepo) ListZones(ctx context.Context, restID int) ([]*domain.DeliveryZone, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, restaurant_id, name, min_lat, max_lat, min_lon, max_lon,
		 COALESCE(delivery_fee,0), COALESCE(min_order,0), is_active, created_at
		 FROM delivery_zones WHERE restaurant_id=$1 AND is_active=true ORDER BY name`, restID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var zones []*domain.DeliveryZone
	for rows.Next() {
		z := &domain.DeliveryZone{}
		if err := rows.Scan(&z.ID, &z.RestaurantID, &z.Name, &z.MinLat, &z.MaxLat,
			&z.MinLon, &z.MaxLon, &z.DeliveryFee, &z.MinOrder, &z.IsActive, &z.CreatedAt); err != nil {
			return nil, err
		}
		zones = append(zones, z)
	}
	return zones, nil
}
