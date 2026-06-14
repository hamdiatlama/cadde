package domain

import "time"

type PropertyCategory struct {
	ID        int       `json:"id"`
	Name      string    `json:"name"`
	Slug      string    `json:"slug"`
	SortOrder int       `json:"sort_order"`
	CreatedAt time.Time `json:"created_at"`
}

type PropertyType struct {
	ID        int       `json:"id"`
	Name      string    `json:"name"`
	Slug      string    `json:"slug"`
	Icon      string    `json:"icon"`
	SortOrder int       `json:"sort_order"`
	CreatedAt time.Time `json:"created_at"`
}

type ContractorCompany struct {
	ID                 int        `json:"id"`
	Name               string     `json:"name"`
	Slug               string     `json:"slug"`
	TaxNo              string     `json:"tax_no"`
	TaxOffice          string     `json:"tax_office"`
	Phone              string     `json:"phone"`
	Email              string     `json:"email"`
	Address            string     `json:"address"`
	Website            string     `json:"website"`
	LogoURL            string     `json:"logo_url"`
	Description        string     `json:"description"`
	Rating             float64    `json:"rating"`
	ReviewCount        int        `json:"review_count"`
	IsVerified         bool       `json:"is_verified"`
	IsActive           bool       `json:"is_active"`
	Latitude           float64    `json:"latitude"`
	Longitude          float64    `json:"longitude"`
	VerificationStatus string     `json:"verification_status"`
	VerificationNote   string     `json:"verification_note"`
	VerifiedAt         *time.Time `json:"verified_at,omitempty"`
	CertificateNo      string     `json:"certificate_no"`
	CertificateExpiry  *time.Time `json:"certificate_expiry,omitempty"`
	CreatedAt          time.Time  `json:"created_at"`
	UpdatedAt          time.Time  `json:"updated_at"`
}

type ContractorReview struct {
	ID        int64     `json:"id"`
	CompanyID int       `json:"company_id"`
	UserID    string    `json:"user_id"`
	Rating    int       `json:"rating"`
	Comment   string    `json:"comment"`
	CreatedAt time.Time `json:"created_at"`
}

type PropertyListing struct {
	ID                     int64      `json:"id"`
	UserID                 string     `json:"user_id"`
	CategoryID             int        `json:"category_id"`
	TypeID                 int        `json:"type_id"`
	ContractorID           *int       `json:"contractor_id,omitempty"`
	Title                  string     `json:"title"`
	Description            string     `json:"description"`
	Price                  float64    `json:"price"`
	Currency               string     `json:"currency"`
	IsForSale              bool       `json:"is_for_sale"`
	IsForRent              bool       `json:"is_for_rent"`
	RentDeposit            *float64   `json:"rent_deposit,omitempty"`
	Dues                   *float64   `json:"dues,omitempty"`
	Latitude               float64    `json:"latitude"`
	Longitude              float64    `json:"longitude"`
	Country                string     `json:"country"`
	City                   string     `json:"city"`
	District               string     `json:"district"`
	Neighborhood           string     `json:"neighborhood"`
	Address                string     `json:"address"`
	MapAddress             string     `json:"map_address"`
	BuildingName           string     `json:"building_name"`
	Block                  string     `json:"block"`
	Floor                  string     `json:"floor"`
	DoorNumber             string     `json:"door_number"`
	ConstructionYear       *int       `json:"construction_year,omitempty"`
	BuildingAge            *int       `json:"building_age,omitempty"`
	FloorCount             *int       `json:"floor_count,omitempty"`
	TotalApartments        *int       `json:"total_apartments,omitempty"`
	ContractorNameHistory  string     `json:"contractor_name_history"`
	LandArea               *float64   `json:"land_area,omitempty"`
	BuildingArea           *float64   `json:"building_area,omitempty"`
	ZoningStatus           string     `json:"zoning_status"`
	LandUseType            string     `json:"land_use_type"`
	DensityValue           string     `json:"density_value"`
	ParcelNo               string     `json:"parcel_no"`
	IslandNo               string     `json:"island_no"`
	RoomCount              string     `json:"room_count"`
	BathroomCount          *int       `json:"bathroom_count,omitempty"`
	NetArea                *float64   `json:"net_area,omitempty"`
	GrossArea              *float64   `json:"gross_area,omitempty"`
	HeatingType            string     `json:"heating_type"`
	Furnishing             string     `json:"furnishing"`
	Facade                 string     `json:"facade"`
	BalconyCount           int        `json:"balcony_count"`
	Status                 string     `json:"status"`
	ViewCount              int        `json:"view_count"`
	IsHighlighted          bool       `json:"is_highlighted"`
	ValidFrom              *time.Time `json:"valid_from,omitempty"`
	ValidUntil             *time.Time `json:"valid_until,omitempty"`
	CreatedAt              time.Time  `json:"created_at"`
	UpdatedAt              time.Time  `json:"updated_at"`
}

type PropertyPhoto struct {
	ID          int64     `json:"id"`
	ListingID   int64     `json:"listing_id"`
	FilePath    string    `json:"file_path"`
	Category    string    `json:"category"`
	Description string    `json:"description"`
	IsCover     bool      `json:"is_cover"`
	SortOrder   int       `json:"sort_order"`
	CreatedAt   time.Time `json:"created_at"`
}

type PropertyFeature struct {
	ID        int       `json:"id"`
	Name      string    `json:"name"`
	Slug      string    `json:"slug"`
	Icon      string    `json:"icon"`
	Category  string    `json:"category"`
	SortOrder int       `json:"sort_order"`
	CreatedAt time.Time `json:"created_at"`
}

type PropertyListingFeature struct {
	ListingID int64  `json:"listing_id"`
	FeatureID int    `json:"feature_id"`
	Value     string `json:"value"`
}

type AuthorizationRequest struct {
	ID             int64      `json:"id"`
	ListingID      int64      `json:"listing_id"`
	OwnerID        string     `json:"owner_id"`
	CompanyID      int        `json:"company_id"`
	AuthType       string     `json:"auth_type"`
	CommissionRate *float64   `json:"commission_rate,omitempty"`
	CommissionFixed *float64  `json:"commission_fixed,omitempty"`
	ValidFrom      time.Time  `json:"valid_from"`
	ValidUntil     *time.Time `json:"valid_until,omitempty"`
	Status         string     `json:"status"`
	OwnerNote      string     `json:"owner_note"`
	CompanyNote    string     `json:"company_note"`
	CreatedAt      time.Time  `json:"created_at"`
	UpdatedAt      time.Time  `json:"updated_at"`
}

type PropertyAppraisalRequest struct {
	ID             int64      `json:"id"`
	UserID         string     `json:"user_id"`
	ListingID      *int64     `json:"listing_id,omitempty"`
	CompanyID      *int       `json:"company_id,omitempty"`
	ExpertID       *int       `json:"expert_id,omitempty"`
	City           string     `json:"city"`
	District       string     `json:"district"`
	Neighborhood   string     `json:"neighborhood"`
	Address        string     `json:"address"`
	Latitude       *float64   `json:"latitude,omitempty"`
	Longitude      *float64   `json:"longitude,omitempty"`
	PropertyTypeID *int       `json:"property_type_id,omitempty"`
	LandArea       *float64   `json:"land_area,omitempty"`
	BuildingArea   *float64   `json:"building_area,omitempty"`
	RoomCount      string     `json:"room_count"`
	ConstructionYear *int     `json:"construction_year,omitempty"`
	Status         string     `json:"status"`
	Notes          string     `json:"notes"`
	ReportData     *string    `json:"report_data,omitempty"`
	ReportFileURL  string     `json:"report_file_url"`
	RequestedDate  *time.Time `json:"requested_date,omitempty"`
	CompletedDate  *time.Time `json:"completed_date,omitempty"`
	CreatedAt      time.Time  `json:"created_at"`
	UpdatedAt      time.Time  `json:"updated_at"`
}

type FavoriteListing struct {
	UserID    string    `json:"user_id"`
	ListingID int64     `json:"listing_id"`
	CreatedAt time.Time `json:"created_at"`
}

type PropertyInquiry struct {
	ID         int64      `json:"id"`
	ListingID  int64      `json:"listing_id"`
	FromUserID string     `json:"from_user_id"`
	ToUserID   string     `json:"to_user_id"`
	Message    string     `json:"message"`
	ParentID   *int64     `json:"parent_id,omitempty"`
	IsRead     bool       `json:"is_read"`
	CreatedAt  time.Time  `json:"created_at"`
}

type CompanyMember struct {
	ID        int       `json:"id"`
	CompanyID int       `json:"company_id"`
	UserID    string    `json:"user_id"`
	Role      string    `json:"role"`
	Title     string    `json:"title"`
	IsActive  bool      `json:"is_active"`
	JoinedAt  time.Time `json:"joined_at"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

type CompanyInvitation struct {
	ID           int        `json:"id"`
	CompanyID    int        `json:"company_id"`
	InviterID    string     `json:"inviter_id"`
	InviteeID    *string    `json:"invitee_id,omitempty"`
	InviteeEmail string     `json:"invitee_email"`
	Role         string     `json:"role"`
	Status       string     `json:"status"`
	Message      string     `json:"message"`
	CreatedAt    time.Time  `json:"created_at"`
	UpdatedAt    time.Time  `json:"updated_at"`
}

type ListingPriceConfig struct {
	ID          int       `json:"id"`
	Domain      string    `json:"domain"`
	Price       float64   `json:"price"`
	Currency    string    `json:"currency"`
	UserRole    string    `json:"user_role"`
	Description string    `json:"description"`
	IsActive    bool      `json:"is_active"`
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
}

type RegionBenchmark struct {
	DistrictAvgPricePerM2  *float64 `json:"district_avg_price_per_m2,omitempty"`
	CityAvgPricePerM2      *float64 `json:"city_avg_price_per_m2,omitempty"`
	DistrictMinPrice       *float64 `json:"district_min_price,omitempty"`
	DistrictMaxPrice       *float64 `json:"district_max_price,omitempty"`
	ComparableListingCount int      `json:"comparable_listing_count"`
}

type ListingPayment struct {
	ID            int64      `json:"id"`
	Domain        string     `json:"domain"`
	ListingID     int64      `json:"listing_id"`
	UserID        string     `json:"user_id"`
	Amount        float64    `json:"amount"`
	Currency      string     `json:"currency"`
	PaymentMethod string     `json:"payment_method"`
	PaymentRef    string     `json:"payment_ref"`
	Status        string     `json:"status"`
	PaidAt        *time.Time `json:"paid_at,omitempty"`
	CreatedAt     time.Time  `json:"created_at"`
	UpdatedAt     time.Time  `json:"updated_at"`
}

type ListingDocument struct {
	ID              int64      `json:"id"`
	Domain          string     `json:"domain"`
	ListingID       int64      `json:"listing_id"`
	UserID          string     `json:"user_id"`
	CompanyID       *int       `json:"company_id,omitempty"`
	IsCompanyDoc    bool       `json:"is_company_doc"`
	DocumentType    string     `json:"document_type"`
	DocumentNumber  string     `json:"document_number"`
	FilePath        string     `json:"file_path"`
	FileName        string     `json:"file_name"`
	FileSize        int64      `json:"file_size"`
	MimeType        string     `json:"mime_type"`
	Description     string     `json:"description"`
	Status          string     `json:"status"`
	RejectionReason string     `json:"rejection_reason"`
	VerifiedBy      *string    `json:"verified_by,omitempty"`
	VerifiedAt      *time.Time `json:"verified_at,omitempty"`
	CreatedAt       time.Time  `json:"created_at"`
	UpdatedAt       time.Time  `json:"updated_at"`
}

type DocumentVerification struct {
	ID         int64     `json:"id"`
	DocumentID int64     `json:"document_id"`
	VerifiedBy string    `json:"verified_by"`
	Action     string    `json:"action"`
	Reason     string    `json:"reason"`
	CreatedAt  time.Time `json:"created_at"`
}
