package infra

import (
	"context"
	"fmt"
	"io"
	"time"

	"github.com/minio/minio-go/v7"
	"github.com/minio/minio-go/v7/pkg/credentials"
)

type Storage struct {
	client *minio.Client
	bucket string
}

func NewStorage(endpoint, accessKey, secretKey, bucket string, useSSL bool) (*Storage, error) {
	client, err := minio.New(endpoint, &minio.Options{
		Creds:  credentials.NewStaticV4(accessKey, secretKey, ""),
		Secure: useSSL,
	})
	if err != nil {
		return nil, fmt.Errorf("minio new: %w", err)
	}
	ctx := context.Background()
	if err := client.MakeBucket(ctx, bucket, minio.MakeBucketOptions{}); err != nil {
		// Bucket may already exist; check
		exists, errBucketExists := client.BucketExists(ctx, bucket)
		if errBucketExists != nil || !exists {
			return nil, fmt.Errorf("minio bucket: %w", err)
		}
	}
	return &Storage{client: client, bucket: bucket}, nil
}

func (s *Storage) Upload(ctx context.Context, key string, reader io.Reader, size int64, contentType string) (string, error) {
	_, err := s.client.PutObject(ctx, s.bucket, key, reader, size, minio.PutObjectOptions{
		ContentType: contentType,
	})
	if err != nil {
		return "", fmt.Errorf("minio upload: %w", err)
	}
	return s.PublicURL(key), nil
}

func (s *Storage) PublicURL(key string) string {
	return fmt.Sprintf("/api/v1/files/%s", key)
}

func (s *Storage) GetURL(ctx context.Context, key string, expires time.Duration) (string, error) {
	u, err := s.client.PresignedGetObject(ctx, s.bucket, key, expires, nil)
	if err != nil {
		return "", fmt.Errorf("minio presigned: %w", err)
	}
	return u.String(), nil
}

func (s *Storage) Delete(ctx context.Context, key string) error {
	return s.client.RemoveObject(ctx, s.bucket, key, minio.RemoveObjectOptions{})
}
