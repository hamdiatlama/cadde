package postgres

import (
	"context"
	"fmt"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/web-platform/backend/internal/domain"
)

type ExpertRepo struct {
	pool *pgxpool.Pool
}

func NewExpertRepo(pool *pgxpool.Pool) *ExpertRepo {
	return &ExpertRepo{pool: pool}
}

// ── Company ───────────────────────────────────────────────

func (r *ExpertRepo) CreateCompany(ctx context.Context, c *domain.ExpertCompany) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO expert_companies (name, slug, address, phone, email, website, logo_url, description, is_active)
		 VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9) RETURNING id, created_at`,
		c.Name, c.Slug, c.Address, c.Phone, c.Email, c.Website, c.LogoURL, c.Description, c.IsActive,
	).Scan(&c.ID, &c.CreatedAt)
}

func (r *ExpertRepo) ListCompanies(ctx context.Context) ([]*domain.ExpertCompany, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, name, slug, COALESCE(address,''), COALESCE(phone,''), COALESCE(email,''), COALESCE(website,''), logo_url, COALESCE(description,''), is_active, created_at, updated_at
		 FROM expert_companies ORDER BY name`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ExpertCompany
	for rows.Next() {
		c := &domain.ExpertCompany{}
		if err := rows.Scan(&c.ID, &c.Name, &c.Slug, &c.Address, &c.Phone, &c.Email, &c.Website, &c.LogoURL, &c.Description, &c.IsActive, &c.CreatedAt, &c.UpdatedAt); err != nil {
			return nil, err
		}
		list = append(list, c)
	}
	return list, nil
}

// ── Expert ────────────────────────────────────────────────

func (r *ExpertRepo) CreateExpert(ctx context.Context, e *domain.Expert) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO experts (company_id, user_id, first_name, last_name, title, email, phone, bio, avatar_url, is_active)
		 VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10) RETURNING id, created_at`,
		e.CompanyID, e.UserID, e.FirstName, e.LastName, e.Title, e.Email, e.Phone, e.Bio, e.AvatarURL, e.IsActive,
	).Scan(&e.ID, &e.CreatedAt)
}

func (r *ExpertRepo) ListExperts(ctx context.Context, companyID *int) ([]*domain.Expert, error) {
	var rows interface{ Scan(...interface{}) error; Close() }
	if companyID != nil {
		rrows, err := r.pool.Query(ctx,
			`SELECT id, company_id, user_id, first_name, last_name, COALESCE(title,''), COALESCE(email,''), COALESCE(phone,''), COALESCE(bio,''), avatar_url, is_active, created_at, updated_at
			 FROM experts WHERE company_id=$1 ORDER BY first_name, last_name`, *companyID)
		if err != nil {
			return nil, err
		}
		rows = rrows
	} else {
		rrows, err := r.pool.Query(ctx,
			`SELECT id, company_id, user_id, first_name, last_name, COALESCE(title,''), COALESCE(email,''), COALESCE(phone,''), COALESCE(bio,''), avatar_url, is_active, created_at, updated_at
			 FROM experts ORDER BY first_name, last_name`)
		if err != nil {
			return nil, err
		}
		rows = rrows
	}
	defer rows.Close()

	var list []*domain.Expert
	for rows.Next() {
		e := &domain.Expert{}
		if err := rows.Scan(&e.ID, &e.CompanyID, &e.UserID, &e.FirstName, &e.LastName, &e.Title, &e.Email, &e.Phone, &e.Bio, &e.AvatarURL, &e.IsActive, &e.CreatedAt, &e.UpdatedAt); err != nil {
			return nil, err
		}
		list = append(list, e)
	}
	return list, nil
}

func (r *ExpertRepo) GetExpert(ctx context.Context, id int) (*domain.Expert, error) {
	e := &domain.Expert{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, company_id, user_id, first_name, last_name, COALESCE(title,''), COALESCE(email,''), COALESCE(phone,''), COALESCE(bio,''), avatar_url, is_active, created_at, updated_at
		 FROM experts WHERE id=$1`, id,
	).Scan(&e.ID, &e.CompanyID, &e.UserID, &e.FirstName, &e.LastName, &e.Title, &e.Email, &e.Phone, &e.Bio, &e.AvatarURL, &e.IsActive, &e.CreatedAt, &e.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("get expert: %w", err)
	}
	return e, nil
}

// ── Package ───────────────────────────────────────────────

func (r *ExpertRepo) CreatePackage(ctx context.Context, p *domain.ExpertPackage) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO expert_packages (company_id, name, slug, description, price, duration_days, features, is_active)
		 VALUES ($1,$2,$3,$4,$5,$6,$7,$8) RETURNING id, created_at`,
		p.CompanyID, p.Name, p.Slug, p.Description, p.Price, p.DurationDays, p.Features, p.IsActive,
	).Scan(&p.ID, &p.CreatedAt)
}

func (r *ExpertRepo) ListPackages(ctx context.Context, companyID *int) ([]*domain.ExpertPackage, error) {
	var rows interface{ Scan(...interface{}) error; Close() }
	if companyID != nil {
		rrows, err := r.pool.Query(ctx,
			`SELECT id, company_id, name, slug, COALESCE(description,''), price, duration_days, COALESCE(features,''), is_active, created_at
			 FROM expert_packages WHERE company_id=$1 ORDER BY price`, *companyID)
		if err != nil {
			return nil, err
		}
		rows = rrows
	} else {
		rrows, err := r.pool.Query(ctx,
			`SELECT id, company_id, name, slug, COALESCE(description,''), price, duration_days, COALESCE(features,''), is_active, created_at
			 FROM expert_packages ORDER BY price`)
		if err != nil {
			return nil, err
		}
		rows = rrows
	}
	defer rows.Close()
	var list []*domain.ExpertPackage
	for rows.Next() {
		p := &domain.ExpertPackage{}
		if err := rows.Scan(&p.ID, &p.CompanyID, &p.Name, &p.Slug, &p.Description, &p.Price, &p.DurationDays, &p.Features, &p.IsActive, &p.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, p)
	}
	return list, nil
}

// ── Vehicle ───────────────────────────────────────────────

func (r *ExpertRepo) CreateVehicle(ctx context.Context, v *domain.ExpertVehicle) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO expert_vehicles (report_id, expert_id, plate, chassis_number, brand_id, model_id, model_year_id, year)
		 VALUES ($1,$2,$3,$4,$5,$6,$7,$8) RETURNING id, created_at`,
		v.ReportID, v.ExpertID, v.Plate, v.ChassisNumber, v.BrandID, v.ModelID, v.ModelYearID, v.Year,
	).Scan(&v.ID, &v.CreatedAt)
}

func (r *ExpertRepo) ListVehicles(ctx context.Context, plate, chassisNumber *string) ([]*domain.ExpertVehicle, error) {
	var rows interface{ Scan(...interface{}) error; Close() }
	if plate != nil {
		rrows, err := r.pool.Query(ctx,
			`SELECT id, report_id, expert_id, COALESCE(plate,''), COALESCE(chassis_number,''), brand_id, model_id, model_year_id, year, created_at
			 FROM expert_vehicles WHERE plate=$1 ORDER BY created_at DESC`, *plate)
		if err != nil {
			return nil, err
		}
		rows = rrows
	} else if chassisNumber != nil {
		rrows, err := r.pool.Query(ctx,
			`SELECT id, report_id, expert_id, COALESCE(plate,''), COALESCE(chassis_number,''), brand_id, model_id, model_year_id, year, created_at
			 FROM expert_vehicles WHERE chassis_number=$1 ORDER BY created_at DESC`, *chassisNumber)
		if err != nil {
			return nil, err
		}
		rows = rrows
	} else {
		rrows, err := r.pool.Query(ctx,
			`SELECT id, report_id, expert_id, COALESCE(plate,''), COALESCE(chassis_number,''), brand_id, model_id, model_year_id, year, created_at
			 FROM expert_vehicles ORDER BY created_at DESC`)
		if err != nil {
			return nil, err
		}
		rows = rrows
	}
	defer rows.Close()

	var list []*domain.ExpertVehicle
	for rows.Next() {
		v := &domain.ExpertVehicle{}
		if err := rows.Scan(&v.ID, &v.ReportID, &v.ExpertID, &v.Plate, &v.ChassisNumber, &v.BrandID, &v.ModelID, &v.ModelYearID, &v.Year, &v.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, v)
	}
	return list, nil
}

// ── Report ────────────────────────────────────────────────

func (r *ExpertRepo) CreateReport(ctx context.Context, rep *domain.ExpertReport) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO expert_reports (expert_vehicle_id, expert_id, company_id, status, report_type, notes, score)
		 VALUES ($1,$2,$3,$4,$5,$6,$7) RETURNING id, created_at`,
		rep.ExpertVehicleID, rep.ExpertID, rep.CompanyID, rep.Status, rep.ReportType, rep.Notes, rep.Score,
	).Scan(&rep.ID, &rep.CreatedAt)
}

func (r *ExpertRepo) ListReports(ctx context.Context, companyID, expertID *int) ([]*domain.ExpertReport, error) {
	var rows interface{ Scan(...interface{}) error; Close() }
	if companyID != nil {
		rrows, err := r.pool.Query(ctx,
			`SELECT id, expert_vehicle_id, expert_id, company_id, status, COALESCE(report_type,''), COALESCE(notes,''), score, created_at, updated_at
			 FROM expert_reports WHERE company_id=$1 ORDER BY created_at DESC`, *companyID)
		if err != nil {
			return nil, err
		}
		rows = rrows
	} else if expertID != nil {
		rrows, err := r.pool.Query(ctx,
			`SELECT id, expert_vehicle_id, expert_id, company_id, status, COALESCE(report_type,''), COALESCE(notes,''), score, created_at, updated_at
			 FROM expert_reports WHERE expert_id=$1 ORDER BY created_at DESC`, *expertID)
		if err != nil {
			return nil, err
		}
		rows = rrows
	} else {
		rrows, err := r.pool.Query(ctx,
			`SELECT id, expert_vehicle_id, expert_id, company_id, status, COALESCE(report_type,''), COALESCE(notes,''), score, created_at, updated_at
			 FROM expert_reports ORDER BY created_at DESC`)
		if err != nil {
			return nil, err
		}
		rows = rrows
	}
	defer rows.Close()

	var list []*domain.ExpertReport
	for rows.Next() {
		rep := &domain.ExpertReport{}
		if err := rows.Scan(&rep.ID, &rep.ExpertVehicleID, &rep.ExpertID, &rep.CompanyID, &rep.Status, &rep.ReportType, &rep.Notes, &rep.Score, &rep.CreatedAt, &rep.UpdatedAt); err != nil {
			return nil, err
		}
		list = append(list, rep)
	}
	return list, nil
}

func (r *ExpertRepo) GetReport(ctx context.Context, id int) (*domain.ExpertReport, error) {
	rep := &domain.ExpertReport{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, expert_vehicle_id, expert_id, company_id, status, COALESCE(report_type,''), COALESCE(notes,''), score, created_at, updated_at
		 FROM expert_reports WHERE id=$1`, id,
	).Scan(&rep.ID, &rep.ExpertVehicleID, &rep.ExpertID, &rep.CompanyID, &rep.Status, &rep.ReportType, &rep.Notes, &rep.Score, &rep.CreatedAt, &rep.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("get report: %w", err)
	}
	return rep, nil
}

func (r *ExpertRepo) UpdateReportStatus(ctx context.Context, id int, status string) error {
	_, err := r.pool.Exec(ctx, `UPDATE expert_reports SET status=$1, updated_at=NOW() WHERE id=$2`, status, id)
	return err
}

func (r *ExpertRepo) ApproveReport(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, `UPDATE expert_reports SET status='approved', updated_at=NOW() WHERE id=$1`, id)
	return err
}

func (r *ExpertRepo) DeleteReport(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM expert_reports WHERE id=$1`, id)
	return err
}

// ── Panel Measurements ────────────────────────────────────

func (r *ExpertRepo) CreatePanelMeasurements(ctx context.Context, items []*domain.ExpertPanelMeasurement) error {
	for _, item := range items {
		if err := r.pool.QueryRow(ctx,
			`INSERT INTO expert_panel_measurements (report_id, panel_name, measurement_type, value, unit, notes)
			 VALUES ($1,$2,$3,$4,$5,$6) RETURNING id, created_at`,
			item.ReportID, item.PanelName, item.MeasurementType, item.Value, item.Unit, item.Notes,
		).Scan(&item.ID, &item.CreatedAt); err != nil {
			return err
		}
	}
	return nil
}

func (r *ExpertRepo) GetPanelMeasurements(ctx context.Context, reportID int) ([]*domain.ExpertPanelMeasurement, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, report_id, panel_name, measurement_type, value, COALESCE(unit,''), COALESCE(notes,''), created_at
		 FROM expert_panel_measurements WHERE report_id=$1 ORDER BY id`, reportID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ExpertPanelMeasurement
	for rows.Next() {
		m := &domain.ExpertPanelMeasurement{}
		if err := rows.Scan(&m.ID, &m.ReportID, &m.PanelName, &m.MeasurementType, &m.Value, &m.Unit, &m.Notes, &m.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, m)
	}
	return list, nil
}

func (r *ExpertRepo) UpdatePanelMeasurements(ctx context.Context, reportID int, items []*domain.ExpertPanelMeasurement) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM expert_panel_measurements WHERE report_id=$1`, reportID)
	if err != nil {
		return err
	}
	return r.CreatePanelMeasurements(ctx, items)
}

// ── Interior Checks ───────────────────────────────────────

func (r *ExpertRepo) CreateInteriorChecks(ctx context.Context, items []*domain.ExpertInteriorCheck) error {
	for _, item := range items {
		if err := r.pool.QueryRow(ctx,
			`INSERT INTO expert_interior_checks (report_id, item_name, condition, notes, score)
			 VALUES ($1,$2,$3,$4,$5) RETURNING id, created_at`,
			item.ReportID, item.ItemName, item.Condition, item.Notes, item.Score,
		).Scan(&item.ID, &item.CreatedAt); err != nil {
			return err
		}
	}
	return nil
}

func (r *ExpertRepo) GetInteriorChecks(ctx context.Context, reportID int) ([]*domain.ExpertInteriorCheck, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, report_id, item_name, condition, COALESCE(notes,''), score, created_at
		 FROM expert_interior_checks WHERE report_id=$1 ORDER BY id`, reportID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ExpertInteriorCheck
	for rows.Next() {
		c := &domain.ExpertInteriorCheck{}
		if err := rows.Scan(&c.ID, &c.ReportID, &c.ItemName, &c.Condition, &c.Notes, &c.Score, &c.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, c)
	}
	return list, nil
}

func (r *ExpertRepo) UpdateInteriorChecks(ctx context.Context, reportID int, items []*domain.ExpertInteriorCheck) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM expert_interior_checks WHERE report_id=$1`, reportID)
	if err != nil {
		return err
	}
	return r.CreateInteriorChecks(ctx, items)
}

// ── Exterior Checks ───────────────────────────────────────

func (r *ExpertRepo) CreateExteriorChecks(ctx context.Context, items []*domain.ExpertExteriorCheck) error {
	for _, item := range items {
		if err := r.pool.QueryRow(ctx,
			`INSERT INTO expert_exterior_checks (report_id, item_name, condition, notes, score)
			 VALUES ($1,$2,$3,$4,$5) RETURNING id, created_at`,
			item.ReportID, item.ItemName, item.Condition, item.Notes, item.Score,
		).Scan(&item.ID, &item.CreatedAt); err != nil {
			return err
		}
	}
	return nil
}

func (r *ExpertRepo) GetExteriorChecks(ctx context.Context, reportID int) ([]*domain.ExpertExteriorCheck, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, report_id, item_name, condition, COALESCE(notes,''), score, created_at
		 FROM expert_exterior_checks WHERE report_id=$1 ORDER BY id`, reportID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ExpertExteriorCheck
	for rows.Next() {
		c := &domain.ExpertExteriorCheck{}
		if err := rows.Scan(&c.ID, &c.ReportID, &c.ItemName, &c.Condition, &c.Notes, &c.Score, &c.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, c)
	}
	return list, nil
}

func (r *ExpertRepo) UpdateExteriorChecks(ctx context.Context, reportID int, items []*domain.ExpertExteriorCheck) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM expert_exterior_checks WHERE report_id=$1`, reportID)
	if err != nil {
		return err
	}
	return r.CreateExteriorChecks(ctx, items)
}

// ── Mechanical Checks ─────────────────────────────────────

func (r *ExpertRepo) CreateMechanicalChecks(ctx context.Context, items []*domain.ExpertMechanicalCheck) error {
	for _, item := range items {
		if err := r.pool.QueryRow(ctx,
			`INSERT INTO expert_mechanical_checks (report_id, item_name, condition, notes, score)
			 VALUES ($1,$2,$3,$4,$5) RETURNING id, created_at`,
			item.ReportID, item.ItemName, item.Condition, item.Notes, item.Score,
		).Scan(&item.ID, &item.CreatedAt); err != nil {
			return err
		}
	}
	return nil
}

func (r *ExpertRepo) GetMechanicalChecks(ctx context.Context, reportID int) ([]*domain.ExpertMechanicalCheck, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, report_id, item_name, condition, COALESCE(notes,''), score, created_at
		 FROM expert_mechanical_checks WHERE report_id=$1 ORDER BY id`, reportID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ExpertMechanicalCheck
	for rows.Next() {
		c := &domain.ExpertMechanicalCheck{}
		if err := rows.Scan(&c.ID, &c.ReportID, &c.ItemName, &c.Condition, &c.Notes, &c.Score, &c.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, c)
	}
	return list, nil
}

func (r *ExpertRepo) UpdateMechanicalChecks(ctx context.Context, reportID int, items []*domain.ExpertMechanicalCheck) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM expert_mechanical_checks WHERE report_id=$1`, reportID)
	if err != nil {
		return err
	}
	return r.CreateMechanicalChecks(ctx, items)
}

// ── Electronic Checks ─────────────────────────────────────

func (r *ExpertRepo) CreateElectronicChecks(ctx context.Context, items []*domain.ExpertElectronicCheck) error {
	for _, item := range items {
		if err := r.pool.QueryRow(ctx,
			`INSERT INTO expert_electronic_checks (report_id, item_name, condition, notes, score)
			 VALUES ($1,$2,$3,$4,$5) RETURNING id, created_at`,
			item.ReportID, item.ItemName, item.Condition, item.Notes, item.Score,
		).Scan(&item.ID, &item.CreatedAt); err != nil {
			return err
		}
	}
	return nil
}

func (r *ExpertRepo) GetElectronicChecks(ctx context.Context, reportID int) ([]*domain.ExpertElectronicCheck, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, report_id, item_name, condition, COALESCE(notes,''), score, created_at
		 FROM expert_electronic_checks WHERE report_id=$1 ORDER BY id`, reportID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ExpertElectronicCheck
	for rows.Next() {
		c := &domain.ExpertElectronicCheck{}
		if err := rows.Scan(&c.ID, &c.ReportID, &c.ItemName, &c.Condition, &c.Notes, &c.Score, &c.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, c)
	}
	return list, nil
}

func (r *ExpertRepo) UpdateElectronicChecks(ctx context.Context, reportID int, items []*domain.ExpertElectronicCheck) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM expert_electronic_checks WHERE report_id=$1`, reportID)
	if err != nil {
		return err
	}
	return r.CreateElectronicChecks(ctx, items)
}

// ── Tire Checks ───────────────────────────────────────────

func (r *ExpertRepo) CreateTireChecks(ctx context.Context, items []*domain.ExpertTireCheck) error {
	for _, item := range items {
		if err := r.pool.QueryRow(ctx,
			`INSERT INTO expert_tire_checks (report_id, tire_position, brand, tread_depth, pressure, condition, notes)
			 VALUES ($1,$2,$3,$4,$5,$6,$7) RETURNING id, created_at`,
			item.ReportID, item.TirePosition, item.Brand, item.TreadDepth, item.Pressure, item.Condition, item.Notes,
		).Scan(&item.ID, &item.CreatedAt); err != nil {
			return err
		}
	}
	return nil
}

func (r *ExpertRepo) GetTireChecks(ctx context.Context, reportID int) ([]*domain.ExpertTireCheck, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, report_id, tire_position, COALESCE(brand,''), tread_depth, pressure, COALESCE(condition,''), COALESCE(notes,''), created_at
		 FROM expert_tire_checks WHERE report_id=$1 ORDER BY id`, reportID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ExpertTireCheck
	for rows.Next() {
		t := &domain.ExpertTireCheck{}
		if err := rows.Scan(&t.ID, &t.ReportID, &t.TirePosition, &t.Brand, &t.TreadDepth, &t.Pressure, &t.Condition, &t.Notes, &t.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, t)
	}
	return list, nil
}

func (r *ExpertRepo) UpdateTireChecks(ctx context.Context, reportID int, items []*domain.ExpertTireCheck) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM expert_tire_checks WHERE report_id=$1`, reportID)
	if err != nil {
		return err
	}
	return r.CreateTireChecks(ctx, items)
}

// ── Tramer Record ─────────────────────────────────────────

func (r *ExpertRepo) CreateTramerRecord(ctx context.Context, tr *domain.ExpertTramerRecord) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO expert_tramer_records (report_id, record_type, source, description)
		 VALUES ($1,$2,$3,$4) RETURNING id, created_at`,
		tr.ReportID, tr.RecordType, tr.Source, tr.Description,
	).Scan(&tr.ID, &tr.CreatedAt)
}

func (r *ExpertRepo) GetTramerRecord(ctx context.Context, reportID int) ([]*domain.ExpertTramerRecord, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, report_id, record_type, COALESCE(source,''), COALESCE(description,''), created_at
		 FROM expert_tramer_records WHERE report_id=$1 ORDER BY id`, reportID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ExpertTramerRecord
	for rows.Next() {
		tr := &domain.ExpertTramerRecord{}
		if err := rows.Scan(&tr.ID, &tr.ReportID, &tr.RecordType, &tr.Source, &tr.Description, &tr.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, tr)
	}
	return list, nil
}

func (r *ExpertRepo) UpdateTramerRecord(ctx context.Context, reportID int, items []*domain.ExpertTramerRecord) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM expert_tramer_records WHERE report_id=$1`, reportID)
	if err != nil {
		return err
	}
	for _, item := range items {
		if err := r.CreateTramerRecord(ctx, item); err != nil {
			return err
		}
	}
	return nil
}

// ── Test Drive ────────────────────────────────────────────

func (r *ExpertRepo) CreateTestDrive(ctx context.Context, td *domain.ExpertTestDrive) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO expert_test_drives (report_id, evaluator_name, start_km, end_km, general_impression, notes)
		 VALUES ($1,$2,$3,$4,$5,$6) RETURNING id, created_at`,
		td.ReportID, td.EvaluatorName, td.StartKm, td.EndKm, td.GeneralImpression, td.Notes,
	).Scan(&td.ID, &td.CreatedAt)
}

func (r *ExpertRepo) GetTestDrive(ctx context.Context, reportID int) (*domain.ExpertTestDrive, error) {
	td := &domain.ExpertTestDrive{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, report_id, COALESCE(evaluator_name,''), COALESCE(start_km,0), COALESCE(end_km,0), COALESCE(general_impression,''), COALESCE(notes,''), created_at
		 FROM expert_test_drives WHERE report_id=$1`, reportID,
	).Scan(&td.ID, &td.ReportID, &td.EvaluatorName, &td.StartKm, &td.EndKm, &td.GeneralImpression, &td.Notes, &td.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("get test drive: %w", err)
	}
	return td, nil
}

func (r *ExpertRepo) UpdateTestDrive(ctx context.Context, td *domain.ExpertTestDrive) error {
	_, err := r.pool.Exec(ctx,
		`UPDATE expert_test_drives SET evaluator_name=$1, start_km=$2, end_km=$3, general_impression=$4, notes=$5 WHERE report_id=$6`,
		td.EvaluatorName, td.StartKm, td.EndKm, td.GeneralImpression, td.Notes, td.ReportID)
	return err
}

// ── Dyno Test ─────────────────────────────────────────────

func (r *ExpertRepo) CreateDynoTests(ctx context.Context, items []*domain.ExpertDynoTest) error {
	for _, item := range items {
		if err := r.pool.QueryRow(ctx,
			`INSERT INTO expert_dyno_tests (report_id, test_type, max_power, max_torque, notes)
			 VALUES ($1,$2,$3,$4,$5) RETURNING id, created_at`,
			item.ReportID, item.TestType, item.MaxPower, item.MaxTorque, item.Notes,
		).Scan(&item.ID, &item.CreatedAt); err != nil {
			return err
		}
	}
	return nil
}

func (r *ExpertRepo) GetDynoTests(ctx context.Context, reportID int) ([]*domain.ExpertDynoTest, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, report_id, COALESCE(test_type,''), max_power, max_torque, COALESCE(notes,''), created_at
		 FROM expert_dyno_tests WHERE report_id=$1 ORDER BY id`, reportID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ExpertDynoTest
	for rows.Next() {
		d := &domain.ExpertDynoTest{}
		if err := rows.Scan(&d.ID, &d.ReportID, &d.TestType, &d.MaxPower, &d.MaxTorque, &d.Notes, &d.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, d)
	}
	return list, nil
}

func (r *ExpertRepo) UpdateDynoTests(ctx context.Context, reportID int, items []*domain.ExpertDynoTest) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM expert_dyno_tests WHERE report_id=$1`, reportID)
	if err != nil {
		return err
	}
	return r.CreateDynoTests(ctx, items)
}

// ── Photos ────────────────────────────────────────────────

func (r *ExpertRepo) CreatePhotos(ctx context.Context, items []*domain.ExpertPhoto) error {
	for _, item := range items {
		if err := r.pool.QueryRow(ctx,
			`INSERT INTO expert_photos (report_id, url, photo_type, description, sort_order)
			 VALUES ($1,$2,$3,$4,$5) RETURNING id, created_at`,
			item.ReportID, item.URL, item.PhotoType, item.Description, item.SortOrder,
		).Scan(&item.ID, &item.CreatedAt); err != nil {
			return err
		}
	}
	return nil
}

func (r *ExpertRepo) ListPhotos(ctx context.Context, reportID int) ([]*domain.ExpertPhoto, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, report_id, url, COALESCE(photo_type,''), COALESCE(description,''), sort_order, created_at
		 FROM expert_photos WHERE report_id=$1 ORDER BY sort_order`, reportID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ExpertPhoto
	for rows.Next() {
		p := &domain.ExpertPhoto{}
		if err := rows.Scan(&p.ID, &p.ReportID, &p.URL, &p.PhotoType, &p.Description, &p.SortOrder, &p.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, p)
	}
	return list, nil
}

// ═══════════════════════════════════════════════════════════
// NEW TABLES (000014)
// ═══════════════════════════════════════════════════════════

// ── Emission Tests ────────────────────────────────────────

func (r *ExpertRepo) CreateEmissionTests(ctx context.Context, items []*domain.ExpertEmissionTest) error {
	for _, item := range items {
		if err := r.pool.QueryRow(ctx,
			`INSERT INTO expert_emission_tests (report_id, co2, hc, co, nox, o2, lambda, result, notes)
			 VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9) RETURNING id, created_at`,
			item.ReportID, item.CO2, item.HC, item.CO, item.NOx, item.O2, item.Lambda, item.Result, item.Notes,
		).Scan(&item.ID, &item.CreatedAt); err != nil {
			return err
		}
	}
	return nil
}

func (r *ExpertRepo) GetEmissionTests(ctx context.Context, reportID int) ([]*domain.ExpertEmissionTest, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, report_id, co2, hc, co, nox, o2, lambda, COALESCE(result,''), COALESCE(notes,''), created_at
		 FROM expert_emission_tests WHERE report_id=$1 ORDER BY id`, reportID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ExpertEmissionTest
	for rows.Next() {
		e := &domain.ExpertEmissionTest{}
		if err := rows.Scan(&e.ID, &e.ReportID, &e.CO2, &e.HC, &e.CO, &e.NOx, &e.O2, &e.Lambda, &e.Result, &e.Notes, &e.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, e)
	}
	return list, nil
}

func (r *ExpertRepo) UpdateEmissionTests(ctx context.Context, reportID int, items []*domain.ExpertEmissionTest) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM expert_emission_tests WHERE report_id=$1`, reportID)
	if err != nil {
		return err
	}
	return r.CreateEmissionTests(ctx, items)
}

// ── Fluid Tests ───────────────────────────────────────────

func (r *ExpertRepo) CreateFluidTests(ctx context.Context, items []*domain.ExpertFluidTest) error {
	for _, item := range items {
		if err := r.pool.QueryRow(ctx,
			`INSERT INTO expert_fluid_tests (report_id, fluid_type, condition, level, notes)
			 VALUES ($1,$2,$3,$4,$5) RETURNING id, created_at`,
			item.ReportID, item.FluidType, item.Condition, item.Level, item.Notes,
		).Scan(&item.ID, &item.CreatedAt); err != nil {
			return err
		}
	}
	return nil
}

func (r *ExpertRepo) GetFluidTests(ctx context.Context, reportID int) ([]*domain.ExpertFluidTest, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, report_id, fluid_type, COALESCE(condition,''), COALESCE(level,''), COALESCE(notes,''), created_at
		 FROM expert_fluid_tests WHERE report_id=$1 ORDER BY id`, reportID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ExpertFluidTest
	for rows.Next() {
		f := &domain.ExpertFluidTest{}
		if err := rows.Scan(&f.ID, &f.ReportID, &f.FluidType, &f.Condition, &f.Level, &f.Notes, &f.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, f)
	}
	return list, nil
}

func (r *ExpertRepo) UpdateFluidTests(ctx context.Context, reportID int, items []*domain.ExpertFluidTest) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM expert_fluid_tests WHERE report_id=$1`, reportID)
	if err != nil {
		return err
	}
	return r.CreateFluidTests(ctx, items)
}

// ── Handbrake Tests ───────────────────────────────────────

func (r *ExpertRepo) CreateHandbrakeTests(ctx context.Context, items []*domain.ExpertHandbrakeTest) error {
	for _, item := range items {
		if err := r.pool.QueryRow(ctx,
			`INSERT INTO expert_handbrake_tests (report_id, effectiveness, notes)
			 VALUES ($1,$2,$3) RETURNING id, created_at`,
			item.ReportID, item.Effectiveness, item.Notes,
		).Scan(&item.ID, &item.CreatedAt); err != nil {
			return err
		}
	}
	return nil
}

func (r *ExpertRepo) GetHandbrakeTests(ctx context.Context, reportID int) ([]*domain.ExpertHandbrakeTest, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, report_id, effectiveness, COALESCE(notes,''), created_at
		 FROM expert_handbrake_tests WHERE report_id=$1 ORDER BY id`, reportID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ExpertHandbrakeTest
	for rows.Next() {
		h := &domain.ExpertHandbrakeTest{}
		if err := rows.Scan(&h.ID, &h.ReportID, &h.Effectiveness, &h.Notes, &h.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, h)
	}
	return list, nil
}

func (r *ExpertRepo) UpdateHandbrakeTests(ctx context.Context, reportID int, items []*domain.ExpertHandbrakeTest) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM expert_handbrake_tests WHERE report_id=$1`, reportID)
	if err != nil {
		return err
	}
	return r.CreateHandbrakeTests(ctx, items)
}

// ── Four Wheel Drive Checks ───────────────────────────────

func (r *ExpertRepo) CreateFourWheelDriveChecks(ctx context.Context, items []*domain.ExpertFourWheelDriveCheck) error {
	for _, item := range items {
		if err := r.pool.QueryRow(ctx,
			`INSERT INTO expert_four_wheel_drive_checks (report_id, front_left, front_right, rear_left, rear_right, notes)
			 VALUES ($1,$2,$3,$4,$5,$6) RETURNING id, created_at`,
			item.ReportID, item.FrontLeft, item.FrontRight, item.RearLeft, item.RearRight, item.Notes,
		).Scan(&item.ID, &item.CreatedAt); err != nil {
			return err
		}
	}
	return nil
}

func (r *ExpertRepo) GetFourWheelDriveChecks(ctx context.Context, reportID int) ([]*domain.ExpertFourWheelDriveCheck, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, report_id, COALESCE(front_left,''), COALESCE(front_right,''), COALESCE(rear_left,''), COALESCE(rear_right,''), COALESCE(notes,''), created_at
		 FROM expert_four_wheel_drive_checks WHERE report_id=$1 ORDER BY id`, reportID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ExpertFourWheelDriveCheck
	for rows.Next() {
		f := &domain.ExpertFourWheelDriveCheck{}
		if err := rows.Scan(&f.ID, &f.ReportID, &f.FrontLeft, &f.FrontRight, &f.RearLeft, &f.RearRight, &f.Notes, &f.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, f)
	}
	return list, nil
}

func (r *ExpertRepo) UpdateFourWheelDriveChecks(ctx context.Context, reportID int, items []*domain.ExpertFourWheelDriveCheck) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM expert_four_wheel_drive_checks WHERE report_id=$1`, reportID)
	if err != nil {
		return err
	}
	return r.CreateFourWheelDriveChecks(ctx, items)
}

// ── Belt Checks ───────────────────────────────────────────

func (r *ExpertRepo) CreateBeltChecks(ctx context.Context, items []*domain.ExpertBeltCheck) error {
	for _, item := range items {
		if err := r.pool.QueryRow(ctx,
			`INSERT INTO expert_belt_checks (report_id, belt_name, condition, notes)
			 VALUES ($1,$2,$3,$4) RETURNING id, created_at`,
			item.ReportID, item.BeltName, item.Condition, item.Notes,
		).Scan(&item.ID, &item.CreatedAt); err != nil {
			return err
		}
	}
	return nil
}

func (r *ExpertRepo) GetBeltChecks(ctx context.Context, reportID int) ([]*domain.ExpertBeltCheck, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, report_id, belt_name, COALESCE(condition,''), COALESCE(notes,''), created_at
		 FROM expert_belt_checks WHERE report_id=$1 ORDER BY id`, reportID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ExpertBeltCheck
	for rows.Next() {
		b := &domain.ExpertBeltCheck{}
		if err := rows.Scan(&b.ID, &b.ReportID, &b.BeltName, &b.Condition, &b.Notes, &b.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, b)
	}
	return list, nil
}

func (r *ExpertRepo) UpdateBeltChecks(ctx context.Context, reportID int, items []*domain.ExpertBeltCheck) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM expert_belt_checks WHERE report_id=$1`, reportID)
	if err != nil {
		return err
	}
	return r.CreateBeltChecks(ctx, items)
}

// ── Chassis Checks ────────────────────────────────────────

func (r *ExpertRepo) CreateChassisChecks(ctx context.Context, items []*domain.ExpertChassisCheck) error {
	for _, item := range items {
		if err := r.pool.QueryRow(ctx,
			`INSERT INTO expert_chassis_checks (report_id, section, condition, notes)
			 VALUES ($1,$2,$3,$4) RETURNING id, created_at`,
			item.ReportID, item.Section, item.Condition, item.Notes,
		).Scan(&item.ID, &item.CreatedAt); err != nil {
			return err
		}
	}
	return nil
}

func (r *ExpertRepo) GetChassisChecks(ctx context.Context, reportID int) ([]*domain.ExpertChassisCheck, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, report_id, section, COALESCE(condition,''), COALESCE(notes,''), created_at
		 FROM expert_chassis_checks WHERE report_id=$1 ORDER BY id`, reportID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ExpertChassisCheck
	for rows.Next() {
		c := &domain.ExpertChassisCheck{}
		if err := rows.Scan(&c.ID, &c.ReportID, &c.Section, &c.Condition, &c.Notes, &c.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, c)
	}
	return list, nil
}

func (r *ExpertRepo) UpdateChassisChecks(ctx context.Context, reportID int, items []*domain.ExpertChassisCheck) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM expert_chassis_checks WHERE report_id=$1`, reportID)
	if err != nil {
		return err
	}
	return r.CreateChassisChecks(ctx, items)
}

// ── Extra Equipment ───────────────────────────────────────

func (r *ExpertRepo) CreateExtraEquipment(ctx context.Context, items []*domain.ExpertExtraEquipment) error {
	for _, item := range items {
		if err := r.pool.QueryRow(ctx,
			`INSERT INTO expert_extra_equipment (report_id, equipment_name, is_working, notes)
			 VALUES ($1,$2,$3,$4) RETURNING id, created_at`,
			item.ReportID, item.EquipmentName, item.IsWorking, item.Notes,
		).Scan(&item.ID, &item.CreatedAt); err != nil {
			return err
		}
	}
	return nil
}

func (r *ExpertRepo) GetExtraEquipment(ctx context.Context, reportID int) ([]*domain.ExpertExtraEquipment, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, report_id, equipment_name, is_working, COALESCE(notes,''), created_at
		 FROM expert_extra_equipment WHERE report_id=$1 ORDER BY id`, reportID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ExpertExtraEquipment
	for rows.Next() {
		e := &domain.ExpertExtraEquipment{}
		if err := rows.Scan(&e.ID, &e.ReportID, &e.EquipmentName, &e.IsWorking, &e.Notes, &e.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, e)
	}
	return list, nil
}

func (r *ExpertRepo) UpdateExtraEquipment(ctx context.Context, reportID int, items []*domain.ExpertExtraEquipment) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM expert_extra_equipment WHERE report_id=$1`, reportID)
	if err != nil {
		return err
	}
	return r.CreateExtraEquipment(ctx, items)
}

// ── Mandatory Equipment ───────────────────────────────────

func (r *ExpertRepo) CreateMandatoryEquipment(ctx context.Context, items []*domain.ExpertMandatoryEquipment) error {
	for _, item := range items {
		if err := r.pool.QueryRow(ctx,
			`INSERT INTO expert_mandatory_equipment (report_id, equipment_name, is_present, is_valid, notes)
			 VALUES ($1,$2,$3,$4,$5) RETURNING id, created_at`,
			item.ReportID, item.EquipmentName, item.IsPresent, item.IsValid, item.Notes,
		).Scan(&item.ID, &item.CreatedAt); err != nil {
			return err
		}
	}
	return nil
}

func (r *ExpertRepo) GetMandatoryEquipment(ctx context.Context, reportID int) ([]*domain.ExpertMandatoryEquipment, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, report_id, equipment_name, is_present, is_valid, COALESCE(notes,''), created_at
		 FROM expert_mandatory_equipment WHERE report_id=$1 ORDER BY id`, reportID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ExpertMandatoryEquipment
	for rows.Next() {
		m := &domain.ExpertMandatoryEquipment{}
		if err := rows.Scan(&m.ID, &m.ReportID, &m.EquipmentName, &m.IsPresent, &m.IsValid, &m.Notes, &m.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, m)
	}
	return list, nil
}

func (r *ExpertRepo) UpdateMandatoryEquipment(ctx context.Context, reportID int, items []*domain.ExpertMandatoryEquipment) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM expert_mandatory_equipment WHERE report_id=$1`, reportID)
	if err != nil {
		return err
	}
	return r.CreateMandatoryEquipment(ctx, items)
}

// ── Acceptance Criteria ───────────────────────────────────

func (r *ExpertRepo) CreateAcceptanceCriteria(ctx context.Context, items []*domain.ExpertAcceptanceCriteria) error {
	for _, item := range items {
		if err := r.pool.QueryRow(ctx,
			`INSERT INTO expert_acceptance_criteria (report_id, criteria_name, is_met, notes)
			 VALUES ($1,$2,$3,$4) RETURNING id, created_at`,
			item.ReportID, item.CriteriaName, item.IsMet, item.Notes,
		).Scan(&item.ID, &item.CreatedAt); err != nil {
			return err
		}
	}
	return nil
}

func (r *ExpertRepo) GetAcceptanceCriteria(ctx context.Context, reportID int) ([]*domain.ExpertAcceptanceCriteria, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, report_id, criteria_name, is_met, COALESCE(notes,''), created_at
		 FROM expert_acceptance_criteria WHERE report_id=$1 ORDER BY id`, reportID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ExpertAcceptanceCriteria
	for rows.Next() {
		a := &domain.ExpertAcceptanceCriteria{}
		if err := rows.Scan(&a.ID, &a.ReportID, &a.CriteriaName, &a.IsMet, &a.Notes, &a.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, a)
	}
	return list, nil
}

func (r *ExpertRepo) UpdateAcceptanceCriteria(ctx context.Context, reportID int, items []*domain.ExpertAcceptanceCriteria) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM expert_acceptance_criteria WHERE report_id=$1`, reportID)
	if err != nil {
		return err
	}
	return r.CreateAcceptanceCriteria(ctx, items)
}
