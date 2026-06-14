ALTER TABLE venues ADD COLUMN venue_type VARCHAR(20) DEFAULT 'kapali';
CREATE INDEX idx_venues_type ON venues(venue_type);
