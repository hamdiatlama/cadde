package postgres

import (
	"context"
	"fmt"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
	"github.com/web-platform/backend/internal/domain"
)

type SupportRepo struct {
	pool *pgxpool.Pool
}

func NewSupportRepo(pool *pgxpool.Pool) *SupportRepo {
	return &SupportRepo{pool: pool}
}

func (r *SupportRepo) CreateTicket(ctx context.Context, t *domain.SupportTicket) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO support_tickets (user_id, order_id, subject, category, status, priority)
		 VALUES ($1,$2,$3,$4,$5,$6) RETURNING id, created_at`,
		t.UserID, t.OrderID, t.Subject, t.Category, t.Status, t.Priority,
	).Scan(&t.ID, &t.CreatedAt)
}

func (r *SupportRepo) CreateMessage(ctx context.Context, m *domain.TicketMessage) error {
	return r.pool.QueryRow(ctx,
		`INSERT INTO ticket_messages (ticket_id, sender_id, message, is_staff)
		 VALUES ($1,$2,$3,$4) RETURNING id, created_at`,
		m.TicketID, m.SenderID, m.Message, m.IsStaff,
	).Scan(&m.ID, &m.CreatedAt)
}

func (r *SupportRepo) CountOpenTickets(ctx context.Context, userID int) (int, error) {
	var count int
	err := r.pool.QueryRow(ctx,
		`SELECT COUNT(*) FROM support_tickets WHERE user_id=$1 AND status IN ('open','in_progress')`,
		userID).Scan(&count)
	return count, err
}

func (r *SupportRepo) GetTicket(ctx context.Context, id int) (*domain.SupportTicket, error) {
	t := &domain.SupportTicket{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, user_id, order_id, subject, category, status, priority, created_at,
		        updated_at, resolved_at FROM support_tickets WHERE id=$1`, id,
	).Scan(&t.ID, &t.UserID, &t.OrderID, &t.Subject, &t.Category, &t.Status, &t.Priority,
		&t.CreatedAt, &t.UpdatedAt, &t.ResolvedAt)
	if err != nil {
		return nil, fmt.Errorf("get ticket: %w", err)
	}
	return t, nil
}

func (r *SupportRepo) ListUserTickets(ctx context.Context, userID int) ([]*domain.SupportTicket, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, user_id, order_id, subject, category, status, priority, created_at,
		        updated_at, resolved_at
		 FROM support_tickets WHERE user_id=$1
		 ORDER BY COALESCE(updated_at, created_at) DESC`, userID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var tickets []*domain.SupportTicket
	for rows.Next() {
		t := &domain.SupportTicket{}
		if err := rows.Scan(&t.ID, &t.UserID, &t.OrderID, &t.Subject, &t.Category,
			&t.Status, &t.Priority, &t.CreatedAt, &t.UpdatedAt, &t.ResolvedAt); err != nil {
			return nil, err
		}
		tickets = append(tickets, t)
	}
	return tickets, nil
}

func (r *SupportRepo) GetMessages(ctx context.Context, ticketID int) ([]*domain.TicketMessage, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, ticket_id, sender_id, message, is_staff, created_at
		 FROM ticket_messages WHERE ticket_id=$1 ORDER BY created_at ASC`, ticketID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var msgs []*domain.TicketMessage
	for rows.Next() {
		m := &domain.TicketMessage{}
		if err := rows.Scan(&m.ID, &m.TicketID, &m.SenderID, &m.Message, &m.IsStaff, &m.CreatedAt); err != nil {
			return nil, err
		}
		msgs = append(msgs, m)
	}
	return msgs, nil
}

func (r *SupportRepo) GetLastMessage(ctx context.Context, ticketID int) (*domain.TicketMessage, error) {
	m := &domain.TicketMessage{}
	err := r.pool.QueryRow(ctx,
		`SELECT id, ticket_id, sender_id, message, is_staff, created_at
		 FROM ticket_messages WHERE ticket_id=$1 ORDER BY created_at DESC LIMIT 1`, ticketID,
	).Scan(&m.ID, &m.TicketID, &m.SenderID, &m.Message, &m.IsStaff, &m.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("get last message: %w", err)
	}
	return m, nil
}

func (r *SupportRepo) UpdateStatus(ctx context.Context, ticketID int, status string) error {
	_, err := r.pool.Exec(ctx,
		`UPDATE support_tickets SET status=$1, updated_at=$2 WHERE id=$3`,
		status, time.Now(), ticketID)
	return err
}

func (r *SupportRepo) ListAllTickets(ctx context.Context, limit, offset int) ([]*domain.SupportTicket, error) {
	rows, err := r.pool.Query(ctx,
		`SELECT id, user_id, order_id, subject, category, status, priority, created_at,
		        updated_at, resolved_at
		 FROM support_tickets
		 ORDER BY COALESCE(updated_at, created_at) DESC LIMIT $1 OFFSET $2`, limit, offset)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var tickets []*domain.SupportTicket
	for rows.Next() {
		t := &domain.SupportTicket{}
		if err := rows.Scan(&t.ID, &t.UserID, &t.OrderID, &t.Subject, &t.Category,
			&t.Status, &t.Priority, &t.CreatedAt, &t.UpdatedAt, &t.ResolvedAt); err != nil {
			return nil, err
		}
		tickets = append(tickets, t)
	}
	return tickets, nil
}

func (r *SupportRepo) UpdateResolvedAt(ctx context.Context, ticketID int) error {
	_, err := r.pool.Exec(ctx,
		`UPDATE support_tickets SET resolved_at=$1, updated_at=$1 WHERE id=$2`,
		time.Now(), ticketID)
	return err
}
