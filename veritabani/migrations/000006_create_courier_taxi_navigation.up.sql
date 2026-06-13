-- ============================================================
-- DOMAIN: KURYE/TAKSİ NAVİGASYON MODÜLÜ
-- ============================================================

CREATE TYPE driver_status AS ENUM ('offline', 'available', 'busy', 'on_delivery');
CREATE TYPE ride_status AS ENUM ('requested', 'accepted', 'arrived', 'in_progress', 'completed', 'cancelled');

-- Sürücü/Kurye profilleri
CREATE TABLE drivers (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    driver_type     VARCHAR(20) NOT NULL CHECK (driver_type IN ('courier', 'taxi', 'both')),
    vehicle_info    JSONB,
    license_plate   VARCHAR(20),
    license_no      VARCHAR(50),
    is_verified     BOOLEAN NOT NULL DEFAULT false,
    is_active       BOOLEAN NOT NULL DEFAULT true,
    rating          NUMERIC(3,2) DEFAULT 0,
    total_rides     INT NOT NULL DEFAULT 0,
    current_lat     NUMERIC(10,7),
    current_lng     NUMERIC(10,7),
    current_location GEOGRAPHY(POINT, 4326),
    status          driver_status NOT NULL DEFAULT 'offline',
    last_location_update TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_drivers_location ON drivers USING GIST(current_location);
CREATE INDEX idx_drivers_status ON drivers(status) WHERE status = 'available';
CREATE INDEX idx_drivers_type ON drivers(driver_type);
CREATE INDEX idx_drivers_rating ON drivers(rating DESC);

-- Sürücü çalışma saatleri
CREATE TABLE driver_shifts (
    id              BIGSERIAL PRIMARY KEY,
    driver_id       UUID NOT NULL REFERENCES drivers(id) ON DELETE CASCADE,
    start_time      TIMESTAMPTZ NOT NULL,
    end_time        TIMESTAMPTZ,
    start_location  GEOGRAPHY(POINT, 4326),
    end_location    GEOGRAPHY(POINT, 4326),
    distance_km     NUMERIC(10,2),
    earnings        NUMERIC(10,2),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_shifts_driver ON driver_shifts(driver_id);
CREATE INDEX idx_shifts_date ON driver_shifts(start_time);

-- Sürücü konum geçmişi (sadece özet, canlı konum Redis'te)
CREATE TABLE driver_location_history (
    id              BIGSERIAL PRIMARY KEY,
    driver_id       UUID NOT NULL REFERENCES drivers(id) ON DELETE CASCADE,
    latitude        NUMERIC(10,7) NOT NULL,
    longitude       NUMERIC(10,7) NOT NULL,
    location        GEOGRAPHY(POINT, 4326),
    speed_kmh       NUMERIC(5,1),
    heading         SMALLINT,
    recorded_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (recorded_at);

CREATE INDEX idx_drvloc_driver ON driver_location_history(driver_id);
CREATE INDEX idx_drvloc_time ON driver_location_history(recorded_at);

CREATE TABLE driver_location_history_2026_01 PARTITION OF driver_location_history
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE driver_location_history_2026_02 PARTITION OF driver_location_history
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE driver_location_history_2026_03 PARTITION OF driver_location_history
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
CREATE TABLE driver_location_history_default PARTITION OF driver_location_history DEFAULT;

-- Teslimat bölgeleri (PostGIS polygon)
CREATE TABLE delivery_zones (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    zone_area       GEOGRAPHY(POLYGON, 4326) NOT NULL,
    base_fee        NUMERIC(10,2) DEFAULT 0,
    fee_per_km      NUMERIC(5,2) DEFAULT 0,
    min_order_amount NUMERIC(10,2),
    is_active       BOOLEAN NOT NULL DEFAULT true,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_deliveryzones_area ON delivery_zones USING GIST(zone_area);

-- Yolculuk/Sipariş teslimatı
CREATE TABLE rides (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id        UUID REFERENCES orders(id),
    driver_id       UUID REFERENCES drivers(id),
    user_id         UUID NOT NULL REFERENCES users(id),
    ride_type       VARCHAR(20) NOT NULL CHECK (ride_type IN ('delivery', 'taxi', 'cargo')),
    status          ride_status NOT NULL DEFAULT 'requested',
    pickup_address  TEXT NOT NULL,
    pickup_location GEOGRAPHY(POINT, 4326) NOT NULL,
    dropoff_address TEXT,
    dropoff_location GEOGRAPHY(POINT, 4326),
    estimated_distance_km NUMERIC(8,2),
    estimated_duration_min SMALLINT,
    actual_distance_km NUMERIC(8,2),
    actual_duration_min SMALLINT,
    base_fee        NUMERIC(10,2),
    distance_fee    NUMERIC(10,2),
    waiting_fee     NUMERIC(10,2),
    total_fee       NUMERIC(10,2),
    driver_rating   SMALLINT CHECK (driver_rating >= 1 AND driver_rating <= 5),
    user_rating     SMALLINT CHECK (user_rating >= 1 AND user_rating <= 5),
    cancelled_by    VARCHAR(20),
    cancel_reason   TEXT,
    requested_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    accepted_at     TIMESTAMPTZ,
    arrived_at      TIMESTAMPTZ,
    started_at      TIMESTAMPTZ,
    completed_at    TIMESTAMPTZ,
    cancelled_at    TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (created_at);

CREATE INDEX idx_rides_driver ON rides(driver_id);
CREATE INDEX idx_rides_user ON rides(user_id);
CREATE INDEX idx_rides_order ON rides(order_id);
CREATE INDEX idx_rides_status ON rides(status);
CREATE INDEX idx_rides_type ON rides(ride_type);

CREATE TABLE rides_2026_01 PARTITION OF rides
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE rides_2026_02 PARTITION OF rides
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
CREATE TABLE rides_2026_03 PARTITION OF rides
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
CREATE TABLE rides_2026_04 PARTITION OF rides
    FOR VALUES FROM ('2026-04-01') TO ('2026-05-01');
CREATE TABLE rides_2026_05 PARTITION OF rides
    FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');
CREATE TABLE rides_2026_06 PARTITION OF rides
    FOR VALUES FROM ('2026-06-01') TO ('2026-07-01');
CREATE TABLE rides_default PARTITION OF rides DEFAULT;

-- Yolculuk rota noktaları
CREATE TABLE ride_waypoints (
    id              BIGSERIAL PRIMARY KEY,
    ride_id         UUID NOT NULL REFERENCES rides(id) ON DELETE CASCADE,
    latitude        NUMERIC(10,7) NOT NULL,
    longitude       NUMERIC(10,7) NOT NULL,
    location        GEOGRAPHY(POINT, 4326),
    timestamp       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_waypoints_ride ON ride_waypoints(ride_id);

-- Sürücü-kullanıcı eşleştirme logu
CREATE TABLE driver_match_log (
    id              BIGSERIAL PRIMARY KEY,
    ride_id         UUID NOT NULL REFERENCES rides(id) ON DELETE CASCADE,
    driver_id       UUID REFERENCES drivers(id),
    match_score     NUMERIC(5,2),
    distance_km     NUMERIC(8,2),
    duration_min    SMALLINT,
    was_selected    BOOLEAN NOT NULL DEFAULT false,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_matchlog_ride ON driver_match_log(ride_id);
