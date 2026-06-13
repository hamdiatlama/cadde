package infra

import (
	"fmt"

	"github.com/meilisearch/meilisearch-go"
)

type Search struct {
	client meilisearch.ServiceManager
}

func NewSearch(url, apiKey string) (*Search, error) {
	client := meilisearch.New(url, meilisearch.WithAPIKey(apiKey))
	// Health check
	_, err := client.Health()
	if err != nil {
		return nil, fmt.Errorf("meilisearch health: %w", err)
	}
	return &Search{client: client}, nil
}

func (s *Search) Index(index string) *meilisearch.Index {
	return s.client.Index(index)
}

func (s *Search) AddDocuments(index string, docs interface{}, primaryKey string) error {
	_, err := s.client.Index(index).AddDocuments(docs, primaryKey)
	return err
}

func (s *Search) Search(index, query string, request *meilisearch.SearchRequest) (*meilisearch.SearchResponse, error) {
	return s.client.Index(index).Search(query, request)
}

func (s *Search) DeleteDocument(index, id string) error {
	_, err := s.client.Index(index).DeleteDocument(id)
	return err
}
