-- ============================================================
-- MIGRATION 000014: Expert Inspection — Legacy Missing Tables
-- ============================================================
-- Ported from oto_ekspertiz_schema.sql:
-- egzoz_emisyon, sivi_testleri, el_freni_testleri,
-- dort_ceker_kontrolleri, kayis_kontrolleri, sasi_kontrolleri,
-- ekstra_donanimlar, kabul_kriterleri, zorunlu_ekipmanlar

-- Emission tests (egzoz_emisyon)
CREATE TABLE expert_emission_tests (
    id              BIGSERIAL PRIMARY KEY,
    report_id       BIGINT NOT NULL REFERENCES expert_reports(id) ON DELETE CASCADE,
    co              NUMERIC(6,2),
    hc              NUMERIC(6,2),
    co2             NUMERIC(6,2),
    lambda          NUMERIC(4,2),
    dpf_doluluk     NUMERIC(5,2),
    is_passed       BOOLEAN
);

CREATE INDEX idx_emission_report ON expert_emission_tests(report_id);

-- Fluid tests (sivi_testleri — brake fluid, antifreeze)
CREATE TABLE expert_fluid_tests (
    id              BIGSERIAL PRIMARY KEY,
    report_id       BIGINT NOT NULL REFERENCES expert_reports(id) ON DELETE CASCADE,
    test_type       VARCHAR(50) NOT NULL,
    water_ratio     NUMERIC(5,2),
    freezing_point  NUMERIC(5,2),
    boiling_point   NUMERIC(5,2),
    is_passed       BOOLEAN
);

CREATE INDEX idx_fluid_report ON expert_fluid_tests(report_id);

-- Handbrake performance tests
CREATE TABLE expert_handbrake_tests (
    id              BIGSERIAL PRIMARY KEY,
    report_id       BIGINT NOT NULL REFERENCES expert_reports(id) ON DELETE CASCADE,
    pull_distance   NUMERIC(5,1),
    force           NUMERIC(6,2),
    efficiency_rate NUMERIC(5,2),
    is_passed       BOOLEAN
);

CREATE INDEX idx_handbrake_report ON expert_handbrake_tests(report_id);

-- Four-wheel drive / differential checks
CREATE TABLE expert_four_wheel_drive_checks (
    id              BIGSERIAL PRIMARY KEY,
    report_id       BIGINT NOT NULL REFERENCES expert_reports(id) ON DELETE CASCADE,
    transfer_case   TEXT,
    front_diff      TEXT,
    rear_diff       TEXT,
    torque_distribution TEXT,
    is_passed       BOOLEAN
);

CREATE INDEX idx_4wd_report ON expert_four_wheel_drive_checks(report_id);

-- Belt checks (timing, alternator, AC)
CREATE TABLE expert_belt_checks (
    id              BIGSERIAL PRIMARY KEY,
    report_id       BIGINT NOT NULL REFERENCES expert_reports(id) ON DELETE CASCADE,
    belt_type       VARCHAR(50) NOT NULL,
    wear_status     VARCHAR(50),
    tension_status  VARCHAR(50),
    is_passed       BOOLEAN
);

CREATE INDEX idx_belt_report ON expert_belt_checks(report_id);

-- Chassis / VIN originality check
CREATE TABLE expert_chassis_checks (
    id              BIGSERIAL PRIMARY KEY,
    report_id       BIGINT NOT NULL REFERENCES expert_reports(id) ON DELETE CASCADE,
    chassis_original BOOLEAN DEFAULT true,
    labels_present  BOOLEAN DEFAULT true,
    vin_plate_status VARCHAR(100),
    description     TEXT
);

CREATE INDEX idx_chassis_report ON expert_chassis_checks(report_id);

-- Extra equipment (sunroof, navigation, camera, etc.)
CREATE TABLE expert_extra_equipment (
    id              BIGSERIAL PRIMARY KEY,
    report_id       BIGINT NOT NULL REFERENCES expert_reports(id) ON DELETE CASCADE,
    equipment_name  VARCHAR(100) NOT NULL,
    is_present      BOOLEAN DEFAULT true
);

CREATE INDEX idx_extra_equip_report ON expert_extra_equipment(report_id);

-- Mandatory equipment (first aid kit, reflector, triangle, tow rope)
CREATE TABLE expert_mandatory_equipment (
    id              BIGSERIAL PRIMARY KEY,
    report_id       BIGINT NOT NULL REFERENCES expert_reports(id) ON DELETE CASCADE,
    equipment_name  VARCHAR(100) NOT NULL,
    is_present      BOOLEAN DEFAULT false
);

CREATE INDEX idx_mandatory_equip_report ON expert_mandatory_equipment(report_id);

-- Acceptance criteria / reference values per report
CREATE TABLE expert_acceptance_criteria (
    id                      BIGSERIAL PRIMARY KEY,
    report_id               BIGINT NOT NULL REFERENCES expert_reports(id) ON DELETE CASCADE,
    brake_balance_deviation_max NUMERIC(5,2) DEFAULT 15.00,
    suspension_efficiency_min   NUMERIC(5,2) DEFAULT 40.00,
    handbrake_efficiency_min    NUMERIC(5,2) DEFAULT 16.00
);

CREATE INDEX idx_acceptance_report ON expert_acceptance_criteria(report_id);
