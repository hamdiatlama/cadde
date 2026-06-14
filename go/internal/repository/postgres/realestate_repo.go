package postgres

import (
	"context"
	"fmt"
	"strings"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/web-platform/backend/internal/domain"
)

type RealEstateRepo struct {
	pool *pgxpool.Pool
}

func NewRealEstateRepo(pool *pgxpool.Pool) *RealEstateRepo {
	return &RealEstateRepo{pool: pool}
}

// ── Property Category ─────────────────────────────────────

func (r *RealEstateRepo) CreateCategory(ctx context.Context, c *domain.PropertyCategory) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO property_categories (name, slug, sort_order) VALUES ($1,$2,$3) RETURNING id, created_at`,
		c.Name, c.Slug, c.SortOrder,
	).Scan(&c.ID, &c.CreatedAt)
}

func (r *RealEstateRepo) ListCategories(ctx context.Context) ([]*domain.PropertyCategory, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, name, slug, sort_order, created_at FROM property_categories ORDER BY sort_order`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.PropertyCategory
	for rows.Next() {
		c := &domain.PropertyCategory{}
		if err := rows.Scan(&c.ID, &c.Name, &c.Slug, &c.SortOrder, &c.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, c)
	}
	return list, nil
}

func (r *RealEstateRepo) DeleteCategory(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM property_categories WHERE id=$1`, id)
	return err
}

// ── Property Type ─────────────────────────────────────────

func (r *RealEstateRepo) CreateType(ctx context.Context, t *domain.PropertyType) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO property_types (name, slug, icon, sort_order) VALUES ($1,$2,$3,$4) RETURNING id, created_at`,
		t.Name, t.Slug, t.Icon, t.SortOrder,
	).Scan(&t.ID, &t.CreatedAt)
}

func (r *RealEstateRepo) ListTypes(ctx context.Context) ([]*domain.PropertyType, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, name, slug, icon, sort_order, created_at FROM property_types ORDER BY sort_order`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.PropertyType
	for rows.Next() {
		t := &domain.PropertyType{}
		if err := rows.Scan(&t.ID, &t.Name, &t.Slug, &t.Icon, &t.SortOrder, &t.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, t)
	}
	return list, nil
}

func (r *RealEstateRepo) DeleteType(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM property_types WHERE id=$1`, id)
	return err
}

// ── Contractor Company ────────────────────────────────────

func (r *RealEstateRepo) CreateCompany(ctx context.Context, c *domain.ContractorCompany) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO contractor_companies (name, slug, tax_no, tax_office, phone, email, address, website, logo_url, description, rating, review_count, is_verified, is_active, latitude, longitude, verification_status, verification_note, certificate_no, certificate_expiry)
		 VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20) RETURNING id, created_at, updated_at`,
		c.Name, c.Slug, c.TaxNo, c.TaxOffice, c.Phone, c.Email, c.Address, c.Website, c.LogoURL, c.Description,
		c.Rating, c.ReviewCount, c.IsVerified, c.IsActive, c.Latitude, c.Longitude,
		c.VerificationStatus, c.VerificationNote, c.CertificateNo, c.CertificateExpiry,
	).Scan(&c.ID, &c.CreatedAt, &c.UpdatedAt)
}

func (r *RealEstateRepo) GetCompany(ctx context.Context, id int) (*domain.ContractorCompany, error) {
	c := &domain.ContractorCompany{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, name, slug, COALESCE(tax_no,''), COALESCE(tax_office,''), COALESCE(phone,''), COALESCE(email,''), COALESCE(address,''), COALESCE(website,''), COALESCE(logo_url,''), COALESCE(description,''), rating, review_count, is_verified, is_active, latitude, longitude, COALESCE(verification_status,''), COALESCE(verification_note,''), verified_at, COALESCE(certificate_no,''), certificate_expiry, created_at, updated_at
		 FROM contractor_companies WHERE id=$1`, id,
	).Scan(&c.ID, &c.Name, &c.Slug, &c.TaxNo, &c.TaxOffice, &c.Phone, &c.Email, &c.Address, &c.Website, &c.LogoURL, &c.Description, &c.Rating, &c.ReviewCount, &c.IsVerified, &c.IsActive, &c.Latitude, &c.Longitude, &c.VerificationStatus, &c.VerificationNote, &c.VerifiedAt, &c.CertificateNo, &c.CertificateExpiry, &c.CreatedAt, &c.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("get company: %w", err)
	}
	return c, nil
}

func (r *RealEstateRepo) ListCompanies(ctx context.Context) ([]*domain.ContractorCompany, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, name, slug, COALESCE(tax_no,''), COALESCE(tax_office,''), COALESCE(phone,''), COALESCE(email,''), COALESCE(address,''), COALESCE(website,''), COALESCE(logo_url,''), COALESCE(description,''), rating, review_count, is_verified, is_active, latitude, longitude, COALESCE(verification_status,''), COALESCE(verification_note,''), verified_at, COALESCE(certificate_no,''), certificate_expiry, created_at, updated_at
		 FROM contractor_companies ORDER BY name`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ContractorCompany
	for rows.Next() {
		c := &domain.ContractorCompany{}
		if err := rows.Scan(&c.ID, &c.Name, &c.Slug, &c.TaxNo, &c.TaxOffice, &c.Phone, &c.Email, &c.Address, &c.Website, &c.LogoURL, &c.Description, &c.Rating, &c.ReviewCount, &c.IsVerified, &c.IsActive, &c.Latitude, &c.Longitude, &c.VerificationStatus, &c.VerificationNote, &c.VerifiedAt, &c.CertificateNo, &c.CertificateExpiry, &c.CreatedAt, &c.UpdatedAt); err != nil {
			return nil, err
		}
		list = append(list, c)
	}
	return list, nil
}

// ── Contractor Review ─────────────────────────────────────

func (r *RealEstateRepo) CreateReview(ctx context.Context, rev *domain.ContractorReview) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO contractor_reviews (company_id, user_id, rating, comment) VALUES ($1,$2,$3,$4) RETURNING id, created_at`,
		rev.CompanyID, rev.UserID, rev.Rating, rev.Comment,
	).Scan(&rev.ID, &rev.CreatedAt)
}

func (r *RealEstateRepo) ListReviews(ctx context.Context, companyID int) ([]*domain.ContractorReview, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, company_id, user_id, rating, COALESCE(comment,''), created_at
		 FROM contractor_reviews WHERE company_id=$1 ORDER BY created_at DESC`, companyID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ContractorReview
	for rows.Next() {
		rev := &domain.ContractorReview{}
		if err := rows.Scan(&rev.ID, &rev.CompanyID, &rev.UserID, &rev.Rating, &rev.Comment, &rev.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, rev)
	}
	return list, nil
}

// ── Property Listing ──────────────────────────────────────

const listingCols = `id, user_id, category_id, type_id, contractor_id, title, COALESCE(description,''), price, COALESCE(currency,'TRY'), is_for_sale, is_for_rent, rent_deposit, dues, latitude, longitude, COALESCE(country,''), COALESCE(city,''), COALESCE(district,''), COALESCE(neighborhood,''), COALESCE(address,''), COALESCE(map_address,''), COALESCE(building_name,''), COALESCE(block,''), COALESCE(floor,''), COALESCE(door_number,''), construction_year, building_age, floor_count, total_apartments, COALESCE(contractor_name_history,''), land_area, building_area, COALESCE(zoning_status,''), COALESCE(land_use_type,''), COALESCE(density_value,''), COALESCE(parcel_no,''), COALESCE(island_no,''), COALESCE(room_count,''), bathroom_count, net_area, gross_area, COALESCE(heating_type,''), COALESCE(furnishing,''), COALESCE(facade,''), balcony_count, COALESCE(status,'active'), view_count, is_highlighted, valid_from, valid_until, created_at, updated_at`

func (r *RealEstateRepo) CreateListing(ctx context.Context, l *domain.PropertyListing) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO property_listings (
			user_id, category_id, type_id, contractor_id, title, description, price, currency,
			is_for_sale, is_for_rent, rent_deposit, dues, latitude, longitude,
			country, city, district, neighborhood, address, map_address,
			building_name, block, floor, door_number, construction_year, building_age,
			floor_count, total_apartments, contractor_name_history, land_area, building_area,
			zoning_status, land_use_type, density_value, parcel_no, island_no,
			room_count, bathroom_count, net_area, gross_area, heating_type, furnishing, facade,
			balcony_count, status, is_highlighted, valid_from, valid_until
		) VALUES (
			$1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,
			$21,$22,$23,$24,$25,$26,$27,$28,$29,$30,$31,$32,$33,$34,$35,$36,$37,$38,$39,$40,
			$41,$42,$43,$44,$45,$46,$47,$48
		) RETURNING id, created_at, updated_at`,
		l.UserID, l.CategoryID, l.TypeID, l.ContractorID, l.Title, l.Description, l.Price, l.Currency,
		l.IsForSale, l.IsForRent, l.RentDeposit, l.Dues, l.Latitude, l.Longitude,
		l.Country, l.City, l.District, l.Neighborhood, l.Address, l.MapAddress,
		l.BuildingName, l.Block, l.Floor, l.DoorNumber, l.ConstructionYear, l.BuildingAge,
		l.FloorCount, l.TotalApartments, l.ContractorNameHistory, l.LandArea, l.BuildingArea,
		l.ZoningStatus, l.LandUseType, l.DensityValue, l.ParcelNo, l.IslandNo,
		l.RoomCount, l.BathroomCount, l.NetArea, l.GrossArea, l.HeatingType, l.Furnishing, l.Facade,
		l.BalconyCount, l.Status, l.IsHighlighted, l.ValidFrom, l.ValidUntil,
	).Scan(&l.ID, &l.CreatedAt, &l.UpdatedAt)
}

func scanListing(scanner interface {
	Scan(dest ...interface{}) error
}, l *domain.PropertyListing) error {
	return scanner.Scan(
		&l.ID, &l.UserID, &l.CategoryID, &l.TypeID, &l.ContractorID, &l.Title, &l.Description, &l.Price, &l.Currency,
		&l.IsForSale, &l.IsForRent, &l.RentDeposit, &l.Dues, &l.Latitude, &l.Longitude,
		&l.Country, &l.City, &l.District, &l.Neighborhood, &l.Address, &l.MapAddress,
		&l.BuildingName, &l.Block, &l.Floor, &l.DoorNumber, &l.ConstructionYear, &l.BuildingAge,
		&l.FloorCount, &l.TotalApartments, &l.ContractorNameHistory, &l.LandArea, &l.BuildingArea,
		&l.ZoningStatus, &l.LandUseType, &l.DensityValue, &l.ParcelNo, &l.IslandNo,
		&l.RoomCount, &l.BathroomCount, &l.NetArea, &l.GrossArea, &l.HeatingType, &l.Furnishing, &l.Facade,
		&l.BalconyCount, &l.Status, &l.ViewCount, &l.IsHighlighted, &l.ValidFrom, &l.ValidUntil,
		&l.CreatedAt, &l.UpdatedAt,
	)
}

func (r *RealEstateRepo) GetListing(ctx context.Context, id int64) (*domain.PropertyListing, error) {
	l := &domain.PropertyListing{}
	err := scanListing(r.pool.QueryRow(ctx,
		`SELECT `+listingCols+` FROM property_listings WHERE id=$1`, id), l)
	if err != nil {
		return nil, fmt.Errorf("get listing: %w", err)
	}
	return l, nil
}

func (r *RealEstateRepo) UpdateListing(ctx context.Context, l *domain.PropertyListing) error {
	return r.pool.QueryRow(ctx,
		`UPDATE property_listings SET
			user_id=$1, category_id=$2, type_id=$3, contractor_id=$4, title=$5, description=$6,
			price=$7, currency=$8, is_for_sale=$9, is_for_rent=$10, rent_deposit=$11, dues=$12,
			latitude=$13, longitude=$14, country=$15, city=$16, district=$17, neighborhood=$18,
			address=$19, map_address=$20, building_name=$21, block=$22, floor=$23, door_number=$24,
			construction_year=$25, building_age=$26, floor_count=$27, total_apartments=$28,
			contractor_name_history=$29, land_area=$30, building_area=$31, zoning_status=$32,
			land_use_type=$33, density_value=$34, parcel_no=$35, island_no=$36, room_count=$37,
			bathroom_count=$38, net_area=$39, gross_area=$40, heating_type=$41, furnishing=$42,
			facade=$43, balcony_count=$44, status=$45, is_highlighted=$46, valid_from=$47, valid_until=$48,
			updated_at=NOW()
		WHERE id=$49 RETURNING updated_at`,
		l.UserID, l.CategoryID, l.TypeID, l.ContractorID, l.Title, l.Description,
		l.Price, l.Currency, l.IsForSale, l.IsForRent, l.RentDeposit, l.Dues,
		l.Latitude, l.Longitude, l.Country, l.City, l.District, l.Neighborhood,
		l.Address, l.MapAddress, l.BuildingName, l.Block, l.Floor, l.DoorNumber,
		l.ConstructionYear, l.BuildingAge, l.FloorCount, l.TotalApartments,
		l.ContractorNameHistory, l.LandArea, l.BuildingArea, l.ZoningStatus,
		l.LandUseType, l.DensityValue, l.ParcelNo, l.IslandNo, l.RoomCount,
		l.BathroomCount, l.NetArea, l.GrossArea, l.HeatingType, l.Furnishing, l.Facade,
		l.BalconyCount, l.Status, l.IsHighlighted, l.ValidFrom, l.ValidUntil, l.ID,
	).Scan(&l.UpdatedAt)
}

func (r *RealEstateRepo) DeleteListing(ctx context.Context, id int64) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM property_listings WHERE id=$1`, id)
	return err
}

func (r *RealEstateRepo) ListListings(ctx context.Context, filters map[string]string, page, limit int) ([]*domain.PropertyListing, error) {
	where := []string{"1=1"}
	args := []interface{}{}
	n := 1

	if v, ok := filters["category_id"]; ok && v != "" {
		where = append(where, fmt.Sprintf("category_id=$%d", n))
		args = append(args, v)
		n++
	}
	if v, ok := filters["type_id"]; ok && v != "" {
		where = append(where, fmt.Sprintf("type_id=$%d", n))
		args = append(args, v)
		n++
	}
	if v, ok := filters["city"]; ok && v != "" {
		where = append(where, fmt.Sprintf("city=$%d", n))
		args = append(args, v)
		n++
	}
	if v, ok := filters["district"]; ok && v != "" {
		where = append(where, fmt.Sprintf("district=$%d", n))
		args = append(args, v)
		n++
	}
	if v, ok := filters["min_price"]; ok && v != "" {
		where = append(where, fmt.Sprintf("price>=$%d", n))
		args = append(args, v)
		n++
	}
	if v, ok := filters["max_price"]; ok && v != "" {
		where = append(where, fmt.Sprintf("price<=$%d", n))
		args = append(args, v)
		n++
	}
	if v, ok := filters["room_count"]; ok && v != "" {
		where = append(where, fmt.Sprintf("room_count=$%d", n))
		args = append(args, v)
		n++
	}
	if v, ok := filters["status"]; ok && v != "" {
		where = append(where, fmt.Sprintf("status=$%d", n))
		args = append(args, v)
		n++
	}

	sortBy := "created_at DESC"
	if v, ok := filters["sort_by"]; ok && v != "" {
		switch v {
		case "price_asc":
			sortBy = "price ASC"
		case "price_desc":
			sortBy = "price DESC"
		case "oldest":
			sortBy = "created_at ASC"
		case "view_count":
			sortBy = "view_count DESC"
		}
	}

	offset := (page - 1) * limit
	query := fmt.Sprintf(`SELECT `+listingCols+` FROM property_listings WHERE %s ORDER BY %s LIMIT $%d OFFSET $%d`,
		strings.Join(where, " AND "), sortBy, n, n+1)
	args = append(args, limit, offset)

	rows, err := r.pool.Query(ctx, query, args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.PropertyListing
	for rows.Next() {
		l := &domain.PropertyListing{}
		if err := scanListing(rows, l); err != nil {
			return nil, err
		}
		list = append(list, l)
	}
	return list, nil
}

func (r *RealEstateRepo) IncrementViewCount(ctx context.Context, id int64) error {
	_, err := r.pool.Exec(ctx, `UPDATE property_listings SET view_count=view_count+1 WHERE id=$1`, id)
	return err
}

func (r *RealEstateRepo) SearchListings(ctx context.Context, q string, page, limit int) ([]*domain.PropertyListing, error) {
	offset := (page - 1) * limit
	search := "%" + q + "%"
	rows, err := r.pool.Query(ctx,
		`SELECT `+listingCols+` FROM property_listings
		 WHERE title ILIKE $1 OR description ILIKE $1
		 ORDER BY created_at DESC LIMIT $2 OFFSET $3`, search, limit, offset)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.PropertyListing
	for rows.Next() {
		l := &domain.PropertyListing{}
		if err := scanListing(rows, l); err != nil {
			return nil, err
		}
		list = append(list, l)
	}
	return list, nil
}

// ── Property Photo ────────────────────────────────────────

func (r *RealEstateRepo) AddPhoto(ctx context.Context, p *domain.PropertyPhoto) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO property_photos (listing_id, file_path, category, description, is_cover, sort_order)
		 VALUES ($1,$2,$3,$4,$5,$6) RETURNING id, created_at`,
		p.ListingID, p.FilePath, p.Category, p.Description, p.IsCover, p.SortOrder,
	).Scan(&p.ID, &p.CreatedAt)
}

func (r *RealEstateRepo) ListPhotos(ctx context.Context, listingID int64) ([]*domain.PropertyPhoto, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, listing_id, file_path, COALESCE(category,''), COALESCE(description,''), is_cover, sort_order, created_at
		 FROM property_photos WHERE listing_id=$1 ORDER BY sort_order`, listingID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.PropertyPhoto
	for rows.Next() {
		p := &domain.PropertyPhoto{}
		if err := rows.Scan(&p.ID, &p.ListingID, &p.FilePath, &p.Category, &p.Description, &p.IsCover, &p.SortOrder, &p.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, p)
	}
	return list, nil
}

func (r *RealEstateRepo) DeletePhoto(ctx context.Context, id int64) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM property_photos WHERE id=$1`, id)
	return err
}

func (r *RealEstateRepo) SetCoverPhoto(ctx context.Context, listingID, photoID int64) error {
	_, err := r.pool.Exec(ctx,
		`UPDATE property_photos SET is_cover=false WHERE listing_id=$1;
		 UPDATE property_photos SET is_cover=true WHERE id=$2`, listingID, photoID)
	return err
}

// ── Property Feature ──────────────────────────────────────

func (r *RealEstateRepo) CreateFeature(ctx context.Context, f *domain.PropertyFeature) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO property_features (name, slug, icon, category, sort_order) VALUES ($1,$2,$3,$4,$5) RETURNING id, created_at`,
		f.Name, f.Slug, f.Icon, f.Category, f.SortOrder,
	).Scan(&f.ID, &f.CreatedAt)
}

func (r *RealEstateRepo) ListFeatures(ctx context.Context) ([]*domain.PropertyFeature, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, name, slug, COALESCE(icon,''), COALESCE(category,''), sort_order, created_at FROM property_features ORDER BY sort_order`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.PropertyFeature
	for rows.Next() {
		f := &domain.PropertyFeature{}
		if err := rows.Scan(&f.ID, &f.Name, &f.Slug, &f.Icon, &f.Category, &f.SortOrder, &f.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, f)
	}
	return list, nil
}

func (r *RealEstateRepo) AddListingFeatures(ctx context.Context, listingID int64, features []domain.PropertyListingFeature) error {
	for _, f := range features {
		_, err := r.pool.Exec(ctx,
			`INSERT INTO property_listing_features (listing_id, feature_id, value) VALUES ($1,$2,$3) ON CONFLICT DO NOTHING`,
			listingID, f.FeatureID, f.Value)
		if err != nil {
			return err
		}
	}
	return nil
}

func (r *RealEstateRepo) GetListingFeatures(ctx context.Context, listingID int64) ([]*domain.PropertyListingFeature, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT listing_id, feature_id, COALESCE(value,'') FROM property_listing_features WHERE listing_id=$1`, listingID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.PropertyListingFeature
	for rows.Next() {
		f := &domain.PropertyListingFeature{}
		if err := rows.Scan(&f.ListingID, &f.FeatureID, &f.Value); err != nil {
			return nil, err
		}
		list = append(list, f)
	}
	return list, nil
}

func (r *RealEstateRepo) RemoveListingFeature(ctx context.Context, listingID int64, featureID int) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM property_listing_features WHERE listing_id=$1 AND feature_id=$2`, listingID, featureID)
	return err
}

// ── Authorization Request ────────────────────────────────

func (r *RealEstateRepo) CreateAuthorization(ctx context.Context, a *domain.AuthorizationRequest) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO authorization_requests (listing_id, owner_id, company_id, auth_type, commission_rate, commission_fixed, valid_from, valid_until, status, owner_note, company_note)
		 VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11) RETURNING id, created_at, updated_at`,
		a.ListingID, a.OwnerID, a.CompanyID, a.AuthType, a.CommissionRate, a.CommissionFixed,
		a.ValidFrom, a.ValidUntil, a.Status, a.OwnerNote, a.CompanyNote,
	).Scan(&a.ID, &a.CreatedAt, &a.UpdatedAt)
}

func (r *RealEstateRepo) ListAuthorizations(ctx context.Context, listingID int64) ([]*domain.AuthorizationRequest, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, listing_id, owner_id, company_id, auth_type, commission_rate, commission_fixed, valid_from, valid_until, status, COALESCE(owner_note,''), COALESCE(company_note,''), created_at, updated_at
		 FROM authorization_requests WHERE listing_id=$1 ORDER BY created_at DESC`, listingID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.AuthorizationRequest
	for rows.Next() {
		a := &domain.AuthorizationRequest{}
		if err := rows.Scan(&a.ID, &a.ListingID, &a.OwnerID, &a.CompanyID, &a.AuthType, &a.CommissionRate, &a.CommissionFixed, &a.ValidFrom, &a.ValidUntil, &a.Status, &a.OwnerNote, &a.CompanyNote, &a.CreatedAt, &a.UpdatedAt); err != nil {
			return nil, err
		}
		list = append(list, a)
	}
	return list, nil
}

func (r *RealEstateRepo) UpdateAuthorizationStatus(ctx context.Context, id int64, status string) error {
	_, err := r.pool.Exec(ctx, `UPDATE authorization_requests SET status=$1, updated_at=NOW() WHERE id=$2`, status, id)
	return err
}

// ── Property Appraisal Request ────────────────────────────

func (r *RealEstateRepo) CreateAppraisalRequest(ctx context.Context, a *domain.PropertyAppraisalRequest) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO property_appraisal_requests (user_id, listing_id, company_id, expert_id, city, district, neighborhood, address, latitude, longitude, property_type_id, land_area, building_area, room_count, construction_year, status, notes, report_data, report_file_url, requested_date, completed_date)
		 VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21) RETURNING id, created_at, updated_at`,
		a.UserID, a.ListingID, a.CompanyID, a.ExpertID, a.City, a.District, a.Neighborhood, a.Address,
		a.Latitude, a.Longitude, a.PropertyTypeID, a.LandArea, a.BuildingArea, a.RoomCount,
		a.ConstructionYear, a.Status, a.Notes, a.ReportData, a.ReportFileURL, a.RequestedDate, a.CompletedDate,
	).Scan(&a.ID, &a.CreatedAt, &a.UpdatedAt)
}

func (r *RealEstateRepo) GetAppraisalRequest(ctx context.Context, id int64) (*domain.PropertyAppraisalRequest, error) {
	a := &domain.PropertyAppraisalRequest{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, user_id, listing_id, company_id, expert_id, COALESCE(city,''), COALESCE(district,''), COALESCE(neighborhood,''), COALESCE(address,''), latitude, longitude, property_type_id, land_area, building_area, COALESCE(room_count,''), construction_year, COALESCE(status,'pending'), COALESCE(notes,''), report_data, COALESCE(report_file_url,''), requested_date, completed_date, created_at, updated_at
		 FROM property_appraisal_requests WHERE id=$1`, id,
	).Scan(&a.ID, &a.UserID, &a.ListingID, &a.CompanyID, &a.ExpertID, &a.City, &a.District, &a.Neighborhood, &a.Address, &a.Latitude, &a.Longitude, &a.PropertyTypeID, &a.LandArea, &a.BuildingArea, &a.RoomCount, &a.ConstructionYear, &a.Status, &a.Notes, &a.ReportData, &a.ReportFileURL, &a.RequestedDate, &a.CompletedDate, &a.CreatedAt, &a.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("get appraisal request: %w", err)
	}
	return a, nil
}

func (r *RealEstateRepo) ListAppraisalRequests(ctx context.Context, userID string) ([]*domain.PropertyAppraisalRequest, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, user_id, listing_id, company_id, expert_id, COALESCE(city,''), COALESCE(district,''), COALESCE(neighborhood,''), COALESCE(address,''), latitude, longitude, property_type_id, land_area, building_area, COALESCE(room_count,''), construction_year, COALESCE(status,'pending'), COALESCE(notes,''), report_data, COALESCE(report_file_url,''), requested_date, completed_date, created_at, updated_at
		 FROM property_appraisal_requests WHERE user_id=$1 ORDER BY created_at DESC`, userID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.PropertyAppraisalRequest
	for rows.Next() {
		a := &domain.PropertyAppraisalRequest{}
		if err := rows.Scan(&a.ID, &a.UserID, &a.ListingID, &a.CompanyID, &a.ExpertID, &a.City, &a.District, &a.Neighborhood, &a.Address, &a.Latitude, &a.Longitude, &a.PropertyTypeID, &a.LandArea, &a.BuildingArea, &a.RoomCount, &a.ConstructionYear, &a.Status, &a.Notes, &a.ReportData, &a.ReportFileURL, &a.RequestedDate, &a.CompletedDate, &a.CreatedAt, &a.UpdatedAt); err != nil {
			return nil, err
		}
		list = append(list, a)
	}
	return list, nil
}

func (r *RealEstateRepo) UpdateAppraisalStatus(ctx context.Context, id int64, status string) error {
	_, err := r.pool.Exec(ctx, `UPDATE property_appraisal_requests SET status=$1, updated_at=NOW() WHERE id=$2`, status, id)
	return err
}

// ── Favorite Listing ──────────────────────────────────────

func (r *RealEstateRepo) AddFavorite(ctx context.Context, userID string, listingID int64) error {
	_, err := r.pool.Exec(ctx,
		`INSERT INTO favorite_listings (user_id, listing_id) VALUES ($1,$2) ON CONFLICT DO NOTHING`,
		userID, listingID)
	return err
}

func (r *RealEstateRepo) RemoveFavorite(ctx context.Context, userID string, listingID int64) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM favorite_listings WHERE user_id=$1 AND listing_id=$2`, userID, listingID)
	return err
}

func (r *RealEstateRepo) ListFavorites(ctx context.Context, userID string) ([]*domain.PropertyListing, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT `+listingCols+` FROM property_listings pl
		 JOIN favorite_listings fl ON fl.listing_id=pl.id
		 WHERE fl.user_id=$1 ORDER BY fl.created_at DESC`, userID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.PropertyListing
	for rows.Next() {
		l := &domain.PropertyListing{}
		if err := scanListing(rows, l); err != nil {
			return nil, err
		}
		list = append(list, l)
	}
	return list, nil
}

func (r *RealEstateRepo) IsFavorite(ctx context.Context, userID string, listingID int64) (bool, error) {
	var exists bool
	err := r.pool.QueryRow(ctx,
		`SELECT EXISTS(SELECT 1 FROM favorite_listings WHERE user_id=$1 AND listing_id=$2)`,
		userID, listingID).Scan(&exists)
	return exists, err
}

// ── Property Inquiry ──────────────────────────────────────

func (r *RealEstateRepo) SendInquiry(ctx context.Context, inq *domain.PropertyInquiry) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO property_inquiries (listing_id, from_user_id, to_user_id, message, parent_id, is_read)
		 VALUES ($1,$2,$3,$4,$5,$6) RETURNING id, created_at`,
		inq.ListingID, inq.FromUserID, inq.ToUserID, inq.Message, inq.ParentID, inq.IsRead,
	).Scan(&inq.ID, &inq.CreatedAt)
}

func (r *RealEstateRepo) ListInquiriesByListing(ctx context.Context, listingID int64) ([]*domain.PropertyInquiry, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, listing_id, from_user_id, to_user_id, COALESCE(message,''), parent_id, is_read, created_at
		 FROM property_inquiries WHERE listing_id=$1 ORDER BY created_at ASC`, listingID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.PropertyInquiry
	for rows.Next() {
		inq := &domain.PropertyInquiry{}
		if err := rows.Scan(&inq.ID, &inq.ListingID, &inq.FromUserID, &inq.ToUserID, &inq.Message, &inq.ParentID, &inq.IsRead, &inq.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, inq)
	}
	return list, nil
}

func (r *RealEstateRepo) ListInquiriesByUser(ctx context.Context, userID string) ([]*domain.PropertyInquiry, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, listing_id, from_user_id, to_user_id, COALESCE(message,''), parent_id, is_read, created_at
		 FROM property_inquiries WHERE from_user_id=$1 OR to_user_id=$1 ORDER BY created_at DESC`, userID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.PropertyInquiry
	for rows.Next() {
		inq := &domain.PropertyInquiry{}
		if err := rows.Scan(&inq.ID, &inq.ListingID, &inq.FromUserID, &inq.ToUserID, &inq.Message, &inq.ParentID, &inq.IsRead, &inq.CreatedAt); err != nil {
			return nil, err
		}
		list = append(list, inq)
	}
	return list, nil
}

func (r *RealEstateRepo) MarkAsRead(ctx context.Context, id int64) error {
	_, err := r.pool.Exec(ctx, `UPDATE property_inquiries SET is_read=true WHERE id=$1`, id)
	return err
}

// ── Company Member ──────────────────────────────────────────

func (r *RealEstateRepo) CreateMember(ctx context.Context, m *domain.CompanyMember) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO company_members (company_id, user_id, role, title, is_active, joined_at)
		 VALUES ($1,$2,$3,$4,$5,$6) RETURNING id, joined_at, created_at, updated_at`,
		m.CompanyID, m.UserID, m.Role, m.Title, m.IsActive, m.JoinedAt,
	).Scan(&m.ID, &m.JoinedAt, &m.CreatedAt, &m.UpdatedAt)
}

func (r *RealEstateRepo) ListMembers(ctx context.Context, companyID int) ([]*domain.CompanyMember, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, company_id, user_id, role, COALESCE(title,''), is_active, joined_at, created_at, updated_at
		 FROM company_members WHERE company_id=$1 ORDER BY joined_at`, companyID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.CompanyMember
	for rows.Next() {
		m := &domain.CompanyMember{}
		if err := rows.Scan(&m.ID, &m.CompanyID, &m.UserID, &m.Role, &m.Title, &m.IsActive, &m.JoinedAt, &m.CreatedAt, &m.UpdatedAt); err != nil {
			return nil, err
		}
		list = append(list, m)
	}
	return list, nil
}

func (r *RealEstateRepo) GetMember(ctx context.Context, companyID int, userID string) (*domain.CompanyMember, error) {
	m := &domain.CompanyMember{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, company_id, user_id, role, COALESCE(title,''), is_active, joined_at, created_at, updated_at
		 FROM company_members WHERE company_id=$1 AND user_id=$2`, companyID, userID,
	).Scan(&m.ID, &m.CompanyID, &m.UserID, &m.Role, &m.Title, &m.IsActive, &m.JoinedAt, &m.CreatedAt, &m.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("get member: %w", err)
	}
	return m, nil
}

func (r *RealEstateRepo) UpdateMemberRole(ctx context.Context, memberID int, role, title string) error {
	_, err := r.pool.Exec(ctx,
		`UPDATE company_members SET role=$1, title=$2, updated_at=NOW() WHERE id=$3`, role, title, memberID)
	return err
}

func (r *RealEstateRepo) RemoveMember(ctx context.Context, memberID int) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM company_members WHERE id=$1`, memberID)
	return err
}

// ── Company Invitation ──────────────────────────────────────

func (r *RealEstateRepo) CreateInvitation(ctx context.Context, inv *domain.CompanyInvitation) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO company_invitations (company_id, inviter_id, invitee_id, invitee_email, role, status, message)
		 VALUES ($1,$2,$3,$4,$5,$6,$7) RETURNING id, created_at, updated_at`,
		inv.CompanyID, inv.InviterID, inv.InviteeID, inv.InviteeEmail, inv.Role, inv.Status, inv.Message,
	).Scan(&inv.ID, &inv.CreatedAt, &inv.UpdatedAt)
}

func (r *RealEstateRepo) ListInvitations(ctx context.Context, companyID int, status string) ([]*domain.CompanyInvitation, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, company_id, inviter_id, invitee_id, COALESCE(invitee_email,''), role, status, COALESCE(message,''), created_at, updated_at
		 FROM company_invitations WHERE company_id=$1 AND ($2='' OR status=$2) ORDER BY created_at DESC`,
		companyID, status)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.CompanyInvitation
	for rows.Next() {
		inv := &domain.CompanyInvitation{}
		if err := rows.Scan(&inv.ID, &inv.CompanyID, &inv.InviterID, &inv.InviteeID, &inv.InviteeEmail, &inv.Role, &inv.Status, &inv.Message, &inv.CreatedAt, &inv.UpdatedAt); err != nil {
			return nil, err
		}
		list = append(list, inv)
	}
	return list, nil
}

func (r *RealEstateRepo) UpdateInvitationStatus(ctx context.Context, invitationID int, status string) error {
	_, err := r.pool.Exec(ctx,
		`UPDATE company_invitations SET status=$1, updated_at=NOW() WHERE id=$2`, status, invitationID)
	return err
}

// ── User Companies ──────────────────────────────────────────

// ── Listing Price Config ──────────────────────────────────────

func (r *RealEstateRepo) GetListingPrice(ctx context.Context, domain, userRole string) (*domain.ListingPriceConfig, error) {
	p := &domain.ListingPriceConfig{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, domain, price, COALESCE(currency,'TRY'), COALESCE(user_role,''), COALESCE(description,''), is_active, created_at, updated_at
		 FROM listing_price_configs WHERE domain=$1 AND ($2='' OR user_role=$2) AND is_active=true
		 ORDER BY user_role DESC NULLS LAST LIMIT 1`, domain, userRole,
	).Scan(&p.ID, &p.Domain, &p.Price, &p.Currency, &p.UserRole, &p.Description, &p.IsActive, &p.CreatedAt, &p.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("get listing price: %w", err)
	}
	return p, nil
}

func (r *RealEstateRepo) GetRegionBenchmark(ctx context.Context, listingID int64) (*domain.RegionBenchmark, error) {
	b := &domain.RegionBenchmark{}
	err := r.pool.QueryRow(ctx,
		`WITH listing_info AS (
			SELECT city, district, type_id, gross_area FROM property_listings WHERE id=$1
		)
		SELECT
			AVG(CASE WHEN l.district=li.district THEN l.price/NULLIF(l.gross_area,0) END) AS district_avg_price_per_m2,
			AVG(CASE WHEN l.city=li.city THEN l.price/NULLIF(l.gross_area,0) END) AS city_avg_price_per_m2,
			MIN(l.price) FILTER (WHERE l.district=li.district) AS district_min_price,
			MAX(l.price) FILTER (WHERE l.district=li.district) AS district_max_price,
			COUNT(*) FILTER (WHERE l.district=li.district AND l.type_id=li.type_id) AS comparable_count
		FROM property_listings l, listing_info li
		WHERE l.id != $1 AND l.status='active'
			AND li.city IS NOT NULL AND li.district IS NOT NULL`,
		listingID,
	).Scan(&b.DistrictAvgPricePerM2, &b.CityAvgPricePerM2, &b.DistrictMinPrice, &b.DistrictMaxPrice, &b.ComparableListingCount)
	if err != nil {
		return nil, fmt.Errorf("get region benchmark: %w", err)
	}
	return b, nil
}

// ── Listing Payment ───────────────────────────────────────────

func (r *RealEstateRepo) CreatePayment(ctx context.Context, p *domain.ListingPayment) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO listing_payments (domain, listing_id, user_id, amount, currency, payment_method, payment_ref, status, paid_at)
		 VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9) RETURNING id, created_at, updated_at`,
		p.Domain, p.ListingID, p.UserID, p.Amount, p.Currency, p.PaymentMethod, p.PaymentRef, p.Status, p.PaidAt,
	).Scan(&p.ID, &p.CreatedAt, &p.UpdatedAt)
}

func (r *RealEstateRepo) GetPaymentByListing(ctx context.Context, domain string, listingID int64) (*domain.ListingPayment, error) {
	p := &domain.ListingPayment{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, domain, listing_id, user_id, amount, COALESCE(currency,'TRY'), COALESCE(payment_method,''), COALESCE(payment_ref,''), COALESCE(status,'pending'), paid_at, created_at, updated_at
		 FROM listing_payments WHERE domain=$1 AND listing_id=$2 ORDER BY created_at DESC LIMIT 1`, domain, listingID,
	).Scan(&p.ID, &p.Domain, &p.ListingID, &p.UserID, &p.Amount, &p.Currency, &p.PaymentMethod, &p.PaymentRef, &p.Status, &p.PaidAt, &p.CreatedAt, &p.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("get payment by listing: %w", err)
	}
	return p, nil
}

func (r *RealEstateRepo) UpdatePaymentStatus(ctx context.Context, paymentID int64, status string) error {
	_, err := r.pool.Exec(ctx,
		`UPDATE listing_payments SET status=$1, paid_at=CASE WHEN $1='completed' THEN NOW() ELSE paid_at END, updated_at=NOW() WHERE id=$2`, status, paymentID)
	return err
}

func (r *RealEstateRepo) ListUserPayments(ctx context.Context, userID string, domain string) ([]*domain.ListingPayment, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, domain, listing_id, user_id, amount, COALESCE(currency,'TRY'), COALESCE(payment_method,''), COALESCE(payment_ref,''), COALESCE(status,'pending'), paid_at, created_at, updated_at
		 FROM listing_payments WHERE user_id=$1 AND ($2='' OR domain=$2) ORDER BY created_at DESC`, userID, domain)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ListingPayment
	for rows.Next() {
		p := &domain.ListingPayment{}
		if err := rows.Scan(&p.ID, &p.Domain, &p.ListingID, &p.UserID, &p.Amount, &p.Currency, &p.PaymentMethod, &p.PaymentRef, &p.Status, &p.PaidAt, &p.CreatedAt, &p.UpdatedAt); err != nil {
			return nil, err
		}
		list = append(list, p)
	}
	return list, nil
}

// ── Listing Document / Tapu-Ruhsat Verification ──────────

func (r *RealEstateRepo) CreateDocument(ctx context.Context, d *domain.ListingDocument) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO listing_documents (domain, listing_id, user_id, company_id, is_company_doc, document_type, document_number, file_path, file_name, file_size, mime_type, description, status)
		 VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13) RETURNING id, created_at, updated_at`,
		d.Domain, d.ListingID, d.UserID, d.CompanyID, d.IsCompanyDoc, d.DocumentType, d.DocumentNumber, d.FilePath, d.FileName, d.FileSize, d.MimeType, d.Description, d.Status,
	).Scan(&d.ID, &d.CreatedAt, &d.UpdatedAt)
}

func (r *RealEstateRepo) GetDocument(ctx context.Context, docID int64) (*domain.ListingDocument, error) {
	d := &domain.ListingDocument{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, domain, listing_id, user_id, company_id, is_company_doc, COALESCE(document_type,''), COALESCE(document_number,''), COALESCE(file_path,''), COALESCE(file_name,''), COALESCE(file_size,0), COALESCE(mime_type,''), COALESCE(description,''), COALESCE(status,'pending'), COALESCE(rejection_reason,''), verified_by, verified_at, created_at, updated_at
		 FROM listing_documents WHERE id=$1`, docID,
	).Scan(&d.ID, &d.Domain, &d.ListingID, &d.UserID, &d.CompanyID, &d.IsCompanyDoc, &d.DocumentType, &d.DocumentNumber, &d.FilePath, &d.FileName, &d.FileSize, &d.MimeType, &d.Description, &d.Status, &d.RejectionReason, &d.VerifiedBy, &d.VerifiedAt, &d.CreatedAt, &d.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("get document: %w", err)
	}
	return d, nil
}

func (r *RealEstateRepo) ListDocuments(ctx context.Context, domainStr string, listingID int64) ([]*domain.ListingDocument, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, domain, listing_id, user_id, company_id, is_company_doc, COALESCE(document_type,''), COALESCE(document_number,''), COALESCE(file_path,''), COALESCE(file_name,''), COALESCE(file_size,0), COALESCE(mime_type,''), COALESCE(description,''), COALESCE(status,'pending'), COALESCE(rejection_reason,''), verified_by, verified_at, created_at, updated_at
		 FROM listing_documents WHERE domain=$1 AND listing_id=$2 ORDER BY created_at DESC`, domainStr, listingID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ListingDocument
	for rows.Next() {
		d := &domain.ListingDocument{}
		if err := rows.Scan(&d.ID, &d.Domain, &d.ListingID, &d.UserID, &d.CompanyID, &d.IsCompanyDoc, &d.DocumentType, &d.DocumentNumber, &d.FilePath, &d.FileName, &d.FileSize, &d.MimeType, &d.Description, &d.Status, &d.RejectionReason, &d.VerifiedBy, &d.VerifiedAt, &d.CreatedAt, &d.UpdatedAt); err != nil {
			return nil, err
		}
		list = append(list, d)
	}
	return list, nil
}

func (r *RealEstateRepo) ListUserDocuments(ctx context.Context, userID, domainStr string) ([]*domain.ListingDocument, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, domain, listing_id, user_id, company_id, is_company_doc, COALESCE(document_type,''), COALESCE(document_number,''), COALESCE(file_path,''), COALESCE(file_name,''), COALESCE(file_size,0), COALESCE(mime_type,''), COALESCE(description,''), COALESCE(status,'pending'), COALESCE(rejection_reason,''), verified_by, verified_at, created_at, updated_at
		 FROM listing_documents WHERE user_id=$1 AND ($2='' OR domain=$2) ORDER BY created_at DESC`, userID, domainStr)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ListingDocument
	for rows.Next() {
		d := &domain.ListingDocument{}
		if err := rows.Scan(&d.ID, &d.Domain, &d.ListingID, &d.UserID, &d.CompanyID, &d.IsCompanyDoc, &d.DocumentType, &d.DocumentNumber, &d.FilePath, &d.FileName, &d.FileSize, &d.MimeType, &d.Description, &d.Status, &d.RejectionReason, &d.VerifiedBy, &d.VerifiedAt, &d.CreatedAt, &d.UpdatedAt); err != nil {
			return nil, err
		}
		list = append(list, d)
	}
	return list, nil
}

func (r *RealEstateRepo) UpdateDocumentStatus(ctx context.Context, docID int64, status, rejectionReason string, verifiedBy string) error {
	_, err := r.pool.Exec(ctx,
		`UPDATE listing_documents SET status=$1, rejection_reason=$2, verified_by=$3, verified_at=CASE WHEN $1 IN ('verified','approved') THEN NOW() ELSE NULL END, updated_at=NOW() WHERE id=$4`,
		status, rejectionReason, verifiedBy, docID)
	return err
}

func (r *RealEstateRepo) CreateVerificationRecord(ctx context.Context, docID int64, verifiedBy, action, reason string) error {
	_, err := r.pool.Exec(ctx,
		`INSERT INTO document_verifications (document_id, verified_by, action, reason) VALUES ($1,$2,$3,$4)`,
		docID, verifiedBy, action, reason)
	return err
}

func (r *RealEstateRepo) CountVerifiedDocuments(ctx context.Context, listingID int64, domainStr string) (int, error) {
	var count int
	err := r.pool.QueryRow(ctx,
		`SELECT COUNT(*) FROM listing_documents WHERE listing_id=$1 AND domain=$2 AND status IN ('verified','approved')`,
		listingID, domainStr).Scan(&count)
	return count, err
}

func (r *RealEstateRepo) UpdateListingStatus(ctx context.Context, listingID int64, status string) error {
	_, err := r.pool.Exec(ctx, `UPDATE property_listings SET status=$1, updated_at=NOW() WHERE id=$2`, status, listingID)
	return err
}

func (r *RealEstateRepo) ListUserCompanies(ctx context.Context, userID string) ([]*domain.ContractorCompany, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT c.id, c.name, c.slug, COALESCE(c.tax_no,''), COALESCE(c.tax_office,''), COALESCE(c.phone,''), COALESCE(c.email,''), COALESCE(c.address,''), COALESCE(c.website,''), COALESCE(c.logo_url,''), COALESCE(c.description,''), c.rating, c.review_count, c.is_verified, c.is_active, c.latitude, c.longitude, COALESCE(c.verification_status,''), COALESCE(c.verification_note,''), c.verified_at, COALESCE(c.certificate_no,''), c.certificate_expiry, c.created_at, c.updated_at
		 FROM contractor_companies c
		 JOIN company_members m ON m.company_id=c.id
		 WHERE m.user_id=$1 AND m.is_active=true
		 ORDER BY c.name`, userID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ContractorCompany
	for rows.Next() {
		c := &domain.ContractorCompany{}
		if err := rows.Scan(&c.ID, &c.Name, &c.Slug, &c.TaxNo, &c.TaxOffice, &c.Phone, &c.Email, &c.Address, &c.Website, &c.LogoURL, &c.Description, &c.Rating, &c.ReviewCount, &c.IsVerified, &c.IsActive, &c.Latitude, &c.Longitude, &c.VerificationStatus, &c.VerificationNote, &c.VerifiedAt, &c.CertificateNo, &c.CertificateExpiry, &c.CreatedAt, &c.UpdatedAt); err != nil {
			return nil, err
		}
		list = append(list, c)
	}
	return list, nil
}

// ── Company Document ──────────────────────────────────────────

func (r *RealEstateRepo) CreateCompanyDocument(ctx context.Context, doc *domain.ListingDocument) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO listing_documents (domain, listing_id, user_id, company_id, is_company_doc, document_type, document_number, file_path, file_name, file_size, mime_type, description, status)
		 VALUES ($1,$2,$3,$4,true,$5,$6,$7,$8,$9,$10,$11,$12) RETURNING id, created_at, updated_at`,
		doc.Domain, doc.ListingID, doc.UserID, doc.CompanyID, doc.DocumentType, doc.DocumentNumber, doc.FilePath, doc.FileName, doc.FileSize, doc.MimeType, doc.Description, doc.Status,
	).Scan(&doc.ID, &doc.CreatedAt, &doc.UpdatedAt)
}

func (r *RealEstateRepo) ListCompanyDocuments(ctx context.Context, companyID int) ([]*domain.ListingDocument, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, domain, listing_id, user_id, company_id, is_company_doc, COALESCE(document_type,''), COALESCE(document_number,''), COALESCE(file_path,''), COALESCE(file_name,''), COALESCE(file_size,0), COALESCE(mime_type,''), COALESCE(description,''), COALESCE(status,'pending'), COALESCE(rejection_reason,''), verified_by, verified_at, created_at, updated_at
		 FROM listing_documents WHERE company_id=$1 AND is_company_doc=true ORDER BY created_at DESC`, companyID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ListingDocument
	for rows.Next() {
		d := &domain.ListingDocument{}
		if err := rows.Scan(&d.ID, &d.Domain, &d.ListingID, &d.UserID, &d.CompanyID, &d.IsCompanyDoc, &d.DocumentType, &d.DocumentNumber, &d.FilePath, &d.FileName, &d.FileSize, &d.MimeType, &d.Description, &d.Status, &d.RejectionReason, &d.VerifiedBy, &d.VerifiedAt, &d.CreatedAt, &d.UpdatedAt); err != nil {
			return nil, err
		}
		list = append(list, d)
	}
	return list, nil
}

func (r *RealEstateRepo) CountCompanyVerifiedDocuments(ctx context.Context, companyID int) (int, error) {
	var count int
	err := r.pool.QueryRow(ctx,
		`SELECT COUNT(*) FROM listing_documents WHERE company_id=$1 AND is_company_doc=true AND status IN ('verified','approved')`,
		companyID).Scan(&count)
	return count, err
}

// ── Company Verification ───────────────────────────────────────

func (r *RealEstateRepo) UpdateCompanyVerification(ctx context.Context, companyID int, status, note string, verifiedBy string) error {
	_, err := r.pool.Exec(ctx,
		`UPDATE contractor_companies SET verification_status=$1, verification_note=$2, verified_at=NOW(), is_verified=$1='approved' WHERE id=$3`,
		status, note, companyID)
	return err
}

func (r *RealEstateRepo) ListCompaniesByVerification(ctx context.Context, status string) ([]*domain.ContractorCompany, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, name, slug, COALESCE(tax_no,''), COALESCE(tax_office,''), COALESCE(phone,''), COALESCE(email,''), COALESCE(address,''), COALESCE(website,''), COALESCE(logo_url,''), COALESCE(description,''), rating, review_count, is_verified, is_active, latitude, longitude, COALESCE(verification_status,''), COALESCE(verification_note,''), verified_at, COALESCE(certificate_no,''), certificate_expiry, created_at, updated_at
		 FROM contractor_companies WHERE verification_status=$1 ORDER BY name`, status)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ContractorCompany
	for rows.Next() {
		c := &domain.ContractorCompany{}
		if err := rows.Scan(&c.ID, &c.Name, &c.Slug, &c.TaxNo, &c.TaxOffice, &c.Phone, &c.Email, &c.Address, &c.Website, &c.LogoURL, &c.Description, &c.Rating, &c.ReviewCount, &c.IsVerified, &c.IsActive, &c.Latitude, &c.Longitude, &c.VerificationStatus, &c.VerificationNote, &c.VerifiedAt, &c.CertificateNo, &c.CertificateExpiry, &c.CreatedAt, &c.UpdatedAt); err != nil {
			return nil, err
		}
		list = append(list, c)
	}
	return list, nil
}

func (r *RealEstateRepo) GetPendingVerificationCompanies(ctx context.Context) ([]*domain.ContractorCompany, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, name, slug, COALESCE(tax_no,''), COALESCE(tax_office,''), COALESCE(phone,''), COALESCE(email,''), COALESCE(address,''), COALESCE(website,''), COALESCE(logo_url,''), COALESCE(description,''), rating, review_count, is_verified, is_active, latitude, longitude, COALESCE(verification_status,''), COALESCE(verification_note,''), verified_at, COALESCE(certificate_no,''), certificate_expiry, created_at, updated_at
		 FROM contractor_companies WHERE verification_status='pending' OR verification_status='' ORDER BY name`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var list []*domain.ContractorCompany
	for rows.Next() {
		c := &domain.ContractorCompany{}
		if err := rows.Scan(&c.ID, &c.Name, &c.Slug, &c.TaxNo, &c.TaxOffice, &c.Phone, &c.Email, &c.Address, &c.Website, &c.LogoURL, &c.Description, &c.Rating, &c.ReviewCount, &c.IsVerified, &c.IsActive, &c.Latitude, &c.Longitude, &c.VerificationStatus, &c.VerificationNote, &c.VerifiedAt, &c.CertificateNo, &c.CertificateExpiry, &c.CreatedAt, &c.UpdatedAt); err != nil {
			return nil, err
		}
		list = append(list, c)
	}
	return list, nil
}
