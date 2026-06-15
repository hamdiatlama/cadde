-- 000033 DOWN: Rollback Hotel Technology Suite
BEGIN;

-- Energy Management
DROP TABLE IF EXISTS sustainability_certifications;
DROP TABLE IF EXISTS energy_saving_rules;
DROP TABLE IF EXISTS energy_consumption_reports;
DROP TABLE IF EXISTS energy_readings;
DROP TABLE IF EXISTS energy_meters;

-- IoT
DROP TABLE IF EXISTS room_environment_logs;
DROP TABLE IF EXISTS iot_automation_rules;
DROP TABLE IF EXISTS iot_device_commands;
DROP TABLE IF EXISTS iot_devices;

-- AI Concierge
DROP TABLE IF EXISTS automated_message_sequences;
DROP TABLE IF EXISTS concierge_knowledge_base;
DROP TABLE IF EXISTS concierge_messages;
DROP TABLE IF EXISTS concierge_conversations;
DROP TABLE IF EXISTS concierge_intents;
DROP TABLE IF EXISTS concierge_configs;

-- Digital Compendium
DROP TABLE IF EXISTS room_service_requests;
DROP TABLE IF EXISTS guest_notifications;
DROP TABLE IF EXISTS compendium_pages;
DROP TABLE IF EXISTS digital_compendiums;

-- Website Builder
DROP TABLE IF EXISTS website_booking_widgets;
DROP TABLE IF EXISTS website_seo;
DROP TABLE IF EXISTS website_pages;
DROP TABLE IF EXISTS hotel_websites;

-- Upselling
DROP TABLE IF EXISTS ancillary_revenue_reports;
DROP TABLE IF EXISTS upsell_campaigns;
DROP TABLE IF EXISTS upsell_booking_items;
DROP TABLE IF EXISTS upsell_offers;

-- Reputation
DROP TABLE IF EXISTS reputation_alerts;
DROP TABLE IF EXISTS sentiment_analysis;
DROP TABLE IF EXISTS review_responses;
DROP TABLE IF EXISTS external_reviews;
DROP TABLE IF EXISTS reputation_profiles;

-- Mobile Check-in
DROP TABLE IF EXISTS late_checkout_requests;
DROP TABLE IF EXISTS early_checkin_requests;
DROP TABLE IF EXISTS digital_keys;
DROP TABLE IF EXISTS mobile_checkins;

-- Multi-Property
DROP TABLE IF EXISTS group_consolidated_reports;
DROP TABLE IF EXISTS property_group_invites;
DROP TABLE IF EXISTS property_group_members;
DROP TABLE IF EXISTS property_groups;

-- Payment Gateway
DROP TABLE IF EXISTS payout_histories;
DROP TABLE IF EXISTS payout_requests;
DROP TABLE IF EXISTS payment_transactions;
DROP TABLE IF EXISTS merchant_accounts;
DROP TABLE IF EXISTS payment_providers;

-- Revenue Management
DROP TABLE IF EXISTS hotel_revenue_reports;
DROP TABLE IF EXISTS hotel_daily_rates;
DROP TABLE IF EXISTS hotel_revenue_rules;

-- Channel Manager
DROP TABLE IF EXISTS ota_sync_logs;
DROP TABLE IF EXISTS ota_bookings;
DROP TABLE IF EXISTS ota_rate_plans;
DROP TABLE IF EXISTS ota_listings;
DROP TABLE IF EXISTS ota_connections;
DROP TABLE IF EXISTS ota_channels;

COMMIT;
