package postgres

import (
	"context"
	"fmt"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/web-platform/backend/internal/domain"
)

type VehicleRepo struct {
	pool *pgxpool.Pool
}

func NewVehicleRepo(pool *pgxpool.Pool) *VehicleRepo {
	return &VehicleRepo{pool: pool}
}

// ── Brand ─────────────────────────────────────────────────

func (r *VehicleRepo) CreateBrand(ctx context.Context, b *domain.VehicleBrand) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO vehicle_brands (name, slug, country, logo_url, is_active)
		 VALUES ($1,$2,$3,$4,$5) RETURNING id, created_at`,
		b.Name, b.Slug, b.Country, b.LogoURL, b.IsActive,
	).Scan(&b.ID, &b.CreatedAt)
}

func (r *VehicleRepo) ListBrands(ctx context.Context) ([]*domain.VehicleBrand, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, name, slug, COALESCE(country,''), logo_url, is_active, created_at FROM vehicle_brands ORDER BY name`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.VehicleBrand
	for rows.Next() {
		b := &domain.VehicleBrand{}
		if err := rows.Scan(&b.ID, &b.Name, &b.Slug, &b.Country, &b.LogoURL, &b.IsActive, &b.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, b)
	}
	return list, nil
}

func (r *VehicleRepo) GetBrand(ctx context.Context, id int) (*domain.VehicleBrand, error) {
	b := &domain.VehicleBrand{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, name, slug, COALESCE(country,''), logo_url, is_active, created_at FROM vehicle_brands WHERE id=$1`, id,
	).Scan(&b.ID, &b.Name, &b.Slug, &b.Country, &b.LogoURL, &b.IsActive, &b.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("get brand: %w", err)
	}
	return b, nil
}

// ── Model ─────────────────────────────────────────────────

func (r *VehicleRepo) CreateModel(ctx context.Context, m *domain.VehicleModel) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO vehicle_models (brand_id, name, segment_code, production_start, production_end, is_active)
		 VALUES ($1,$2,$3,$4,$5,$6) RETURNING id, created_at`,
		m.BrandID, m.Name, m.SegmentCode, m.ProductionStart, m.ProductionEnd, m.IsActive,
	).Scan(&m.ID, &m.CreatedAt)
}

func (r *VehicleRepo) ListModels(ctx context.Context, brandID *int) ([]*domain.VehicleModel, error) {
	var rows interface{ Scan(...interface{}) error; Close() }

	if brandID != nil {
		rrows, err := r.pool.Query(ctx,
			`SELECT id, brand_id, name, segment_code, production_start, production_end, is_active, created_at FROM vehicle_models WHERE brand_id=$1 ORDER BY name`, *brandID)
		if err != nil {
			return nil, err
		}
		rows = rrows
	} else {
		rrows, err := r.pool.Query(ctx,
			`SELECT id, brand_id, name, segment_code, production_start, production_end, is_active, created_at FROM vehicle_models ORDER BY name`)
		if err != nil {
			return nil, err
		}
		rows = rrows
	}
	defer rows.Close()

	var list []*domain.VehicleModel
	for rows.Next() {
		m := &domain.VehicleModel{}
		if err := rows.Scan(&m.ID, &m.BrandID, &m.Name, &m.SegmentCode, &m.ProductionStart, &m.ProductionEnd, &m.IsActive, &m.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, m)
	}
	return list, nil
}

func (r *VehicleRepo) GetModel(ctx context.Context, id int) (*domain.VehicleModel, error) {
	m := &domain.VehicleModel{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, brand_id, name, segment_code, production_start, production_end, is_active, created_at FROM vehicle_models WHERE id=$1`, id,
	).Scan(&m.ID, &m.BrandID, &m.Name, &m.SegmentCode, &m.ProductionStart, &m.ProductionEnd, &m.IsActive, &m.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("get model: %w", err)
	}
	return m, nil
}

// ── Categories / Segments / BodyTypes ─────────────────────

func (r *VehicleRepo) ListCategories(ctx context.Context) ([]*domain.VehicleCategory, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, name, slug, parent_id, sort_order, created_at FROM vehicle_categories ORDER BY sort_order`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.VehicleCategory
	for rows.Next() {
		c := &domain.VehicleCategory{}
		if err := rows.Scan(&c.ID, &c.Name, &c.Slug, &c.ParentID, &c.SortOrder, &c.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, c)
	}
	return list, nil
}

func (r *VehicleRepo) ListSegments(ctx context.Context) ([]*domain.VehicleSegment, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT code, name, COALESCE(description,''), created_at FROM vehicle_segments ORDER BY name`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.VehicleSegment
	for rows.Next() {
		s := &domain.VehicleSegment{}
		if err := rows.Scan(&s.Code, &s.Name, &s.Description, &s.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, s)
	}
	return list, nil
}

func (r *VehicleRepo) ListBodyTypes(ctx context.Context) ([]*domain.BodyType, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, name, slug, created_at FROM body_types ORDER BY name`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.BodyType
	for rows.Next() {
		b := &domain.BodyType{}
		if err := rows.Scan(&b.ID, &b.Name, &b.Slug, &b.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, b)
	}
	return list, nil
}

// ── Model Years ───────────────────────────────────────────

func (r *VehicleRepo) ListModelYears(ctx context.Context, modelID int) ([]*domain.VehicleModelYear, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, model_id, year, trim_name, engine_volume, horsepower, fuel_type, transmission, created_at
		 FROM vehicle_model_years WHERE model_id=$1 ORDER BY year DESC`, modelID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.VehicleModelYear
	for rows.Next() {
		y := &domain.VehicleModelYear{}
		if err := rows.Scan(&y.ID, &y.ModelID, &y.Year, &y.TrimName, &y.EngineVolume, &y.Horsepower, &y.FuelType, &y.Transmission, &y.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, y)
	}
	return list, nil
}

// ── Feature Groups & Features ─────────────────────────────

func (r *VehicleRepo) ListFeatureGroups(ctx context.Context) ([]*domain.FeatureGroup, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, name, slug, sort_order, created_at FROM feature_groups ORDER BY sort_order`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.FeatureGroup
	for rows.Next() {
		fg := &domain.FeatureGroup{}
		if err := rows.Scan(&fg.ID, &fg.Name, &fg.Slug, &fg.SortOrder, &fg.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, fg)
	}
	return list, nil
}

func (r *VehicleRepo) ListFeatures(ctx context.Context, groupID *int) ([]*domain.Feature, error) {
	var rows interface{ Scan(...interface{}) error; Close() }

	if groupID != nil {
		rrows, err := r.pool.Query(ctx,
			`SELECT id, group_id, name, slug, created_at FROM features WHERE group_id=$1 ORDER BY name`, *groupID)
		if err != nil {
			return nil, err
		}
		rows = rrows
	} else {
		rrows, err := r.pool.Query(ctx,
			`SELECT id, group_id, name, slug, created_at FROM features ORDER BY name`)
		if err != nil {
			return nil, err
		}
		rows = rrows
	}
	defer rows.Close()

	var list []*domain.Feature
	for rows.Next() {
		f := &domain.Feature{}
		if err := rows.Scan(&f.ID, &f.GroupID, &f.Name, &f.Slug, &f.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, f)
	}
	return list, nil
}

func (r *VehicleRepo) CreateFeatureGroup(ctx context.Context, fg *domain.FeatureGroup) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO feature_groups (name, slug, sort_order) VALUES ($1,$2,$3) RETURNING id, created_at`,
		fg.Name, fg.Slug, fg.SortOrder,
	).Scan(&fg.ID, &fg.CreatedAt)
}

func (r *VehicleRepo) CreateFeature(ctx context.Context, f *domain.Feature) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO features (group_id, name, slug) VALUES ($1,$2,$3) RETURNING id, created_at`,
		f.GroupID, f.Name, f.Slug,
	).Scan(&f.ID, &f.CreatedAt)
}
