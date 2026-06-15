-- 000036: Rental + Trip Planner modules
-- rental_companies, rental_branches, rental_vehicles, rental_bookings, rental_insurances, rental_reviews
-- trip_plans, trip_segments, trip_stays, trip_activities, trip_foods, trip_rentals, trip_deliveries

BEGIN;

-- ─── RENTAL ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS rental_companies (
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
    categories      TEXT,
    is_verified     INTEGER DEFAULT 0,
    is_active       INTEGER DEFAULT 1,
    rating          REAL DEFAULT 0,
    review_count    INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rental_branches (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id      INTEGER NOT NULL REFERENCES rental_companies(id),
    name            VARCHAR(200),
    city            VARCHAR(100) NOT NULL,
    district        VARCHAR(100),
    address         VARCHAR(500),
    lat             REAL,
    lng             REAL,
    phone           VARCHAR(20),
    is_active       INTEGER DEFAULT 1,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_rental_branch_city ON rental_branches(city);

CREATE TABLE IF NOT EXISTS rental_vehicles (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id        INTEGER NOT NULL REFERENCES rental_companies(id),
    branch_id         INTEGER REFERENCES rental_branches(id),
    category          VARCHAR(20) NOT NULL,
    brand             VARCHAR(100) NOT NULL,
    model             VARCHAR(100) NOT NULL,
    year              INTEGER,
    color             VARCHAR(50),
    plate_number      VARCHAR(20) UNIQUE,
    fuel_type         VARCHAR(20),
    seat_count        INTEGER,
    luggage_capacity  VARCHAR(50),
    engine_power      VARCHAR(50),
    has_ac            INTEGER DEFAULT 1,
    has_gps           INTEGER DEFAULT 0,
    has_bluetooth     INTEGER DEFAULT 0,
    mileage_limit_km  INTEGER,
    daily_price       REAL NOT NULL,
    weekly_price      REAL,
    monthly_price     REAL,
    currency          VARCHAR(3) DEFAULT 'TRY',
    deposit_amount    REAL DEFAULT 0,
    photos            TEXT,
    features          TEXT,
    min_driver_age    INTEGER DEFAULT 21,
    license_required_years INTEGER DEFAULT 1,
    status            VARCHAR(20) DEFAULT 'available',
    is_active         INTEGER DEFAULT 1,
    rating            REAL DEFAULT 0,
    review_count      INTEGER DEFAULT 0,
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_rental_vehicle_category ON rental_vehicles(category);
CREATE INDEX idx_rental_vehicle_company ON rental_vehicles(company_id);
CREATE INDEX idx_rental_vehicle_status ON rental_vehicles(status);

CREATE TABLE IF NOT EXISTS rental_bookings (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_no        VARCHAR(20) NOT NULL UNIQUE,
    vehicle_id        INTEGER NOT NULL REFERENCES rental_vehicles(id),
    user_id           INTEGER NOT NULL REFERENCES users(id),
    agency_id         INTEGER REFERENCES agencies(id),
    pickup_branch_id  INTEGER REFERENCES rental_branches(id),
    dropoff_branch_id INTEGER REFERENCES rental_branches(id),
    pickup_date       TIMESTAMP NOT NULL,
    dropoff_date      TIMESTAMP NOT NULL,
    pickup_location   VARCHAR(500),
    dropoff_location  VARCHAR(500),
    total_days        INTEGER,
    daily_price       REAL,
    total_price       REAL NOT NULL,
    currency          VARCHAR(3) DEFAULT 'TRY',
    deposit_paid      REAL DEFAULT 0,
    insurance_type    VARCHAR(50),
    insurance_cost    REAL DEFAULT 0,
    additional_driver INTEGER DEFAULT 0,
    additional_driver_name VARCHAR(200),
    driver_name       VARCHAR(200) NOT NULL,
    driver_phone      VARCHAR(20),
    driver_email      VARCHAR(200),
    driver_license_no VARCHAR(50),
    status            VARCHAR(20) DEFAULT 'pending',
    reseller_fee      REAL DEFAULT 0,
    commission_rate   REAL DEFAULT 0,
    notes             TEXT,
    cancellation_reason TEXT,
    booked_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    returned_at       TIMESTAMP,
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_rental_book_user ON rental_bookings(user_id);
CREATE INDEX idx_rental_book_vehicle ON rental_bookings(vehicle_id);
CREATE INDEX idx_rental_book_agency ON rental_bookings(agency_id);
CREATE INDEX idx_rental_book_status ON rental_bookings(status);

CREATE TABLE IF NOT EXISTS rental_insurances (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id      INTEGER NOT NULL REFERENCES rental_companies(id),
    name            VARCHAR(200) NOT NULL,
    description     TEXT,
    coverage        TEXT,
    daily_cost      REAL NOT NULL,
    currency        VARCHAR(3) DEFAULT 'TRY',
    is_active       INTEGER DEFAULT 1,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rental_reviews (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    booking_id        INTEGER NOT NULL REFERENCES rental_bookings(id),
    vehicle_id        INTEGER NOT NULL REFERENCES rental_vehicles(id),
    user_id           INTEGER NOT NULL REFERENCES users(id),
    vehicle_rating    INTEGER,
    company_rating    INTEGER,
    cleanliness_rating INTEGER,
    overall_rating    INTEGER NOT NULL,
    comment           TEXT,
    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_rental_review_vehicle ON rental_reviews(vehicle_id);

-- ─── TRIP PLANNER (Rota Olustur) ────────────────────────────
CREATE TABLE IF NOT EXISTS trip_plans (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL REFERENCES users(id),
    name            VARCHAR(300) NOT NULL,
    description     TEXT,
    start_date      DATE NOT NULL,
    end_date        DATE NOT NULL,
    origin_city     VARCHAR(100),
    origin_address  VARCHAR(500),
    status          VARCHAR(20) DEFAULT 'draft',
    total_budget    REAL DEFAULT 0,
    currency        VARCHAR(3) DEFAULT 'TRY',
    is_public       INTEGER DEFAULT 0,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_trip_plan_user ON trip_plans(user_id);

CREATE TABLE IF NOT EXISTS trip_segments (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_id             INTEGER NOT NULL REFERENCES trip_plans(id),
    sequence            INTEGER NOT NULL,
    segment_type        VARCHAR(20) DEFAULT 'transport',
    origin_name         VARCHAR(300),
    origin_type         VARCHAR(50),
    origin_id           INTEGER,
    origin_lat          REAL,
    origin_lng          REAL,
    origin_address      VARCHAR(500),
    destination_name    VARCHAR(300),
    destination_type    VARCHAR(50),
    destination_id      INTEGER,
    destination_lat     REAL,
    destination_lng     REAL,
    destination_address VARCHAR(500),
    transport_mode      VARCHAR(30),
    transport_schedule_id INTEGER,
    transport_ticket_id   INTEGER,
    estimated_duration_minutes INTEGER,
    estimated_distance_km REAL,
    cost                REAL DEFAULT 0,
    currency            VARCHAR(3) DEFAULT 'TRY',
    planned_departure   TIMESTAMP,
    planned_arrival     TIMESTAMP,
    actual_departure    TIMESTAMP,
    actual_arrival      TIMESTAMP,
    is_confirmed        INTEGER DEFAULT 0,
    notes               TEXT,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_trip_seg_plan ON trip_segments(trip_id);

CREATE TABLE IF NOT EXISTS trip_stays (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_id             INTEGER NOT NULL REFERENCES trip_plans(id),
    segment_id          INTEGER REFERENCES trip_segments(id),
    sequence            INTEGER NOT NULL,
    accommodation_type  VARCHAR(50),
    accommodation_id    INTEGER,
    accommodation_name  VARCHAR(300),
    accommodation_booking_id INTEGER,
    check_in            TIMESTAMP NOT NULL,
    check_out           TIMESTAMP NOT NULL,
    address             VARCHAR(500),
    lat                 REAL,
    lng                 REAL,
    phone               VARCHAR(20),
    confirmation_code   VARCHAR(100),
    cost                REAL DEFAULT 0,
    currency            VARCHAR(3) DEFAULT 'TRY',
    is_confirmed        INTEGER DEFAULT 0,
    notes               TEXT,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_trip_stay_plan ON trip_stays(trip_id);

CREATE TABLE IF NOT EXISTS trip_activities (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_id             INTEGER NOT NULL REFERENCES trip_plans(id),
    segment_id          INTEGER REFERENCES trip_segments(id),
    stay_id             INTEGER REFERENCES trip_stays(id),
    sequence            INTEGER NOT NULL,
    activity_type       VARCHAR(50),
    activity_id         INTEGER,
    activity_name       VARCHAR(300),
    category            VARCHAR(50),
    booking_id          INTEGER,
    booking_no          VARCHAR(50),
    start_time          TIMESTAMP NOT NULL,
    end_time            TIMESTAMP,
    location_name       VARCHAR(300),
    location_address    VARCHAR(500),
    lat                 REAL,
    lng                 REAL,
    cost                REAL DEFAULT 0,
    currency            VARCHAR(3) DEFAULT 'TRY',
    is_confirmed        INTEGER DEFAULT 0,
    notes               TEXT,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_trip_act_plan ON trip_activities(trip_id);

CREATE TABLE IF NOT EXISTS trip_foods (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_id             INTEGER NOT NULL REFERENCES trip_plans(id),
    stay_id             INTEGER REFERENCES trip_stays(id),
    sequence            INTEGER NOT NULL,
    food_type           VARCHAR(20),
    restaurant_id       INTEGER,
    restaurant_name     VARCHAR(300),
    restaurant_address  VARCHAR(500),
    lat                 REAL,
    lng                 REAL,
    meal_time           TIMESTAMP NOT NULL,
    participant_count   INTEGER DEFAULT 1,
    cost                REAL DEFAULT 0,
    currency            VARCHAR(3) DEFAULT 'TRY',
    order_id            INTEGER,
    is_confirmed        INTEGER DEFAULT 0,
    notes               TEXT,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_trip_food_plan ON trip_foods(trip_id);

CREATE TABLE IF NOT EXISTS trip_rentals (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_id             INTEGER NOT NULL REFERENCES trip_plans(id),
    sequence            INTEGER NOT NULL,
    vehicle_type        VARCHAR(50),
    rental_booking_id   INTEGER REFERENCES rental_bookings(id),
    rental_company      VARCHAR(200),
    pickup_location     VARCHAR(300),
    pickup_address      VARCHAR(500),
    pickup_lat          REAL,
    pickup_lng          REAL,
    pickup_time         TIMESTAMP NOT NULL,
    dropoff_location    VARCHAR(300),
    dropoff_address     VARCHAR(500),
    dropoff_lat         REAL,
    dropoff_lng         REAL,
    dropoff_time        TIMESTAMP,
    total_cost          REAL DEFAULT 0,
    currency            VARCHAR(3) DEFAULT 'TRY',
    booking_reference   VARCHAR(100),
    is_confirmed        INTEGER DEFAULT 0,
    notes               TEXT,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_trip_rental_plan ON trip_rentals(trip_id);

CREATE TABLE IF NOT EXISTS trip_deliveries (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_id             INTEGER NOT NULL REFERENCES trip_plans(id),
    stay_id             INTEGER NOT NULL REFERENCES trip_stays(id),
    sequence            INTEGER NOT NULL,
    order_id            INTEGER NOT NULL,
    order_no            VARCHAR(50),
    cargo_company       VARCHAR(100),
    tracking_no         VARCHAR(100),
    estimated_delivery  DATE,
    delivery_address    VARCHAR(500),
    delivery_lat        REAL,
    delivery_lng        REAL,
    is_delivered        INTEGER DEFAULT 0,
    delivered_at        TIMESTAMP,
    notes               TEXT,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_trip_del_plan ON trip_deliveries(trip_id);

COMMIT;
