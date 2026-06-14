package domain

import "time"

type ExpertCompany struct {
	ID          int        `json:"id"`
	Name        string     `json:"name"`
	Slug        string     `json:"slug"`
	Address     string     `json:"address,omitempty"`
	Phone       string     `json:"phone,omitempty"`
	Email       string     `json:"email,omitempty"`
	Website     string     `json:"website,omitempty"`
	LogoURL     *string    `json:"logo_url,omitempty"`
	Description string     `json:"description,omitempty"`
	IsActive    bool       `json:"is_active"`
	CreatedAt   time.Time  `json:"created_at"`
	UpdatedAt   *time.Time `json:"updated_at,omitempty"`
}

type Expert struct {
	ID        int        `json:"id"`
	CompanyID int        `json:"company_id"`
	UserID    *int       `json:"user_id,omitempty"`
	FirstName string     `json:"first_name"`
	LastName  string     `json:"last_name"`
	Title     string     `json:"title,omitempty"`
	Email     string     `json:"email,omitempty"`
	Phone     string     `json:"phone,omitempty"`
	Bio       string     `json:"bio,omitempty"`
	AvatarURL *string    `json:"avatar_url,omitempty"`
	IsActive  bool       `json:"is_active"`
	CreatedAt time.Time  `json:"created_at"`
	UpdatedAt *time.Time `json:"updated_at,omitempty"`
}

type ExpertPackage struct {
	ID           int        `json:"id"`
	CompanyID    int        `json:"company_id"`
	Name         string     `json:"name"`
	Slug         string     `json:"slug"`
	Description  string     `json:"description,omitempty"`
	Price        float64    `json:"price"`
	DurationDays int        `json:"duration_days"`
	Features     string     `json:"features,omitempty"`
	IsActive     bool       `json:"is_active"`
	CreatedAt    time.Time  `json:"created_at"`
}

type ExpertVehicle struct {
	ID            int       `json:"id"`
	ReportID      *int      `json:"report_id,omitempty"`
	ExpertID      *int      `json:"expert_id,omitempty"`
	Plate         string    `json:"plate,omitempty"`
	ChassisNumber string    `json:"chassis_number,omitempty"`
	BrandID       int       `json:"brand_id"`
	ModelID       int       `json:"model_id"`
	ModelYearID   int       `json:"model_year_id"`
	Year          int       `json:"year"`
	CreatedAt     time.Time `json:"created_at"`
}

type ExpertReport struct {
	ID             int        `json:"id"`
	ExpertVehicleID int       `json:"expert_vehicle_id"`
	ExpertID       int        `json:"expert_id"`
	CompanyID      int        `json:"company_id"`
	Status         string     `json:"status"`
	ReportType     string     `json:"report_type,omitempty"`
	Notes          string     `json:"notes,omitempty"`
	Score          *float64   `json:"score,omitempty"`
	CreatedAt      time.Time  `json:"created_at"`
	UpdatedAt      *time.Time `json:"updated_at,omitempty"`
}

type ExpertPanelMeasurement struct {
	ID              int       `json:"id"`
	ReportID        int       `json:"report_id"`
	PanelName       string    `json:"panel_name"`
	MeasurementType string    `json:"measurement_type"`
	Value           float64   `json:"value"`
	Unit            string    `json:"unit,omitempty"`
	Notes           string    `json:"notes,omitempty"`
	CreatedAt       time.Time `json:"created_at"`
}

type ExpertInteriorCheck struct {
	ID        int       `json:"id"`
	ReportID  int       `json:"report_id"`
	ItemName  string    `json:"item_name"`
	Condition string    `json:"condition"`
	Notes     string    `json:"notes,omitempty"`
	Score     *int      `json:"score,omitempty"`
	CreatedAt time.Time `json:"created_at"`
}

type ExpertExteriorCheck struct {
	ID        int       `json:"id"`
	ReportID  int       `json:"report_id"`
	ItemName  string    `json:"item_name"`
	Condition string    `json:"condition"`
	Notes     string    `json:"notes,omitempty"`
	Score     *int      `json:"score,omitempty"`
	CreatedAt time.Time `json:"created_at"`
}

type ExpertMechanicalCheck struct {
	ID        int       `json:"id"`
	ReportID  int       `json:"report_id"`
	ItemName  string    `json:"item_name"`
	Condition string    `json:"condition"`
	Notes     string    `json:"notes,omitempty"`
	Score     *int      `json:"score,omitempty"`
	CreatedAt time.Time `json:"created_at"`
}

type ExpertElectronicCheck struct {
	ID        int       `json:"id"`
	ReportID  int       `json:"report_id"`
	ItemName  string    `json:"item_name"`
	Condition string    `json:"condition"`
	Notes     string    `json:"notes,omitempty"`
	Score     *int      `json:"score,omitempty"`
	CreatedAt time.Time `json:"created_at"`
}

type ExpertTireCheck struct {
	ID          int       `json:"id"`
	ReportID    int       `json:"report_id"`
	TirePosition string   `json:"tire_position"`
	Brand       string    `json:"brand,omitempty"`
	TreadDepth  *float64  `json:"tread_depth,omitempty"`
	Pressure    *float64  `json:"pressure,omitempty"`
	Condition   string    `json:"condition,omitempty"`
	Notes       string    `json:"notes,omitempty"`
	CreatedAt   time.Time `json:"created_at"`
}

type ExpertTramerRecord struct {
	ID          int       `json:"id"`
	ReportID    int       `json:"report_id"`
	RecordType  string    `json:"record_type"`
	Source      string    `json:"source,omitempty"`
	Description string    `json:"description,omitempty"`
	CreatedAt   time.Time `json:"created_at"`
}

type ExpertTestDrive struct {
	ID               int        `json:"id"`
	ReportID         int        `json:"report_id"`
	EvaluatorName    string     `json:"evaluator_name,omitempty"`
	StartKm          int        `json:"start_km,omitempty"`
	EndKm            int        `json:"end_km,omitempty"`
	GeneralImpression string    `json:"general_impression,omitempty"`
	Notes            string     `json:"notes,omitempty"`
	CreatedAt        time.Time  `json:"created_at"`
}

type ExpertDynoTest struct {
	ID        int       `json:"id"`
	ReportID  int       `json:"report_id"`
	TestType  string    `json:"test_type,omitempty"`
	MaxPower  *float64  `json:"max_power,omitempty"`
	MaxTorque *float64  `json:"max_torque,omitempty"`
	Notes     string    `json:"notes,omitempty"`
	CreatedAt time.Time `json:"created_at"`
}

type ExpertPhoto struct {
	ID          int       `json:"id"`
	ReportID    int       `json:"report_id"`
	URL         string    `json:"url"`
	PhotoType   string    `json:"photo_type,omitempty"`
	Description string    `json:"description,omitempty"`
	SortOrder   int       `json:"sort_order"`
	CreatedAt   time.Time `json:"created_at"`
}

type ExpertEmissionTest struct {
	ID        int       `json:"id"`
	ReportID  int       `json:"report_id"`
	CO2       *float64  `json:"co2,omitempty"`
	HC        *float64  `json:"hc,omitempty"`
	CO        *float64  `json:"co,omitempty"`
	NOx       *float64  `json:"nox,omitempty"`
	O2        *float64  `json:"o2,omitempty"`
	Lambda    *float64  `json:"lambda,omitempty"`
	Result    string    `json:"result,omitempty"`
	Notes     string    `json:"notes,omitempty"`
	CreatedAt time.Time `json:"created_at"`
}

type ExpertFluidTest struct {
	ID        int       `json:"id"`
	ReportID  int       `json:"report_id"`
	FluidType string    `json:"fluid_type"`
	Condition string    `json:"condition,omitempty"`
	Level     string    `json:"level,omitempty"`
	Notes     string    `json:"notes,omitempty"`
	CreatedAt time.Time `json:"created_at"`
}

type ExpertHandbrakeTest struct {
	ID            int       `json:"id"`
	ReportID      int       `json:"report_id"`
	Effectiveness *int      `json:"effectiveness,omitempty"`
	Notes         string    `json:"notes,omitempty"`
	CreatedAt     time.Time `json:"created_at"`
}

type ExpertFourWheelDriveCheck struct {
	ID         int       `json:"id"`
	ReportID   int       `json:"report_id"`
	FrontLeft  string    `json:"front_left,omitempty"`
	FrontRight string    `json:"front_right,omitempty"`
	RearLeft   string    `json:"rear_left,omitempty"`
	RearRight  string    `json:"rear_right,omitempty"`
	Notes      string    `json:"notes,omitempty"`
	CreatedAt  time.Time `json:"created_at"`
}

type ExpertBeltCheck struct {
	ID        int       `json:"id"`
	ReportID  int       `json:"report_id"`
	BeltName  string    `json:"belt_name"`
	Condition string    `json:"condition,omitempty"`
	Notes     string    `json:"notes,omitempty"`
	CreatedAt time.Time `json:"created_at"`
}

type ExpertChassisCheck struct {
	ID        int       `json:"id"`
	ReportID  int       `json:"report_id"`
	Section   string    `json:"section"`
	Condition string    `json:"condition,omitempty"`
	Notes     string    `json:"notes,omitempty"`
	CreatedAt time.Time `json:"created_at"`
}

type ExpertExtraEquipment struct {
	ID            int       `json:"id"`
	ReportID      int       `json:"report_id"`
	EquipmentName string    `json:"equipment_name"`
	IsWorking     bool      `json:"is_working"`
	Notes         string    `json:"notes,omitempty"`
	CreatedAt     time.Time `json:"created_at"`
}

type ExpertMandatoryEquipment struct {
	ID            int       `json:"id"`
	ReportID      int       `json:"report_id"`
	EquipmentName string    `json:"equipment_name"`
	IsPresent     bool      `json:"is_present"`
	IsValid       bool      `json:"is_valid"`
	Notes         string    `json:"notes,omitempty"`
	CreatedAt     time.Time `json:"created_at"`
}

type ExpertAcceptanceCriteria struct {
	ID           int       `json:"id"`
	ReportID     int       `json:"report_id"`
	CriteriaName string    `json:"criteria_name"`
	IsMet        bool      `json:"is_met"`
	Notes        string    `json:"notes,omitempty"`
	CreatedAt    time.Time `json:"created_at"`
}
