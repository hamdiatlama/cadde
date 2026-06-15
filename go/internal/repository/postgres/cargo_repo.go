package postgres

import (
	"context"
	"fmt"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/web-platform/backend/internal/domain"
)

type CargoRepo struct {
	pool *pgxpool.Pool
}

func NewCargoRepo(pool *pgxpool.Pool) *CargoRepo {
	return &CargoRepo{pool: pool}
}

func (r *CargoRepo) CreateCompany(ctx context.Context, userID int, name, slug string) (*domain.CargoCompany, error) {
	var c domain.CargoCompany
	err := r.pool.QueryRow(ctx,
		`INSERT INTO cargo_companies (user_id, company_name, slug) VALUES ($1, $2, $3)
		 RETURNING id, user_id, company_name, slug, is_verified, verification_status,
		           is_active, rating, shipment_count, created_at`,
		userID, name, slug,
	).Scan(&c.ID, &c.UserID, &c.CompanyName, &c.Slug,
		&c.IsVerified, &c.VerificationStatus, &c.IsActive, &c.Rating, &c.ShipmentCount, &c.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("create cargo company: %w", err)
	}
	return &c, nil
}

func (r *CargoRepo) GetCompanyByUser(ctx context.Context, userID int) (*domain.CargoCompany, error) {
	var c domain.CargoCompany
	err := r.pool.QueryRow(ctx,
		`SELECT id, user_id, company_name, slug, is_verified, verification_status,
		        is_active, rating, shipment_count, created_at
		 FROM cargo_companies WHERE user_id = $1`, userID,
	).Scan(&c.ID, &c.UserID, &c.CompanyName, &c.Slug,
		&c.IsVerified, &c.VerificationStatus, &c.IsActive, &c.Rating, &c.ShipmentCount, &c.CreatedAt)
	if err != nil {
		return nil, err
	}
	return &c, nil
}

func (r *CargoRepo) GetCompany(ctx context.Context, id int) (*domain.CargoCompany, error) {
	var c domain.CargoCompany
	err := r.pool.QueryRow(ctx,
		`SELECT id, user_id, company_name, slug, is_verified, verification_status,
		        is_active, rating, shipment_count, created_at
		 FROM cargo_companies WHERE id = $1`, id,
	).Scan(&c.ID, &c.UserID, &c.CompanyName, &c.Slug,
		&c.IsVerified, &c.VerificationStatus, &c.IsActive, &c.Rating, &c.ShipmentCount, &c.CreatedAt)
	if err != nil {
		return nil, err
	}
	return &c, nil
}

func (r *CargoRepo) ListCompanies(ctx context.Context) ([]domain.CargoCompany, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, user_id, company_name, slug, is_verified, verification_status,
		        is_active, rating, shipment_count, created_at
		 FROM cargo_companies WHERE is_active = true ORDER BY company_name`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var res []domain.CargoCompany
	for rows.Next() {
		var c domain.CargoCompany
		if err := rows.Scan(&c.ID, &c.UserID, &c.CompanyName, &c.Slug,
			&c.IsVerified, &c.VerificationStatus, &c.IsActive, &c.Rating, &c.ShipmentCount, &c.CreatedAt); err != nil {
			return nil, err
		}
		res = append(res, c)
	}
	return res, nil
}

func (r *CargoRepo) CreateShipment(ctx context.Context, companyID int, trackingNo, senderName, recipientName, recipientCity, recipientAddress string) (*domain.CargoShipment, error) {
	var s domain.CargoShipment
	err := r.pool.QueryRow(ctx,
		`INSERT INTO cargo_shipments (company_id, tracking_no, sender_name, recipient_name, recipient_city, recipient_address)
		 VALUES ($1, $2, $3, $4, $5, $6)
		 RETURNING id, company_id, tracking_no, sender_name, recipient_city,
		           recipient_name, recipient_address, status, is_fragile, created_at`,
		companyID, trackingNo, senderName, recipientName, recipientCity, recipientAddress,
	).Scan(&s.ID, &s.CompanyID, &s.TrackingNo, &s.SenderName,
		&s.RecipientCity, &s.RecipientName, &s.RecipientAddress,
		&s.Status, &s.IsFragile, &s.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("create shipment: %w", err)
	}
	return &s, nil
}

func (r *CargoRepo) GetShipmentByTracking(ctx context.Context, trackingNo string) (*domain.CargoShipment, error) {
	var s domain.CargoShipment
	err := r.pool.QueryRow(ctx,
		`SELECT id, company_id, tracking_no, sender_name, recipient_city,
		        recipient_name, recipient_address, status, is_fragile, created_at
		 FROM cargo_shipments WHERE tracking_no = $1`, trackingNo,
	).Scan(&s.ID, &s.CompanyID, &s.TrackingNo, &s.SenderName,
		&s.RecipientCity, &s.RecipientName, &s.RecipientAddress,
		&s.Status, &s.IsFragile, &s.CreatedAt)
	if err != nil {
		return nil, err
	}
	return &s, nil
}
