package infra

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

type Notifier struct {
	serverKey string
	client    *http.Client
}

type FCMRequest struct {
	To               string            `json:"to,omitempty"`
	Condition        string            `json:"condition,omitempty"`
	Priority         string            `json:"priority,omitempty"`
	Notification     *FCMNotification  `json:"notification,omitempty"`
	Data             map[string]string `json:"data,omitempty"`
}

type FCMNotification struct {
	Title string `json:"title"`
	Body  string `json:"body"`
}

type FCMResponse struct {
	Success  bool   `json:"success"`
	MessageID string `json:"message_id,omitempty"`
	Error    string `json:"error,omitempty"`
}

func NewNotifier(serverKey string) *Notifier {
	return &Notifier{
		serverKey: serverKey,
		client:    &http.Client{},
	}
}

func (n *Notifier) SendToDevice(deviceToken, title, body string, data map[string]string) (*FCMResponse, error) {
	payload := FCMRequest{
		To:       deviceToken,
		Priority: "high",
		Notification: &FCMNotification{
			Title: title,
			Body:  body,
		},
		Data: data,
	}
	return n.send(payload)
}

func (n *Notifier) SendToTopic(topic, title, body string, data map[string]string) (*FCMResponse, error) {
	payload := FCMRequest{
		To:       fmt.Sprintf("/topics/%s", topic),
		Priority: "high",
		Notification: &FCMNotification{
			Title: title,
			Body:  body,
		},
		Data: data,
	}
	return n.send(payload)
}

func (n *Notifier) send(payload FCMRequest) (*FCMResponse, error) {
	body, err := json.Marshal(payload)
	if err != nil {
		return nil, fmt.Errorf("fcm marshal: %w", err)
	}

	req, err := http.NewRequest("POST", "https://fcm.googleapis.com/fcm/send", bytes.NewReader(body))
	if err != nil {
		return nil, fmt.Errorf("fcm request: %w", err)
	}
	req.Header.Set("Authorization", "key="+n.serverKey)
	req.Header.Set("Content-Type", "application/json")

	resp, err := n.client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("fcm send: %w", err)
	}
	defer resp.Body.Close()

	respBody, _ := io.ReadAll(resp.Body)
	var result FCMResponse
	if err := json.Unmarshal(respBody, &result); err != nil {
		return nil, fmt.Errorf("fcm decode: %w", err)
	}
	result.Success = resp.StatusCode == 200
	return &result, nil
}
