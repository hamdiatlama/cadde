package postgres

import (
	"context"
	"fmt"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/web-platform/backend/internal/domain"
)

type CourierRepo struct {
	pool *pgxpool.Pool
}

func NewCourierRepo(pool *pgxpool.Pool) *CourierRepo {
	return &CourierRepo{pool: pool}
}

func (r *CourierRepo) GetByUserID(ctx context.Context, userID int) (*domain.Courier, error) {
	c := &domain.Courier{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, user_id, vehicle_type, COALESCE(plate_number,''), is_available, status,
		 current_latitude, current_longitude, current_speed_kmh, current_heading,
		 last_location_update, rating, total_deliveries,
		 COALESCE(gps_spoofing_score,0), COALESCE(consecutive_anomalies,0), created_at
		 FROM couriers WHERE user_id=$1`, userID,
	).Scan(&c.ID, &c.UserID, &c.VehicleType, &c.PlateNumber, &c.IsAvailable, &c.Status,
		&c.CurrentLatitude, &c.CurrentLongitude, &c.CurrentSpeedKmh, &c.CurrentHeading,
		&c.LastLocationUpdate, &c.Rating, &c.TotalDeliveries,
		&c.GPSPpoofingScore, &c.ConsecutiveAnomalies, &c.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("get courier: %w", err)
	}
	return c, nil
}

func (r *CourierRepo) GetAvailableNearby(ctx context.Context, lat, lon, radiusKm float64) ([]*domain.Courier, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, user_id, vehicle_type, COALESCE(plate_number,''), is_available, status,
		 current_latitude, current_longitude, current_speed_kmh, current_heading,
		 last_location_update, rating, total_deliveries,
		 COALESCE(gps_spoofing_score,0), COALESCE(consecutive_anomalies,0), created_at
		 FROM couriers
		 WHERE is_available=true AND status='online'
		 AND earth_distance(ll_to_earth(current_latitude, current_longitude), ll_to_earth($1,$2)) < $3*1000`,
		lat, lon, radiusKm)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var couriers []*domain.Courier
	for rows.Next() {
		c := &domain.Courier{}
		if err := rows.Scan(&c.ID, &c.UserID, &c.VehicleType, &c.PlateNumber, &c.IsAvailable, &c.Status,
			&c.CurrentLatitude, &c.CurrentLongitude, &c.CurrentSpeedKmh, &c.CurrentHeading,
			&c.LastLocationUpdate, &c.Rating, &c.TotalDeliveries,
			&c.GPSPpoofingScore, &c.ConsecutiveAnomalies, &c.CreatedAt); err != nil {
			return nil, err
		}
		couriers = append(couriers, c)
	}
	return couriers, nil
}

func (r *CourierRepo) UpdateLocation(ctx context.Context, courierID int, lat, lon, speed, heading float64) error {
	_, err := r.pool.Exec(ctx,
		`UPDATE couriers SET current_latitude=$1, current_longitude=$2,
		 current_speed_kmh=$3, current_heading=$4, last_location_update=NOW()
		 WHERE id=$5`,
		lat, lon, speed, heading, courierID)
	return err
}
