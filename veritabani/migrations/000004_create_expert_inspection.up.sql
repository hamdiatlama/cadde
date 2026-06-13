-- ============================================================
-- DOMAIN: OTO EKSPERTİZ (Auto Expert Inspection)
-- ============================================================
-- Mevcut oto_ekspertiz_schema.sql'deki yapıyı e-ticaret
-- sistemine entegre eder. Fotoğraflar MinIO'ya taşınır.

-- Firma / Bayi
CREATE TABLE expert_companies (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    tse_no          VARCHAR(50),
    phone           VARCHAR(20),
    address         TEXT,
    email           VARCHAR(100),
    tax_office      VARCHAR(100),
    tax_no          VARCHAR(20),
    authorized_person VARCHAR(100),
    is_active       BOOLEAN NOT NULL DEFAULT true,
    location        GEOGRAPHY(POINT, 4326),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Eksper kullanıcıları (users tablosuna referans)
CREATE TABLE experts (
    id              SERIAL PRIMARY KEY,
    user_id         UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    company_id      INT NOT NULL REFERENCES expert_companies(id) ON DELETE CASCADE,
    title           VARCHAR(100),
    signature_data  TEXT,
    license_no      VARCHAR(50),
    is_active       BOOLEAN NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Ekspertiz paketleri
CREATE TABLE expert_packages (
    id              SMALLSERIAL PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    price           NUMERIC(10,2) NOT NULL DEFAULT 0,
    description     TEXT,
    is_active       BOOLEAN NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Araçlar
CREATE TABLE expert_vehicles (
    id              SERIAL PRIMARY KEY,
    plate           VARCHAR(20) NOT NULL,
    chassis_no      VARCHAR(50) NOT NULL,
    engine_no       VARCHAR(50),
    brand_id        INT REFERENCES vehicle_brands(id),
    model_id        INT REFERENCES vehicle_models(id),
    model_year      SMALLINT,
    color_type      VARCHAR(20),
    fuel_type       VARCHAR(20),
    vehicle_type    VARCHAR(20),
    mileage         INT,
    inspection_date DATE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (plate, chassis_no)
);

CREATE INDEX idx_expveh_plate ON expert_vehicles(plate);
CREATE INDEX idx_expveh_chassis ON expert_vehicles(chassis_no);

-- Raport durumları
CREATE TYPE report_status AS ENUM ('draft', 'approved', 'cancelled');
CREATE TYPE check_result AS ENUM ('passed', 'failed', 'warning');

-- Ana rapor tablosu
CREATE TABLE expert_reports (
    id              BIGSERIAL PRIMARY KEY,
    report_no       VARCHAR(50) UNIQUE NOT NULL,
    company_id      INT NOT NULL REFERENCES expert_companies(id),
    expert_id       INT NOT NULL REFERENCES experts(id),
    vehicle_id      INT NOT NULL REFERENCES expert_vehicles(id),
    package_id      SMALLINT REFERENCES expert_packages(id),
    report_date     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    key_check       BOOLEAN DEFAULT true,
    license_check   BOOLEAN DEFAULT true,
    fee             NUMERIC(10,2),
    expert_note     TEXT,
    overall_result  check_result,
    qr_code         TEXT,
    validity_date   DATE,
    status          report_status NOT NULL DEFAULT 'draft',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (report_date);

CREATE INDEX idx_reports_company ON expert_reports(company_id);
CREATE INDEX idx_reports_expert ON expert_reports(expert_id);
CREATE INDEX idx_reports_vehicle ON expert_reports(vehicle_id);
CREATE INDEX idx_reports_no ON expert_reports(report_no);

-- Aylık partitionlar
CREATE TABLE expert_reports_2026_01 PARTITION OF expert_reports
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE expert_reports_2026_02 PARTITION OF expert_reports
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE expert_reports_2026_03 PARTITION OF expert_reports
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
CREATE TABLE expert_reports_2026_04 PARTITION OF expert_reports
    FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');
CREATE TABLE expert_reports_2026_05 PARTITION OF expert_reports
    FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');
CREATE TABLE expert_reports_2026_06 PARTITION OF expert_reports
    FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');
CREATE TABLE expert_reports_2026_07 PARTITION OF expert_reports
    FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');
CREATE TABLE expert_reports_2026_08 PARTITION OF expert_reports
    FOR VALUES FROM ('2026-08-01') TO ('2026-09-01');
CREATE TABLE expert_reports_2026_09 PARTITION OF expert_reports
    FOR VALUES FROM ('2026-09-01') TO ('2026-10-01');
CREATE TABLE expert_reports_2026_10 PARTITION OF expert_reports
    FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');
CREATE TABLE expert_reports_2026_11 PARTITION OF expert_reports
    FOR VALUES FROM ('2026-11-01') TO ('2026-12-01');
CREATE TABLE expert_reports_2026_12 PARTITION OF expert_reports
    FOR VALUES FROM ('2026-12-01') TO ('2027-01-01');

-- Panel ölçümleri (kaporta/boya)
CREATE TABLE expert_panel_measurements (
    id              BIGSERIAL PRIMARY KEY,
    report_id       BIGINT NOT NULL REFERENCES expert_reports(id) ON DELETE CASCADE,
    panel_name      VARCHAR(100) NOT NULL,
    status_code     VARCHAR(50),
    paint_thickness INT,
    description     TEXT,
    sort_order      SMALLINT DEFAULT 0
);

CREATE INDEX idx_panel_report ON expert_panel_measurements(report_id);

-- İç mekan kontrolleri
CREATE TABLE expert_interior_checks (
    id              BIGSERIAL PRIMARY KEY,
    report_id       BIGINT NOT NULL REFERENCES expert_reports(id) ON DELETE CASCADE,
    check_point     VARCHAR(100) NOT NULL,
    condition       VARCHAR(20),
    description     TEXT
);

CREATE INDEX idx_interior_report ON expert_interior_checks(report_id);

-- Dış kontroller
CREATE TABLE expert_exterior_checks (
    id              BIGSERIAL PRIMARY KEY,
    report_id       BIGINT NOT NULL REFERENCES expert_reports(id) ON DELETE CASCADE,
    part_name       VARCHAR(100) NOT NULL,
    condition       VARCHAR(20),
    description     TEXT
);

CREATE INDEX idx_exterior_report ON expert_exterior_checks(report_id);

-- Mekanik kontroller
CREATE TABLE expert_mechanical_checks (
    id              BIGSERIAL PRIMARY KEY,
    report_id       BIGINT NOT NULL REFERENCES expert_reports(id) ON DELETE CASCADE,
    test_name       VARCHAR(100) NOT NULL,
    result_value    TEXT,
    unit            VARCHAR(30),
    reference_value TEXT,
    is_passed       BOOLEAN,
    description     TEXT
);

CREATE INDEX idx_mechanical_report ON expert_mechanical_checks(report_id);

-- Elektronik kontroller (OBD)
CREATE TABLE expert_electronic_checks (
    id              BIGSERIAL PRIMARY KEY,
    report_id       BIGINT NOT NULL REFERENCES expert_reports(id) ON DELETE CASCADE,
    system_name     VARCHAR(100) NOT NULL,
    check_result    TEXT,
    error_code      VARCHAR(20),
    is_passed       BOOLEAN,
    description     TEXT
);

CREATE INDEX idx_electronic_report ON expert_electronic_checks(report_id);

-- Lastik & Jant kontrolleri
CREATE TABLE expert_tire_checks (
    id              BIGSERIAL PRIMARY KEY,
    report_id       BIGINT NOT NULL REFERENCES expert_reports(id) ON DELETE CASCADE,
    position        VARCHAR(20) NOT NULL,
    tread_depth     NUMERIC(4,1),
    rim_condition   VARCHAR(30),
    tire_brand      VARCHAR(50),
    tire_size       VARCHAR(30),
    description     TEXT
);

-- Tramer kayıtları
CREATE TABLE expert_tramer_records (
    id              BIGSERIAL PRIMARY KEY,
    report_id       BIGINT NOT NULL REFERENCES expert_reports(id) ON DELETE CASCADE,
    has_accident    BOOLEAN DEFAULT false,
    damage_detail   TEXT,
    is_heavy_damage BOOLEAN DEFAULT false,
    replaced_parts  TEXT,
    query_date      TIMESTAMPTZ DEFAULT NOW()
);

-- Test sürüşü
CREATE TABLE expert_test_drive (
    id              BIGSERIAL PRIMARY KEY,
    report_id       BIGINT NOT NULL REFERENCES expert_reports(id) ON DELETE CASCADE,
    steering        TEXT,
    cornering       TEXT,
    vibration       TEXT,
    noise           TEXT,
    pulling         TEXT,
    overall_note    TEXT
);

-- Dyno testi
CREATE TABLE expert_dyno_tests (
    id              BIGSERIAL PRIMARY KEY,
    report_id       BIGINT NOT NULL REFERENCES expert_reports(id) ON DELETE CASCADE,
    measurement_name VARCHAR(100) NOT NULL,
    measured_value  NUMERIC(10,2),
    unit            VARCHAR(20),
    factory_value   NUMERIC(10,2),
    diff_percent    NUMERIC(5,2),
    is_passed       BOOLEAN
);

-- Fotoğraflar (MinIO referansı)
CREATE TABLE expert_photos (
    id              BIGSERIAL PRIMARY KEY,
    report_id       BIGINT NOT NULL REFERENCES expert_reports(id) ON DELETE CASCADE,
    file_path       TEXT NOT NULL,
    category        VARCHAR(50),
    description     TEXT,
    sort_order      SMALLINT DEFAULT 0
);

CREATE INDEX idx_photos_report ON expert_photos(report_id);
