-- 000033: Hotel Technology Suite — Channel Manager, Revenue, Payments, Multi-Property, Mobile Check-in, Reputation, Upselling, Website Builder, Digital Compendium, AI Concierge, IoT, Energy Management

BEGIN;

-- ============================================================
-- 1. CHANNEL MANAGER (OTA Integration)
-- ============================================================
CREATE TABLE ota_channels (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(50) NOT NULL UNIQUE,
    logo_url VARCHAR(500),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE ota_connections (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    ota_channel_id INTEGER NOT NULL REFERENCES ota_channels(id),
    status VARCHAR(20) DEFAULT 'disconnected',
    api_key TEXT,
    api_secret TEXT,
    webhook_url VARCHAR(500),
    connected_at TIMESTAMPTZ,
    last_sync_at TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT true
);

CREATE TABLE ota_listings (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    ota_connection_id INTEGER NOT NULL REFERENCES ota_connections(id),
    external_listing_id VARCHAR(200),
    external_url VARCHAR(500),
    listing_title VARCHAR(200),
    status VARCHAR(20) DEFAULT 'active',
    last_synced_at TIMESTAMPTZ,
    sync_errors TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE ota_rate_plans (
    id SERIAL PRIMARY KEY,
    listing_id INTEGER NOT NULL REFERENCES ota_listings(id),
    room_type_id INTEGER NOT NULL REFERENCES room_types(id),
    external_rate_plan_id VARCHAR(200),
    name VARCHAR(200),
    base_price FLOAT,
    currency VARCHAR(3) DEFAULT 'TRY',
    is_active BOOLEAN DEFAULT true
);

CREATE TABLE ota_bookings (
    id SERIAL PRIMARY KEY,
    ota_listing_id INTEGER NOT NULL REFERENCES ota_listings(id),
    external_booking_id VARCHAR(200) NOT NULL UNIQUE,
    guest_name VARCHAR(200),
    guest_email VARCHAR(200),
    check_in TIMESTAMPTZ NOT NULL,
    check_out TIMESTAMPTZ NOT NULL,
    adults INTEGER DEFAULT 1,
    children INTEGER DEFAULT 0,
    total_price FLOAT,
    currency VARCHAR(3) DEFAULT 'TRY',
    status VARCHAR(20) DEFAULT 'pending',
    booking_data JSONB,
    synced_to_pms BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE ota_sync_logs (
    id SERIAL PRIMARY KEY,
    connection_id INTEGER NOT NULL REFERENCES ota_connections(id),
    sync_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    message TEXT,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    errors_count INTEGER DEFAULT 0
);

CREATE INDEX idx_ota_connections_hotel ON ota_connections(hotel_id);
CREATE INDEX idx_ota_listings_hotel ON ota_listings(hotel_id);
CREATE INDEX idx_ota_listings_connection ON ota_listings(ota_connection_id);
CREATE INDEX idx_ota_rate_plans_listing ON ota_rate_plans(listing_id);
CREATE INDEX idx_ota_bookings_listing ON ota_bookings(ota_listing_id);
CREATE INDEX idx_ota_bookings_status ON ota_bookings(status);
CREATE INDEX idx_ota_sync_logs_connection ON ota_sync_logs(connection_id);

-- ============================================================
-- 2. HOTEL REVENUE MANAGEMENT
-- ============================================================
CREATE TABLE hotel_revenue_rules (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    rule_type VARCHAR(50) NOT NULL,
    name VARCHAR(200) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    priority INTEGER DEFAULT 0,
    conditions JSONB,
    adjustment_type VARCHAR(20),
    adjustment_value FLOAT,
    min_stay INTEGER,
    max_stay INTEGER,
    advance_days_min INTEGER,
    advance_days_max INTEGER,
    occupancy_threshold FLOAT,
    day_of_week VARCHAR(50),
    start_date TIMESTAMPTZ,
    end_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE hotel_daily_rates (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    room_type_id INTEGER NOT NULL REFERENCES room_types(id),
    date DATE NOT NULL,
    base_price FLOAT,
    dynamic_price FLOAT,
    final_price FLOAT,
    occupancy_rate FLOAT DEFAULT 0,
    is_boosted BOOLEAN DEFAULT false,
    is_sale BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(room_type_id, date)
);

CREATE TABLE hotel_revenue_reports (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    report_date DATE NOT NULL,
    revpar FLOAT,
    adr FLOAT,
    occupancy_rate FLOAT,
    total_revenue FLOAT,
    room_revenue FLOAT,
    ancillary_revenue FLOAT,
    booked_rooms INTEGER,
    available_rooms INTEGER,
    cancellation_rate FLOAT,
    avg_length_of_stay FLOAT,
    report_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_revenue_rules_hotel ON hotel_revenue_rules(hotel_id);
CREATE INDEX idx_daily_rates_hotel ON hotel_daily_rates(hotel_id);
CREATE INDEX idx_daily_rates_date ON hotel_daily_rates(date);
CREATE INDEX idx_revenue_reports_hotel ON hotel_revenue_reports(hotel_id);

-- ============================================================
-- 3. PAYMENT GATEWAY
-- ============================================================
CREATE TABLE payment_providers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(50) NOT NULL UNIQUE,
    is_active BOOLEAN DEFAULT true,
    supported_currencies VARCHAR(200),
    fee_percentage FLOAT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE merchant_accounts (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    provider_id INTEGER NOT NULL REFERENCES payment_providers(id),
    api_key TEXT,
    api_secret TEXT,
    merchant_id VARCHAR(100),
    is_verified BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE payment_transactions (
    id SERIAL PRIMARY KEY,
    booking_id INTEGER REFERENCES bookings(id),
    merchant_account_id INTEGER REFERENCES merchant_accounts(id),
    transaction_id VARCHAR(200),
    reference_no VARCHAR(100) UNIQUE,
    amount FLOAT NOT NULL,
    currency VARCHAR(3) DEFAULT 'TRY',
    fee FLOAT,
    net_amount FLOAT,
    status VARCHAR(20) DEFAULT 'pending',
    payment_method VARCHAR(50),
    card_last_four VARCHAR(4),
    installment INTEGER DEFAULT 1,
    paid_at TIMESTAMPTZ,
    refunded_at TIMESTAMPTZ,
    raw_response JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE payout_requests (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    amount FLOAT NOT NULL,
    fee FLOAT,
    net_amount FLOAT,
    status VARCHAR(20) DEFAULT 'pending',
    account_holder VARCHAR(200),
    iban VARCHAR(50),
    bank_name VARCHAR(200),
    requested_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    notes TEXT
);

CREATE TABLE payout_histories (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    payout_request_id INTEGER REFERENCES payout_requests(id),
    amount FLOAT,
    fee FLOAT,
    net_amount FLOAT,
    status VARCHAR(20),
    external_payout_id VARCHAR(200),
    processed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_merchant_accounts_hotel ON merchant_accounts(hotel_id);
CREATE INDEX idx_payment_transactions_booking ON payment_transactions(booking_id);
CREATE INDEX idx_payment_transactions_status ON payment_transactions(status);
CREATE INDEX idx_payout_requests_hotel ON payout_requests(hotel_id);

-- ============================================================
-- 4. MULTI-PROPERTY GROUP MANAGEMENT
-- ============================================================
CREATE TABLE property_groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    owner_id INTEGER NOT NULL REFERENCES users(id),
    logo_url VARCHAR(500),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE property_group_members (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES property_groups(id) ON DELETE CASCADE,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL DEFAULT 'staff',
    is_primary BOOLEAN DEFAULT false,
    joined_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(group_id, hotel_id)
);

CREATE TABLE property_group_invites (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES property_groups(id) ON DELETE CASCADE,
    email VARCHAR(200) NOT NULL,
    role VARCHAR(50),
    token VARCHAR(100) NOT NULL UNIQUE,
    status VARCHAR(20) DEFAULT 'pending',
    invited_by INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ
);

CREATE TABLE group_consolidated_reports (
    id SERIAL PRIMARY KEY,
    group_id INTEGER NOT NULL REFERENCES property_groups(id) ON DELETE CASCADE,
    report_date DATE NOT NULL,
    total_revenue FLOAT,
    total_bookings INTEGER,
    avg_occupancy FLOAT,
    avg_revpar FLOAT,
    total_hotels INTEGER,
    report_data JSONB,
    generated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_property_groups_owner ON property_groups(owner_id);
CREATE INDEX idx_group_members_group ON property_group_members(group_id);
CREATE INDEX idx_group_members_hotel ON property_group_members(hotel_id);
CREATE INDEX idx_group_invites_group ON property_group_invites(group_id);

-- ============================================================
-- 5. MOBILE CHECK-IN & DIGITAL KEY
-- ============================================================
CREATE TABLE mobile_checkins (
    id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL UNIQUE REFERENCES bookings(id),
    guest_id INTEGER NOT NULL REFERENCES users(id),
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    checkin_data JSONB,
    id_verified BOOLEAN DEFAULT false,
    status VARCHAR(20) DEFAULT 'pending',
    verified_by INTEGER REFERENCES users(id),
    checked_in_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE digital_keys (
    id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL REFERENCES bookings(id),
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    room_type_id INTEGER REFERENCES room_types(id),
    room_number VARCHAR(20),
    guest_id INTEGER NOT NULL REFERENCES users(id),
    key_code VARCHAR(100) NOT NULL UNIQUE,
    qr_code VARCHAR(500),
    status VARCHAR(20) DEFAULT 'active',
    valid_from TIMESTAMPTZ,
    valid_until TIMESTAMPTZ,
    issued_at TIMESTAMPTZ DEFAULT NOW(),
    used_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE early_checkin_requests (
    id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL REFERENCES bookings(id),
    requested_time TIME NOT NULL,
    is_approved BOOLEAN,
    approved_by INTEGER REFERENCES users(id),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE late_checkout_requests (
    id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL REFERENCES bookings(id),
    requested_time TIME NOT NULL,
    is_approved BOOLEAN,
    additional_fee FLOAT,
    approved_by INTEGER REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_mobile_checkins_hotel ON mobile_checkins(hotel_id);
CREATE INDEX idx_digital_keys_booking ON digital_keys(booking_id);
CREATE INDEX idx_digital_keys_guest ON digital_keys(guest_id);
CREATE INDEX idx_digital_keys_status ON digital_keys(status);

-- ============================================================
-- 6. ONLINE REPUTATION MANAGEMENT
-- ============================================================
CREATE TABLE reputation_profiles (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL UNIQUE REFERENCES hotels(id) ON DELETE CASCADE,
    overall_score FLOAT DEFAULT 0,
    review_count INTEGER DEFAULT 0,
    response_rate FLOAT DEFAULT 0,
    avg_response_time_hours FLOAT,
    platform_scores JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE external_reviews (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,
    external_review_id VARCHAR(200),
    reviewer_name VARCHAR(200),
    rating FLOAT,
    title VARCHAR(200),
    comment TEXT,
    language VARCHAR(10),
    reviewed_at TIMESTAMPTZ,
    imported_at TIMESTAMPTZ DEFAULT NOW(),
    is_responded BOOLEAN DEFAULT false
);

CREATE TABLE review_responses (
    id SERIAL PRIMARY KEY,
    review_id INTEGER NOT NULL REFERENCES external_reviews(id) ON DELETE CASCADE,
    response_text TEXT NOT NULL,
    responded_by INTEGER NOT NULL REFERENCES users(id),
    is_auto_generated BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE sentiment_analysis (
    id SERIAL PRIMARY KEY,
    review_id INTEGER NOT NULL REFERENCES external_reviews(id) ON DELETE CASCADE,
    sentiment VARCHAR(20) NOT NULL,
    score FLOAT,
    keywords JSONB,
    category VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE reputation_alerts (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    alert_type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) DEFAULT 'medium',
    message TEXT,
    is_resolved BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_external_reviews_hotel ON external_reviews(hotel_id);
CREATE INDEX idx_external_reviews_platform ON external_reviews(platform);
CREATE INDEX idx_reputation_alerts_hotel ON reputation_alerts(hotel_id);

-- ============================================================
-- 7. UPSELLING & ANCILLARY REVENUE
-- ============================================================
CREATE TABLE upsell_offers (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(50) NOT NULL,
    price FLOAT NOT NULL,
    currency VARCHAR(3) DEFAULT 'TRY',
    is_active BOOLEAN DEFAULT true,
    is_auto_offer BOOLEAN DEFAULT false,
    trigger_event VARCHAR(50),
    display_order INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE upsell_booking_items (
    id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL REFERENCES bookings(id),
    offer_id INTEGER NOT NULL REFERENCES upsell_offers(id),
    quantity INTEGER DEFAULT 1,
    unit_price FLOAT,
    total_price FLOAT,
    status VARCHAR(20) DEFAULT 'pending',
    added_at TIMESTAMPTZ DEFAULT NOW(),
    confirmed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE upsell_campaigns (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    rules JSONB,
    discount_percentage FLOAT,
    is_active BOOLEAN DEFAULT true,
    start_date TIMESTAMPTZ,
    end_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE ancillary_revenue_reports (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    report_date DATE NOT NULL,
    total_upsell_revenue FLOAT,
    total_orders INTEGER,
    breakdown JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_upsell_offers_hotel ON upsell_offers(hotel_id);
CREATE INDEX idx_upsell_booking_items_booking ON upsell_booking_items(booking_id);

-- ============================================================
-- 8. HOTEL WEBSITE BUILDER
-- ============================================================
CREATE TABLE hotel_websites (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL UNIQUE REFERENCES hotels(id) ON DELETE CASCADE,
    domain VARCHAR(200) UNIQUE,
    subdomain VARCHAR(200) UNIQUE,
    template_id VARCHAR(50) DEFAULT 'default',
    primary_color VARCHAR(7) DEFAULT '#4A7FD4',
    secondary_color VARCHAR(7) DEFAULT '#EEF4FF',
    font_family VARCHAR(100) DEFAULT 'Space Grotesk',
    logo_url VARCHAR(500),
    hero_image_url VARCHAR(500),
    about_text TEXT,
    is_published BOOLEAN DEFAULT false,
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE website_pages (
    id SERIAL PRIMARY KEY,
    website_id INTEGER NOT NULL REFERENCES hotel_websites(id) ON DELETE CASCADE,
    slug VARCHAR(200) NOT NULL,
    title VARCHAR(200) NOT NULL,
    content JSONB,
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE website_seo (
    id SERIAL PRIMARY KEY,
    website_id INTEGER NOT NULL REFERENCES hotel_websites(id) ON DELETE CASCADE,
    page_id INTEGER REFERENCES website_pages(id),
    meta_title VARCHAR(200),
    meta_description VARCHAR(500),
    meta_keywords VARCHAR(500),
    og_image_url VARCHAR(500),
    canonical_url VARCHAR(500),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE website_booking_widgets (
    id SERIAL PRIMARY KEY,
    website_id INTEGER NOT NULL REFERENCES hotel_websites(id) ON DELETE CASCADE,
    widget_type VARCHAR(50) DEFAULT 'inline',
    is_enabled BOOLEAN DEFAULT true,
    embed_code TEXT,
    custom_css TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_website_pages_website ON website_pages(website_id);

-- ============================================================
-- 9. DIGITAL COMPENDIUM (In-Room Guest Directory)
-- ============================================================
CREATE TABLE digital_compendiums (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL UNIQUE REFERENCES hotels(id) ON DELETE CASCADE,
    welcome_message TEXT,
    wifi_ssid VARCHAR(100),
    wifi_password VARCHAR(100),
    breakfast_info TEXT,
    restaurant_info TEXT,
    room_service_info TEXT,
    spa_info TEXT,
    gym_info TEXT,
    parking_info TEXT,
    house_rules TEXT,
    emergency_info TEXT,
    checkout_info TEXT,
    local_attractions JSONB,
    hotel_services JSONB,
    contact_info TEXT,
    is_published BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE compendium_pages (
    id SERIAL PRIMARY KEY,
    compendium_id INTEGER NOT NULL REFERENCES digital_compendiums(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    icon VARCHAR(50),
    sort_order INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE guest_notifications (
    id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL REFERENCES bookings(id),
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    room_number VARCHAR(20),
    notification_type VARCHAR(50) NOT NULL,
    title VARCHAR(200),
    message TEXT,
    is_read BOOLEAN DEFAULT false,
    sent_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE room_service_requests (
    id SERIAL PRIMARY KEY,
    booking_id INTEGER NOT NULL REFERENCES bookings(id),
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    room_number VARCHAR(20),
    category VARCHAR(50) NOT NULL,
    item_name VARCHAR(200),
    quantity INTEGER DEFAULT 1,
    notes TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    requested_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE INDEX idx_compendium_pages_compendium ON compendium_pages(compendium_id);
CREATE INDEX idx_guest_notifications_booking ON guest_notifications(booking_id);
CREATE INDEX idx_room_service_hotel ON room_service_requests(hotel_id);

-- ============================================================
-- 10. AI CONCIERGE & AUTOMATED MESSAGING
-- ============================================================
CREATE TABLE concierge_configs (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL UNIQUE REFERENCES hotels(id) ON DELETE CASCADE,
    is_active BOOLEAN DEFAULT false,
    language VARCHAR(10) DEFAULT 'tr',
    greeting_message TEXT,
    operating_hours_start VARCHAR(5) DEFAULT '00:00',
    operating_hours_end VARCHAR(5) DEFAULT '23:59',
    auto_respond BOOLEAN DEFAULT true,
    escalation_threshold INTEGER DEFAULT 3,
    whatsapp_enabled BOOLEAN DEFAULT false,
    whatsapp_number VARCHAR(20),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE concierge_intents (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    intent_key VARCHAR(100) NOT NULL,
    trigger_phrases JSONB,
    response_template TEXT,
    requires_human BOOLEAN DEFAULT false,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE concierge_conversations (
    id SERIAL PRIMARY KEY,
    booking_id INTEGER REFERENCES bookings(id),
    guest_id INTEGER NOT NULL REFERENCES users(id),
    hotel_id INTEGER NOT NULL REFERENCES hotels(id),
    channel VARCHAR(20) DEFAULT 'in_app',
    status VARCHAR(20) DEFAULT 'active',
    started_at TIMESTAMPTZ DEFAULT NOW(),
    resolved_at TIMESTAMPTZ
);

CREATE TABLE concierge_messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES concierge_conversations(id) ON DELETE CASCADE,
    sender_type VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    intent_matched VARCHAR(100),
    is_auto_response BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE concierge_knowledge_base (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    category VARCHAR(50),
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE automated_message_sequences (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    trigger_event VARCHAR(50) NOT NULL,
    delay_hours INTEGER DEFAULT 0,
    message_template TEXT NOT NULL,
    channel VARCHAR(20) DEFAULT 'in_app',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_concierge_intents_hotel ON concierge_intents(hotel_id);
CREATE INDEX idx_concierge_conversations_hotel ON concierge_conversations(hotel_id);
CREATE INDEX idx_concierge_conversations_booking ON concierge_conversations(booking_id);
CREATE INDEX idx_concierge_messages_conversation ON concierge_messages(conversation_id);
CREATE INDEX idx_concierge_kb_hotel ON concierge_knowledge_base(hotel_id);
CREATE INDEX idx_auto_sequences_hotel ON automated_message_sequences(hotel_id);

-- ============================================================
-- 11. IoT & SMART ROOM CONTROLS
-- ============================================================
CREATE TABLE iot_devices (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    room_type_id INTEGER REFERENCES room_types(id),
    room_number VARCHAR(20),
    device_type VARCHAR(50) NOT NULL,
    device_name VARCHAR(200),
    manufacturer VARCHAR(100),
    model VARCHAR(100),
    serial_number VARCHAR(200) NOT NULL UNIQUE,
    ip_address VARCHAR(50),
    mac_address VARCHAR(50),
    firmware_version VARCHAR(50),
    status VARCHAR(20) DEFAULT 'offline',
    is_active BOOLEAN DEFAULT true,
    last_seen_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE iot_device_commands (
    id SERIAL PRIMARY KEY,
    device_id INTEGER NOT NULL REFERENCES iot_devices(id) ON DELETE CASCADE,
    command_type VARCHAR(50) NOT NULL,
    command_value VARCHAR(200),
    executed_by INTEGER REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'sent',
    executed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE iot_automation_rules (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    trigger_event VARCHAR(50) NOT NULL,
    conditions JSONB,
    actions JSONB,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE room_environment_logs (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    room_number VARCHAR(20),
    temperature FLOAT,
    humidity FLOAT,
    light_level FLOAT,
    noise_level FLOAT,
    occupancy_detected BOOLEAN,
    logged_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_iot_devices_hotel ON iot_devices(hotel_id);
CREATE INDEX idx_iot_devices_type ON iot_devices(device_type);
CREATE INDEX idx_iot_commands_device ON iot_device_commands(device_id);
CREATE INDEX idx_iot_automation_hotel ON iot_automation_rules(hotel_id);
CREATE INDEX idx_room_env_hotel ON room_environment_logs(hotel_id);

-- ============================================================
-- 12. ENERGY MANAGEMENT & SUSTAINABILITY
-- ============================================================
CREATE TABLE energy_meters (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    meter_type VARCHAR(20) NOT NULL,
    meter_name VARCHAR(200),
    location VARCHAR(200),
    unit VARCHAR(20),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE energy_readings (
    id SERIAL PRIMARY KEY,
    meter_id INTEGER NOT NULL REFERENCES energy_meters(id) ON DELETE CASCADE,
    reading_value FLOAT NOT NULL,
    unit VARCHAR(20),
    reading_date TIMESTAMPTZ NOT NULL,
    source VARCHAR(20) DEFAULT 'manual',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE energy_consumption_reports (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    report_date DATE NOT NULL,
    total_electricity_kwh FLOAT,
    total_water_m3 FLOAT,
    total_gas_m3 FLOAT,
    total_cost FLOAT,
    electricity_cost FLOAT,
    water_cost FLOAT,
    gas_cost FLOAT,
    occupancy_rate FLOAT,
    cost_per_occupied_room FLOAT,
    report_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE energy_saving_rules (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    rule_name VARCHAR(200) NOT NULL,
    trigger_type VARCHAR(50),
    conditions JSONB,
    actions JSONB,
    estimated_savings_percent FLOAT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE sustainability_certifications (
    id SERIAL PRIMARY KEY,
    hotel_id INTEGER NOT NULL REFERENCES hotels(id) ON DELETE CASCADE,
    certification_name VARCHAR(200) NOT NULL,
    issuing_body VARCHAR(200),
    certificate_number VARCHAR(100),
    awarded_date DATE,
    expiry_date DATE,
    is_verified BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_energy_meters_hotel ON energy_meters(hotel_id);
CREATE INDEX idx_energy_readings_meter ON energy_readings(meter_id);
CREATE INDEX idx_energy_reports_hotel ON energy_consumption_reports(hotel_id);
CREATE INDEX idx_energy_saving_rules_hotel ON energy_saving_rules(hotel_id);
CREATE INDEX idx_sustainability_certs_hotel ON sustainability_certifications(hotel_id);

COMMIT;
