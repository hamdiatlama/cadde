package infra

import (
	"context"
	"fmt"
	"time"

	"github.com/redis/go-redis/v9"
)

type Cache struct {
	rdb *redis.Client
}

func NewCache(ctx context.Context, url string) (*Cache, error) {
	opts, err := redis.ParseURL(url)
	if err != nil {
		return nil, fmt.Errorf("redis parse url: %w", err)
	}
	rdb := redis.NewClient(opts)
	if err := rdb.Ping(ctx).Err(); err != nil {
		return nil, fmt.Errorf("redis ping: %w", err)
	}
	return &Cache{rdb: rdb}, nil
}

func (c *Cache) Close() error {
	return c.rdb.Close()
}

func (c *Cache) Get(ctx context.Context, key string) (string, error) {
	return c.rdb.Get(ctx, key).Result()
}

func (c *Cache) Set(ctx context.Context, key string, value interface{}, ttl time.Duration) error {
	return c.rdb.Set(ctx, key, value, ttl).Err()
}

func (c *Cache) Del(ctx context.Context, keys ...string) error {
	return c.rdb.Del(ctx, keys...).Err()
}

// GeoAdd adds a courier location to the geo index.
func (c *Cache) GeoAdd(ctx context.Context, key string, lon, lat float64, member string) error {
	return c.rdb.GeoAdd(ctx, key, &redis.GeoLocation{
		Longitude: lon,
		Latitude:  lat,
		Name:      member,
	}).Err()
}

// GeoRadius finds couriers near a point within radius_km.
func (c *Cache) GeoRadius(ctx context.Context, key string, lon, lat, radiusKm float64) ([]redis.GeoLocation, error) {
	return c.rdb.GeoRadius(ctx, key, lon, lat, &redis.GeoRadiusQuery{
		Radius:    radiusKm,
		Unit:      "km",
		WithCoord: true,
		WithDist:  true,
	}).Result()
}
