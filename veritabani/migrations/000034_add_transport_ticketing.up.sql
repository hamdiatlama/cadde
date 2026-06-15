-- 000034: Transport Ticketing System v2 — Route-based pickup, fleet, driver, ratings
BEGIN;

CREATE TYPE vehicle_type AS ENUM ('bus','minibus','dolmus','train','high_speed_train','airplane','ferry');
CREATE TYPE seat_class AS ENUM ('economy','business','first','premium');
CREATE TYPE ticket_status AS ENUM ('pending','confirmed','cancelled','used','refunded');

-- FIRMA / ŞİRKET
CREATE TABLE transport_companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    vehicle_type vehicle_type NOT NULL,
    code VARCHAR(20) UNIQUE,
    logo_url VARCHAR(500),
    phone VARCHAR(20),
    email VARCHAR(200),
    website VARCHAR(200),
    description TEXT,
    is_operator BOOLEAN DEFAULT true,
    commission_percent FLOAT DEFAULT 2.0,
    is_active BOOLEAN DEFAULT true,
    rating FLOAT DEFAULT 0,
    review_count INTEGER DEFAULT 0,
    tax_id VARCHAR(50),
    company_address TEXT,
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- İSTASYON / DURAK
CREATE TABLE transport_stations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    city VARCHAR(100) NOT NULL,
    district VARCHAR(100),
    address VARCHAR(500),
    lat FLOAT,
    lng FLOAT,
    code VARCHAR(20),
    type VARCHAR(50),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ROTA
CREATE TABLE transport_routes (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES transport_companies(id),
    origin_station_id INTEGER NOT NULL REFERENCES transport_stations(id),
    destination_station_id INTEGER NOT NULL REFERENCES transport_stations(id),
    name VARCHAR(200),
    duration_minutes INTEGER,
    distance_km FLOAT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ROTA ÜZERİ DURAKLAR
CREATE TABLE transport_route_stops (
    id SERIAL PRIMARY KEY,
    route_id INTEGER NOT NULL REFERENCES transport_routes(id),
    station_id INTEGER REFERENCES transport_stations(id),
    name VARCHAR(200) NOT NULL,
    lat FLOAT,
    lng FLOAT,
    km_from_start FLOAT DEFAULT 0,
    minutes_from_departure INTEGER DEFAULT 0,
    can_pickup BOOLEAN DEFAULT true,
    can_dropoff BOOLEAN DEFAULT true,
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ARAÇ / FİLO
CREATE TABLE transport_vehicles (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES transport_companies(id),
    plate_number VARCHAR(20) NOT NULL UNIQUE,
    brand VARCHAR(100),
    model VARCHAR(100),
    year INTEGER,
    color VARCHAR(50),
    seat_count INTEGER NOT NULL,
    features JSONB,
    has_wifi BOOLEAN DEFAULT false,
    has_ac BOOLEAN DEFAULT true,
    has_toilet BOOLEAN DEFAULT false,
    has_usb BOOLEAN DEFAULT false,
    has_tv BOOLEAN DEFAULT false,
    photo_url VARCHAR(500),
    last_maintenance_date DATE,
    next_maintenance_date DATE,
    inspection_date DATE,
    insurance_date DATE,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ŞOFÖR
CREATE TABLE transport_drivers (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES transport_companies(id),
    name VARCHAR(100) NOT NULL,
    surname VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(200),
    license_number VARCHAR(50),
    license_class VARCHAR(20),
    license_expiry DATE,
    tc_kimlik VARCHAR(20),
    address TEXT,
    photo_url VARCHAR(500),
    is_verified BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    rating FLOAT DEFAULT 0,
    review_count INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- SEFER (her sefer = rota + gün + araç + şoför)
CREATE TABLE transport_schedules (
    id SERIAL PRIMARY KEY,
    route_id INTEGER NOT NULL REFERENCES transport_routes(id),
    vehicle_id INTEGER REFERENCES transport_vehicles(id),
    driver_id INTEGER REFERENCES transport_drivers(id),
    departure_date DATE NOT NULL,
    departure_time TIME NOT NULL,
    arrival_time TIME,
    base_price FLOAT NOT NULL,
    currency VARCHAR(3) DEFAULT 'TRY',
    total_seats INTEGER NOT NULL,
    available_seats INTEGER NOT NULL,
    vehicle_number VARCHAR(50),
    status VARCHAR(20) DEFAULT 'active',
    is_pickup_route BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- SEFER DURAK ZAMANLARI (tahmini varış)
CREATE TABLE schedule_stop_times (
    id SERIAL PRIMARY KEY,
    schedule_id INTEGER NOT NULL REFERENCES transport_schedules(id),
    route_stop_id INTEGER NOT NULL REFERENCES transport_route_stops(id),
    estimated_time TIME NOT NULL,
    estimated_minutes INTEGER,
    is_active BOOLEAN DEFAULT true
);

-- KOLTUK
CREATE TABLE transport_seats (
    id SERIAL PRIMARY KEY,
    schedule_id INTEGER NOT NULL REFERENCES transport_schedules(id),
    seat_number VARCHAR(10) NOT NULL,
    seat_class seat_class DEFAULT 'economy',
    price FLOAT,
    is_window BOOLEAN DEFAULT false,
    is_aisle BOOLEAN DEFAULT false,
    is_available BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- BİLET
CREATE TABLE transport_tickets (
    id SERIAL PRIMARY KEY,
    ticket_no VARCHAR(20) UNIQUE NOT NULL,
    schedule_id INTEGER NOT NULL REFERENCES transport_schedules(id),
    seat_id INTEGER REFERENCES transport_seats(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    pickup_stop_id INTEGER REFERENCES transport_route_stops(id),
    dropoff_stop_id INTEGER REFERENCES transport_route_stops(id),
    passenger_name VARCHAR(200) NOT NULL,
    passenger_surname VARCHAR(200),
    passenger_id_no VARCHAR(20),
    passenger_phone VARCHAR(20),
    passenger_email VARCHAR(200),
    pickup_lat FLOAT,
    pickup_lng FLOAT,
    pickup_address VARCHAR(500),
    price FLOAT NOT NULL,
    currency VARCHAR(3) DEFAULT 'TRY',
    provider_ticket_no VARCHAR(100),
    reseller_fee FLOAT DEFAULT 0,
    commission_rate FLOAT DEFAULT 0,
    status ticket_status DEFAULT 'pending',
    booking_reference VARCHAR(50),
    qr_code VARCHAR(500),
    checked_in BOOLEAN DEFAULT false,
    notified_pickup_15min BOOLEAN DEFAULT false,
    notified_driver BOOLEAN DEFAULT false,
    cancellation_reason TEXT,
    bought_at TIMESTAMPTZ DEFAULT NOW(),
    cancelled_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ROTA ÜZERİNDEN YOLCU ALMA
CREATE TABLE transport_pickup_bookings (
    id SERIAL PRIMARY KEY,
    ticket_id INTEGER NOT NULL REFERENCES transport_tickets(id),
    schedule_id INTEGER NOT NULL REFERENCES transport_schedules(id),
    pickup_stop_id INTEGER NOT NULL REFERENCES transport_route_stops(id),
    pickup_time TIME,
    passenger_phone VARCHAR(20),
    status VARCHAR(20) DEFAULT 'pending',
    driver_notified BOOLEAN DEFAULT false,
    passenger_notified BOOLEAN DEFAULT false,
    picked_up BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- DEĞERLENDİRME
CREATE TABLE transport_ratings (
    id SERIAL PRIMARY KEY,
    ticket_id INTEGER NOT NULL REFERENCES transport_tickets(id),
    company_id INTEGER NOT NULL REFERENCES transport_companies(id),
    driver_id INTEGER REFERENCES transport_drivers(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    company_rating INTEGER,
    driver_rating INTEGER,
    cleanliness_rating INTEGER,
    comfort_rating INTEGER,
    punctuality_rating INTEGER,
    overall_rating INTEGER,
    comment TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- BELGE YÖNETİMİ
CREATE TABLE transport_documents (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES transport_companies(id),
    vehicle_id INTEGER REFERENCES transport_vehicles(id),
    driver_id INTEGER REFERENCES transport_drivers(id),
    doc_type VARCHAR(50) NOT NULL,
    doc_name VARCHAR(200),
    doc_number VARCHAR(100),
    file_url VARCHAR(500),
    issue_date DATE,
    expiry_date DATE,
    is_verified BOOLEAN DEFAULT false,
    verified_by INTEGER REFERENCES users(id),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_companies_type ON transport_companies(vehicle_type);
CREATE INDEX idx_stations_city ON transport_stations(city);
CREATE INDEX idx_routes_origin ON transport_routes(origin_station_id);
CREATE INDEX idx_routes_dest ON transport_routes(destination_station_id);
CREATE INDEX idx_route_stops_route ON transport_route_stops(route_id);
CREATE INDEX idx_vehicles_company ON transport_vehicles(company_id);
CREATE INDEX idx_drivers_company ON transport_drivers(company_id);
CREATE INDEX idx_schedules_date ON transport_schedules(departure_date);
CREATE INDEX idx_schedules_route ON transport_schedules(route_id);
CREATE INDEX idx_schedules_vehicle ON transport_schedules(vehicle_id);
CREATE INDEX idx_schedules_driver ON transport_schedules(driver_id);
CREATE INDEX idx_stop_times_schedule ON schedule_stop_times(schedule_id);
CREATE INDEX idx_seats_schedule ON transport_seats(schedule_id);
CREATE INDEX idx_tickets_user ON transport_tickets(user_id);
CREATE INDEX idx_tickets_schedule ON transport_tickets(schedule_id);
CREATE INDEX idx_tickets_status ON transport_tickets(status);
CREATE INDEX idx_pickup_bookings_schedule ON transport_pickup_bookings(schedule_id);
CREATE INDEX idx_ratings_company ON transport_ratings(company_id);
CREATE INDEX idx_ratings_driver ON transport_ratings(driver_id);
CREATE INDEX idx_documents_company ON transport_documents(company_id);
CREATE INDEX idx_documents_vehicle ON transport_documents(vehicle_id);
CREATE INDEX idx_documents_driver ON transport_documents(driver_id);

COMMIT;
