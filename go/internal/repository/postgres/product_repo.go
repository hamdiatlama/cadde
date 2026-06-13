package postgres

import (
	"context"
	"fmt"
	"strings"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/web-platform/backend/internal/domain"
)

type ProductRepo struct {
	pool *pgxpool.Pool
}

func NewProductRepo(pool *pgxpool.Pool) *ProductRepo {
	return &ProductRepo{pool: pool}
}

func (r *ProductRepo) Create(ctx context.Context, p *domain.Product) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO products (seller_id, name, description, price, compare_price,
		 category, subcategory, occasion, color, stock, is_active, is_featured)
		 VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12)
		 RETURNING id, rating, review_count, created_at, updated_at`,
		p.SellerID, p.Name, p.Description, p.Price, p.ComparePrice,
		p.Category, p.Subcategory, p.Occasion, p.Color, p.Stock, p.IsActive, p.IsFeatured,
	).Scan(&p.ID, &p.Rating, &p.ReviewCount, &p.CreatedAt, &p.UpdatedAt)
}

func (r *ProductRepo) GetByID(ctx context.Context, id int) (*domain.Product, error) {
	p := &domain.Product{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, seller_id, name, COALESCE(description,''), price, COALESCE(compare_price,0),
		 category, COALESCE(subcategory,''), COALESCE(occasion,''), COALESCE(color,''),
		 COALESCE(images,'{}'), stock, is_active, is_featured, rating, review_count,
		 created_at, updated_at
		 FROM products WHERE id=$1`, id,
	).Scan(&p.ID, &p.SellerID, &p.Name, &p.Description, &p.Price, &p.ComparePrice,
		&p.Category, &p.Subcategory, &p.Occasion, &p.Color, &p.Images,
		&p.Stock, &p.IsActive, &p.IsFeatured, &p.Rating, &p.ReviewCount,
		&p.CreatedAt, &p.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("get product: %w", err)
	}
	return p, nil
}

func (r *ProductRepo) Search(ctx context.Context, q, category, subcategory string, minPrice, maxPrice float64, page, perPage int) (int, []*domain.Product, error) {
	where := []string{"1=1"}
	args := []interface{}{}
	argIdx := 1

	if q != "" {
		where = append(where, fmt.Sprintf("(name ILIKE $%d OR description ILIKE $%d)", argIdx, argIdx))
		args = append(args, "%"+q+"%")
		argIdx++
	}
	if category != "" {
		where = append(where, fmt.Sprintf("category=$%d", argIdx))
		args = append(args, category)
		argIdx++
	}
	if subcategory != "" {
		where = append(where, fmt.Sprintf("subcategory=$%d", argIdx))
		args = append(args, subcategory)
		argIdx++
	}
	if minPrice > 0 {
		where = append(where, fmt.Sprintf("price>=$%d", argIdx))
		args = append(args, minPrice)
		argIdx++
	}
	if maxPrice > 0 {
		where = append(where, fmt.Sprintf("price<=$%d", argIdx))
		args = append(args, maxPrice)
		argIdx++
	}

	whereClause := strings.Join(where, " AND ")

	var total int
	err := r.pool.QueryRow(ctx, fmt.Sprintf(`SELECT COUNT(*) FROM products WHERE %s`, whereClause), args...).Scan(&total)
	if err != nil {
		return 0, nil, err
	}

	offset := (page - 1) * perPage
	rows, err := r.pool.Query(ctx,
		fmt.Sprintf(`SELECT id, seller_id, name, COALESCE(description,''), price, COALESCE(compare_price,0),
		 category, COALESCE(subcategory,''), COALESCE(occasion,''), COALESCE(color,''),
		 COALESCE(images,'{}'), stock, is_active, is_featured, rating, review_count,
		 created_at, updated_at
		 FROM products WHERE %s ORDER BY created_at DESC LIMIT $%d OFFSET $%d`, whereClause, argIdx, argIdx+1),
		append(args, perPage, offset)...,
	)
	if err != nil {
		return 0, nil, err
	}
	defer rows.Close()

	var products []*domain.Product
	for rows.Next() {
		p := &domain.Product{}
		if err := rows.Scan(&p.ID, &p.SellerID, &p.Name, &p.Description, &p.Price, &p.ComparePrice,
			&p.Category, &p.Subcategory, &p.Occasion, &p.Color, &p.Images,
			&p.Stock, &p.IsActive, &p.IsFeatured, &p.Rating, &p.ReviewCount,
			&p.CreatedAt, &p.UpdatedAt); err != nil {
			return 0, nil, err
		}
		products = append(products, p)
	}
	return total, products, nil
}

func (r *ProductRepo) Update(ctx context.Context, p *domain.Product) error {
	_, err := r.pool.Exec(ctx,
		`UPDATE products SET name=$1, description=$2, price=$3, compare_price=$4,
		 category=$5, subcategory=$6, occasion=$7, color=$8, stock=$9,
		 is_active=$10, is_featured=$11 WHERE id=$12`,
		p.Name, p.Description, p.Price, p.ComparePrice,
		p.Category, p.Subcategory, p.Occasion, p.Color, p.Stock,
		p.IsActive, p.IsFeatured, p.ID)
	return err
}

func (r *ProductRepo) Delete(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM products WHERE id=$1`, id)
	return err
}
