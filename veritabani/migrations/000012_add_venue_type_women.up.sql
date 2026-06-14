ALTER TABLE venues ADD COLUMN venue_type VARCHAR(20) DEFAULT 'kapali';
CREATE INDEX idx_venues_type ON venues(venue_type);

ALTER TABLE event_sessions ADD COLUMN women_only BOOLEAN DEFAULT false;
CREATE INDEX idx_session_women ON event_sessions(women_only);
