package infra

import (
	"fmt"
	"log"
	"time"

	"github.com/nats-io/nats.go"
)

type EventBus struct {
	conn *nats.Conn
	js   nats.JetStreamContext
}

func NewEventBus(url string) (*EventBus, error) {
	conn, err := nats.Connect(url, nats.Timeout(10*time.Second))
	if err != nil {
		return nil, fmt.Errorf("nats connect: %w", err)
	}
	js, err := conn.JetStream()
	if err != nil {
		conn.Close()
		return nil, fmt.Errorf("nats jetstream: %w", err)
	}
	return &EventBus{conn: conn, js: js}, nil
}

func (eb *EventBus) Close() {
	eb.conn.Close()
}

func (eb *EventBus) Publish(subject string, data []byte) error {
	_, err := eb.js.Publish(subject, data)
	if err != nil {
		log.Printf("nats publish %s: %v", subject, err)
	}
	return err
}

func (eb *EventBus) Subscribe(subject string, handler func(msg []byte)) error {
	_, err := eb.js.Subscribe(subject, func(msg *nats.Msg) {
		handler(msg.Data)
	})
	return err
}
