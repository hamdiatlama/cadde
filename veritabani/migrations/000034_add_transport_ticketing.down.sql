-- 000034 DOWN
BEGIN;
DROP TABLE IF EXISTS transport_tickets;
DROP TABLE IF EXISTS transport_seats;
DROP TABLE IF EXISTS transport_schedules;
DROP TABLE IF EXISTS transport_routes;
DROP TABLE IF EXISTS transport_stations;
DROP TABLE IF EXISTS transport_companies;
DROP TYPE IF EXISTS ticket_status;
DROP TYPE IF EXISTS seat_class;
DROP TYPE IF EXISTS vehicle_type;
COMMIT;
