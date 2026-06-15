-- 000035: Agency + Tourism modules
-- agencies: cross-domain agency records
-- agency_authorizations: agencies sell transport/hotel/event/tourism tickets
-- tourism_providers, tourism_experiences, tourism_schedules, tourism_bookings, tourism_reviews
-- transport_tickets.agency_id FK
-- DROP transport_agency_authorizations

BEGIN;

-- ─── AGENCY ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS agencies (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL REFERENCES users(id),
    company_name    VARCHAR(200) NOT NULL,
    trade_name      VARCHAR(200),
    tax_id          VARCHAR(50),
    tax_office      VARCHAR(100),
    phone           VARCHAR(20),
    email           VARCHAR(200),
    website         VARCHAR(200),
    address         TEXT,
    is_verified     INTEGER DEFAULT 0,
    is_active       INTEGER DEFAULT 1,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS agency_authorizations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    agency_id       INTEGER NOT NULL REFERENCES agencies(id),
    domain          VARCHAR(50) NOT NULL,
    provider_id     INTEGER NOT NULL,
    provider_name   VARCHAR(200),
    commission_split REAL DEFAULT 0,
    status          VARCHAR(20) DEFAULT 'pending',
    authorized_by   INTEGER REFERENCES users(id),
    authorized_at   TIMESTAMP,
    valid_until     TIMESTAMP,
    notes           TEXT,
    is_active       INTEGER DEFAULT 1,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_agency_auth_agency ON agency_authorizations(agency_id);
CREATE INDEX idx_agency_auth_domain ON agency_authorizations(domain);
CREATE INDEX idx_agency_auth_provider ON agency_authorizations(provider_id);
CREATE INDEX idx_agency_auth_status ON agency_authorizations(status);

-- ─── TOURISM ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS tourism_providers (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL REFERENCES users(id),
    company_name    VARCHAR(200) NOT NULL,
    tax_id          VARCHAR(50),
    phone           VARCHAR(20),
    email           VARCHAR(200),
    website         VARCHAR(200),
    address         TEXT,
    description     TEXT,
    logo_url        VARCHAR(500),
    is_verified     INTEGER DEFAULT 0,
    is_active       INTEGER DEFAULT 1,
    rating          REAL DEFAULT 0,
    review_count    INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tourism_experiences (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    provider_id       INTEGER NOT NULL REFERENCES tourism_providers(id),
    category          VARCHAR(50) NOT NULL,
    name              VARCHAR(300) NOT NULL,
    description       TEXT,
    short_description VARCHAR(500),
    location          VARCHAR(300),
    city              VARCHAR(100),
    district          VARCHAR(100),
    lat               REAL,
    lng               REAL,
    duration_minutes  INTEGER,
    min_participants  INTEGER DEFAULT 1,
    max_participants  INTEGER,
    includes          TEXT,
    excludes          TEXT,
    what_to_bring     TEXT,
    highlights        TEXT,
    photos            TEXT,
    cover_photo_url   VARCHAR(500),
    base_price        REAL NOT NULL,
    currency          VARCHAR(3) DEFAULT 'TRY',
    is_featured       INTEGER DEFAULT 0,
    is_active         INTEGER DEFAULT 1,
    cancellation_policy TEXT,
    rating            REAL DEFAULT 0,
    review_count      INTEGER DEFAULT 0,
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tourism_exp_category ON tourism_experiences(category);
CREATE INDEX idx_tourism_exp_city ON tourism_experiences(city);
CREATE INDEX idx_tourism_exp_provider ON tourism_experiences(provider_id);

CREATE TABLE IF NOT EXISTS tourism_schedules (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    experience_id   INTEGER NOT NULL REFERENCES tourism_experiences(id),
    date            DATE NOT NULL,
    time            TIME NOT NULL,
    capacity        INTEGER NOT NULL,
    available       INTEGER NOT NULL,
    price           REAL,
    currency        VARCHAR(3) DEFAULT 'TRY',
    is_active       INTEGER DEFAULT 1,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tourism_sched_exp ON tourism_schedules(experience_id);
CREATE INDEX idx_tourism_sched_date ON tourism_schedules(date);

CREATE TABLE IF NOT EXISTS tourism_bookings (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_no        VARCHAR(20) NOT NULL UNIQUE,
    schedule_id       INTEGER NOT NULL REFERENCES tourism_schedules(id),
    user_id           INTEGER NOT NULL REFERENCES users(id),
    agency_id         INTEGER REFERENCES agencies(id),
    participant_count INTEGER DEFAULT 1,
    participant_names TEXT,
    total_price       REAL NOT NULL,
    currency          VARCHAR(3) DEFAULT 'TRY',
    status            VARCHAR(20) DEFAULT 'pending',
    reseller_fee      REAL DEFAULT 0,
    commission_rate   REAL DEFAULT 0,
    customer_name     VARCHAR(200) NOT NULL,
    customer_phone    VARCHAR(20),
    customer_email    VARCHAR(200),
    notes             TEXT,
    qr_code           VARCHAR(500),
    cancellation_reason TEXT,
    booked_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cancelled_at      TIMESTAMP,
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tourism_book_user ON tourism_bookings(user_id);
CREATE INDEX idx_tourism_book_agency ON tourism_bookings(agency_id);
CREATE INDEX idx_tourism_book_schedule ON tourism_bookings(schedule_id);
CREATE INDEX idx_tourism_book_status ON tourism_bookings(status);

CREATE TABLE IF NOT EXISTS tourism_reviews (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    experience_id   INTEGER NOT NULL REFERENCES tourism_experiences(id),
    booking_id      INTEGER REFERENCES tourism_bookings(id),
    user_id         INTEGER NOT NULL REFERENCES users(id),
    rating          INTEGER NOT NULL,
    comment         TEXT,
    photos          TEXT,
    is_verified     INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tourism_review_exp ON tourism_reviews(experience_id);

-- ─── TRANSPORT: add agency_id to tickets ────────────────────
ALTER TABLE transport_tickets ADD COLUMN agency_id INTEGER REFERENCES agencies(id);
CREATE INDEX idx_transport_ticket_agency ON transport_tickets(agency_id);

-- ─── DROP old transport-specific auth table ─────────────────
DROP TABLE IF EXISTS transport_agency_authorizations;

COMMIT;
