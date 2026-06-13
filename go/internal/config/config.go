package config

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

type Config struct {
	Port         int
	DatabaseURL  string
	RedisURL     string
	NATSURL      string
	MinIOEndpoint  string
	MinIOAccessKey string
	MinIOSecretKey string
	MinIOBucket    string
	MeilisearchURL string
	MeilisearchKey string
	OSRMURL       string
	FCMKey        string
	JWTSecret     string
	CorsOrigin    string
}

func Load() *Config {
	return &Config{
		Port:           envInt("PORT", 8080),
		DatabaseURL:    env("DATABASE_URL", "postgres://postgres:postgres@localhost:5432/webplatform"),
		RedisURL:       env("REDIS_URL", "redis://localhost:6379/0"),
		NATSURL:        env("NATS_URL", "nats://localhost:4222"),
		MinIOEndpoint:  env("MINIO_ENDPOINT", "localhost:9000"),
		MinIOAccessKey: env("MINIO_ACCESS_KEY", "minioadmin"),
		MinIOSecretKey: env("MINIO_SECRET_KEY", "minioadmin"),
		MinIOBucket:    env("MINIO_BUCKET", "uploads"),
		MeilisearchURL: env("MEILISEARCH_URL", "http://localhost:7700"),
		MeilisearchKey: env("MEILISEARCH_KEY", "masterKey"),
		OSRMURL:        env("OSRM_URL", "http://localhost:5000"),
		FCMKey:         env("FCM_SERVER_KEY", ""),
		JWTSecret:      env("JWT_SECRET", "change-me-in-production"),
		CorsOrigin:     env("CORS_ORIGIN", "*"),
	}
}

func (c *Config) Addr() string {
	return fmt.Sprintf(":%d", c.Port)
}

func env(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}

func envInt(key string, fallback int) int {
	if v := os.Getenv(key); v != "" {
		if n, err := strconv.Atoi(v); err == nil {
			return n
		}
	}
	return fallback
}

func envDur(key string, fallback time.Duration) time.Duration {
	if v := os.Getenv(key); v != "" {
		if d, err := time.ParseDuration(v); err == nil {
			return d
		}
	}
	return fallback
}
