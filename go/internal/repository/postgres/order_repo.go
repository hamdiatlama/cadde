package postgres

import (
	"context"
	"fmt"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/web-platform/backend/internal/domain"
)

type OrderRepo struct {
	pool *pgxpool.Pool
}

func NewOrderRepo(pool *pgxpool.Pool) *OrderRepo {
	return &OrderRepo{pool: pool}
}

func (r *OrderRepo) Create(ctx context.Context, o *domain.Order) error {
	tx, err := r.pool.Begin(ctx)
	if err != nil {
		return err
	}
	defer tx.Rollback(ctx)

	err = tx.QueryRow(ctx,
		`INSERT INTO orders (user_id, seller_id, status, subtotal, delivery_fee, discount, total,
		 payment_method, payment_status, delivery_address, delivery_latitude, delivery_longitude, notes)
		 VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13)
		 RETURNING id, created_at, updated_at`,
		o.UserID, o.SellerID, o.Status, o.Subtotal, o.DeliveryFee, o.Discount, o.Total,
		o.PaymentMethod, o.PaymentStatus, o.DeliveryAddress, o.DeliveryLatitude, o.DeliveryLongitude, o.Notes,
	).Scan(&o.ID, &o.CreatedAt, &o.UpdatedAt)
	if err != nil {
		return fmt.Errorf("create order: %w", err)
	}

	for _, item := range o.Items {
		_, err = tx.Exec(ctx,
			`INSERT INTO order_items (order_id, product_id, name, price, quantity, image_url)
			 VALUES ($1,$2,$3,$4,$5,$6)`,
			o.ID, item.ProductID, item.Name, item.Price, item.Quantity, item.ImageURL)
		if err != nil {
			return fmt.Errorf("create order item: %w", err)
		}
	}

	return tx.Commit(ctx)
}

func (r *OrderRepo) GetByID(ctx context.Context, id int) (*domain.Order, error) {
	o := &domain.Order{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, user_id, seller_id, courier_id, status, subtotal, delivery_fee, discount, total,
		 payment_method, payment_status, delivery_address, delivery_latitude, delivery_longitude,
		 COALESCE(notes,''), estimated_at, delivered_at, cancelled_at, COALESCE(cancel_reason,''),
		 created_at, updated_at
		 FROM orders WHERE id=$1`, id,
	).Scan(&o.ID, &o.UserID, &o.SellerID, &o.CourierID, &o.Status,
		&o.Subtotal, &o.DeliveryFee, &o.Discount, &o.Total,
		&o.PaymentMethod, &o.PaymentStatus, &o.DeliveryAddress,
		&o.DeliveryLatitude, &o.DeliveryLongitude, &o.Notes,
		&o.EstimatedAt, &o.DeliveredAt, &o.CancelledAt, &o.CancelReason,
		&o.CreatedAt, &o.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("get order: %w", err)
	}

	// Load items
	rows, err := r.pool.Query(ctx,
		`SELECT id, order_id, product_id, name, price, quantity, COALESCE(image_url,'')
		 FROM order_items WHERE order_id=$1`, id)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	for rows.Next() {
		var item domain.OrderItem
		if err := rows.Scan(&item.ID, &item.OrderID, &item.ProductID, &item.Name,
			&item.Price, &item.Quantity, &item.ImageURL); err != nil {
			return nil, err
		}
		o.Items = append(o.Items, item)
	}
	return o, nil
}

func (r *OrderRepo) ListByUser(ctx context.Context, userID, page, perPage int) (int, []*domain.Order, error) {
	var total int
	err := r.pool.QueryRow(ctx, `SELECT COUNT(*) FROM orders WHERE user_id=$1`, userID).Scan(&total)
	if err != nil {
		return 0, nil, err
	}

	offset := (page - 1) * perPage
	rows, err := r.pool.Query(ctx,
		`SELECT id, user_id, seller_id, courier_id, status, subtotal, delivery_fee, discount, total,
		 payment_method, payment_status, delivery_address, delivery_latitude, delivery_longitude,
		 COALESCE(notes,''), estimated_at, delivered_at, cancelled_at, COALESCE(cancel_reason,''),
		 created_at, updated_at
		 FROM orders WHERE user_id=$1 ORDER BY created_at DESC LIMIT $2 OFFSET $3`,
		userID, perPage, offset)
	if err != nil {
		return 0, nil, err
	}
	defer rows.Close()

	var orders []*domain.Order
	for rows.Next() {
		o := &domain.Order{}
		if err := rows.Scan(&o.ID, &o.UserID, &o.SellerID, &o.CourierID, &o.Status,
			&o.Subtotal, &o.DeliveryFee, &o.Discount, &o.Total,
			&o.PaymentMethod, &o.PaymentStatus, &o.DeliveryAddress,
			&o.DeliveryLatitude, &o.DeliveryLongitude, &o.Notes,
			&o.EstimatedAt, &o.DeliveredAt, &o.CancelledAt, &o.CancelReason,
			&o.CreatedAt, &o.UpdatedAt); err != nil {
			return 0, nil, err
		}
		orders = append(orders, o)
	}
	return total, orders, nil
}

func (r *OrderRepo) UpdateStatus(ctx context.Context, id int, status string) error {
	_, err := r.pool.Exec(ctx, `UPDATE orders SET status=$1, updated_at=$2 WHERE id=$3`,
		status, time.Now(), id)
	return err
}

func (r *OrderRepo) ListBySeller(ctx context.Context, sellerID, page, perPage int) (int, []*domain.Order, error) {
	var total int
	err := r.pool.QueryRow(ctx, `SELECT COUNT(*) FROM orders WHERE seller_id=$1`, sellerID).Scan(&total)
	if err != nil {
		return 0, nil, err
	}
	offset := (page - 1) * perPage
	rows, err := r.pool.Query(ctx,
		`SELECT id, user_id, seller_id, courier_id, status, subtotal, delivery_fee, discount, total,
		 payment_method, payment_status, delivery_address, delivery_latitude, delivery_longitude,
		 COALESCE(notes,''), estimated_at, delivered_at, cancelled_at, COALESCE(cancel_reason,''),
		 created_at, updated_at
		 FROM orders WHERE seller_id=$1 ORDER BY created_at DESC LIMIT $2 OFFSET $3`,
		sellerID, perPage, offset)
	if err != nil {
		return 0, nil, err
	}
	defer rows.Close()
	var orders []*domain.Order
	for rows.Next() {
		o := &domain.Order{}
		if err := rows.Scan(&o.ID, &o.UserID, &o.SellerID, &o.CourierID, &o.Status,
			&o.Subtotal, &o.DeliveryFee, &o.Discount, &o.Total,
			&o.PaymentMethod, &o.PaymentStatus, &o.DeliveryAddress,
			&o.DeliveryLatitude, &o.DeliveryLongitude, &o.Notes,
			&o.EstimatedAt, &o.DeliveredAt, &o.CancelledAt, &o.CancelReason,
			&o.CreatedAt, &o.UpdatedAt); err != nil {
			return 0, nil, err
		}
		orders = append(orders, o)
	}
	return total, orders, nil
}
