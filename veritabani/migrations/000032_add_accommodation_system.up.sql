-- Migration 000032: Accommodation system (otel, pansiyon, villa, yazlik, oda kiralama)
-- Customer satisfaction, fumigation, housekeeping, kitchen, safety, compliance

-- 1. Hotel/Acommodation property type & company info (ALTER hotels)
ALTER TABLE hotels ADD COLUMN IF NOT EXISTS property_type VARCHAR(20) DEFAULT 'hotel';
ALTER TABLE hotels ADD COLUMN IF NOT EXISTS listing_type VARCHAR(20) DEFAULT 'entire_place';
ALTER TABLE hotels ADD COLUMN IF NOT EXISTS website VARCHAR(200);
ALTER TABLE hotels ADD COLUMN IF NOT EXISTS tax_id VARCHAR(50);
ALTER TABLE hotels ADD COLUMN IF NOT EXISTS company_name VARCHAR(200);
ALTER TABLE hotels ADD COLUMN IF NOT EXISTS company_description TEXT;
ALTER TABLE hotels ADD COLUMN IF NOT EXISTS house_rules TEXT;
ALTER TABLE hotels ADD COLUMN IF NOT EXISTS suspended_until TIMESTAMPTZ;
ALTER TABLE hotels ADD COLUMN IF NOT EXISTS suspension_reason TEXT;
ALTER TABLE hotels ADD COLUMN IF NOT EXISTS original_location_id INTEGER REFERENCES hotels(id);
ALTER TABLE hotels ADD COLUMN IF NOT EXISTS requires_location_approval BOOLEAN DEFAULT FALSE;
ALTER TABLE hotels ADD COLUMN IF NOT EXISTS location_approved_by INTEGER REFERENCES users(id);

-- 2. Photo categories
ALTER TABLE hotel_photos ADD COLUMN IF NOT EXISTS category VARCHAR(50) DEFAULT 'exterior';
ALTER TABLE hotel_photos ADD COLUMN IF NOT EXISTS is_main BOOLEAN DEFAULT FALSE;
ALTER TABLE room_photos ADD COLUMN IF NOT EXISTS caption VARCHAR(200);
ALTER TABLE room_photos ADD COLUMN IF NOT EXISTS category VARCHAR(50) DEFAULT 'interior';

-- 3. Service categories (Klik/Tag sistemi)
CREATE TABLE IF NOT EXISTS service_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    icon VARCHAR(50),
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS property_services (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    category_id INTEGER NOT NULL REFERENCES service_categories(id),
    name VARCHAR(100) NOT NULL,
    icon VARCHAR(50),
    description VARCHAR(200),
    is_free BOOLEAN DEFAULT TRUE,
    price DOUBLE PRECISION,
    is_active BOOLEAN DEFAULT TRUE
);

-- 4. Satisfaction surveys
CREATE TABLE IF NOT EXISTS accommodation_satisfaction_surveys (
    id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL REFERENCES bookings(id),
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    overall_score INTEGER,
    would_recommend BOOLEAN,
    checkin_experience INTEGER,
    cleanliness_score INTEGER,
    service_score INTEGER,
    view_score INTEGER,
    food_score INTEGER,
    value_score INTEGER,
    noise_score INTEGER,
    bed_comfort INTEGER,
    comments TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 5. Review photos
CREATE TABLE IF NOT EXISTS accommodation_review_photos (
    id SERIAL PRIMARY KEY,
    review_id INTEGER NOT NULL REFERENCES hotel_reviews(id),
    url VARCHAR(500) NOT NULL,
    caption VARCHAR(200),
    sort_order INTEGER DEFAULT 0
);

-- 6. Guest complaints & resolutions
CREATE TABLE IF NOT EXISTS guest_complaints (
    id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL REFERENCES bookings(id),
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    category VARCHAR(50) NOT NULL,
    priority VARCHAR(20) DEFAULT 'normal',
    description TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'open',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS complaint_resolutions (
    id SERIAL PRIMARY KEY,
    complaint_id INTEGER NOT NULL REFERENCES guest_complaints(id),
    resolved_by INTEGER NOT NULL REFERENCES users(id),
    resolution_notes TEXT,
    compensation VARCHAR(500),
    resolved_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. Guest preferences
CREATE TABLE IF NOT EXISTS guest_preferences (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    preferred_room_type VARCHAR(100),
    dietary_restrictions TEXT,
    special_needs TEXT,
    preferred_floor VARCHAR(20),
    smoking_preference VARCHAR(20),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 8. Housekeeping logs
CREATE TABLE IF NOT EXISTS housekeeping_logs (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    room_type_id INTEGER REFERENCES room_types(id),
    room_number VARCHAR(20),
    cleaning_date TIMESTAMPTZ NOT NULL,
    cleaner_name VARCHAR(100),
    checklist_items JSONB,
    status VARCHAR(20) DEFAULT 'completed',
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 9. Fumigation / Pest control logs (ILACLAMA)
CREATE TABLE IF NOT EXISTS property_fumigation_logs (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    scheduled_date TIMESTAMPTZ,
    fumigation_date TIMESTAMPTZ,
    next_fumigation_date TIMESTAMPTZ,
    chemical_used VARCHAR(200),
    company_name VARCHAR(200),
    technician_name VARCHAR(100),
    target_pests VARCHAR(200),
    areas_treated TEXT,
    status VARCHAR(20) DEFAULT 'scheduled',
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 10. Hotel kitchens / restaurants
CREATE TABLE IF NOT EXISTS hotel_kitchens (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    name VARCHAR(200) NOT NULL,
    cuisine_type VARCHAR(100),
    is_open BOOLEAN DEFAULT TRUE,
    opening_time VARCHAR(5) DEFAULT '07:00',
    closing_time VARCHAR(5) DEFAULT '22:00',
    min_order_amount DOUBLE PRECISION DEFAULT 0,
    preparation_time_min INTEGER DEFAULT 30,
    phone VARCHAR(20),
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 11. Hotel menu items
CREATE TABLE IF NOT EXISTS hotel_menu_items (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    kitchen_id INTEGER NOT NULL REFERENCES hotel_kitchens(id),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    price DOUBLE PRECISION NOT NULL,
    compare_price DOUBLE PRECISION,
    is_available BOOLEAN DEFAULT TRUE,
    is_vegetarian BOOLEAN DEFAULT FALSE,
    is_vegan BOOLEAN DEFAULT FALSE,
    is_gluten_free BOOLEAN DEFAULT FALSE,
    image_url VARCHAR(500),
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 12. In-room dining orders
CREATE TABLE IF NOT EXISTS in_room_dining_orders (
    id SERIAL PRIMARY KEY,
    order_no VARCHAR(20) UNIQUE NOT NULL,
    booking_id INTEGER NOT NULL REFERENCES bookings(id),
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    kitchen_id INTEGER NOT NULL REFERENCES hotel_kitchens(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    room_number VARCHAR(20),
    items JSONB NOT NULL,
    total_price DOUBLE PRECISION NOT NULL,
    status VARCHAR(20) DEFAULT 'ordered',
    special_instructions TEXT,
    ordered_at TIMESTAMPTZ DEFAULT NOW(),
    prepared_at TIMESTAMPTZ,
    delivered_at TIMESTAMPTZ,
    cancelled_at TIMESTAMPTZ
);

-- 13. Hotel kitchen reviews
CREATE TABLE IF NOT EXISTS hotel_kitchen_reviews (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    kitchen_id INTEGER NOT NULL REFERENCES hotel_kitchens(id),
    order_id INTEGER NOT NULL REFERENCES in_room_dining_orders(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    food_quality INTEGER,
    presentation INTEGER,
    delivery_speed INTEGER,
    temperature INTEGER,
    comment TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 14. Nearby places
CREATE TABLE IF NOT EXISTS nearby_places (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    name VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL,
    distance_km DOUBLE PRECISION,
    lat DOUBLE PRECISION,
    lng DOUBLE PRECISION,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 15. Building info (insaat bilgisi)
CREATE TABLE IF NOT EXISTS property_building_info (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) UNIQUE,
    year_built INTEGER,
    architect VARCHAR(200),
    contractor VARCHAR(200),
    construction_company VARCHAR(200),
    building_type VARCHAR(100),
    number_of_floors INTEGER,
    total_room_count INTEGER,
    has_elevator BOOLEAN DEFAULT FALSE,
    has_generator BOOLEAN DEFAULT FALSE,
    has_parking BOOLEAN DEFAULT FALSE,
    has_shelter BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 16. Fire safety systems (yangin sistemi)
CREATE TABLE IF NOT EXISTS fire_safety_systems (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    system_type VARCHAR(100) NOT NULL,
    has_sprinkler BOOLEAN DEFAULT FALSE,
    has_fire_alarm BOOLEAN DEFAULT FALSE,
    has_fire_extinguisher BOOLEAN DEFAULT FALSE,
    has_fire_hose BOOLEAN DEFAULT FALSE,
    has_emergency_exit BOOLEAN DEFAULT FALSE,
    has_fire_escape BOOLEAN DEFAULT FALSE,
    installation_company VARCHAR(200),
    last_service_date TIMESTAMPTZ,
    next_service_date TIMESTAMPTZ,
    certificate_number VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 17. Security systems
CREATE TABLE IF NOT EXISTS property_security_systems (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    has_cctv BOOLEAN DEFAULT FALSE,
    has_alarm BOOLEAN DEFAULT FALSE,
    has_security_personnel BOOLEAN DEFAULT FALSE,
    has_room_safe BOOLEAN DEFAULT FALSE,
    has_electronic_card BOOLEAN DEFAULT FALSE,
    has_24h_front_desk BOOLEAN DEFAULT FALSE,
    has_fire_door BOOLEAN DEFAULT FALSE,
    has_emergency_lighting BOOLEAN DEFAULT FALSE,
    has_smoke_detector BOOLEAN DEFAULT FALSE,
    has_co_detector BOOLEAN DEFAULT FALSE,
    installation_company VARCHAR(200),
    verification_date TIMESTAMPTZ,
    verification_company VARCHAR(200),
    is_active BOOLEAN DEFAULT TRUE,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 18. Property inspections (belediye/bakanlik denetimi)
CREATE TABLE IF NOT EXISTS property_inspections (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    inspection_type VARCHAR(50) NOT NULL,
    inspector_name VARCHAR(200),
    inspector_organization VARCHAR(200),
    inspection_date TIMESTAMPTZ NOT NULL,
    result VARCHAR(20),
    certificate_number VARCHAR(100),
    valid_until TIMESTAMPTZ,
    findings TEXT,
    notes TEXT,
    document_url VARCHAR(500),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 19. Safety certificates
CREATE TABLE IF NOT EXISTS safety_certificates (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    certificate_type VARCHAR(100) NOT NULL,
    certificate_number VARCHAR(200),
    issuing_authority VARCHAR(200),
    issue_date TIMESTAMPTZ,
    expiry_date TIMESTAMPTZ,
    document_url VARCHAR(500),
    is_valid BOOLEAN DEFAULT TRUE,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 20. Tourism associations (turizm dernegi)
CREATE TABLE IF NOT EXISTS tourism_associations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    association_type VARCHAR(50) NOT NULL,
    city VARCHAR(100),
    phone VARCHAR(20),
    website VARCHAR(200),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 21. Property association members
CREATE TABLE IF NOT EXISTS property_association_members (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    association_id INTEGER NOT NULL REFERENCES tourism_associations(id),
    membership_number VARCHAR(100),
    member_since TIMESTAMPTZ,
    valid_until TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 22. Property documents (resmi izin belgeleri)
CREATE TABLE IF NOT EXISTS property_documents (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    document_type VARCHAR(100) NOT NULL,
    document_name VARCHAR(200),
    file_url VARCHAR(500) NOT NULL,
    reference_number VARCHAR(100),
    issuing_authority VARCHAR(200),
    issue_date TIMESTAMPTZ,
    expiry_date TIMESTAMPTZ,
    is_verified BOOLEAN DEFAULT FALSE,
    verified_by INTEGER REFERENCES users(id),
    verified_at TIMESTAMPTZ,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 23. Hotel suspensions (kademeli askı sistemi)
CREATE TABLE IF NOT EXISTS hotel_suspensions (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    suspension_number INTEGER DEFAULT 1,
    reason TEXT NOT NULL,
    duration_days INTEGER NOT NULL,
    start_date TIMESTAMPTZ NOT NULL,
    end_date TIMESTAMPTZ NOT NULL,
    triggered_by_complaint_id INTEGER REFERENCES guest_complaints(id),
    resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 24. Complaint actions (24 saat kuralı)
CREATE TABLE IF NOT EXISTS complaint_actions (
    id SERIAL PRIMARY KEY,
    complaint_id INTEGER NOT NULL REFERENCES guest_complaints(id),
    action_type VARCHAR(50) NOT NULL,
    description TEXT,
    performed_by INTEGER REFERENCES users(id),
    deadline TIMESTAMPTZ,
    resolved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 25. Guest bans (müşteri men etme sistemi)
CREATE TABLE IF NOT EXISTS guest_bans (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    user_id INTEGER NOT NULL REFERENCES users(id),
    reason_category VARCHAR(50) NOT NULL,
    description TEXT,
    is_permanent BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMPTZ,
    issued_by INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    revoked_at TIMESTAMPTZ,
    revoked_by INTEGER REFERENCES users(id)
);

-- 26. Location registration requests (aynı lokasyon yeniden açılış)
CREATE TABLE IF NOT EXISTS location_registration_requests (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    existing_hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    requester_id INTEGER NOT NULL REFERENCES users(id),
    reason TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    approved_by INTEGER REFERENCES users(id),
    approved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_suspension_hotel ON hotel_suspensions(hotel_id);
CREATE INDEX IF NOT EXISTS idx_suspension_active ON hotel_suspensions(hotel_id, resolved);
CREATE INDEX IF NOT EXISTS idx_complaint_action_complaint ON complaint_actions(complaint_id);
CREATE INDEX IF NOT EXISTS idx_complaint_action_deadline ON complaint_actions(deadline);
CREATE INDEX IF NOT EXISTS idx_location_request_hotel ON location_registration_requests(hotel_id);
CREATE INDEX IF NOT EXISTS idx_guest_ban_hotel_user ON guest_bans(hotel_id, user_id);
CREATE INDEX IF NOT EXISTS idx_guest_ban_revoked ON guest_bans(revoked_at);
CREATE INDEX IF NOT EXISTS idx_location_request_status ON location_registration_requests(status);
CREATE INDEX IF NOT EXISTS idx_property_services_hotel ON property_services(hotel_id);
CREATE INDEX IF NOT EXISTS idx_property_services_category ON property_services(category_id);
CREATE INDEX IF NOT EXISTS idx_surveys_hotel ON accommodation_satisfaction_surveys(hotel_id);
CREATE INDEX IF NOT EXISTS idx_surveys_booking ON accommodation_satisfaction_surveys(booking_id);
CREATE INDEX IF NOT EXISTS idx_complaints_hotel ON guest_complaints(hotel_id);
CREATE INDEX IF NOT EXISTS idx_complaints_user ON guest_complaints(user_id);
CREATE INDEX IF NOT EXISTS idx_complaints_status ON guest_complaints(status);
CREATE INDEX IF NOT EXISTS idx_housekeeping_hotel ON housekeeping_logs(hotel_id);
CREATE INDEX IF NOT EXISTS idx_housekeeping_date ON housekeeping_logs(cleaning_date);
CREATE INDEX IF NOT EXISTS idx_fumigation_hotel ON property_fumigation_logs(hotel_id);
CREATE INDEX IF NOT EXISTS idx_fumigation_status ON property_fumigation_logs(status);
CREATE INDEX IF NOT EXISTS idx_fumigation_scheduled ON property_fumigation_logs(scheduled_date);
CREATE INDEX IF NOT EXISTS idx_kitchen_hotel ON hotel_kitchens(hotel_id);
CREATE INDEX IF NOT EXISTS idx_menu_kitchen ON hotel_menu_items(kitchen_id);
CREATE INDEX IF NOT EXISTS idx_dining_booking ON in_room_dining_orders(booking_id);
CREATE INDEX IF NOT EXISTS idx_dining_kitchen ON in_room_dining_orders(kitchen_id);
CREATE INDEX IF NOT EXISTS idx_dining_status ON in_room_dining_orders(status);
CREATE INDEX IF NOT EXISTS idx_nearby_hotel ON nearby_places(hotel_id);
CREATE INDEX IF NOT EXISTS idx_building_hotel ON property_building_info(hotel_id);
CREATE INDEX IF NOT EXISTS idx_fire_hotel ON fire_safety_systems(hotel_id);
CREATE INDEX IF NOT EXISTS idx_security_hotel ON property_security_systems(hotel_id);
CREATE INDEX IF NOT EXISTS idx_inspection_hotel ON property_inspections(hotel_id);
CREATE INDEX IF NOT EXISTS idx_certificate_hotel ON safety_certificates(hotel_id);
CREATE INDEX IF NOT EXISTS idx_assoc_member_hotel ON property_association_members(hotel_id);
CREATE INDEX IF NOT EXISTS idx_doc_hotel ON property_documents(hotel_id);
CREATE INDEX IF NOT EXISTS idx_doc_verified ON property_documents(is_verified);
CREATE INDEX IF NOT EXISTS idx_pref_user ON guest_preferences(user_id);
