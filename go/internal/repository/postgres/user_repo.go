package postgres

import (
	"context"
	"fmt"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/web-platform/backend/internal/domain"
)

type UserRepo struct {
	pool *pgxpool.Pool
}

func NewUserRepo(pool *pgxpool.Pool) *UserRepo {
	return &UserRepo{pool: pool}
}

func (r *UserRepo) Create(ctx context.Context, u *domain.User) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO users (email, phone, password_hash, full_name, role, is_active, is_verified)
		 VALUES ($1,$2,$3,$4,$5,$6,$7)
		 RETURNING id, created_at, updated_at`,
		u.Email, u.Phone, u.PasswordHash, u.FullName, u.Role, u.IsActive, u.IsVerified,
	).Scan(&u.ID, &u.CreatedAt, &u.UpdatedAt)
}

func (r *UserRepo) GetByID(ctx context.Context, id int) (*domain.User, error) {
	u := &domain.User{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, email, phone, password_hash, full_name, role, is_active, is_verified,
		        COALESCE(avatar_url,''), created_at, updated_at
		 FROM users WHERE id=$1`, id,
	).Scan(&u.ID, &u.Email, &u.Phone, &u.PasswordHash, &u.FullName, &u.Role,
		&u.IsActive, &u.IsVerified, &u.AvatarURL, &u.CreatedAt, &u.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("get user: %w", err)
	}
	return u, nil
}

func (r *UserRepo) GetByEmail(ctx context.Context, email string) (*domain.User, error) {
	u := &domain.User{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, email, phone, password_hash, full_name, role, is_active, is_verified,
		        COALESCE(avatar_url,''), created_at, updated_at
		 FROM users WHERE email=$1`, email,
	).Scan(&u.ID, &u.Email, &u.Phone, &u.PasswordHash, &u.FullName, &u.Role,
		&u.IsActive, &u.IsVerified, &u.AvatarURL, &u.CreatedAt, &u.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("get user by email: %w", err)
	}
	return u, nil
}

func (r *UserRepo) GetByPhone(ctx context.Context, phone string) (*domain.User, error) {
	u := &domain.User{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, email, phone, password_hash, full_name, role, is_active, is_verified,
		        COALESCE(avatar_url,''), created_at, updated_at
		 FROM users WHERE phone=$1`, phone,
	).Scan(&u.ID, &u.Email, &u.Phone, &u.PasswordHash, &u.FullName, &u.Role,
		&u.IsActive, &u.IsVerified, &u.AvatarURL, &u.CreatedAt, &u.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("get user by phone: %w", err)
	}
	return u, nil
}

func (r *UserRepo) Update(ctx context.Context, u *domain.User) error {
	_, err := r.pool.Exec(ctx,
		`UPDATE users SET email=$1, phone=$2, full_name=$3, avatar_url=$4,
		 is_active=$5, is_verified=$6 WHERE id=$7`,
		u.Email, u.Phone, u.FullName, u.AvatarURL, u.IsActive, u.IsVerified, u.ID)
	return err
}

func (r *UserRepo) UpdatePassword(ctx context.Context, userID int, hash string) error {
	_, err := r.pool.Exec(ctx, `UPDATE users SET password_hash=$1 WHERE id=$2`, hash, userID)
	return err
}
