BEGIN;

DROP TABLE IF EXISTS tourism_reviews;
DROP TABLE IF EXISTS tourism_bookings;
DROP TABLE IF EXISTS tourism_schedules;
DROP TABLE IF EXISTS tourism_experiences;
DROP TABLE IF EXISTS tourism_providers;

CREATE TABLE IF NOT EXISTS transport_agency_authorizations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    agency_company_id INTEGER NOT NULL REFERENCES transport_companies(id),
    operator_company_id INTEGER NOT NULL REFERENCES transport_companies(id),
    status          VARCHAR(20) DEFAULT 'pending',
    commission_split REAL DEFAULT 0,
    authorized_by   INTEGER REFERENCES users(id),
    authorized_at   TIMESTAMP,
    valid_until     TIMESTAMP,
    is_active       INTEGER DEFAULT 1,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS agency_authorizations;
DROP TABLE IF EXISTS agencies;

COMMIT;
