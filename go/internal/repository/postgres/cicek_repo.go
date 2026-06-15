package postgres

import (
	"context"
	"fmt"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/web-platform/backend/internal/domain"
)

type CicekRepo struct {
	pool *pgxpool.Pool
}

func NewCicekRepo(pool *pgxpool.Pool) *CicekRepo {
	return &CicekRepo{pool: pool}
}

// --- Florist Profile ---

func (r *CicekRepo) CreateFlorist(ctx context.Context, userID int, shopName, slug string) (*domain.FloristProfile, error) {
	var f domain.FloristProfile
	err := r.pool.QueryRow(ctx,
		`INSERT INTO florist_profiles (user_id, shop_name, slug) VALUES ($1, $2, $3)
		 RETURNING id, user_id, shop_name, slug, is_active, is_open, preparation_time_min,
		           delivery_radius_km, min_order_amount, delivery_fee, verification_status,
		           rating, review_count, total_score, created_at`,
		userID, shopName, slug,
	).Scan(&f.ID, &f.UserID, &f.ShopName, &f.Slug, &f.IsActive, &f.IsOpen,
		&f.PreparationTimeMin, &f.DeliveryRadiusKm, &f.MinOrderAmount, &f.DeliveryFee,
		&f.VerificationStatus, &f.Rating, &f.ReviewCount, &f.TotalScore, &f.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("create florist: %w", err)
	}
	return &f, nil
}

func (r *CicekRepo) GetFloristByUser(ctx context.Context, userID int) (*domain.FloristProfile, error) {
	var f domain.FloristProfile
	err := r.pool.QueryRow(ctx,
		`SELECT id, user_id, shop_name, slug, is_active, is_open, preparation_time_min,
		        delivery_radius_km, min_order_amount, delivery_fee, verification_status,
		        rating, review_count, total_score, created_at
		 FROM florist_profiles WHERE user_id = $1`, userID,
	).Scan(&f.ID, &f.UserID, &f.ShopName, &f.Slug, &f.IsActive, &f.IsOpen,
		&f.PreparationTimeMin, &f.DeliveryRadiusKm, &f.MinOrderAmount, &f.DeliveryFee,
		&f.VerificationStatus, &f.Rating, &f.ReviewCount, &f.TotalScore, &f.CreatedAt)
	if err != nil {
		return nil, err
	}
	return &f, nil
}

func (r *CicekRepo) GetFloristBySlug(ctx context.Context, slug string) (*domain.FloristProfile, error) {
	var f domain.FloristProfile
	err := r.pool.QueryRow(ctx,
		`SELECT id, user_id, shop_name, slug, is_active, is_open, preparation_time_min,
		        delivery_radius_km, min_order_amount, delivery_fee, verification_status,
		        rating, review_count, total_score, created_at
		 FROM florist_profiles WHERE slug = $1`, slug,
	).Scan(&f.ID, &f.UserID, &f.ShopName, &f.Slug, &f.IsActive, &f.IsOpen,
		&f.PreparationTimeMin, &f.DeliveryRadiusKm, &f.MinOrderAmount, &f.DeliveryFee,
		&f.VerificationStatus, &f.Rating, &f.ReviewCount, &f.TotalScore, &f.CreatedAt)
	if err != nil {
		return nil, err
	}
	return &f, nil
}

func (r *CicekRepo) GetFloristByID(ctx context.Context, id int) (*domain.FloristProfile, error) {
	var f domain.FloristProfile
	err := r.pool.QueryRow(ctx,
		`SELECT id, user_id, shop_name, slug, is_active, is_open, preparation_time_min,
		        delivery_radius_km, min_order_amount, delivery_fee, verification_status,
		        rating, review_count, total_score, created_at
		 FROM florist_profiles WHERE id = $1`, id,
	).Scan(&f.ID, &f.UserID, &f.ShopName, &f.Slug, &f.IsActive, &f.IsOpen,
		&f.PreparationTimeMin, &f.DeliveryRadiusKm, &f.MinOrderAmount, &f.DeliveryFee,
		&f.VerificationStatus, &f.Rating, &f.ReviewCount, &f.TotalScore, &f.CreatedAt)
	if err != nil {
		return nil, err
	}
	return &f, nil
}

func (r *CicekRepo) UpdateFlorist(ctx context.Context, id int, vals map[string]any) error {
	if len(vals) == 0 {
		return nil
	}
	query := "UPDATE florist_profiles SET "
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

func (r *CicekRepo) ListActiveFlorists(ctx context.Context, city string, page, limit int) ([]domain.FloristProfile, int, error) {
	where := "WHERE is_active = true"
	args := make([]any, 0)
	i := 1
	if city != "" {
		where += " AND city = $" + fmt.Sprintf("%d", i)
		args = append(args, city)
		i++
	}
	var total int
	err := r.pool.QueryRow(ctx, "SELECT COUNT(*) FROM florist_profiles "+where, args...).Scan(&total)
	if err != nil {
		return nil, 0, err
	}
	offset := (page - 1) * limit
	query := fmt.Sprintf("SELECT id, user_id, shop_name, slug, is_active, is_open, preparation_time_min, delivery_radius_km, min_order_amount, delivery_fee, verification_status, rating, review_count, total_score, created_at FROM florist_profiles %s ORDER BY total_score DESC, rating DESC LIMIT $%d OFFSET $%d", where, i, i+1)
	args = append(args, limit, offset)
	rows, err := r.pool.Query(ctx, query, args...)
	if err != nil {
		return nil, 0, err
	}
	defer rows.Close()
	var items []domain.FloristProfile
	for rows.Next() {
		var f domain.FloristProfile
		if err := rows.Scan(&f.ID, &f.UserID, &f.ShopName, &f.Slug, &f.IsActive, &f.IsOpen, &f.PreparationTimeMin, &f.DeliveryRadiusKm, &f.MinOrderAmount, &f.DeliveryFee, &f.VerificationStatus, &f.Rating, &f.ReviewCount, &f.TotalScore, &f.CreatedAt); err != nil {
			return nil, 0, err
		}
		items = append(items, f)
	}
	return items, total, nil
}

func (r *CicekRepo) ToggleFloristOpen(ctx context.Context, id int) (bool, error) {
	var isOpen bool
	err := r.pool.QueryRow(ctx,
		`UPDATE florist_profiles SET is_open = NOT is_open WHERE id = $1 RETURNING is_open`, id,
	).Scan(&isOpen)
	if err != nil {
		return false, err
	}
	return isOpen, nil
}

// --- Products ---

func (r *CicekRepo) CreateProduct(ctx context.Context, sellerType string, sellerID int, name string, price float64) (*domain.FlowerProduct, error) {
	var p domain.FlowerProduct
	err := r.pool.QueryRow(ctx,
		`INSERT INTO flower_products (seller_type, seller_id, name, price)
		 VALUES ($1, $2, $3, $4)
		 RETURNING id, seller_type, seller_id, name, price, stock, is_active, is_express_eligible, is_customizable, rating, review_count, created_at`,
		sellerType, sellerID, name, price,
	).Scan(&p.ID, &p.SellerType, &p.SellerID, &p.Name, &p.Price, &p.Stock, &p.IsActive, &p.IsExpressEligible, &p.IsCustomizable, &p.Rating, &p.ReviewCount, &p.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("create product: %w", err)
	}
	return &p, nil
}

// --- Reminders ---

func (r *CicekRepo) CreateReminder(ctx context.Context, userID int, name string, date time.Time) (*domain.SpecialDayReminder, error) {
	var rem domain.SpecialDayReminder
	err := r.pool.QueryRow(ctx,
		`INSERT INTO special_day_reminders (user_id, name, reminder_date) VALUES ($1, $2, $3)
		 RETURNING id, user_id, name, reminder_date, is_yearly, is_active, created_at`,
		userID, name, date,
	).Scan(&rem.ID, &rem.UserID, &rem.Name, &rem.ReminderDate, &rem.IsYearly, &rem.IsActive, &rem.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("create reminder: %w", err)
	}
	return &rem, nil
}
