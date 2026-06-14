-- ============================================================
-- DOMAIN: EVENT / TICKETING (sinema, tiyatro, konser, spor)
-- ============================================================

CREATE TYPE event_category AS ENUM (
    'sinema', 'tiyatro', 'konser', 'futbol', 'voleybol',
    'basketbol', 'tenis', 'diger_spor', 'standup', 'festival',
    'komedi', 'cocuk', 'bale_opera', 'müze_sergi', 'espor',
    'konferans', 'workshop', 'fuar_expo', 'gosteri', 'aile_parki',
    'diger'
);

-- Mekanlar
CREATE TABLE venues (
    id              SERIAL PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    city            VARCHAR(100) NOT NULL,
    district        VARCHAR(100),
    address         TEXT,
    latitude        NUMERIC(10,7),
    longitude       NUMERIC(10,7),
    capacity        INT DEFAULT 0,
    phone           VARCHAR(20),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Mekan bölümleri (VIP, Tribün, Balkon, vs.)
CREATE TABLE venue_sections (
    id              SERIAL PRIMARY KEY,
    venue_id        INT NOT NULL REFERENCES venues(id) ON DELETE CASCADE,
    name            VARCHAR(100) NOT NULL,
    capacity        INT DEFAULT 0,
    price_multiplier NUMERIC(4,2) DEFAULT 1.00
);
CREATE INDEX idx_vsection_venue ON venue_sections(venue_id);

-- Etkinlikler
CREATE TABLE events (
    id              SERIAL PRIMARY KEY,
    title           VARCHAR(300) NOT NULL,
    category        event_category NOT NULL,
    venue_id        INT NOT NULL REFERENCES venues(id) ON DELETE CASCADE,
    description     TEXT,
    poster_url      TEXT,
    min_age         INT DEFAULT 0,
    organizer       VARCHAR(200),
    status          VARCHAR(20) DEFAULT 'published', -- draft, published, cancelled, completed
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ
);
CREATE INDEX idx_events_venue ON events(venue_id);
CREATE INDEX idx_events_category ON events(category);

-- Seanslar / Gösterimler
CREATE TABLE event_sessions (
    id              SERIAL PRIMARY KEY,
    event_id        INT NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    start_time      TIMESTAMPTZ NOT NULL,
    end_time        TIMESTAMPTZ,
    is_active       BOOLEAN DEFAULT true,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_session_event ON event_sessions(event_id);
CREATE INDEX idx_session_start ON event_sessions(start_time);

-- Bölüm bazında fiyatlandırma (her seans + her bölüm için ayrı fiyat)
CREATE TABLE session_pricing (
    id              SERIAL PRIMARY KEY,
    session_id      INT NOT NULL REFERENCES event_sessions(id) ON DELETE CASCADE,
    section_id      INT NOT NULL REFERENCES venue_sections(id) ON DELETE CASCADE,
    price           NUMERIC(10,2) NOT NULL,
    currency        VARCHAR(3) DEFAULT 'TRY'
);
CREATE INDEX idx_spricing_session ON session_pricing(session_id);

-- Koltuklar (opsiyonel — numarasız salonlar için kullanılmaz)
CREATE TABLE seats (
    id              SERIAL PRIMARY KEY,
    section_id      INT NOT NULL REFERENCES venue_sections(id) ON DELETE CASCADE,
    row_label       VARCHAR(10),
    seat_number     INT,
    seat_label      VARCHAR(20) GENERATED ALWAYS AS (
        CASE WHEN row_label IS NOT NULL AND seat_number IS NOT NULL
             THEN row_label || seat_number::TEXT
             ELSE NULL END
    ) STORED,
    is_active       BOOLEAN DEFAULT true
);
CREATE INDEX idx_seats_section ON seats(section_id);

-- Rezervasyon / Sipariş
CREATE TABLE ticket_bookings (
    id              SERIAL PRIMARY KEY,
    user_id         INT NOT NULL REFERENCES users(id),
    session_id      INT NOT NULL REFERENCES event_sessions(id),
    status          VARCHAR(20) DEFAULT 'pending', -- pending, confirmed, cancelled, refunded
    total_amount    NUMERIC(10,2) NOT NULL,
    currency        VARCHAR(3) DEFAULT 'TRY',
    paid_at         TIMESTAMPTZ,
    cancelled_at    TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_booking_user ON ticket_bookings(user_id);
CREATE INDEX idx_booking_session ON ticket_bookings(session_id);

-- Biletler
CREATE TABLE tickets (
    id              SERIAL PRIMARY KEY,
    booking_id      INT NOT NULL REFERENCES ticket_bookings(id) ON DELETE CASCADE,
    session_id      INT NOT NULL REFERENCES event_sessions(id),
    section_id      INT NOT NULL REFERENCES venue_sections(id),
    seat_id         INT REFERENCES seats(id) ON DELETE SET NULL,
    seat_label      VARCHAR(20),
    price           NUMERIC(10,2) NOT NULL,
    barcode         VARCHAR(100) UNIQUE,
    status          VARCHAR(20) DEFAULT 'active', -- active, used, refunded, cancelled
    used_at         TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_tickets_booking ON tickets(booking_id);
CREATE INDEX idx_tickets_session ON tickets(session_id);
CREATE INDEX idx_tickets_barcode ON tickets(barcode);
