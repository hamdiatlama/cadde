package postgres

import (
	"context"
	"fmt"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/web-platform/backend/internal/domain"
)

type EventRepo struct {
	pool *pgxpool.Pool
}

func NewEventRepo(pool *pgxpool.Pool) *EventRepo {
	return &EventRepo{pool: pool}
}

func (r *EventRepo) CreateVenue(ctx context.Context, v *domain.Venue) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO venues (name, city, district, address, latitude, longitude, capacity, phone)
		 VALUES ($1,$2,$3,$4,$5,$6,$7,$8) RETURNING id, created_at`,
		v.Name, v.City, v.District, v.Address, v.Latitude, v.Longitude, v.Capacity, v.Phone,
	).Scan(&v.ID, &v.CreatedAt)
}

func (r *EventRepo) ListVenues(ctx context.Context) ([]*domain.Venue, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, name, city, district, address, latitude, longitude, capacity, phone, created_at
		 FROM venues ORDER BY created_at DESC`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var venues []*domain.Venue
	for rows.Next() {
		v := &domain.Venue{}
		if err := rows.Scan(&v.ID, &v.Name, &v.City, &v.District, &v.Address,
			&v.Latitude, &v.Longitude, &v.Capacity, &v.Phone, &v.CreatedAt); err != nil {
			return nil, err
		}
		venues = append(venues, v)
	}
	return venues, nil
}

func (r *EventRepo) GetVenue(ctx context.Context, id int) (*domain.Venue, error) {
	v := &domain.Venue{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, name, city, district, address, latitude, longitude, capacity, phone, created_at
		 FROM venues WHERE id=$1`, id,
	).Scan(&v.ID, &v.Name, &v.City, &v.District, &v.Address,
		&v.Latitude, &v.Longitude, &v.Capacity, &v.Phone, &v.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("get venue: %w", err)
	}
	return v, nil
}

func (r *EventRepo) DeleteVenue(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM venues WHERE id=$1`, id)
	return err
}

func (r *EventRepo) CreateVenueSection(ctx context.Context, vs *domain.VenueSection) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO venue_sections (venue_id, name, capacity, price_multiplier)
		 VALUES ($1,$2,$3,$4) RETURNING id`,
		vs.VenueID, vs.Name, vs.Capacity, vs.PriceMultiplier,
	).Scan(&vs.ID)
}

func (r *EventRepo) ListVenueSections(ctx context.Context, venueID int) ([]*domain.VenueSection, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, venue_id, name, capacity, price_multiplier
		 FROM venue_sections WHERE venue_id=$1 ORDER BY id`, venueID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var sections []*domain.VenueSection
	for rows.Next() {
		s := &domain.VenueSection{}
		if err := rows.Scan(&s.ID, &s.VenueID, &s.Name, &s.Capacity, &s.PriceMultiplier); err != nil {
			return nil, err
		}
		sections = append(sections, s)
	}
	return sections, nil
}

func (r *EventRepo) DeleteVenueSection(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM venue_sections WHERE id=$1`, id)
	return err
}

func (r *EventRepo) CreateEvent(ctx context.Context, e *domain.Event) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO events (title, category, venue_id, description, poster_url, min_age, organizer, status)
		 VALUES ($1,$2,$3,$4,$5,$6,$7,$8) RETURNING id, created_at`,
		e.Title, e.Category, e.VenueID, e.Description, e.PosterURL, e.MinAge, e.Organizer, e.Status,
	).Scan(&e.ID, &e.CreatedAt)
}

func (r *EventRepo) ListEvents(ctx context.Context, category *string, venueID *int, venueType *string) ([]*domain.Event, error) {
	query := `SELECT e.id, e.title, e.category, e.venue_id, e.description, e.poster_url, e.min_age, e.organizer, e.status, e.created_at, e.updated_at
		 FROM events e`
	var args []interface{}
	argIdx := 1
	conditions := ""

	if category != nil {
		conditions = fmt.Sprintf(" WHERE e.category=$%d", argIdx)
		args = append(args, *category)
		argIdx++
	}
	if venueID != nil {
		if conditions == "" {
			conditions = " WHERE"
		} else {
			conditions += " AND"
		}
		conditions += fmt.Sprintf(" e.venue_id=$%d", argIdx)
		args = append(args, *venueID)
		argIdx++
	}
	if venueType != nil {
		query += " JOIN venues v ON e.venue_id = v.id"
		if conditions == "" {
			conditions = " WHERE"
		} else {
			conditions += " AND"
		}
		conditions += fmt.Sprintf(" v.venue_type=$%d", argIdx)
		args = append(args, *venueType)
		argIdx++
	}

	query += conditions + " ORDER BY e.created_at DESC"

	rows, err := r.pool.Query(ctx, query, args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var events []*domain.Event
	for rows.Next() {
		e := &domain.Event{}
		if err := rows.Scan(&e.ID, &e.Title, &e.Category, &e.VenueID, &e.Description,
			&e.PosterURL, &e.MinAge, &e.Organizer, &e.Status, &e.CreatedAt, &e.UpdatedAt); err != nil {
			return nil, err
		}
		events = append(events, e)
	}
	return events, nil
}

func (r *EventRepo) GetEvent(ctx context.Context, id int) (*domain.Event, error) {
	e := &domain.Event{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, title, category, venue_id, description, poster_url, min_age, organizer, status, created_at, updated_at
		 FROM events WHERE id=$1`, id,
	).Scan(&e.ID, &e.Title, &e.Category, &e.VenueID, &e.Description,
		&e.PosterURL, &e.MinAge, &e.Organizer, &e.Status, &e.CreatedAt, &e.UpdatedAt)
	if err != nil {
		return nil, fmt.Errorf("get event: %w", err)
	}
	return e, nil
}

func (r *EventRepo) UpdateEventStatus(ctx context.Context, id int, status string) error {
	_, err := r.pool.Exec(ctx,
		`UPDATE events SET status=$1, updated_at=$2 WHERE id=$3`,
		status, time.Now(), id)
	return err
}

func (r *EventRepo) DeleteEvent(ctx context.Context, id int) error {
	_, err := r.pool.Exec(ctx, `DELETE FROM events WHERE id=$1`, id)
	return err
}

func (r *EventRepo) CreateEventSession(ctx context.Context, s *domain.EventSession) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO event_sessions (event_id, start_time, end_time, is_active)
		 VALUES ($1,$2,$3,$4) RETURNING id, created_at`,
		s.EventID, s.StartTime, s.EndTime, s.IsActive,
	).Scan(&s.ID, &s.CreatedAt)
}

func (r *EventRepo) ListEventSessions(ctx context.Context, eventID int) ([]*domain.EventSession, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, event_id, start_time, end_time, is_active, created_at
		 FROM event_sessions WHERE event_id=$1 ORDER BY start_time`, eventID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var sessions []*domain.EventSession
	for rows.Next() {
		s := &domain.EventSession{}
		if err := rows.Scan(&s.ID, &s.EventID, &s.StartTime, &s.EndTime, &s.IsActive, &s.CreatedAt); err != nil {
			return nil, err
		}
		sessions = append(sessions, s)
	}
	return sessions, nil
}

func (r *EventRepo) CreateSessionPricing(ctx context.Context, sp *domain.SessionPricing) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO session_pricing (session_id, section_id, price, currency)
		 VALUES ($1,$2,$3,$4) RETURNING id`,
		sp.SessionID, sp.SectionID, sp.Price, sp.Currency,
	).Scan(&sp.ID)
}

func (r *EventRepo) ListSessionPricing(ctx context.Context, sessionID int) ([]*domain.SessionPricing, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, session_id, section_id, price, currency
		 FROM session_pricing WHERE session_id=$1 ORDER BY id`, sessionID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var pricing []*domain.SessionPricing
	for rows.Next() {
		p := &domain.SessionPricing{}
		if err := rows.Scan(&p.ID, &p.SessionID, &p.SectionID, &p.Price, &p.Currency); err != nil {
			return nil, err
		}
		pricing = append(pricing, p)
	}
	return pricing, nil
}

func (r *EventRepo) BulkCreateSeats(ctx context.Context, seats []*domain.Seat) error {
	for _, s := range seats {
		err := r.pool.QueryRow(ctx,
			`INSERT INTO seats (section_id, row_label, seat_number, is_active)
			 VALUES ($1,$2,$3,$4) RETURNING id`,
			s.SectionID, s.RowLabel, s.SeatNumber, s.IsActive,
		).Scan(&s.ID)
		if err != nil {
			return err
		}
	}
	return nil
}

func (r *EventRepo) ListSeatsBySection(ctx context.Context, sectionID int) ([]*domain.Seat, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, section_id, row_label, seat_number, is_active
		 FROM seats WHERE section_id=$1 ORDER BY row_label, seat_number`, sectionID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var seats []*domain.Seat
	for rows.Next() {
		s := &domain.Seat{}
		if err := rows.Scan(&s.ID, &s.SectionID, &s.RowLabel, &s.SeatNumber, &s.IsActive); err != nil {
			return nil, err
		}
		seats = append(seats, s)
	}
	return seats, nil
}

func (r *EventRepo) CreateTicketBooking(ctx context.Context, b *domain.TicketBooking) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO ticket_bookings (user_id, session_id, status, total_amount, currency)
		 VALUES ($1,$2,$3,$4,$5) RETURNING id, created_at`,
		b.UserID, b.SessionID, b.Status, b.TotalAmount, b.Currency,
	).Scan(&b.ID, &b.CreatedAt)
}

func (r *EventRepo) GetTicketBooking(ctx context.Context, id int) (*domain.TicketBooking, error) {
	b := &domain.TicketBooking{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, user_id, session_id, status, total_amount, currency, paid_at, cancelled_at, created_at
		 FROM ticket_bookings WHERE id=$1`, id,
	).Scan(&b.ID, &b.UserID, &b.SessionID, &b.Status, &b.TotalAmount,
		&b.Currency, &b.PaidAt, &b.CancelledAt, &b.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("get booking: %w", err)
	}
	return b, nil
}

func (r *EventRepo) ListUserBookings(ctx context.Context, userID int) ([]*domain.TicketBooking, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, user_id, session_id, status, total_amount, currency, paid_at, cancelled_at, created_at
		 FROM ticket_bookings WHERE user_id=$1 ORDER BY created_at DESC`, userID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var bookings []*domain.TicketBooking
	for rows.Next() {
		b := &domain.TicketBooking{}
		if err := rows.Scan(&b.ID, &b.UserID, &b.SessionID, &b.Status, &b.TotalAmount,
			&b.Currency, &b.PaidAt, &b.CancelledAt, &b.CreatedAt); err != nil {
			return nil, err
		}
		bookings = append(bookings, b)
	}
	return bookings, nil
}

func (r *EventRepo) UpdateBookingStatus(ctx context.Context, id int, status string, paidAt, cancelledAt *time.Time) error {
	_, err := r.pool.Exec(ctx,
		`UPDATE ticket_bookings SET status=$1, paid_at=$2, cancelled_at=$3 WHERE id=$4`,
		status, paidAt, cancelledAt, id)
	return err
}

func (r *EventRepo) CreateTicket(ctx context.Context, t *domain.Ticket) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO tickets (booking_id, session_id, section_id, seat_id, seat_label, price, barcode, status)
		 VALUES ($1,$2,$3,$4,$5,$6,$7,$8) RETURNING id, created_at`,
		t.BookingID, t.SessionID, t.SectionID, t.SeatID, t.SeatLabel, t.Price, t.Barcode, t.Status,
	).Scan(&t.ID, &t.CreatedAt)
}

func (r *EventRepo) ListTicketsByBooking(ctx context.Context, bookingID int) ([]*domain.Ticket, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, booking_id, session_id, section_id, seat_id, seat_label, price, barcode, status, used_at, created_at
		 FROM tickets WHERE booking_id=$1 ORDER BY id`, bookingID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var tickets []*domain.Ticket
	for rows.Next() {
		t := &domain.Ticket{}
		if err := rows.Scan(&t.ID, &t.BookingID, &t.SessionID, &t.SectionID, &t.SeatID,
			&t.SeatLabel, &t.Price, &t.Barcode, &t.Status, &t.UsedAt, &t.CreatedAt); err != nil {
			return nil, err
		}
		tickets = append(tickets, t)
	}
	return tickets, nil
}

func (r *EventRepo) ListTicketsBySession(ctx context.Context, sessionID int) ([]*domain.Ticket, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, booking_id, session_id, section_id, seat_id, seat_label, price, barcode, status, used_at, created_at
		 FROM tickets WHERE session_id=$1 ORDER BY id`, sessionID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var tickets []*domain.Ticket
	for rows.Next() {
		t := &domain.Ticket{}
		if err := rows.Scan(&t.ID, &t.BookingID, &t.SessionID, &t.SectionID, &t.SeatID,
			&t.SeatLabel, &t.Price, &t.Barcode, &t.Status, &t.UsedAt, &t.CreatedAt); err != nil {
			return nil, err
		}
		tickets = append(tickets, t)
	}
	return tickets, nil
}

func (r *EventRepo) UpdateTicketStatus(ctx context.Context, id int, status string, usedAt *time.Time) error {
	_, err := r.pool.Exec(ctx,
		`UPDATE tickets SET status=$1, used_at=$2 WHERE id=$3`,
		status, usedAt, id)
	return err
}

func (r *EventRepo) GetAvailableSeats(ctx context.Context, sessionID, sectionID int) ([]*domain.Seat, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT s.id, s.section_id, s.row_label, s.seat_number, s.is_active
		 FROM seats s
		 WHERE s.section_id=$1 AND s.is_active=true
		   AND s.id NOT IN (
		     SELECT t.seat_id FROM tickets t
		     WHERE t.session_id=$2 AND t.seat_id IS NOT NULL AND t.status IN ('active','used')
		   )
		 ORDER BY s.row_label, s.seat_number`, sectionID, sessionID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var seats []*domain.Seat
	for rows.Next() {
		s := &domain.Seat{}
		if err := rows.Scan(&s.ID, &s.SectionID, &s.RowLabel, &s.SeatNumber, &s.IsActive); err != nil {
			return nil, err
		}
		seats = append(seats, s)
	}
	return seats, nil
}
