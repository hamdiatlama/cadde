package postgres

import (
	"context"
	"fmt"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/web-platform/backend/internal/domain"
)

type RideRepo struct {
	pool *pgxpool.Pool
}

func NewRideRepo(pool *pgxpool.Pool) *RideRepo {
	return &RideRepo{pool: pool}
}

func (r *RideRepo) Create(ctx context.Context, ride *domain.Ride) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO rides (customer_id, status, pickup_address, pickup_latitude, pickup_longitude,
		 dropoff_address, dropoff_latitude, dropoff_longitude, estimated_fare, surge_multiplier,
		 optimal_distance_km, eta_at_booking, payment_method, notes)
		 VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14)
		 RETURNING id, created_at, updated_at`,
		ride.CustomerID, ride.Status, ride.PickupAddress, ride.PickupLatitude, ride.PickupLongitude,
		ride.DropoffAddress, ride.DropoffLatitude, ride.DropoffLongitude,
		ride.EstimatedFare, ride.SurgeMultiplier, ride.OptimalDistanceKm, ride.EtaAtBooking,
		ride.PaymentMethod, ride.Notes,
	).Scan(&ride.ID, &ride.CreatedAt, &ride.UpdatedAt)
}

func (r *RideRepo) GetByID(ctx context.Context, id int) (*domain.Ride, error) {
	ride := &domain.Ride{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, customer_id, driver_id, status, pickup_address, pickup_latitude, pickup_longitude,
		 dropoff_address, dropoff_latitude, dropoff_longitude, estimated_fare, actual_fare,
		 surge_multiplier, optimal_distance_km, eta_at_booking, payment_method, COALESCE(notes,''),
		 rating, COALESCE(feedback,''), started_at, completed_at, cancelled_at, COALESCE(cancel_reason,''),
		 created_at, updated_at
		 FROM rides WHERE id=$1`, id,
	).Scan(&ride.ID, &ride.CustomerID, &ride.DriverID, &ride.Status,
		&ride.PickupAddress, &ride.PickupLatitude, &ride.PickupLongitude,
		&ride.DropoffAddress, &ride.DropoffLatitude, &ride.DropoffLongitude,
		&ride.EstimatedFare, &ride.ActualFare, &ride.SurgeMultiplier,
		&ride.OptimalDistanceKm, &ride.EtaAtBooking, &ride.PaymentMethod, &ride.Notes,
		&ride.Rating, &ride.Feedback, &ride.StartedAt, &ride.CompletedAt,
		&ride.CancelledAt, &ride.CancelReason, &ride.CreatedAt, &ride.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("get ride: %w", err)
	}
	return ride, nil
}
